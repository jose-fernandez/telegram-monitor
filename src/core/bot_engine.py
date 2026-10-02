import asyncio
import html
import json
import logging
from collections import deque
import time
import aiohttp
from telethon import TelegramClient, events

from src.utils.config import load_config, save_config, load_env, session_path
from src.utils.i18n import get_translation as t_func

logger = logging.getLogger(__name__)

# The Bot API rejects messages over 4096 UTF-16 code units; leave room for
# the alert header.
MAX_CHUNK_UNITS = 3500
MAX_RETRY_DELAY = 60

def _utf16_len(text):
    return len(text.encode('utf-16-le')) // 2

def split_text(text, max_units=MAX_CHUNK_UNITS):
    # Split into pieces the Bot API accepts, without dropping a character.
    chunks, current, units = [], [], 0
    for char in text:
        char_units = _utf16_len(char)
        if current and units + char_units > max_units:
            chunks.append(''.join(current))
            current, units = [], 0
        current.append(char)
        units += char_units
    chunks.append(''.join(current))
    return chunks

class TelegramMonitorBot:
    def __init__(self, session_name=None):
        if session_name is None:
            session_name = session_path()
        self.api_id, self.api_hash, self.bot_token = load_env()
        if not self.api_id or not self.api_hash:
            raise ValueError("API credentials missing in .env")
            
        self.client = TelegramClient(session_name, int(self.api_id), self.api_hash)
        self.state = load_config()
        
        self.max_notifications = 3
        self.time_window = 60
        self.notification_timestamps = deque()
        # Injectable so tests can drive the clock
        self._now = time.time
        self._sleep = asyncio.sleep
        self.my_user_id = None
        self.is_running = False

    def t(self, key, **kwargs):
        lang = self.state.get('language', 'en')
        return t_func(lang, key, **kwargs)

    def build_alerts(self, chat_title, text):
        # Channel text is arbitrary; escape it so a stray '<' or '&' cannot make
        # the Bot API reject the alert. Long posts become several messages.
        chunks = split_text(text)
        if len(chunks) == 1:
            return [self.t('alert', chat_title=html.escape(chat_title), text=html.escape(text))]
        total = len(chunks)
        return [
            self.t('alert', chat_title=html.escape(f"{chat_title} ({i}/{total})"), text=html.escape(chunk))
            for i, chunk in enumerate(chunks, start=1)
        ]

    async def wait_for_notification_slot(self):
        # Anti-spam: at most max_notifications per time_window. Alerts over
        # the limit wait for a free slot instead of being dropped.
        while True:
            now = self._now()
            while self.notification_timestamps and now - self.notification_timestamps[0] >= self.time_window:
                self.notification_timestamps.popleft()
            if len(self.notification_timestamps) < self.max_notifications:
                self.notification_timestamps.append(now)
                return
            wait = self.time_window - (now - self.notification_timestamps[0])
            logger.info(f"Rate limit reached. Alert queued for {wait:.0f}s.")
            await self._sleep(wait)

    async def send_bot_alert(self, message):
        if not self.bot_token or not self.my_user_id:
            logger.error("Cannot send bot alert: missing BOT_TOKEN or MY_USER_ID")
            return False
            
        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            "chat_id": self.my_user_id,
            "text": message,
            "parse_mode": "HTML"
        }
        # Temporary failures (rate limiting, server errors, network) are retried
        # until the alert gets through; only a request Telegram rejects outright
        # is given up on, since resending it cannot succeed.
        delay = 1
        while True:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload) as response:
                        if response.status == 200:
                            return True
                        body = await response.text()
                        if response.status == 429:
                            try:
                                wait = json.loads(body)['parameters']['retry_after']
                            except (ValueError, KeyError, TypeError):
                                wait = delay
                        elif response.status >= 500:
                            wait = delay
                        else:
                            logger.error(f"Failed to send bot alert: {body}")
                            return False
                        reason = f"HTTP {response.status}"
            except Exception as e:
                wait = delay
                reason = repr(e)
            logger.warning(f"Bot alert not delivered ({reason}); retrying in {wait}s")
            await self._sleep(wait)
            delay = min(delay * 2, MAX_RETRY_DELAY)

    def setup_handlers(self):
        @self.client.on(events.NewMessage(chats='me'))
        async def command_handler(event):
            self.state = load_config()
            if not event.raw_text or not event.raw_text.startswith('/'):
                return

            text = event.raw_text.strip()
            parts = text.split(maxsplit=1)
            command = parts[0].lower()
            args = parts[1] if len(parts) > 1 else ""

            if command == '/start':
                self.state['is_monitoring'] = True
                save_config(self.state)
                await event.respond(self.t('monitoring_started_cmd'))
                logger.info("Monitoring started via command.")
                
            elif command == '/stop':
                self.state['is_monitoring'] = False
                save_config(self.state)
                await event.respond(self.t('monitoring_stopped_cmd'))
                logger.info("Monitoring stopped via command.")
                
            elif command == '/status':
                status_state = self.t('active') if self.state['is_monitoring'] else self.t('paused')
                kws = ", ".join(self.state['keywords']) if self.state['keywords'] else self.t('none')
                chs = ", ".join(map(str, self.state['channels'])) if self.state['channels'] else self.t('none')
                
                status_msg = (
                    f"{self.t('bot_status')}\n"
                    f"{self.t('monitoring')} {status_state}\n\n"
                    f"{self.t('keywords')}\n{kws}\n\n"
                    f"{self.t('channels')}\n{chs}"
                )
                await event.respond(status_msg)
                
            elif command == '/add_kw':
                if args:
                    kw = args.lower()
                    if kw not in self.state['keywords']:
                        self.state['keywords'].append(kw)
                        save_config(self.state)
                        await event.respond(f"{self.t('kw_added')} `{kw}`")
                    else:
                        await event.respond(self.t('kw_exists'))
                else:
                    await event.respond(self.t('usage_add_kw'))
                    
            elif command == '/rm_kw':
                if args:
                    kw = args.lower()
                    if kw in self.state['keywords']:
                        self.state['keywords'].remove(kw)
                        save_config(self.state)
                        await event.respond(f"{self.t('kw_removed')} `{kw}`")
                    else:
                        await event.respond(self.t('kw_not_found'))
                else:
                    await event.respond(self.t('usage_rm_kw'))
                    
            elif command == '/add_ch':
                if args:
                    try:
                        ch = int(args) if args.lstrip('-').isdigit() else args
                        if ch not in self.state['channels']:
                            self.state['channels'].append(ch)
                            save_config(self.state)
                            await event.respond(f"{self.t('ch_added')} `{ch}`")
                        else:
                            await event.respond(self.t('ch_exists'))
                    except ValueError:
                        await event.respond(self.t('invalid_ch'))
                else:
                    await event.respond(self.t('usage_add_ch'))
                    
            elif command == '/rm_ch':
                if args:
                    try:
                        ch = int(args) if args.lstrip('-').isdigit() else args
                        if ch in self.state['channels']:
                            self.state['channels'].remove(ch)
                            save_config(self.state)
                            await event.respond(f"{self.t('ch_removed')} `{ch}`")
                        else:
                            await event.respond(self.t('ch_not_found'))
                    except ValueError:
                        await event.respond(self.t('invalid_ch'))
                else:
                    await event.respond(self.t('usage_rm_ch'))
                    
            elif command == '/lang':
                if args and args.lower() in ['en', 'es']:
                    self.state['language'] = args.lower()
                    save_config(self.state)
                    await event.respond(self.t('lang_changed'))
                else:
                    await event.respond(self.t('usage_lang'))
                    
            else:
                await event.respond(self.t('unknown_cmd'))

        @self.client.on(events.NewMessage())
        async def monitor_handler(event):
            self.state = load_config()
            if not self.state['is_monitoring']:
                return

            chat_id = event.chat_id
            
            chat = await event.get_chat()
            chat_username = getattr(chat, 'username', None)
            
            is_monitored = False
            if chat_id in self.state['channels']:
                is_monitored = True
            elif chat_username and f"@{chat_username}" in self.state['channels']:
                is_monitored = True
                
            if not is_monitored:
                return

            if not event.raw_text:
                return
            
            text_lower = event.raw_text.lower()
            match_found = any(keyword in text_lower for keyword in self.state['keywords'])
            
            if match_found:
                await self.wait_for_notification_slot()
                try:
                    chat_title = getattr(chat, 'title', str(chat.id))
                    if chat_username:
                        chat_title = f"@{chat_username}"

                    delivered = True
                    for message in self.build_alerts(chat_title, event.raw_text):
                        delivered = await self.send_bot_alert(message) and delivered
                    if delivered:
                        logger.info(f"Alert sent for channel {chat_title}")
                except Exception as e:
                    logger.error(f"Error sending alert: {e}")

    async def start(self):
        logger.info("Starting monitor bot...")
        self.setup_handlers()
        await self.client.start()
        
        me = await self.client.get_me()
        self.my_user_id = me.id
        
        self.is_running = True
        logger.info("Monitor bot started and listening...")
        await self.client.send_message('me', self.t('bot_started_msg'))
        await self.client.run_until_disconnected()
        
    async def stop(self):
        if self.is_running:
            await self.client.disconnect()
            self.is_running = False
            logger.info("Bot stopped.")
