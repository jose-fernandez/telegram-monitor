import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.core.bot_engine import TelegramMonitorBot

@pytest.fixture
def mock_telethon(monkeypatch):
    # Mock TelegramClient class
    client_mock = MagicMock()
    monkeypatch.setattr("src.core.bot_engine.TelegramClient", MagicMock(return_value=client_mock))
    monkeypatch.setenv("API_ID", "123")
    monkeypatch.setenv("API_HASH", "abc")
    monkeypatch.setenv("BOT_TOKEN", "test_token")

@pytest.mark.asyncio
async def test_bot_send_alert(mock_telethon):
    bot = TelegramMonitorBot()
    bot.my_user_id = 12345
    
    with patch("src.core.bot_engine.aiohttp.ClientSession.post") as mock_post:
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_post.return_value.__aenter__.return_value = mock_response
        
        await bot.send_bot_alert("Test alert message")
        
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert kwargs['json']['text'] == "Test alert message"
        assert kwargs['json']['chat_id'] == 12345
