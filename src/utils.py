import json
import logging
from pathlib import Path

def load_messages(language: str, config_path: Path) -> dict[str, dict]:
    """Load messages from the JSON configuration file."""
    if not config_path.is_file():
        error_message = f"Configuration file not found: {config_path}"
        logging.error(error_message)
        raise FileNotFoundError(error_message)
    with config_path.open(encoding="utf-8") as file:
        messages = json.load(file)
    return messages.get(language, {})

def get_repository_directory(messages: dict[str, dict[str, str]]) -> Path:
    """Prompt the user for the repository directory and validate it."""
    while True:
        repo_dir_input = input(messages["input"]["enter_repo_dir"]).strip()
        repo_dir = Path(repo_dir_input)
        if not repo_dir.is_dir():
            logging.error(messages["input"]["dir_not_exist"])
            continue
        java_files = list(repo_dir.rglob("*.java"))
        if not java_files:
            logging.error(messages["input"]["no_java_files"])
            continue
        return repo_dir
