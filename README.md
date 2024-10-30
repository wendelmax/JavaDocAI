# **JavaDocAI**

**JavaDocAI** é uma ferramenta automatizada projetada para aprimorar seu código Java adicionando comentários Javadoc abrangentes a todas as classes, métodos e campos. Utilizando o poder da API ChatGPT da OpenAI, o JavaDocAI não apenas gera comentários Javadoc padrão, mas também referencia e cria cruzamentos inteligentes com classes relacionadas dentro do seu projeto. Isso garante que sua documentação seja detalhada e interconectada, facilitando a compreensão e manutenção do código.

## 📄 Sumário

- [Recursos](#🌟-recursos)
- [Pré-requisitos](#🚀-pré-requisitos)
- [Instalação](#🛠-instalação)
- [Configuração](#⚙️-configuração)
- [Uso](#📚-uso)
- [Estrutura do Projeto](#🗂-estrutura-do-projeto)
- [Arquivo Auxiliar](#🛠-arquivo-auxiliar)
- [Considerações](#⚠️-considerações)
- [Contribuindo](#🤝-contribuindo)
- [Licença](#📝-licença)

## 🌟 Recursos

- **Geração Automatizada de Javadoc**: Adiciona automaticamente comentários Javadoc a todas as classes, métodos e campos Java.
- **Referências Cruzadas Inteligentes**: Analisa dependências de classes e inclui tags `@see` para referenciar classes relacionadas.
- **Documentação Abrangente**: Utiliza o modelo GPT-4 da OpenAI para gerar documentação detalhada e significativa.
- **Mapeamento de Relacionamentos Auxiliar**: Gera um arquivo `class_relationships.json` que mapeia as relações entre as classes do seu projeto.
- **Integração Simplificada**: Integra-se facilmente a projetos Java existentes com configuração mínima.
- **Tratamento de Erros e Limitação de Taxa**: Lida com limites de taxa da API de forma graciosa e garante operação confiável.

## 🚀 Pré-requisitos

Antes de configurar o JavaDocAI, certifique-se de ter o seguinte:

1. **Python 3.7+**: Verifique se o Python está instalado no seu sistema. Você pode baixá-lo em [python.org](https://www.python.org/downloads/).

2. **Chave da API OpenAI**: Obtenha uma chave de API da [OpenAI](https://platform.openai.com/account/api-keys). Esta chave é necessária para interagir com a API ChatGPT.

3. **Git** (opcional): Para controle de versão e gerenciamento de backups.

## 🛠 Instalação

1. **Clone o Repositório**

   ```bash
   git clone https://github.com/wendelmax/JavaDocAI.git
   cd JavaDocAI
   ```

2. **Crie um Ambiente Virtual** (Opcional, mas recomendado)

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as Bibliotecas Python Necessárias**

   ```bash
   pip install -r requirements.txt
   ```

   *Se o arquivo `requirements.txt` não estiver disponível, instale as dependências manualmente:*

   ```bash
   pip install openai tqdm javalang
   ```

## ⚙️ Configuração

1. **Configure a Chave da API OpenAI**

   É recomendado armazenar sua chave da API OpenAI como uma variável de ambiente para segurança.

   - **No Linux/macOS:**

     ```bash
     export OPENAI_API_KEY="sua-chave-api-aqui"
     ```

   - **No Windows (Prompt de Comando):**

     ```cmd
     set OPENAI_API_KEY="sua-chave-api-aqui"
     ```

   - **No Windows (PowerShell):**

     ```powershell
     $env:OPENAI_API_KEY="sua-chave-api-aqui"
     ```

   *Alternativamente, você pode definir diretamente a variável `openai.api_key` no script, mas isso **não é recomendado** por questões de segurança.*

## 📚 Uso

1. **Navegue até o Diretório do Projeto**

   ```bash
   cd JavaDocAI
   ```

2. **Execute o Script**

   ```bash
   python java_doc_ai.py
   ```

   *Certifique-se de ter ativado seu ambiente virtual, se você criou um.*

3. **Siga as Instruções**

   - **Entrada do Diretório do Repositório Java:**
     
     Ao executar o script, você será solicitado a inserir o caminho absoluto do diretório do repositório Java que deseja processar. Por exemplo:

     ```
     Por favor, insira o caminho absoluto do diretório do repositório Java: /home/usuario/meu-projeto-java
     ```

   - **Processo de Execução:**

     - O script escaneará o repositório especificado em busca de todos os arquivos `.java`.
     - Analisa cada arquivo Java para identificar nomes de classes e suas dependências.
     - Gera um arquivo auxiliar (`class_relationships.json`) que mapeia as relações entre as classes.
     - Envia cada arquivo Java para a API da OpenAI com um prompt para adicionar comentários Javadoc, incluindo referências às classes relacionadas.
     - Sobrescreve os arquivos Java originais com o código atualizado contendo os Javadocs adicionados.

## 🗂 Estrutura do Projeto

```
JavaDocAI/
├── java_doc_ai.py
├── class_relationships.json
├── requirements.txt
├── README.md
└── ... (outros arquivos)
```

- **java_doc_ai.py**: Script principal que realiza a geração de Javadoc e o mapeamento de relacionamentos entre classes.
- **class_relationships.json**: Arquivo auxiliar que armazena os relacionamentos entre classes.
- **requirements.txt**: Lista todas as dependências Python.
- **README.md**: Documentação do projeto.

## 🛠 Arquivo Auxiliar

### `class_relationships.json`

Este arquivo JSON fornece um mapeamento claro de como as classes dentro do seu projeto se relacionam. Ele está estruturado da seguinte forma:

```json
{
    "ClasseA": ["ClasseB", "ClasseC"],
    "ClasseB": ["ClasseC"],
    "ClasseC": []
}
```

- **Chave (Key)**: Nome da classe principal.
- **Valor (Value)**: Lista de classes que são dependências internas da classe principal.

*Este arquivo pode ser utilizado para análises adicionais, documentação ou geração de diagramas de dependência.*

## ⚠️ Considerações

- **Backup do Código**: Antes de executar o script, **certifique-se de ter um backup** do seu repositório ou use um sistema de controle de versão (como Git) para poder reverter alterações, se necessário.

- **Limites da API**: A API da OpenAI possui limites de tokens por requisição. Arquivos Java muito grandes podem precisar ser divididos ou ajustados para se adequarem aos limites.

- **Custo**: O uso da API da OpenAI está sujeito a cobranças. Monitore seu consumo para evitar despesas inesperadas.

- **Qualidade dos Comentários**: Embora o modelo GPT-4 seja poderoso, é recomendado revisar os comentários Javadoc gerados para garantir precisão e relevância.

- **Análise Estática Limitada**: A análise de dependências é baseada em importações e tipos utilizados. Pode não capturar todas as nuances das relações entre classes, como dependências dinâmicas ou reflexões.

## 🤝 Contribuindo

Contribuições são bem-vindas! Se você deseja melhorar o JavaDocAI, siga estas etapas:

1. **Fork o Repositório**

2. **Crie uma Branch para sua Feature**

   ```bash
   git checkout -b minha-nova-feature
   ```

3. **Faça Commit das Suas Alterações**

   ```bash
   git commit -m "Descrição da feature"
   ```

4. **Push para a Branch**

   ```bash
   git push origin minha-nova-feature
   ```

5. **Abra um Pull Request**

## 📝 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
