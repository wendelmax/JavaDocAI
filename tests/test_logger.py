import pytest
from pathlib import Path
from src.logger import setup_logger

def test_logger_setup(tmp_path):
    # Test logger initialization
    logger = setup_logger()
    assert logger is not None

def test_log_file_creation(tmp_path):
    # Setup logger with temporary directory
    logger = setup_logger()
    
    # Test logging
    logger.info("Test log message")
    
    # Check if log file exists
    log_file = Path("logs/java_doc_ai.log")
    assert log_file.exists()
    
    # Check log content
    log_content = log_file.read_text()
    assert "Test log message" in log_content
