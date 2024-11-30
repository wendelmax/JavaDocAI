import argparse
from pathlib import Path

from src.java_doc_ai import JavaDocAI
from src.config import CONFIG_PATH, LANGUAGE
from src.utils import load_messages, get_repository_directory
from src.logger import log

def main():
    """Main function to coordinate the Javadoc addition process."""
    # Load language messages
    try:
        messages = load_messages(LANGUAGE, CONFIG_PATH)
        if not messages:
            log.error(f"Messages for language '{LANGUAGE}' not found in the configuration file.")
            return
    except Exception as e:
        log.error(f"Could not load language messages: {e}")
        return

    repo_dir = get_repository_directory(messages)

    log.info(messages["logs"]["repo_dir_set"].format(repo_dir=repo_dir))

    # Initialize JavaDocAI and run
    ai = JavaDocAI(repo_dir, messages=messages)
    ai.run()

if __name__ == "__main__":
    main()
