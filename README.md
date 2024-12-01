# JavaDocAI 

An AI-powered tool that automatically generates high-quality Javadoc comments for your Java codebase using Ollama LLM.

## Features

- Automatic Javadoc generation for Java files
- Support for multiple Ollama models
- Multi-threaded processing for large codebases
- Configurable logging and processing options
- Internationalization support

## Requirements

- Python 3.10+
- Ollama installed and running
- Git (for cloning tree-sitter grammar)

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/wendelmax/JavaDocAI.git
   cd JavaDocAI
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Build Java Parser**
   ```bash
   python build_parsers.py
   ```
   This step is **mandatory** after cloning the repository. It will:
   - Clone the tree-sitter-java repository
   - Compile the Java grammar
   - Generate necessary files in the `build/` directory

   > **Note**: Generated files are not versioned and must be recreated after cloning.

## Configuration

### Model Selection
JavaDocAI supports any model available in Ollama. To choose a model:

1. **List Available Models**
   ```bash
   ollama list
   ```

2. **Update Configuration**
   Edit `config/config.yaml` and set your preferred model:
   ```yaml
   ollama:
     model: "your-chosen-model"  # e.g., "codellama:7b", "qwen:7b", etc.
   ```

   Recommended models for Javadoc generation:
   - qwen2.5-coder:7b (default)
   - codellama:7b
   - deepseek-coder:6.7b
   - phind-codellama:34b

### Logging Configuration
Configure logging in `config/config.yaml`:
```yaml
logging:
  level: "DEBUG"  # Options: DEBUG, INFO, WARNING, ERROR
  rotation: "1 day"
  retention: "1 week"
```

### Processing Options
Adjust processing settings in `config/config.yaml`:
```yaml
processing:
  batch_size: 10
  max_concurrent_tasks: 4
  timeout: 300
```

## Usage

1. **Start Ollama Server**
   ```bash
   ollama serve
   ```

2. **Run JavaDocAI**
   ```bash
   python main.py
   ```
   When prompted, enter the path to your Java repository.

## Output

Generated Javadoc comments will be added to your Java files following standard Javadoc format:
```java
/**
 * Calculates the sum of two numbers.
 *
 * @param a the first number
 * @param b the second number
 * @return the sum of a and b
 */
public int add(int a, int b) {
    return a + b;
}
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Note

Make sure to review generated comments before committing them to your codebase. While the AI strives for accuracy, human verification is recommended.