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
        "Adicione comentários Javadoc ao seguinte código Java. Use as tags apropriadas "
        "e inclua referências cruzadas para as seguintes classes relacionadas: "
        f"{related_classes_str}.\n\n"
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
   
