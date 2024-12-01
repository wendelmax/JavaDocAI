# **JavaDocAI**

**JavaDocAI** é uma ferramenta automatizada projetada para aprimorar seu código Java adicionando comentários Javadoc abrangentes a todas as classes, métodos e campos. Utilizando o poder de uma instância local do **Ollama3**, o JavaDocAI não apenas gera comentários Javadoc padrão, mas também referencia classes relacionadas dentro do seu projeto.

## 📄 Sumário

- [🌟 Recursos](#-recursos)
- [🚀 Pré-requisitos](#-pré-requisitos)
- [🛠 Instalação](#-instalação)
- [⚙️ Configuração](#-configuração)
- [📚 Uso](#-uso)
- [🤝 Contribuindo](#-contribuindo)

## 🌟 Recursos

- **Geração Automatizada de Javadoc**: Adiciona automaticamente comentários Javadoc a todas as classes, métodos e campos Java.
- **Referências Inteligentes**: Adiciona referências para dependências diretas no código.
- **Documentação Abrangente**: Utiliza uma instância local do Ollama para gerar documentação detalhada.
- **Processamento Paralelo**: Utiliza múltiplas threads para acelerar o processamento de grandes bases de código.
- **Suporte Multilíngue**: Suporte para diferentes idiomas através do arquivo `i18n.json`.

## 🚀 Pré-requisitos

1. **Python 3.10+**
2. **Git**
3. **Ollama** (será instalado automaticamente pelo script)

## 🛠 Instalação

1. **Clone o Repositório**
   ```bash
   git clone https://github.com/wendelmax/JavaDocAI.git
   cd JavaDocAI
   ```

2. **Crie e Ative o Ambiente Virtual**
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. **Instale as Dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o Parser Java**
   ```bash
   python build_parsers.py
   ```
   Este passo é **obrigatório** após clonar o repositório. Ele irá:
   - Clonar o repositório tree-sitter-java
   - Compilar a gramática Java
   - Gerar os arquivos necessários na pasta `build/`

   > ⚠️ **Nota**: Os arquivos gerados não são versionados e devem ser recriados após clonar o repositório.

## ⚙️ Configuração

1. **Crie seu arquivo .env**
   ```bash
   cp .env.example .env
   ```
   
   Edite o arquivo `.env` conforme necessário. As principais configurações são:
   - `OLLAMA_HOST`: Host do servidor Ollama
   - `OLLAMA_PORT`: Porta do servidor Ollama
   - `OLLAMA_MODEL`: Modelo a ser usado
   - `LOG_LEVEL`: Nível de logging
   - `BATCH_SIZE`: Tamanho do lote para processamento
   - `MAX_CONCURRENT_TASKS`: Número máximo de tarefas concorrentes

2. **Configuração do Idioma**
   - O idioma padrão é definido no arquivo `config/i18n.json`
   - Para mudar o idioma, edite a variável `LANGUAGE_CONFIG` no arquivo `.env`

3. **Arquivo de Configuração (config.yaml)**
   
   O arquivo `config/config.yaml` contém as configurações principais do sistema:

   ```yaml
   ollama:
     # Configurações do modelo LLM
     model: "qwen2.5-coder:7b"    # Modelo usado para geração
     temperature: 0.7             # Criatividade do modelo (0.0 - 1.0)
     top_p: 0.95                 # Probabilidade de amostragem
     context_window: 4096        # Tamanho da janela de contexto

   logging:
     level: "DEBUG"              # Nível de log (DEBUG, INFO, WARNING, ERROR)
     rotation: "1 day"           # Rotação do arquivo de log
     retention: "1 week"         # Retenção dos logs

   processing:
     batch_size: 10              # Quantidade de arquivos processados por vez
     max_concurrent_tasks: 4     # Número máximo de tarefas paralelas
   ```

4. **Níveis de Log**

   O sistema suporta diferentes níveis de log que podem ser configurados no `config.yaml`:

   - `ERROR`: Apenas erros críticos
   - `WARNING`: Avisos e erros
   - `INFO`: Informações gerais de execução
   - `DEBUG`: Informações detalhadas, incluindo:
     - Prompts enviados para o modelo LLM
     - Respostas recebidas do modelo
     - Detalhes do processamento de arquivos
     - Informações de depuração

   Para ver a geração do LLM em tempo real, use o nível `DEBUG`:
   ```yaml
   logging:
     level: "DEBUG"
   ```

## 📚 Uso

1. **Execute o Script Principal**
   ```bash
   python main.py
   ```

2. **Insira o Caminho do Repositório**
   - Quando solicitado, insira o caminho do repositório Java que deseja documentar
   - O script processará todos os arquivos Java encontrados no diretório

3. **Acompanhe o Progresso**
   - O script mostrará o progresso do processamento
   - Os arquivos serão atualizados com os comentários Javadoc gerados

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor, siga estes passos:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request