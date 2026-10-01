import pytest
import os
import tempfile

@pytest.fixture
def temp_config_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname

@pytest.fixture
def dummy_app_state():
    return {
        "keywords": ["test", "keyword"],
        "channels": ["@testchannel"],
        "language": "en"
    }

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("API_ID", "12345")
    monkeypatch.setenv("API_HASH", "test_hash")
    monkeypatch.setenv("BOT_TOKEN", "test_token")
