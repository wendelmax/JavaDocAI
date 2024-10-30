import os
import openai
import time
import json
import javalang
from tqdm import tqdm
import sys

# Configure sua chave da API OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")  # Recomenda-se usar variáveis de ambiente

# Arquivo auxiliar para armazenar relacionamentos entre classes
AUXILIARY_FILE = "class_relationships.json"

def get_repository_directory():
    """
    Solicita ao usuário que insira o caminho do diretório do repositório Java.
    Valida se o diretório existe e contém arquivos .java.
    """
    while True:
        repo_dir = input("Por favor, insira o caminho absoluto do diretório do repositório Java: ").strip()
        if not os.path.isdir(repo_dir):
            print("O diretório fornecido não existe. Por favor, tente novamente.\n")
            continue
        # Verifica se o diretório contém arquivos .java
        java_files = []
        for root, dirs, files in os.walk(repo_dir):
            for file in files:
                if file.endswith(".java"):
                    java_files.append(os.path.join(root, file))
        if not java_files:
            print("O diretório fornecido não contém arquivos .java. Por favor, verifique o caminho e tente novamente.\n")
            continue
        return repo_dir

# Função para buscar todos os arquivos .java
def get_java_files(repo_dir):
    java_files = []
    for root, dirs, files in os.walk(repo_dir):
        for file in files:
            if file.endswith(".java"):
                java_files.append(os.path.join(root, file))
    return java_files

# Função para extrair o nome da classe a partir do arquivo
def get_class_name(java_code):
    try:
        tree = javalang.parse.parse(java_code)
        for path, node in tree.filter(javalang.tree.TypeDeclaration):
            if isinstance(node, javalang.tree.ClassDeclaration):
                return node.name
        return None
    except javalang.parser.JavaSyntaxError as e:
        print(f"Erro de sintaxe ao analisar classe: {e}")
        return None

# Função para extrair dependências de uma classe
def get_class_dependencies(java_code):
    dependencies = set()
    try:
        tree = javalang.parse.parse(java_code)
        package = tree.package.name if tree.package else ""
        imports = [imp.path.split('.')[-1] for imp in tree.imports]
        for imp in tree.imports:
            if not imp.wildcard:
                dependencies.add(imp.path.split('.')[-1])
        for path, node in tree.filter(javalang.tree.Type):
            if isinstance(node, javalang.tree.ReferenceType):
                type_name = node.name
                if type_name not in dependencies:
                    dependencies.add(type_name)
        return list(dependencies)
    except javalang.parser.JavaSyntaxError as e:
        print(f"Erro de sintaxe ao analisar dependências: {e}")
        return []

# Função para adicionar Javadoc usando a API do OpenAI
def add_javadoc_to_class(java_code, related_classes):
    related_classes_str = ', '.join(related_classes) if related_classes else 'Nenhuma'
    prompt = (
        "Você é um especialista em desenvolvimento Java e Javadoc. Sua tarefa é adicionar comentários Javadoc completos e detalhados ao seguinte código Java. "
        "Utilize todas as tags Javadoc apropriadas, incluindo, mas não se limitando a:\n\n"
        "- `@param`: Descreva cada parâmetro do método.\n"
        "- `@return`: Descreva o valor de retorno do método, se aplicável.\n"
        "- `@throws` ou `@exception`: Descreva as exceções que o método pode lançar.\n"
        "- `@see`: Adicione referências cruzadas para outras classes ou métodos relacionados.\n"
        "- `@deprecated`: Indique se a classe ou método está obsoleta e forneça uma alternativa, se houver.\n"
        "- `@since`: Indique desde qual versão a classe ou método existe.\n"
        "- `@autor`\n"
        "- `@version`\n\n"
        f"Além disso, analise as classes relacionadas fornecidas e inclua referências cruzadas adequadas nos comentários Javadoc usando a tag `@see`.\n\n"
        "Aqui está o código Java para o qual os comentários Javadoc devem ser adicionados:\n\n"
        f"{java_code}\n"
    )
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use o modelo apropriado
            messages=[
                {"role": "system", "content": "Você é um assistente que adiciona comentários Javadoc ao código Java."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,  # Ajuste conforme necessário
            temperature=0.2,
        )
        return response.choices[0].message["content"]
    except openai.error.RateLimitError:
        print("Limite de taxa atingido. Aguardando 60 segundos...")
        time.sleep(60)
        return add_javadoc_to_class(java_code, related_classes)
    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")
        return None

def main():
    # Obtém o diretório do repositório a partir do usuário
    repo_dir = get_repository_directory()
    print(f"\nDiretório do repositório definido para: {repo_dir}\n")
    
    java_files = get_java_files(repo_dir)
    print(f"Encontrados {len(java_files)} arquivos Java.\n")
    
    class_relationships = {}
    class_name_to_file = {}

    print("Mapeando nomes de classes para arquivos...")
    # Primeiro mapeia o nome das classes para seus caminhos de arquivo
    for file_path in tqdm(java_files, desc="Mapeando classes"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
            class_name = get_class_name(code)
            if class_name:
                class_name_to_file[class_name] = file_path
        except Exception as e:
            print(f"Erro ao ler {file_path}: {e}")

    print("\nAnalisando dependências entre classes...")
    # Agora, para cada classe, encontra suas dependências
    for file_path in tqdm(java_files, desc="Analisando dependências"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                code = file.read()
            class_name = get_class_name(code)
            if class_name:
                dependencies = get_class_dependencies(code)
                # Filtra apenas dependências internas (ou seja, classes presentes no repositório)
                internal_dependencies = [dep for dep in dependencies if dep in class_name_to_file]
                class_relationships[class_name] = internal_dependencies
        except Exception as e:
            print(f"Erro ao analisar {file_path}: {e}")

    # Salva os relacionamentos em um arquivo auxiliar
    with open(AUXILIARY_FILE, "w", encoding="utf-8") as aux_file:
        json.dump(class_relationships, aux_file, indent=4, ensure_ascii=False)
    print(f"\nRelacionamentos entre classes salvos em {AUXILIARY_FILE}.\n")

    print("Adicionando Javadoc com referências cruzadas...")
    # Agora, processa cada arquivo para adicionar Javadoc
    for file_path in tqdm(java_files, desc="Processando Javadocs"):
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                original_code = file.read()
            
            class_name = get_class_name(original_code)
            if class_name:
                related_classes = class_relationships.get(class_name, [])
                updated_code = add_javadoc_to_class(original_code, related_classes)
                
                if updated_code:
                    with open(file_path, "w", encoding="utf-8") as file:
                        file.write(updated_code)
                    time.sleep(1)  # Pequena pausa para evitar limites de taxa
        except Exception as e:
            print(f"Erro ao processar {file_path}: {e}")

    print("\nProcessamento concluído.")

if __name__ == "__main__":
    main()
