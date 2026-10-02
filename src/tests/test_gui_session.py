import os
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.gui.app import PhoneSetupFrame

# Calls the frame's coroutine with a stand-in for the widget, so this runs
# without a display, unlike test_gui_flows.py.

@pytest.mark.asyncio
async def test_gui_login_uses_the_data_dir_session(monkeypatch, tmp_path):
    data = tmp_path / "data"
    data.mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("MONITOR_DATA_DIR", str(data))
    monkeypatch.setenv("TELEGRAM_API_ID", "123")
    monkeypatch.setenv("TELEGRAM_API_HASH", "abc")

    client = MagicMock()
    client.connect = AsyncMock()
    client.disconnect = AsyncMock()
    client.is_user_authorized = AsyncMock(return_value=True)
    client_class = MagicMock(return_value=client)
    monkeypatch.setattr("src.gui.app.TelegramClient", client_class)

    frame = SimpleNamespace(app=MagicMock())
    await PhoneSetupFrame.do_request_code(frame, "+34600000000")

    assert client_class.call_args.args[0] == os.path.join(str(data), "sesion_monitor")
