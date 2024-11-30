import os
import time
import socket
import subprocess
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

from tree_sitter import Language, Parser
import tree_sitter_java as java
from tqdm import tqdm
from ollama import Client, ResponseError

from src.config import config
from src.logger import log

class JavaDocAI:
    """Main class to add Javadoc comments to Java files in a repository."""

    def __init__(self, repo_dir: Path, messages: Dict[str, Dict[str, str]]):
        """Initialize JavaDocAI with repository directory and messages."""
        self.repo_dir = repo_dir
        self.messages = messages
        self.logs = messages["logs"]
        self.debug_msgs = messages["debug"]
        self.info_msgs = messages["info"]
        self.prompts = messages["prompts"]
        self.misc = messages["misc"]
        self.errors = messages["errors"]
        self.input_msgs = messages["input"]
        self.cli_msgs = messages["cli"]
        self.ollama_msgs = messages["ollama"]
        self.warnings = messages["warnings"]
        self.class_relationships: Dict[str, List[str]] = {}
        self.parser = self.initialize_parser()
        self.client = Client(host=f'http://localhost:{config["ollama"]["server_port"]}')
        self.max_retries = config["ollama"]["max_retries"]
        self.retry_delay = config["ollama"]["retry_delay"]
        self.batch_size = config["processing"]["batch_size"]
        self.max_concurrent_tasks = config["processing"]["max_concurrent_tasks"]

    @staticmethod
    def initialize_parser() -> Parser:
        """Initialize the Tree-sitter parser for Java."""
        try:
            JAVA_LANGUAGE = Language(java.language())
            parser = Parser(JAVA_LANGUAGE)
            return parser
        except Exception as e:
            log.error(f"Failed to initialize Java parser: {e}")
            raise

    def run(self):
        """Execute the main flow of JavaDocAI."""
        try:
            # Ensure Ollama is configured
            if not self.ensure_ollama_setup():
                log.error("Ollama setup failed")
                return

            # Check if Ollama server is running
            if not self.is_ollama_server_running():
                log.error("Ollama server is not running")
                return

            # Process Java files to add Javadoc
            self.process_files()
        except Exception as e:
            log.error(f"Error in main execution: {e}")
            raise

    def ensure_ollama_setup(self) -> bool:
        """Ensure Ollama is installed and set up with proper error handling."""
        try:
            if not self.is_ollama_installed():
                log.info("Installing Ollama...")
                self.install_ollama()
                if not self.is_ollama_installed():
                    log.error("Failed to install Ollama")
                    return False

            # Check if model is available
            model_name = config["ollama"]["model"]
            available_models = self.client.list()
            model_present = any(
                model["name"] == model_name for model in available_models.get("models", [])
            )

            if not model_present:
                log.info(f"Downloading model {model_name}...")
                self.client.pull(model_name)
                log.info(f"Model {model_name} downloaded successfully")
            else:
                log.info(f"Model {model_name} is already available")

            return True
        except Exception as e:
            log.error(f"Error in Ollama setup: {e}")
            return False

    def is_ollama_server_running(self) -> bool:
        """Check if Ollama server is running with proper error handling."""
        try:
            with socket.create_connection(("localhost", config["ollama"]["server_port"]), timeout=5):
                return True
        except (socket.timeout, ConnectionRefusedError):
            log.error("Could not connect to Ollama server")
            return False
        except Exception as e:
            log.error(f"Unexpected error checking Ollama server: {e}")
            return False

    def process_files(self):
        """Process Java files in batches with proper error handling."""
        try:
            java_files = list(self.repo_dir.rglob("*.java"))
            log.info(f"Found {len(java_files)} Java files to process")

            with ThreadPoolExecutor(max_workers=self.max_concurrent_tasks) as executor:
                for i in range(0, len(java_files), self.batch_size):
                    batch = java_files[i:i + self.batch_size]
                    futures = [executor.submit(self.process_file, file) for file in batch]
                    
                    for future in tqdm(as_completed(futures), total=len(batch)):
                        try:
                            result = future.result()
                            if result:
                                log.info(f"Successfully processed file: {result}")
                        except Exception as e:
                            log.error(f"Error processing file in batch: {e}")
        except Exception as e:
            log.error(f"Error in file processing: {e}")
            raise

    def process_file(self, file_path: Path):
        """Process a single Java file."""
        try:
            with file_path.open("r", encoding="utf-8") as file:
                original_code = file.read()
        except Exception as e:
            log.error(f"Error reading file: {file_path} - {e}")
            return

        updated_code = self.add_javadocs(original_code, file_path)
        if updated_code:
            self.update_java_file(file_path, updated_code)
            log.info(f"File processed: {file_path}")
            return file_path
        else:
            log.warning(f"Error processing file: {file_path}")

        time.sleep(1)  # Small pause to avoid rate limits

    def update_java_file(self, file_path: Path, updated_code: str):
        """Update the Java file with the new code."""
        try:
            # Write the updated code to the original file
            with file_path.open("w", encoding="utf-8") as file:
                file.write(updated_code)
        except Exception as e:
            log.error(f"Error writing file: {file_path} - {e}")

    def add_javadocs(self, java_code: str, file_path: Path) -> Optional[str]:
        """
        Generates Javadoc comments and merges them into the original code.

        Args:
            java_code (str): Original Java code.
            file_path (Path): Path to the Java file.

        Returns:
            Optional[str]: Java code updated with Javadocs or None if an error occurs.
        """
        classes = self.extract_class_structures(java_code)
        if not classes:
            log.warning(f"No signatures found in file: {file_path}")
            return None

        insertions = []

        for class_info in classes:
            # Get Javadoc for the class
            class_javadoc = self.get_javadoc_for_signature(class_info['signature'], 'class')
            if class_javadoc:
                # Prepare the insertion for the class (before the class declaration)
                insertions.append({
                    'line': class_info['start_line'],
                    'comment': class_javadoc
                })

            # Process methods of the class
            for method_info in class_info['methods']:
                method_javadoc = self.get_javadoc_for_signature(method_info['signature'], 'method')
                if method_javadoc:
                    # Prepare the insertion for the method (before the method declaration)
                    insertions.append({
                        'line': method_info['start_line'],
                        'comment': method_javadoc
                    })

        if not insertions:
            log.info("No Javadoc comments to add")
            return java_code

        # Sort insertions by line number in descending order
        insertions_sorted = sorted(insertions, key=lambda x: x['line'], reverse=True)

        updated_code = java_code.splitlines()
        cumulative_offset = 0

        for insertion in insertions_sorted:
            line_number = insertion['line'] + cumulative_offset  # Adjust for previous insertions
            comment = insertion['comment']

            # Check if Javadoc already exists above the line
            if self.has_javadoc_above(updated_code, line_number):
                log.info(f"Javadoc already exists above line {line_number + 1}. Skipping insertion.")
                continue

            # Insert the comment before the specified line
            updated_code.insert(line_number, comment)
            log.debug(f"Inserting Javadoc at line {line_number + 1}:\n{comment}")

            cumulative_offset += 1  # Each insertion adds a line

        # Join the updated code
        final_code = '\n'.join(updated_code)
        return final_code

    def has_javadoc_above(self, code_lines: List[str], line_number: int) -> bool:
        """
        Check if a Javadoc comment already exists above a specific line.

        Args:
            code_lines (List[str]): List of code lines.
            line_number (int): Line number to check (0-based index).

        Returns:
            bool: True if a Javadoc comment exists above the line, False otherwise.
        """
        if line_number == 0:
            return False  # No lines above

        previous_line = code_lines[line_number - 1].strip()
        return previous_line.startswith('/**')

    def get_javadoc_for_signature(self, signature: str, signature_type: str) -> Optional[str]:
        """
        Send a signature to the AI and get the corresponding Javadoc comment.

        Args:
            signature (str): The signature of the class or method.
            signature_type (str): 'class' or 'method'.

        Returns:
            Optional[str]: The generated Javadoc comment or None if an error occurs.
        """
        prompt = self.prompts["single_prompt"].format(
            signature_type=signature_type,
            signature=signature
        )

        try:
            response = self.get_ai_single_response(prompt)
            if response:
                # Validate the Javadoc comment format
                response = response.strip()
                if response.startswith('/**') and response.endswith('*/'):
                    # Remove any additional '*/' in the middle of the comment
                    first_closing = response.find('*/')
                    if first_closing != len(response) - 2:
                        # Truncate after the first '*/'
                        response = response[:first_closing + 2]
                    return response
                else:
                    log.warning(f"Invalid Javadoc format received for {signature_type}: {signature}")
                    log.debug(f"Received Javadoc: {response}")
                    return None
            else:
                return None
        except Exception as e:
            log.error(f"Error getting Javadoc for signature: {e}")
            return None

    def get_ai_single_response(self, prompt: str) -> Optional[str]:
        """
        Send a prompt to the AI and get the response.

        Args:
            prompt (str): The prompt to send.

        Returns:
            Optional[str]: The AI response as a string.
        """
        try:
            stream = self.client.chat(
                model=config["ollama"]["model"],
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional Java developer. Your task is to generate high-quality Javadoc comments that follow best practices."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                stream=True,
                options={
                    "temperature": config["ollama"]["temperature"],
                    "top_p": config["ollama"]["top_p"],
                    "context_window": config["ollama"]["context_window"]
                }
            )

            response = ""
            for chunk in stream:
                content = chunk.get('message', {}).get('content', '')
                response += content

            # Log the complete model response
            log.debug(f"Complete model response: {response}")

            return response.strip()

        except ResponseError as e:
            log.error(f"Ollama API error: {e.error}")
            return None
        except Exception as e:
            log.error(f"Error getting AI response: {e}")
            return None

    def extract_class_structures(self, java_code: str) -> List[Dict]:
        """
        Extract the structure of classes and methods from the Java code.

        Args:
            java_code (str): The original Java code.

        Returns:
            List[Dict]: A list of dictionaries representing each class, with their methods.
        """
        tree = self.parser.parse(bytes(java_code, "utf8"))
        root_node = tree.root_node
        classes = []

        # Function to recursively walk the syntax tree
        def walk(node, parent_class=None):
            if node.type in ['class_declaration', 'interface_declaration', 'enum_declaration']:
                # Extract the class signature
                start = node.start_byte
                for child in node.children:
                    if child.type == 'class_body':
                        end = child.start_byte  # Exclude the body
                        break
                else:
                    end = node.end_byte
                class_signature = java_code[start:end].strip()
                # Get the class name
                class_name = None
                for child in node.children:
                    if child.type == 'identifier':
                        class_name = java_code[child.start_byte:child.end_byte]
                        break
                # Get the starting line number
                start_line = node.start_point[0]  # 0-based index

                class_dict = {
                    'type': 'class',
                    'signature': class_signature,
                    'name': class_name,
                    'methods': [],
                    'start_line': start_line
                }
                # Recurse into the class body
                for child in node.children:
                    if child.type == 'class_body':
                        for class_body_child in child.children:
                            walk(class_body_child, parent_class=class_dict)
                classes.append(class_dict)
            elif node.type == 'method_declaration' and parent_class is not None:
                # Extract the method signature
                start = node.start_byte
                for child in node.children:
                    if child.type == 'block':
                        end = child.start_byte  # Exclude the method body
                        break
                else:
                    end = node.end_byte
                method_signature = java_code[start:end].strip()
                # Get the method name
                method_name = None
                for child in node.children:
                    if child.type == 'identifier':
                        method_name = java_code[child.start_byte:child.end_byte]
                        break
                # Get the starting line number
                start_line = node.start_point[0]  # 0-based index

                method_dict = {
                    'type': 'method',
                    'signature': method_signature,
                    'name': method_name,
                    'start_line': start_line
                }
                parent_class['methods'].append(method_dict)
            else:
                # Recurse into child nodes
                for child in node.children:
                    walk(child, parent_class=parent_class)

        walk(root_node)
        return classes

    def is_ollama_installed(self) -> bool:
        """Check if Ollama is installed."""
        return shutil.which("ollama") is not None

    def install_ollama(self):
        """Install Ollama."""
        try:
            log.info("Installing Ollama...")
            subprocess.run(
                "curl -fsSL https://ollama.com/install.sh | sh",
                shell=True,
                check=True
            )
            log.info("Ollama installed successfully")
        except subprocess.CalledProcessError as e:
            log.error(f"Error installing Ollama: {e}")
        except Exception as e:
            log.error(f"Unexpected error installing Ollama: {e}")

    def start_ollama_server(self):
        """Start the Ollama server."""
        try:
            log.info("Starting Ollama server...")
            subprocess.Popen(["ollama", "serve"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            log.info("Ollama server started")
            time.sleep(15)  # Wait to ensure the server is operational
            if self.is_ollama_server_running():
                log.info("Ollama server is running")
            else:
                log.error("Ollama server failed to start")
        except Exception as e:
            log.error(f"Error starting Ollama server: {e}")