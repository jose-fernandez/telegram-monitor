import os
import json
from src.utils.config import load_config, save_config

def test_save_and_load_config(temp_config_dir, dummy_app_state, monkeypatch):
    # Patch the actual config loading to use temp_config_dir
    monkeypatch.chdir(temp_config_dir)
    
    save_config(dummy_app_state)
    assert os.path.exists("config.json")
    
    loaded = load_config()
    assert loaded["keywords"] == dummy_app_state["keywords"]
    assert loaded["language"] == "en"

def test_load_config_defaults(temp_config_dir, monkeypatch):
    monkeypatch.chdir(temp_config_dir)
    loaded = load_config()
    assert "keywords" in loaded
    assert "channels" in loaded
    assert loaded["language"] == "en"
