# Contributing to Telegram Monitor Bot

Welcome! We've designed this project to be highly modular and easy to contribute to.

## Architecture
- `src/core/`: Contains `bot_engine.py` with all the Telethon logic. It is completely decoupled from the UI.
- `src/gui/`: Contains `app.py`, an intuitive `customtkinter` desktop app for managing the bot setup and lifecycle.
- `src/utils/`: Handlers for reading/writing configuration files (`config.json`, `.env`) and managing translations (`i18n.py`).
- `main_gui.py`: Entry point for the visual desktop app.
- `main_cli.py`: Entry point for running the bot directly (e.g. inside Docker or on a VPS).

## Setup for Development
1. Clone the repository.
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the visual wizard to test GUI changes:
   ```bash
   python main_gui.py
   ```
4. Run the CLI version to test core bot logic headless:
   ```bash
   python main_cli.py
   ```

## Adding Features
- **New Bot Commands**: Add them in `src/core/bot_engine.py` under the `setup_handlers` method.
- **New Languages**: Add your translations to the `TRANSLATIONS` dictionary in `src/utils/i18n.py`.
- **UI Enhancements**: Modify `src/gui/app.py`. Try to keep the UI simple, modern, and accessible for non-technical users.
