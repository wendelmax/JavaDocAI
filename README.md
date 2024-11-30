Aqui está o README atualizado com a nova estrutura do projeto e as opções de idioma:

---

# **JavaDocAI**

**JavaDocAI** é uma ferramenta automatizada projetada para aprimorar seu código Java adicionando comentários Javadoc abrangentes a todas as classes, métodos e campos. Utilizando o poder de uma instância local do **Ollama3**, o JavaDocAI não apenas gera comentários Javadoc padrão, mas também referencia classes relacionadas dentro do seu projeto. Isso garante que sua documentação seja detalhada, interconectada e de fácil manutenção.

## 📄 Sumário

- [🌟 Recursos](#-recursos)
- [🚀 Pré-requisitos](#-pré-requisitos)
- [🛠 Instalação](#-instalação)
  - [📄 Conteúdo do `requirements.txt`](#-conteúdo-do-requirementstxt)
- [⚙️ Configuração](#-configuração)
  - [📝 Configurando o Suporte Multilíngue e Variáveis no `.env`](#-configurando-o-suporte-multilíngue-e-variáveis-no-env)
- [📚 Uso](#-uso)
  - [Passo Único: Executar o Script Principal](#passo-único-executar-o-script-principal)
    - [📝 Exemplo de Uso do `main.py`](#-exemplo-de-uso-do-mainpy)
- [🗂 Estrutura do Projeto](#-estrutura-do-projeto)
- [⚠️ Considerações](#-considerações)
- [🤝 Contribuindo](#-contribuindo)
- [📝 Licença](#-licença)
- [📚 Exemplo de Uso](#-exemplo-de-uso)
- [📌 Dicas para Maximizar a Efetividade do JavaDocAI](#-dicas-para-maximizar-a-efetividade-do-javadocai)

## 🌟 Recursos

- **Geração Automatizada de Javadoc**: Adiciona automaticamente comentários Javadoc a todas as classes, métodos e campos Java.
- **Referências Inteligentes**: Adiciona referências para dependências diretas no código.
- **Documentação Abrangente**: Utiliza uma instância local do Ollama3 para gerar documentação detalhada.
- **Integração Simplificada**: Integra-se facilmente a projetos Java existentes com configuração mínima.
- **Processamento Paralelo**: Utiliza múltiplas threads para acelerar o processamento de grandes bases de código.
- **Suporte Multilíngue**: Adicione idiomas ao arquivo `i18n.json` e defina o idioma no `.env` ou no próprio script.

## 🚀 Pré-requisitos

Antes de configurar o **JavaDocAI**, certifique-se de ter o seguinte:

1. **Python 3.7+**: Verifique se o Python está instalado no seu sistema. Baixe-o em [python.org](https://www.python.org/downloads/).

2. **Ollama3**:
   - **Instalação**:
     - **Linux/macOS/Windows:** Execute o comando abaixo para instalar o Ollama3:
       ```bash
       curl -fsSL https://ollama.com/install.sh | sh
       ```
     - Após a instalação, reinicie o terminal ou execute `source ~/.bashrc` para atualizar as variáveis de ambiente.
   - **Baixar o Modelo `llama3.2`:**
     ```bash
     ollama pull llama3.2
     ```

3. **Tree-sitter via `pip`**: Utilizado para análise estática do código Java.
   - As bibliotecas necessárias serão instaladas ao seguir as instruções de instalação abaixo.

4. **Git** (opcional): Para controle de versão.

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

3. **Instale as Bibliotecas Necessárias**

   ```bash
   pip install -r requirements.txt
   ```

   _Se o arquivo `requirements.txt` não estiver disponível, instale as dependências manualmente:_

   ```bash
   pip install tree_sitter tree_sitter_java ollama tqdm python-dotenv
   ```

### 📄 Conteúdo do `requirements.txt`

O arquivo `requirements.txt` lista as dependências necessárias para o **JavaDocAI**:

```plaintext
tree_sitter>=0.19.0
tree_sitter_java>=0.19.0
ollama>=0.1.0
tqdm>=4.64.0
python-dotenv>=0.19.0
```

## ⚙️ Configuração

A configuração é feita através do arquivo `config/config.yaml`. As principais configurações são:

```yaml
ollama:
  model: "qwen2.5-coder:7b"
  temperature: 0.7
  top_p: 0.95
  context_window: 4096

processing:
  batch_size: 10
  max_concurrent_tasks: 4
```

### Variáveis de Ambiente

O projeto inclui um arquivo `.env.example` com todas as configurações possíveis. Para usar, copie para `.env`:

```bash
cp .env.example .env
```

Principais variáveis de ambiente:

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| OLLAMA_SERVER_PORT | Porta do servidor Ollama | 11434 |
| LOG_LEVEL | Nível de logging | INFO |
| LANGUAGE_CONFIG | Idioma das mensagens | en |
| BATCH_SIZE | Tamanho do lote de processamento | 10 |
| MAX_CONCURRENT_TASKS | Número máximo de tarefas simultâneas | 4 |
| MODEL_TEMPERATURE | Temperatura do modelo (criatividade) | 0.7 |
| MODEL_TOP_P | Probabilidade top-p do modelo | 0.95 |
| DEBUG | Modo de desenvolvimento | false |

### 📝 Configurando o Suporte Multilíngue e Variáveis no `.env`

Na raiz do diretório, crie um arquivo `.env`:

```bash
touch .env
```

Abra o arquivo e adicione as seguintes variáveis:

```env
OLLAMA_SCHED_SPREAD=true
OLLAMA_FLASH_ATTENTION=true
OLLAMA_SERVER_PORT=11434
LOG_LEVEL=INFO
LANGUAGE_CONFIG=en
```

**Descrição das Variáveis:**

- `OLLAMA_SCHED_SPREAD`: Espalha tarefas no Ollama (`true` ou `false`).
- `OLLAMA_FLASH_ATTENTION`: Ativa ou desativa o Flash Attention (`true` ou `false`).
- `OLLAMA_SERVER_PORT`: Define a porta da API do Ollama. O padrão é `11434`.
- `LOG_LEVEL`: Define o nível de log (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
- `LANGUAGE_CONFIG`: Define o idioma usado no `i18n.json` (padrão é `en`).

Para suporte a um novo idioma, adicione uma nova entrada em `config/i18n.json` e defina o idioma no `LANGUAGE_CONFIG`.

## 📚 Uso

O **JavaDocAI** adiciona comentários Javadoc automaticamente aos arquivos Java utilizando uma instância local do **Ollama3**.

### Passo Único: Executar o Script Principal

Este comando analisa seu repositório Java para adicionar os comentários Javadoc.

#### 📝 Exemplo de Uso do `main.py`

**Comando:**

```bash
python main.py
```

**Interação:**

```plaintext
Por favor, insira o caminho absoluto do diretório do repositório Java: /home/usuario/meu-projeto-java
```

**Saída:**

```plaintext
2024-10-30 12:00:00,000 - INFO - Diretório do repositório definido para: /home/usuario/meu-projeto-java
2024-10-30 12:00:00,200 - INFO - Encontrados 25 arquivos Java.
2024-10-30 12:00:25,800 - INFO - Adicionando Javadoc...
Processando Javadocs: 100%|███████████████████████████████████████| 25/25 [05:30<00:00,  1.55s/it]
2024-10-30 12:10:30,000 - INFO - Processamento concluído.
```

**Resultado:**

- Os arquivos `.java` são atualizados com comentários Javadoc completos e referências apropriadas.

## 🗂 Estrutura do Projeto

```
JavaDocAI/
├── config/
│   └── i18n.json
├── LICENSE
├── logs/
│   └── java_doc_ai.log
├── main.py
├── README.md
├── requirements.txt
└── src/
    ├── config.py
    ├── __init__.py
    ├── java_doc_ai.py
    └── utils.py
```

- **config/i18n.json**: Arquivo de internacionalização com traduções para diferentes idiomas.
- **logs/java_doc_ai.log**: Arquivo de log do projeto.
- **main.py**: Script principal para execução.
- **requirements.txt**: Lista de dependências.
- **README.md**: Documentação do projeto.
- **src/config.py**: Arquivo de configuração do projeto.
- **src/java_doc_ai.py**: Script que implementa a geração de Javadoc.
- **src/utils.py**: Utilitários de apoio ao projeto.

## ⚠️ Considerações

- **Backup do Código**: O script sobrescreve diretamente os arquivos Java. **Recomendado** utilizar um sistema de controle de versão como Git.
  
- **Limites de Recursos do Ollama3**:
  - **Desempenho**: Processar muitos arquivos pode consumir significativamente os recursos do sistema.
  - **Tempo de Processamento**: O processamento pode demorar dependendo da capacidade do Ollama3 e do tamanho dos arquivos.

- **Ambiente Virtual**: Recomenda-se o uso de ambientes virtuais (`venv`, `virtualenv`).

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. **Fork o Repositório**
2. **Crie uma Branch para sua Feature**
3. **Commit das Suas Alterações**
4. **Push para a Branch**
5. **Abra um Pull Request**

## 📝 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 📚 Exemplo de Uso

### Exemplo de Classe Java Sem Comentários Javadoc

```java
public class Usuario {
    private String nome;
    private String email;

    public Usuario(String nome, String email) {
        this.nome = nome;
        this.email = email;
    }

    public String getNome() {
        return nome;
    }

    public void setNome(String nome) {
        this.nome = nome;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }
}
```

### Após Executar o JavaDocAI

```java
/**
 * Representa um usuário no sistema.
 *
 * @param nome Nome do usuário.
 * @param email Email do usuário.
 */
public class Usuario {
    private String nome;
    private String email;

    /**
     * Constrói um novo usuário com o nome e email especificados.
     *
     * @param nome  O nome do usuário.
     * @param email O email do usuário.
     */
    public Usuario(String nome, String email) {
        this.nome = nome;
        this.email = email;
    }

    /**
     * Obtém o nome do usuário.
     *
     * @return O nome do usuário.
     */
    public String getNome() {
        return nome;
    }

    /**
     * Define o nome do usuário.
     *
     * @param nome O novo nome do usuário.
     */
    public void setNome(String nome) {
        this.nome = nome;
    }

    /**
     * Obtém o email do usuário.
     *
     * @return O email do usuário.
     */
    public String getEmail() {
        return email;
    }

    /**
     * Define o email do usuário.
     *
     * @param email O novo email do usuário.
     */
    public void setEmail(String email) {
        this.email = email;
    }
}
```

Neste exemplo, após executar o **JavaDocAI**, a classe `Usuario` foi enriquecida com comentários Javadoc completos. Cada método também possui descrições detalhadas utilizando tags como `@param` e `@return`, garantindo uma documentação completa e útil para futuros desenvolvedores.

---

## 📌 Dicas para Maximizar a Efetividade do JavaDocAI

1. **Revisão Manual dos Comentários Gerados**: Embora o Ollama3 seja poderoso, revise os Javadocs para garantir precisão e relevância.

2. **Atualização Contínua**: À medida que seu projeto evolui, execute o script regularmente para manter a documentação atualizada.

3. **Gerenciamento de Limites de Recursos**: Ajuste o número de threads (`max_workers`) para gerenciar o consumo de recursos.

4. **Personalização do Prompt**: Personalize o prompt no `java_doc_ai.py` para adaptar os comentários ao estilo de documentação da sua organização.