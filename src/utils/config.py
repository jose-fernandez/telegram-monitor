import os
import json
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

CONFIG_FILE = 'config.json'
ENV_FILE = '.env'
SESSION_NAME = 'sesion_monitor'

def data_dir():
    # Where config.json and the session file live. Defaults to the working
    # directory; Docker points it at a mounted volume.
    return os.environ.get('MONITOR_DATA_DIR', '.')

def config_path():
    return os.path.join(data_dir(), CONFIG_FILE)

def session_path():
    return os.path.join(data_dir(), SESSION_NAME)

def load_env():
    load_dotenv(ENV_FILE)
    api_id = os.environ.get('TELEGRAM_API_ID')
    api_hash = os.environ.get('TELEGRAM_API_HASH')
    bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
    return api_id, api_hash, bot_token

def save_env(api_id, api_hash, bot_token):
    with open(ENV_FILE, 'w') as f:
        f.write(f"TELEGRAM_API_ID={api_id}\n")
        f.write(f"TELEGRAM_API_HASH={api_hash}\n")
        f.write(f"TELEGRAM_BOT_TOKEN={bot_token}\n")

def load_config():
    if os.path.exists(config_path()):
        try:
            with open(config_path(), 'r') as f:
                config = json.load(f)
                if 'language' not in config:
                    config['language'] = 'en'
                return config
        except Exception as e:
            logger.error(f"Error loading config.json: {e}")
    return {
        "keywords": ["keyword"],
        "channels": [],
        "is_monitoring": True,
        "language": "en"
    }

def save_config(config):
    try:
        with open(config_path(), 'w') as f:
            json.dump(config, f, indent=4)
    except Exception as e:
        logger.error(f"Error saving config.json: {e}")
