import json
from pathlib import Path
import pytest

def load_i18n_file():
    i18n_path = Path(__file__).parent.parent / "config" / "i18n.json"
    with open(i18n_path, "r", encoding="utf-8") as f:
        return json.load(f)

def test_i18n_file_exists():
    i18n_path = Path(__file__).parent.parent / "config" / "i18n.json"
    assert i18n_path.exists(), "i18n.json file should exist"

def test_i18n_file_is_valid_json():
    data = load_i18n_file()
    assert isinstance(data, dict), "i18n file should be a valid JSON object"

def test_supported_languages():
    data = load_i18n_file()
    required_languages = ["en", "pt"]
    for lang in required_languages:
        assert lang in data, f"Language '{lang}' should be supported"

def test_message_structure():
    data = load_i18n_file()
    required_categories = ["errors", "warnings", "info", "success", "progress", "prompts", "logs", "debug", "input"]
    
    for lang in data:
        for category in required_categories:
            assert category in data[lang], f"Category '{category}' should exist in language '{lang}'"

def test_message_consistency():
    """Ensure all languages have the same message keys"""
    data = load_i18n_file()
    languages = list(data.keys())
    
    # Use first language as reference
    reference_lang = languages[0]
    reference_messages = _get_all_message_keys(data[reference_lang])
    
    for lang in languages[1:]:
        current_messages = _get_all_message_keys(data[lang])
        assert reference_messages == current_messages, \
            f"Language '{lang}' has different message keys than '{reference_lang}'"

def test_placeholder_consistency():
    """Ensure placeholders are consistent across translations"""
    data = load_i18n_file()
    languages = list(data.keys())
    
    for category in data[languages[0]]:
        for msg_key, msg_value in data[languages[0]][category].items():
            placeholders = _extract_placeholders(msg_value)
            
            for lang in languages[1:]:
                if category in data[lang] and msg_key in data[lang][category]:
                    trans_placeholders = _extract_placeholders(data[lang][category][msg_key])
                    assert placeholders == trans_placeholders, \
                        f"Placeholders mismatch in '{category}.{msg_key}' for language '{lang}'"

def _get_all_message_keys(lang_data):
    """Get all message keys from a language section"""
    keys = set()
    for category in lang_data:
        if isinstance(lang_data[category], dict):
            keys.update(f"{category}.{k}" for k in lang_data[category].keys())
    return keys

def _extract_placeholders(text):
    """Extract all placeholders like {name} from a text"""
    import re
    return set(re.findall(r'\{([^}]+)\}', str(text)))
