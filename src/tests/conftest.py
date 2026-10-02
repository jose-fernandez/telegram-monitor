import pytest
import os
import tempfile

@pytest.fixture(autouse=True)
def no_ambient_data_dir(monkeypatch):
    # MONITOR_DATA_DIR moves config and session files; a value set on the
    # machine running the tests must not leak in.
    monkeypatch.delenv("MONITOR_DATA_DIR", raising=False)

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
    monkeypatch.setenv("TELEGRAM_API_ID", "12345")
    monkeypatch.setenv("TELEGRAM_API_HASH", "test_hash")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
