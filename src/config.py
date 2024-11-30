import os
from pathlib import Path
from typing import Dict, Any
import yaml
from dotenv import load_dotenv

# Load environment variables from a .env file, if it exists
load_dotenv()

# Constants for paths
BASE_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = BASE_DIR / "config" / "i18n.json"
CONFIG_YAML = BASE_DIR / "config" / "config.yaml"
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

def load_config() -> Dict[str, Any]:
    """Load configuration from YAML file with environment variable overrides."""
    if not CONFIG_YAML.is_file():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_YAML}")
    
    with CONFIG_YAML.open("r") as f:
        config = yaml.safe_load(f)
    
    # Override with environment variables if they exist
    env_mappings = {
        "OLLAMA_SERVER_PORT": ("ollama", "server_port"),
        "OLLAMA_SCHED_SPREAD": ("ollama", "sched_spread"),
        "OLLAMA_FLASH_ATTENTION": ("ollama", "flash_attention"),
        "LOG_LEVEL": ("logging", "level"),
        "LANGUAGE_CONFIG": ("language", "default"),
    }
    
    for env_var, (section, key) in env_mappings.items():
        if env_value := os.getenv(env_var):
            if section not in config:
                config[section] = {}
            config[section][key] = env_value if not env_value.isdigit() else int(env_value)
    
    return config

# Load configuration
config = load_config()

# Export configuration values
OLLAMA_SERVER_PORT = config["ollama"]["server_port"]
OLLAMA_SCHED_SPREAD = str(config["ollama"]["sched_spread"]).lower()
OLLAMA_FLASH_ATTENTION = str(config["ollama"]["flash_attention"]).lower()
MAX_RETRIES = config["ollama"]["max_retries"]
RETRY_DELAY = config["ollama"]["retry_delay"]
LOG_FILE_PATH = LOG_DIR / config["paths"]["log_file"]
LANGUAGE = config["language"]["default"]
