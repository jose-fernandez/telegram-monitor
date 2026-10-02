# Telegram Monitor Bot

Get a notification on your phone whenever a Telegram channel you follow posts a message containing one of your keywords.

It works with two Telegram identities:

- **Your own account** reads the channels. It only listens; it never posts. You don't need to be an admin of the channels, just a member.
- **A bot you create** sends you the alerts. Because they come from a bot, your phone rings like any normal notification, even if you've muted the channels themselves.

You run it on your own computer, or 24/7 on a home server with Docker (a Raspberry Pi, a VPS…).

## Features

- **Silent Monitoring:** Uses your Telegram account (Userbot) to listen to channels you are a member of, without needing to be an administrator.
- **Push Notifications:** Uses the Official Telegram Bots API to send you alerts, ensuring you receive a notification with sound on your mobile phone.
- **Interactive Configuration:** No need to touch the code or restart the server. Control the bot directly from your **Saved Messages** in Telegram using commands.
- **Anti-spam Protection:** Avoids saturating your phone by limiting notifications (by default, maximum 3 alerts per minute).
- **No Lost Alerts:** Alerts over that limit wait their turn instead of being dropped, long posts are split across several messages, and temporary Telegram or network failures are retried until the alert arrives.
- **Simple Deployment:** Includes `Dockerfile` and `docker-compose.yml`, and a ready-made image is published for servers.

## Setup at a glance

