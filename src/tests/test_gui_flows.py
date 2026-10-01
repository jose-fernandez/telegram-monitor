import pytest
from unittest.mock import AsyncMock, patch, MagicMock
import os
import tkinter as tk

from src.gui.app import WizardApp, ApiSetupFrame, PhoneSetupFrame, DashboardFrame

# Only run these tests if there is a display available
import os
has_display = os.environ.get('DISPLAY') or os.name == 'nt' or os.uname().sysname == 'Darwin'

@pytest.fixture
def app_instance(monkeypatch):
    monkeypatch.setenv("API_ID", "")
    monkeypatch.setenv("API_HASH", "")
    monkeypatch.setenv("BOT_TOKEN", "")
    
    # Use mock config
    monkeypatch.setattr("src.gui.app.load_config", lambda: {"language": "en"})
    monkeypatch.setattr("src.gui.app.save_config", lambda x: None)
    
    app = WizardApp()
    app.update()
    yield app
    app.destroy()

@pytest.mark.skipif(not has_display, reason="Requires a display server (e.g. X11/macOS)")
@pytest.mark.asyncio
async def test_api_to_dashboard_flow_authorized(app_instance, monkeypatch):
    app_instance.show_frame(ApiSetupFrame)
    frame = app_instance.current_frame
    
    frame.api_id.insert(0, "123")
    frame.api_hash.insert(0, "abc")
    frame.bot_token.insert(0, "bot123")
    
    mock_client = AsyncMock()
    mock_client.is_user_authorized.return_value = True
    
    with patch("src.gui.app.TelegramClient", return_value=mock_client):
        await frame.check_auth("123", "abc")
        
    app_instance.update()
    assert isinstance(app_instance.current_frame, DashboardFrame)

@pytest.mark.skipif(not has_display, reason="Requires a display server (e.g. X11/macOS)")
@pytest.mark.asyncio
async def test_logout_flow(app_instance, monkeypatch):
    app_instance.app_state['phone'] = "+1234567890"
    app_instance.show_frame(DashboardFrame)
    frame = app_instance.current_frame
    
    mock_client = AsyncMock()
    mock_client.is_connected = MagicMock(return_value=True)
    app_instance.client = mock_client
    
    await frame._do_logout()
    app_instance.update()
    
    assert isinstance(app_instance.current_frame, PhoneSetupFrame)
    assert 'phone' not in app_instance.app_state
