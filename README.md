# 🤖 JavaDocAI 

> 🌟 Supercharge your Java codebase with AI-powered Javadoc generation!

JavaDocAI is an intelligent tool that automatically enhances your Java code by adding comprehensive Javadoc comments to all classes, methods, and fields. Using the power of a local **Ollama** instance, JavaDocAI not only generates standard Javadoc comments but also references related classes within your project.

## 📄 Table of Contents

- [✨ Features](#-features)
- [🚀 Requirements](#-requirements)
- [🛠️ Installation](#️-installation)
- [⚙️ Configuration](#️-configuration)
- [📚 Usage](#-usage)
- [🤝 Contributing](#-contributing)
- [📝 License](#-license)

## ✨ Features

- 🎯 **Smart Javadoc Generation**: Automatically adds Javadoc comments to all Java classes, methods, and fields
- 🔄 **Intelligent References**: Adds references to direct dependencies in the code
- 🧠 **AI-Powered**: Uses local Ollama instance for detailed documentation
- ⚡ **Parallel Processing**: Utilizes multiple threads to speed up processing of large codebases
- 🌍 **Multilingual Support**: Support for different languages through `i18n.json`
- 🎨 **Model Flexibility**: Support for various Ollama models

## 🚀 Requirements

- 🐍 Python 3.10+
- 🖥️ Ollama installed and running
- 📦 Git (for cloning tree-sitter grammar)

## 🛠️ Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/wendelmax/JavaDocAI.git
cd JavaDocAI
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Build Java Parser
```bash
python build_parsers.py
```

> 🔨 This step is **mandatory** after cloning. It will:
> - Clone the tree-sitter-java repository
> - Compile the Java grammar
> - Generate necessary files in `build/`
>
> ⚠️ **Note**: Generated files are not versioned and must be recreated after cloning.

## ⚙️ Configuration

### 🤖 Model Selection

JavaDocAI supports any model available in your Ollama installation! Here's how to choose your preferred model:

1. **📋 List Available Models**
   ```bash
   ollama list
   ```

2. **🎯 Choose Your Model**
   Edit `config/config.yaml` and set your preferred model:
   ```yaml
   ollama:
     model: "your-chosen-model"  # e.g., "codellama:7b", "qwen:7b", etc.
   ```

   🌟 **Recommended Models**:
   - `qwen2.5-coder:7b` (default) - Excellent for detailed documentation
   - `codellama:7b` - Great for technical accuracy
   - `deepseek-coder:6.7b` - Balanced performance
   - `phind-codellama:34b` - Most comprehensive but slower

### 📝 Logging Configuration

Customize logging in `config/config.yaml`:
```yaml
logging:
  level: "DEBUG"  # Choose: DEBUG, INFO, WARNING, ERROR
  rotation: "1 day"
  retention: "1 week"
```

#### 🔍 Log Levels Explained:
- `DEBUG`: Shows detailed LLM generation process
- `INFO`: General execution information
- `WARNING`: Important warnings
- `ERROR`: Critical issues only

### ⚡ Processing Options

Fine-tune performance in `config/config.yaml`:
```yaml
processing:
  batch_size: 10              # Files processed per batch
  max_concurrent_tasks: 4     # Parallel processing threads
  timeout: 300               # Processing timeout in seconds
```

## 📚 Usage

### 1️⃣ Start Ollama Server
```bash
ollama serve
```

### 2️⃣ Run JavaDocAI
```bash
python main.py
```
When prompted, enter the path to your Java repository.

### 📝 Example Output

JavaDocAI generates professional Javadoc comments like this:
```java
/**
 * Calculates the sum of two integers.
 * 
 * This method performs basic arithmetic addition of two numbers
 * and returns their sum. It handles both positive and negative integers.
 *
 * @param a the first integer operand
 * @param b the second integer operand
 * @return the sum of a and b
 * @throws ArithmeticException if the result exceeds integer bounds
 */
public int add(int a, int b) {
    return a + b;
}
```

## 🤝 Contributing

We love your input! We want to make contributing to JavaDocAI as easy and transparent as possible. Please follow these steps:

1. 🍴 Fork the project
2. 🌱 Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. 💾 Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. 📤 Push to the branch (`git push origin feature/AmazingFeature`)
5. 🔍 Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Important Notes

- 🔍 Always review generated comments before committing
- 🚀 Start with a small codebase to test the configuration
- 📊 Use DEBUG logging to see the generation process
- 💡 Try different models to find the best fit for your needs

---

Made with ❤️ by the JavaDocAI team