1. [Get your three Telegram keys](#step-1--get-your-three-telegram-keys) (about 5 minutes, done once).
2. [Log in once on your computer](#step-2--log-in-once-on-your-computer), either with the visual setup window or from a terminal.
3. [Tell the bot what to watch](#step-3--tell-the-bot-what-to-watch) by sending it commands from Telegram.
4. *Optional:* [run it 24/7 on a server](#step-4-optional--run-it-247-on-a-server-with-docker) with Docker.

## Step 1 — Get your three Telegram keys

Treat these like passwords: anyone holding them can act as your app or your bot.

1. **`TELEGRAM_API_ID`** and **`TELEGRAM_API_HASH`** let the program read Telegram as you:
   - Go to [my.telegram.org](https://my.telegram.org) and log in with your phone number.
   - Go to **API development tools**.
   - Create a new application (you can make up the name) and copy the `api_id` (a number) and `api_hash` (a long string of letters and numbers).
2. **`TELEGRAM_BOT_TOKEN`** lets the program send you alerts through your own bot:
   - Open Telegram and search for **@BotFather**.
   - Send the `/newbot` command and follow the steps. It asks for a name and a username ending in `bot`.
   - Copy the token it gives you at the end (it looks like `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`).
   - **Important:** open a chat with your new bot and press **Start** (or send `/start`). A bot cannot message you until you've done this, and without it no alert will ever arrive.

## Step 2 — Log in once on your computer

The program has to log in to your Telegram account once, typing your phone number and the code Telegram sends you. That login is saved in a file called `sesion_monitor.session`, so you won't be asked again. **This step always happens on a computer with a screen and keyboard, even if the bot will later run on a server**, because a server has no way to type the code.

You need **Python 3.11 or newer**:

- **Windows / macOS:** download it from [python.org](https://www.python.org/downloads/). On Windows, tick **"Add Python to PATH"** in the installer.
- **Linux:** usually already installed. For the visual window you also need Tk: `sudo apt install python3-tk` on Debian/Ubuntu.

Download this project: the green **Code** button on GitHub → **Download ZIP**, then unzip it (or `git clone` it). Open a terminal in the project folder:

- **Windows:** open the folder in File Explorer, click the address bar, type `cmd` and press Enter.
- **macOS:** right-click the folder → **New Terminal at Folder**.

Install what the program needs (once):

```bash
pip install -r requirements.txt
```

If `pip` is not found, try `pip3`, or `python -m pip`.

Then pick **one** of the two options below. Both end up in the same place.

### Option A — Visual setup window (easiest)

```bash
python main_gui.py
```

(On macOS and Linux it may be `python3 main_gui.py`.)

A window guides you through it:

1. **API keys:** paste the three keys from Step 1.
2. **Phone:** your number with the country code, e.g. `+34600000000`.
3. **Code:** the code Telegram sends you, inside the Telegram app.
4. **Dashboard:** add keywords and channels, and press **Start** to run the bot.

The bot runs as long as that window is open and the computer is awake. To keep it running all the time, continue with Step 4.

### Option B — Terminal

1. Copy `.env.example` to a new file named `.env` and fill in the three keys:
   ```env
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_BOT_TOKEN=your_bot_token
   ```
2. Copy `config.json.example` to a new file named `config.json`.
3. Run the bot:
   ```bash
   python main_cli.py
   ```
   It asks for your phone number and then for the login code Telegram sends you. Once it prints `Monitor bot started and listening...`, it is running. Stop it at any time with **Ctrl+C**.

### How to know it worked

- A message **"🤖 Bot Started"** appears in your **Saved Messages** chat in Telegram.
- The project folder now contains `sesion_monitor.session`, `config.json` and `.env`.

> 🔒 **`sesion_monitor.session` is your Telegram login.** Anyone with this file can read your chats. Never share it or upload it anywhere. If you think it leaked, end it in Telegram → **Settings → Devices**, then repeat this step. `config.json` may also contain your phone number.

## Step 3 — Tell the bot what to watch

Everything is managed from Telegram. Open your **Saved Messages** chat (the chat with yourself) and send commands there. A typical first setup:

```
/add_ch @channel_name
/add_kw iphone
/start
/status
```

- **Channels:** you must have **joined** the channel with your account. For a public channel, use its username **including the `@`**: `@channel_name`, not `channel_name`. Without the `@` it will never match. For a private channel without a username, use its numeric ID, which starts with `-100` (e.g. `-1001234567890`).
- **Keywords** are not case-sensitive, and they also match inside longer words: `car` matches "Car", "cars" and "scar". A keyword can contain spaces (`/add_kw free shipping`) and then matches that exact phrase.
- **`/start` is required.** A fresh `config.json.example` starts paused, so nothing happens until you send `/start`.
- If you used the setup window without a `config.json`, the bot starts with an example keyword, **`keyword`**. Remove it with `/rm_kw keyword`.
- `/status` shows whether monitoring is active, and the current keywords and channels. Use it to check your setup.

### All commands

- `/start` - Starts/resumes monitoring.
- `/stop` - Pauses monitoring.
- `/status` - Shows if the bot is active and the current list of channels and keywords.
- `/add_kw <keyword>` - Adds a new keyword.
- `/rm_kw <keyword>` - Removes a keyword.
- `/add_ch <channel>` - Adds a channel (you can use the numeric ID like `-1001234567890` or the username like `@channel_name`).
- `/rm_ch <channel>` - Removes a channel.
- `/lang <en|es>` - Changes the bot's message language to English (`en`) or Spanish (`es`).

All configuration is automatically saved in `config.json` and will persist across restarts.

## Step 4 (optional) — Run it 24/7 on a server with Docker

The server runs the same bot using the login from Step 2. Everything it needs lives in one folder named `data`.

1. On the server, create a folder for the bot and a `data` folder inside it.
2. Copy into `data/` the two files Step 2 created: `sesion_monitor.session` and `config.json`.
3. Put `docker-compose.yml` and your `.env` (from Step 2, or written by hand as in Option B) next to the `data` folder:
   ```
   telegram-monitor/
   ├── docker-compose.yml
   ├── .env
   └── data/
       ├── sesion_monitor.session
       └── config.json
   ```
4. **Stop the bot on your computer.** One login should not run in two places at once.
5. Start it on the server:
   ```bash
   docker compose up -d
   ```

Useful commands, run from that folder:

| What | Command |
|------|---------|
| See what the bot is doing | `docker compose logs -f` (Ctrl+C to stop watching) |
| Update to the latest version | `docker compose pull && docker compose up -d` |
| Stop it | `docker compose down` |

The ready-made image is `ghcr.io/jose-fernandez/telegram-monitor:latest`, rebuilt on every change to `main`. `docker compose up -d --build` builds it from the source instead. Inside the container the data folder is `/app/data`, set by the `MONITOR_DATA_DIR` variable. Outside Docker, `MONITOR_DATA_DIR` also works and defaults to the current folder.

## Troubleshooting

| Symptom | Cause and fix |
|---------|---------------|
| No alerts at all | Send `/status`. If it says *Paused*, send `/start`. Check that each channel starts with `@` (or is a `-100…` ID), that your account has joined it, and that the example keyword `keyword` isn't the only one. |
| The bot never messages me | You haven't pressed **Start** in the chat with your bot (Step 1). |
| Logs show `EOFError: EOF when reading a line` after "Please enter your phone" | The server found no valid login. Check that `sesion_monitor.session` is inside `data/` and that the folder is mounted, or repeat Step 2. |
| `API credentials missing in .env` | The `.env` file is missing, misnamed, or not next to `docker-compose.yml`. |
| The setup window doesn't open on Linux | Install Tk: `sudo apt install python3-tk`. |
| It worked, then stopped after I ended a session in Telegram | That session was the bot's login. Repeat Step 2 and copy the new `sesion_monitor.session` to the server. |

## Privacy and Git

The `.gitignore` file is already configured to prevent you from accidentally uploading credentials. Files like `.env`, `config.json`, session files `*.session` and the `data/` directory will be ignored by Git.
