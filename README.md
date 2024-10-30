# **JavaDocAI**

**JavaDocAI** is an automated tool designed to enhance your Java codebase by adding comprehensive Javadoc comments to all classes, methods, and fields. Leveraging the power of OpenAI's ChatGPT API, JavaDocAI not only generates standard Javadoc comments but also intelligently references and cross-references related classes within your project. This ensures that your documentation is both thorough and interconnected, facilitating better code understanding and maintenance.

## 📄 Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Auxiliary File](#auxiliary-file)
- [Considerations](#considerations)
- [Contributing](#contributing)
- [License](#license)

## 🌟 Features

- **Automated Javadoc Generation**: Automatically adds Javadoc comments to all Java classes, methods, and fields.
- **Intelligent Cross-Referencing**: Analyzes class dependencies and includes `@see` tags to reference related classes.
- **Comprehensive Documentation**: Utilizes OpenAI's GPT-4 model to generate detailed and meaningful documentation.
- **Auxiliary Relationship Mapping**: Generates a `class_relationships.json` file that maps out the relationships between classes in your project.
- **Seamless Integration**: Easily integrates into existing Java projects with minimal setup.
- **Error Handling & Rate Limiting**: Handles API rate limits gracefully and ensures reliable operation.

## 🚀 Prerequisites

Before setting up JavaDocAI, ensure you have the following:

1. **Python 3.7+**: Ensure Python is installed on your system. You can download it from [python.org](https://www.python.org/downloads/).

2. **OpenAI API Key**: Obtain an API key from [OpenAI](https://platform.openai.com/account/api-keys). This key is necessary to interact with the ChatGPT API.

3. **Git** (optional): For version control and managing backups.

## 🛠 Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/seu-usuario/JavaDocAI.git
   cd JavaDocAI
   ```

2. **Create a Virtual Environment** (Optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Required Python Libraries**

   ```bash
   pip install -r requirements.txt
   ```

   *If `requirements.txt` is not provided, install the dependencies manually:*

   ```bash
   pip install openai tqdm javalang
   ```

## ⚙️ Configuration

1. **Set Up OpenAI API Key**

   It's recommended to store your OpenAI API key as an environment variable for security.

   - **On Linux/macOS:**

     ```bash
     export OPENAI_API_KEY="sua-chave-api-aqui"
     ```

   - **On Windows (Command Prompt):**

     ```cmd
     set OPENAI_API_KEY="sua-chave-api-aqui"
     ```

   - **On Windows (PowerShell):**

     ```powershell
     $env:OPENAI_API_KEY="sua-chave-api-aqui"
     ```

   *Alternatively, you can directly set the `openai.api_key` variable in the script, but this is **not recommended** for security reasons.*

2. **Specify the Java Repository Path**

   In the `java_doc_ai.py` script, update the `REPO_DIR` variable to point to the root directory of your Java project.

   ```python
   REPO_DIR = "/caminho/para/seu/repositorio"
   ```

## 📚 Usage

1. **Navigate to the Project Directory**

   ```bash
   cd JavaDocAI
   ```

2. **Run the Script**

   ```bash
   python java_doc_ai.py
   ```

   *Ensure that you've activated your virtual environment if you created one.*

3. **Process Overview**

   - The script scans the specified Java repository for all `.java` files.
   - It parses each Java file to identify class names and their dependencies.
   - An auxiliary JSON file (`class_relationships.json`) is generated, mapping out relationships between classes.
   - Each Java file is sent to the OpenAI API with a prompt to add Javadoc comments, including references to related classes.
   - The original Java files are overwritten with the updated code containing the newly added Javadocs.

## 🗂 Project Structure

```
JavaDocAI/
├── java_doc_ai.py
├── class_relationships.json
├── requirements.txt
├── README.md
└── ... (outros arquivos)
```

- **java_doc_ai.py**: Main script that performs Javadoc generation and class relationship mapping.
- **class_relationships.json**: Auxiliary file that stores the relationships between classes.
- **requirements.txt**: Lists all Python dependencies.
- **README.md**: Documentation for the project.

## 🛠 Auxiliary File

### `class_relationships.json`

This JSON file provides a clear mapping of how classes within your project relate to each other. It is structured as follows:

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

## ⚠️ Considerations

- **Backup do Código**: Antes de executar o script, **certifique-se de ter um backup** do seu repositório ou use um sistema de controle de versão (como Git) para poder reverter alterações, se necessário.

- **Limites de API**: A API do OpenAI possui limites de tokens por requisição. Arquivos Java muito grandes podem precisar ser divididos ou ajustados para se adequar aos limites.

- **Custo**: O uso da API do OpenAI está sujeito a cobranças. Monitore seu consumo para evitar despesas inesperadas.

- **Qualidade dos Comentários**: Embora o modelo GPT-4 seja poderoso, é recomendado revisar os Javadocs gerados para garantir precisão e relevância.

- **Análise Estática Limitada**: A análise de dependências é baseada em importações e tipos utilizados. Pode não capturar todas as nuances das relações entre classes, como dependências dinâmicas ou reflexões.

## 🤝 Contributing

Contribuições são bem-vindas! Se você deseja melhorar JavaDocAI, siga estas etapas:

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

## 📝 License

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

**JavaDocAI** facilita a manutenção e documentação do seu projeto Java, garantindo que seu código esteja bem documentado e interconectado. Aproveite esta ferramenta para melhorar a legibilidade e a colaboração em seu códigobase!
