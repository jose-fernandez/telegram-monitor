import html
import os
import re
import aiohttp
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from src.core.bot_engine import TelegramMonitorBot, MAX_CHUNK_UNITS

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

    messages = bot.build_alerts("@deals<&>", "50% off <b>today</b> & *now* _only_ [link")

    assert messages == [
        "🚨 <b>Alert in @deals&lt;&amp;&gt;</b>\n\n"
        "50% off &lt;b&gt;today&lt;/b&gt; &amp; *now* _only_ [link"
    ]

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

def utf16_len(text):
    return len(text.encode('utf-16-le')) // 2

def visible_text(message):
    # What the Bot API's 4096 limit counts: the text after HTML is parsed
    return html.unescape(re.sub(r"</?b>", "", message))

def alert_bodies(messages):
    # Strip the header and undo the escaping, giving back the channel text
    return [html.unescape(m.split("\n\n", 1)[1]) for m in messages]

def test_long_alert_is_split_without_losing_text(mock_telethon):
    bot = TelegramMonitorBot()
    bot.state['language'] = 'en'
    text = ("line with <tags> & stuff\n\n" * 400)[:9000]

    messages = bot.build_alerts("@deals", text)

    assert len(messages) == 3
    assert "".join(alert_bodies(messages)) == text
    assert all(utf16_len(visible_text(m)) <= 4096 for m in messages)
    assert messages[0].startswith("🚨 <b>Alert in @deals (1/3)</b>")
    assert messages[2].startswith("🚨 <b>Alert in @deals (3/3)</b>")

def test_split_counts_emoji_as_two_units(mock_telethon):
    bot = TelegramMonitorBot()
    text = "😀" * 3000  # 6000 UTF-16 units, but only 3000 Python characters

    messages = bot.build_alerts("@deals", text)

    assert len(messages) == 2
    assert "".join(alert_bodies(messages)) == text
    assert all(utf16_len(body) <= MAX_CHUNK_UNITS for body in alert_bodies(messages))

class FakeClock:
    def __init__(self):
        self.now = 1000.0
        self.sleeps = []

    def time(self):
        return self.now

    async def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds

@pytest.fixture
def clocked_bot(mock_telethon):
    bot = TelegramMonitorBot()
    clock = FakeClock()
    bot._now = clock.time
    bot._sleep = clock.sleep
    return bot, clock

@pytest.mark.asyncio
async def test_alerts_over_the_rate_limit_wait_instead_of_dropping(clocked_bot):
    bot, clock = clocked_bot

    for _ in range(3):
        await bot.wait_for_notification_slot()
    assert clock.sleeps == []

    await bot.wait_for_notification_slot()

    assert clock.sleeps == [60]
    assert len(bot.notification_timestamps) == 1

def response(status, body=""):
    resp = AsyncMock()
    resp.status = status
    resp.text.return_value = body
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=resp)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm

@pytest.mark.asyncio
@pytest.mark.parametrize("failure, expected_wait", [
    (response(429, '{"ok": false, "parameters": {"retry_after": 7}}'), 7),
    (response(502, "Bad Gateway"), 1),
    (aiohttp.ClientConnectionError("network down"), 1),
])
async def test_temporary_failures_are_retried(clocked_bot, failure, expected_wait):
    bot, clock = clocked_bot
    bot.my_user_id = 12345

    with patch("src.core.bot_engine.aiohttp.ClientSession.post",
               side_effect=[failure, response(200)]) as mock_post:
        delivered = await bot.send_bot_alert("hi")

    assert delivered is True
    assert mock_post.call_count == 2
    assert clock.sleeps == [expected_wait]

@pytest.mark.asyncio
async def test_retry_delay_backs_off(clocked_bot):
    bot, clock = clocked_bot
    bot.my_user_id = 12345
    failures = [response(500) for _ in range(8)]

    with patch("src.core.bot_engine.aiohttp.ClientSession.post",
               side_effect=failures + [response(200)]):
        assert await bot.send_bot_alert("hi") is True

    assert clock.sleeps == [1, 2, 4, 8, 16, 32, 60, 60]

@pytest.mark.asyncio
async def test_rejected_request_is_not_retried(clocked_bot):
    bot, clock = clocked_bot
    bot.my_user_id = 12345

    with patch("src.core.bot_engine.aiohttp.ClientSession.post",
               side_effect=[response(400, "Bad Request: chat not found")]) as mock_post:
        delivered = await bot.send_bot_alert("hi")

    assert delivered is False
    assert mock_post.call_count == 1
    assert clock.sleeps == []

