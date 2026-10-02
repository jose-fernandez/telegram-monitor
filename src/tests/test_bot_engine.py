import os
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.core.bot_engine import TelegramMonitorBot

@pytest.fixture
def mock_telethon(monkeypatch, tmp_path):
    # Mock TelegramClient class
    client_mock = MagicMock()
    client_class = MagicMock(return_value=client_mock)
    monkeypatch.setattr("src.core.bot_engine.TelegramClient", client_class)
    # Run from an empty directory so a developer's real config.json is never read
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("TELEGRAM_API_ID", "123")
    monkeypatch.setenv("TELEGRAM_API_HASH", "abc")
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
    return client_class

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
        assert kwargs['json']['parse_mode'] == "HTML"

def test_build_alert_escapes_channel_text(mock_telethon):
    bot = TelegramMonitorBot()
    bot.state['language'] = 'en'

    message = bot.build_alert("@deals<&>", "50% off <b>today</b> & *now* _only_ [link")

    assert message == (
        "🚨 <b>Alert in @deals&lt;&amp;&gt;</b>\n\n"
        "50% off &lt;b&gt;today&lt;/b&gt; &amp; *now* _only_ [link"
    )

def test_session_defaults_to_working_directory(mock_telethon):
    TelegramMonitorBot()

    session = mock_telethon.call_args.args[0]
    assert session == os.path.join(".", "sesion_monitor")

def test_session_lives_in_data_dir(mock_telethon, monkeypatch, tmp_path):
    data = tmp_path / "data"
    data.mkdir()
    monkeypatch.setenv("MONITOR_DATA_DIR", str(data))

    TelegramMonitorBot()

    session = mock_telethon.call_args.args[0]
    assert session == os.path.join(str(data), "sesion_monitor")
