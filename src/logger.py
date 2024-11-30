from loguru import logger
import sys
from pathlib import Path
from src.config import config, LOG_DIR

def setup_logger():
    """Configure loguru logger with rotation and custom format."""
    # Remove default handler
    logger.remove()
    
    # Add console handler
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=config["logging"]["level"],
        colorize=True,
    )
    
    # Add file handler with rotation
    log_file = LOG_DIR / "java_doc_ai.log"
    logger.add(
        log_file,
        rotation=config["logging"]["rotation"],
        retention=config["logging"]["retention"],
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=config["logging"]["level"],
        compression="zip",
    )
    
    return logger

# Create logger instance
log = setup_logger()
