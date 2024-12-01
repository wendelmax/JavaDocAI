from tree_sitter import Language, Parser
import os
from pathlib import Path

def build_languages():
    # Create the build directory if it doesn't exist
    build_dir = Path('build')
    build_dir.mkdir(exist_ok=True)
    
    # Clone the Java grammar repository if it doesn't exist
    java_repo_path = Path('tree-sitter-java')
    if not java_repo_path.exists():
        os.system('git clone https://github.com/tree-sitter/tree-sitter-java.git')
    
    # Build the languages
    Language.build_library(
        # Store the library in the `build` directory
        'build/java-languages.so',
        # Include the Java grammar
        [str(java_repo_path)]
    )

if __name__ == '__main__':
    build_languages()
