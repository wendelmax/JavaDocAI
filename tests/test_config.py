import os
import pytest
from pathlib import Path
from src.config import load_config

@pytest.fixture
def mock_config_file(tmp_path):
    config_content = """
    ollama:
      server_port: 11434
      sched_spread: true
      flash_attention: true
    language:
      default: "en"
    """
    config_file = tmp_path / "config.yaml"
    config_file.write_text(config_content)
    return config_file

def test_load_config_with_env_override(monkeypatch, mock_config_file):
    # Setup
    monkeypatch.setenv("OLLAMA_SERVER_PORT", "11435")
    monkeypatch.setenv("LANGUAGE_CONFIG", "pt")
    
    # Test
    config = load_config()
    
    # Assert
    assert config["ollama"]["server_port"] == 11435
    assert config["language"]["default"] == "pt"

def test_load_config_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config()
