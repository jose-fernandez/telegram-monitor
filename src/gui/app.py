import customtkinter as ctk
import threading
import asyncio
import os
import webbrowser
import re
from telethon import TelegramClient

from src.utils.config import load_env, save_env, load_config, save_config
from src.utils.i18n import get_translation as t_func

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TutorialWindow(ctk.CTkToplevel):
    def __init__(self, master, title, steps, url=None, url_text=None):
        super().__init__(master)
        self.title(title)
        self.geometry("400x400")
        self.attributes("-topmost", True)
        self.resizable(False, False)
        
        lbl_title = ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=20, weight="bold"))
        lbl_title.pack(pady=(20, 10))
        
        for step in steps:
            lbl_step = ctk.CTkLabel(self, text=step, font=ctk.CTkFont(size=14), justify="left", wraplength=350)
            lbl_step.pack(anchor="w", padx=20, pady=5)
            
        if url and url_text:
            btn = ctk.CTkButton(self, text=url_text, command=lambda: webbrowser.open(url))
            btn.pack(pady=20)

class WizardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Telegram Monitor")
        self.geometry("500x650")
        self.resizable(False, False)
        
        self.app_state = load_config()
        self.lang = self.app_state.get('language', 'es')

        self.client = None
        self.phone = None
        self.phone_code_hash = None
        
        # Navigation Bar
        self.nav_frame = ctk.CTkFrame(self, height=50, fg_color="transparent")
        self.nav_frame.pack(fill="x", padx=10, pady=10)
        self.nav_frame.pack_propagate(False)
        
        self.back_btn = ctk.CTkButton(self.nav_frame, text="< Atrás", width=60, fg_color="transparent", 
                                      hover_color="#333333", command=self.go_back)
        self.back_btn.pack(side="left")
        self.back_btn.pack_forget() # Hide initially
        
        self.lang_btn = ctk.CTkSegmentedButton(self.nav_frame, values=["EN", "ES"], command=self.change_language)
        self.lang_btn.pack(side="right")
        self.lang_btn.set(self.lang.upper())
        
        # Avatar
        self.avatar_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.avatar_frame.pack(fill="x")
        
        avatar_path = os.path.join(os.path.dirname(__file__), "..", "assets", "avatar.jpg")
        if not os.path.exists(avatar_path):
            avatar_path = os.path.join(os.path.dirname(__file__), "..", "assets", "avatar.png")
            
        if os.path.exists(avatar_path):
            try:
                from PIL import Image, ImageDraw
                
                # Make it circular
                size = (120, 120)
                img = Image.open(avatar_path).convert("RGBA")
                
                # Crop to square first to avoid squishing
                width, height = img.size
                min_dim = min(width, height)
                left = (width - min_dim)/2
                top = (height - min_dim)/2
                right = (width + min_dim)/2
                bottom = (height + min_dim)/2
                img = img.crop((left, top, right, bottom))
                
                img = img.resize(size, Image.Resampling.LANCZOS)
                
                mask = Image.new('L', size, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + size, fill=255)
                
                output = Image.new('RGBA', size, (0, 0, 0, 0))
                output.paste(img, (0, 0), mask=mask)
                
                self.avatar_img = ctk.CTkImage(light_image=output, dark_image=output, size=size)
                self.avatar_lbl = ctk.CTkLabel(self.avatar_frame, image=self.avatar_img, text="")
                self.avatar_lbl.pack(pady=15)
            except Exception:
                pass
        
        # Main content container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(fill="both", expand=True)

        self.frames = []
        self.current_frame = None
        
        self.show_frame(WelcomeFrame, animate=False)

    def t(self, key, **kwargs):
        return t_func(self.lang, key, **kwargs)

    def change_language(self, value):
        self.lang = value.lower()
        self.app_state['language'] = self.lang
        save_config(self.app_state)
        # Re-render current frame
        self.back_btn.configure(text=self.t('back'))
        if self.current_frame:
            self.current_frame.update_language()

    def go_back(self):
        if len(self.frames) > 1:
            self.frames.pop() # remove current
            prev_frame_class = self.frames[-1]
            self._transition(prev_frame_class, direction="right")

    def show_frame(self, frame_class, animate=True):
        if len(self.frames) == 0 or self.frames[-1] != frame_class:
            self.frames.append(frame_class)
            
        if animate and self.current_frame:
            self._transition(frame_class, direction="left")
        else:
            if self.current_frame:
                self.current_frame.destroy()
            self.current_frame = frame_class(self.container, self)
            self.current_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
            self._update_nav_bar()

    def _transition(self, new_frame_class, direction="left"):
        new_frame = new_frame_class(self.container, self)
        
        start_x = 1.0 if direction == "left" else -1.0
        new_frame.place(relx=start_x, rely=0, relwidth=1, relheight=1)
        
        old_frame = self.current_frame
        self.current_frame = new_frame
        
        self._update_nav_bar()
        
        # Animation loop
        steps = 15
        delay = 10
        
        def step_anim(step):
            progress = step / steps
            # ease out cubic
            ease = 1 - pow(1 - progress, 3)
            
            if direction == "left":
                new_x = 1.0 - ease
                old_x = -ease
            else:
                new_x = -1.0 + ease
                old_x = ease
                
            new_frame.place(relx=new_x)
            old_frame.place(relx=old_x)
            
            if step < steps:
                self.after(delay, step_anim, step + 1)
            else:
                old_frame.destroy()
                new_frame.place(relx=0)
                
        step_anim(1)

    def _update_nav_bar(self):
        if len(self.frames) > 1 and self.frames[-1] != DashboardFrame:
            self.back_btn.pack(side="left")
        else:
            self.back_btn.pack_forget()

    def run_async(self, coro):
        def thread_target():
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(coro)
            loop.close()
        threading.Thread(target=thread_target, daemon=True).start()

class WelcomeFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        
        self.title = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=32, weight="bold"))
        self.title.pack(pady=(100, 20))
        
        self.desc = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.desc.pack(pady=(0, 50))
        
        self.btn = ctk.CTkButton(self, text="", font=ctk.CTkFont(size=16), height=50, command=lambda: app.show_frame(ApiSetupFrame))
        self.btn.pack(pady=20)
        
        self.update_language()

    def update_language(self):
        self.title.configure(text=self.app.t('welcome_title'))
        self.desc.configure(text=self.app.t('welcome_desc'))
        self.btn.configure(text=self.app.t('start_now'))

class ApiSetupFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        
        self.title = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=24, weight="bold"))
        self.title.pack(pady=(20, 10))
        
        self.desc = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14), text_color="gray")
        self.desc.pack(pady=(0, 20))
        
        # API ID Row
        api_id_frame = ctk.CTkFrame(self, fg_color="transparent")
        api_id_frame.pack(pady=5)
        self.api_id = ctk.CTkEntry(api_id_frame, width=260, height=40)
        self.api_id.pack(side="left", padx=(0, 5))
        self.btn_help_id = ctk.CTkButton(api_id_frame, text="?", width=35, height=40, fg_color="#3a3a3a", hover_color="#555555", command=lambda: self.show_tutorial("api"))
        self.btn_help_id.pack(side="left")
        
        # API Hash Row
        api_hash_frame = ctk.CTkFrame(self, fg_color="transparent")
        api_hash_frame.pack(pady=5)
        self.api_hash = ctk.CTkEntry(api_hash_frame, width=260, height=40)
        self.api_hash.pack(side="left", padx=(0, 5))
        self.btn_help_hash = ctk.CTkButton(api_hash_frame, text="?", width=35, height=40, fg_color="#3a3a3a", hover_color="#555555", command=lambda: self.show_tutorial("api"))
        self.btn_help_hash.pack(side="left")
        
        # Bot Token Row
        bot_token_frame = ctk.CTkFrame(self, fg_color="transparent")
        bot_token_frame.pack(pady=(15, 5))
        self.bot_token = ctk.CTkEntry(bot_token_frame, width=260, height=40)
        self.bot_token.pack(side="left", padx=(0, 5))
        self.btn_help_bot = ctk.CTkButton(bot_token_frame, text="?", width=35, height=40, fg_color="#3a3a3a", hover_color="#555555", command=lambda: self.show_tutorial("bot"))
        self.btn_help_bot.pack(side="left")
        
        # Pre-fill if exists
        aid, ahash, btoken = load_env()
        if aid: self.api_id.insert(0, aid)
        if ahash: self.api_hash.insert(0, ahash)
        if btoken: self.bot_token.insert(0, btoken)
        
        self.btn = ctk.CTkButton(self, text="", font=ctk.CTkFont(size=16), height=50, command=self.save_and_next)
        self.btn.pack(pady=20)
        
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack()
        
        self.update_language()

    def update_language(self):
        self.title.configure(text=self.app.t('api_title'))
        self.desc.configure(text=self.app.t('api_desc'))
        self.api_id.configure(placeholder_text=self.app.t('api_id_ph'))
        self.api_hash.configure(placeholder_text=self.app.t('api_hash_ph'))
        self.bot_token.configure(placeholder_text=self.app.t('bot_token_ph'))
        self.btn.configure(text=self.app.t('next'))

    def show_tutorial(self, type_str):
        if type_str == "api":
            title = self.app.t('tut_api_title')
            steps = [self.app.t('tut_api_1'), self.app.t('tut_api_2'), self.app.t('tut_api_3'), self.app.t('tut_api_4')]
            url = "https://my.telegram.org"
            url_text = self.app.t('tut_api_btn')
        else:
            title = self.app.t('tut_bot_title')
            steps = [self.app.t('tut_bot_1'), self.app.t('tut_bot_2'), self.app.t('tut_bot_3'), self.app.t('tut_bot_4')]
            url = "https://t.me/BotFather"
            url_text = self.app.t('tut_bot_btn')
            
        TutorialWindow(self, title, steps, url, url_text)

    def save_and_next(self):
        aid = self.api_id.get().strip()
        ahash = self.api_hash.get().strip()
        btoken = self.bot_token.get().strip()
        
        if not aid or not ahash or not btoken:
            self.error_label.configure(text="Todos los campos son obligatorios" if self.app.lang == 'es' else "All fields are required")
            # Shake animation
            self._shake()
            return
            
        save_env(aid, ahash, btoken)
        self.btn.configure(state="disabled", text=self.app.t('checking'))
        self.app.run_async(self.check_auth(aid, ahash))

    async def check_auth(self, aid, ahash):
        from telethon import TelegramClient
        try:
            if not self.app.client or not self.app.client.is_connected():
                self.app.client = TelegramClient('sesion_monitor', int(aid), ahash)
                await self.app.client.connect()
            
            is_auth = await self.app.client.is_user_authorized()
            if is_auth:
                await self.app.client.disconnect()
                self.app.after(0, lambda: self.app.show_frame(DashboardFrame))
            else:
                self.app.after(0, lambda: self.app.show_frame(PhoneSetupFrame))
        except Exception as e:
            def show_error():
                self.error_label.configure(text=f"Error: {e}")
                self.btn.configure(state="normal", text=self.app.t('next'))
            self.app.after(0, show_error)

    def _shake(self):
        for i in range(6):
            offset = 5 if i % 2 == 0 else -5
            if i == 5: offset = 0
            self.after(50 * i, lambda o=offset: self.place(relx=0, x=o))

class PhoneSetupFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        
        self.title = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=24, weight="bold"))
        self.title.pack(pady=(50, 20))
        
        self.desc = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.desc.pack(pady=(0, 20))
        
        self.phone = ctk.CTkEntry(self, width=300, height=40)
        self.phone.pack(pady=10)
        
        saved_phone = self.app.app_state.get('phone', '')
        if saved_phone:
            self.phone.insert(0, saved_phone)
        
        self.btn = ctk.CTkButton(self, text="", font=ctk.CTkFont(size=16), height=50, command=self.request_code)
        self.btn.pack(pady=10)
        
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate", width=200)
        self.progress.set(0)
        
        self.error_label = ctk.CTkLabel(self, text="", text_color="#b83a3a")
        self.error_label.pack()
        
        self.update_language()

    def update_language(self):
        self.title.configure(text=self.app.t('phone_title'))
        self.desc.configure(text=self.app.t('phone_desc'))
        self.phone.configure(placeholder_text=self.app.t('phone_ph'))
        self.btn.configure(text=self.app.t('send_code'))
        self.error_label.configure(text="")

    def request_code(self):
        phone = self.phone.get().strip().replace(" ", "")
        
        # Validation: Must start with + and have 8-15 digits
        if not re.match(r'^\+\d{8,15}$', phone):
            self.phone.configure(border_color="red")
            self.error_label.configure(text=self.app.t('invalid_phone'))
            return
            
        self.phone.configure(border_color=["#979DA2", "#565B5E"]) # reset
        self.error_label.configure(text="")
        
        self.btn.configure(state="disabled", text=self.app.t('sending'))
        self.progress.pack(pady=10)
        self.progress.start()
        
        self.app.phone = phone
        self.app.app_state['phone'] = phone
        save_config(self.app.app_state)
        
        self.app.run_async(self.do_request_code(phone))

    async def do_request_code(self, phone):
        aid, ahash, _ = load_env()
        self.app.client = TelegramClient('sesion_monitor', int(aid), ahash)
        await self.app.client.connect()
        
        if await self.app.client.is_user_authorized():
            await self.app.client.disconnect()
            self.app.after(0, lambda: self.app.show_frame(DashboardFrame))
            return

        try:
            res = await self.app.client.send_code_request(phone)
            self.app.phone_code_hash = res.phone_code_hash
            self.app.after(0, lambda: self.app.show_frame(CodeSetupFrame))
        except Exception as e:
            def show_error():
                self.progress.stop()
                self.progress.pack_forget()
                self.error_label.configure(text=f"Error: {e}")
                self.btn.configure(state="normal", text=self.app.t('btn_next'))
            self.app.after(0, show_error)

class CodeSetupFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        
        self.title = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=24, weight="bold"))
        self.title.pack(pady=(50, 20))
        
        self.desc = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=14))
        self.desc.pack(pady=(0, 20))
        
        self.code = ctk.CTkEntry(self, width=300, height=40)
        self.code.pack(pady=10)
        
        self.btn = ctk.CTkButton(self, text="", font=ctk.CTkFont(size=16), height=50, command=self.verify_code)
        self.btn.pack(pady=10)
        
        self.progress = ctk.CTkProgressBar(self, mode="indeterminate", width=200)
        self.progress.set(0)
        
        self.error_label = ctk.CTkLabel(self, text="", text_color="#b83a3a")
        self.error_label.pack()
        
        self.update_language()

    def update_language(self):
        self.title.configure(text=self.app.t('code_title'))
        desc_text = self.app.t('code_desc')
        if getattr(self.app, 'phone', None):
            desc_text += f"\n\n({self.app.phone})"
        self.desc.configure(text=desc_text)
        self.code.configure(placeholder_text=self.app.t('code_ph'))
        self.btn.configure(text=self.app.t('verify'))
        self.error_label.configure(text="")

    def verify_code(self):
        code = self.code.get().strip()
        
        if not re.match(r'^\d{5}$', code):
            self.code.configure(border_color="red")
            self.error_label.configure(text=self.app.t('invalid_code'))
            return
            
        self.code.configure(border_color=["#979DA2", "#565B5E"])
        self.error_label.configure(text="")
        
        self.btn.configure(state="disabled", text=self.app.t('sending'))
        self.progress.pack(pady=10)
        self.progress.start()
        
        self.app.run_async(self.do_verify_code(code))

    async def do_verify_code(self, code):
        try:
            await self.app.client.sign_in(self.app.phone, code, phone_code_hash=self.app.phone_code_hash)
            await self.app.client.disconnect()
            self.app.after(0, lambda: self.app.show_frame(DashboardFrame))
        except Exception as e:
            def show_error():
                self.progress.stop()
                self.progress.pack_forget()
                self.error_label.configure(text=f"Error: {e}")
                self.btn.configure(state="normal", text=self.app.t('verify'))
            self.app.after(0, show_error)

class DashboardFrame(ctk.CTkFrame):
    def __init__(self, master, app):
        super().__init__(master, fg_color="transparent")
        self.app = app
        
        self.tabview = ctk.CTkTabview(self, width=460, height=550, command=self.on_tab_change)
        self.tabview.pack(padx=10, pady=10, expand=True, fill="both")
        
        self.name_status = self.app.t('dash_tab_status')
        self.name_kw = self.app.t('dash_tab_kw')
        self.name_ch = self.app.t('dash_tab_ch')
        
        self.tab_status = self.tabview.add(self.name_status)
        self.tab_kw = self.tabview.add(self.name_kw)
        self.tab_ch = self.tabview.add(self.name_ch)
        
        # --- TAB: STATUS ---
        self.title = ctk.CTkLabel(self.tab_status, text="", font=ctk.CTkFont(size=24, weight="bold"))
        self.title.pack(pady=(50, 10))
        
        self.status_label = ctk.CTkLabel(self.tab_status, text="", text_color="gray", font=ctk.CTkFont(size=14))
        self.status_label.pack(pady=5)
        
        self.btn = ctk.CTkButton(self.tab_status, text="", font=ctk.CTkFont(size=16, weight="bold"), 
                                 height=40, width=200, command=self.toggle_bot)
        self.btn.pack(pady=30)
        
        self.logout_btn = ctk.CTkButton(self.tab_status, text="", fg_color="transparent", text_color="#b83a3a", 
                                        hover_color="#333333", command=self.logout)
        self.logout_btn.pack(side="bottom", pady=20)
        
        # --- TAB: KEYWORDS ---
        self.kw_header = ctk.CTkFrame(self.tab_kw, fg_color="transparent")
        self.kw_header.pack(fill="x", pady=5)
        self.kw_lbl = ctk.CTkLabel(self.kw_header, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.kw_lbl.pack(side="left", padx=5)
        self.btn_help_kw = ctk.CTkButton(self.kw_header, text="?", width=30, height=30, fg_color="#3a3a3a", hover_color="#555555", command=lambda: self.show_tutorial("kw"))
        self.btn_help_kw.pack(side="left", padx=5)
        
        self.kw_input_frame = ctk.CTkFrame(self.tab_kw, fg_color="transparent")
        self.kw_input_frame.pack(fill="x", pady=5)
        self.kw_entry = ctk.CTkEntry(self.kw_input_frame)
        self.kw_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.kw_add_btn = ctk.CTkButton(self.kw_input_frame, text="+", width=40, command=self.add_kw)
        self.kw_add_btn.pack(side="right")
        
        self.kw_scroll = ctk.CTkScrollableFrame(self.tab_kw)
        self.kw_scroll.pack(fill="both", expand=True, pady=5)
        
        # --- TAB: CHANNELS ---
        self.ch_header = ctk.CTkFrame(self.tab_ch, fg_color="transparent")
        self.ch_header.pack(fill="x", pady=5)
        self.ch_lbl = ctk.CTkLabel(self.ch_header, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.ch_lbl.pack(side="left", padx=5)
        self.btn_help_ch = ctk.CTkButton(self.ch_header, text="?", width=30, height=30, fg_color="#3a3a3a", hover_color="#555555", command=lambda: self.show_tutorial("ch"))
        self.btn_help_ch.pack(side="left", padx=5)
        
        self.ch_input_frame = ctk.CTkFrame(self.tab_ch, fg_color="transparent")
        self.ch_input_frame.pack(fill="x", pady=5)
        self.ch_entry = ctk.CTkEntry(self.ch_input_frame)
        self.ch_entry.pack(side="left", fill="x", expand=True, padx=(0, 5))
        self.ch_add_btn = ctk.CTkButton(self.ch_input_frame, text="+", width=40, command=self.add_ch)
        self.ch_add_btn.pack(side="right")
        
        self.ch_scroll = ctk.CTkScrollableFrame(self.tab_ch)
        self.ch_scroll.pack(fill="both", expand=True, pady=5)
        
        self.bot_process = None
        self.is_running = False
        
        self.update_language()
        self.refresh_lists()

    def update_language(self):
        new_status = self.app.t('dash_tab_status')
        new_kw = self.app.t('dash_tab_kw')
        new_ch = self.app.t('dash_tab_ch')
        
        try:
            self.tabview.rename(self.name_status, new_status)
            self.name_status = new_status
            self.tabview.rename(self.name_kw, new_kw)
            self.name_kw = new_kw
            self.tabview.rename(self.name_ch, new_ch)
            self.name_ch = new_ch
        except Exception:
            pass # Failsafe if tabs changed
            
        self.title.configure(text=self.app.t('dash_title'))
        self.kw_lbl.configure(text=self.app.t('dash_kw_title'))
        self.ch_lbl.configure(text=self.app.t('dash_ch_title'))
        self.kw_entry.configure(placeholder_text=self.app.t('dash_kw_ph'))
        self.ch_entry.configure(placeholder_text=self.app.t('dash_ch_ph'))
        self.kw_add_btn.configure(text=self.app.t('dash_add'))
        self.ch_add_btn.configure(text=self.app.t('dash_add'))
        self.logout_btn.configure(text=self.app.t('btn_logout'))
        self._update_ui_state()

    def show_tutorial(self, type_str):
        if type_str == "kw":
            title = self.app.t('tut_kw_title')
            steps = [self.app.t('tut_kw_desc')]
        else:
            title = self.app.t('tut_ch_title')
            steps = [self.app.t('tut_ch_desc')]
        TutorialWindow(self, title, steps)

    def on_tab_change(self):
        self.refresh_lists(with_loader=True)

    def refresh_lists(self, with_loader=False):
        current_tab = self.tabview.get()
        if current_tab == self.name_kw:
            if with_loader:
                self._simulate_load(self.kw_scroll, self._render_kw)
            else:
                for w in self.kw_scroll.winfo_children(): w.destroy()
                self._render_kw()
        elif current_tab == self.name_ch:
            if with_loader:
                self._simulate_load(self.ch_scroll, self._render_ch)
            else:
                for w in self.ch_scroll.winfo_children(): w.destroy()
                self._render_ch()

    def _simulate_load(self, container, render_func):
        for widget in container.winfo_children():
            widget.destroy()
            
        loader = ctk.CTkProgressBar(container, mode="indeterminate", width=150)
        loader.pack(pady=20)
        loader.start()
        
        def _finish_load():
            try:
                loader.stop()
                loader.destroy()
                render_func()
            except Exception:
                pass
        self.app.after(300, _finish_load)

    def _render_kw(self):
        for kw in self.app.app_state.get('keywords', []):
            self._create_list_item(self.kw_scroll, kw, lambda k=kw: self.remove_kw(k))

    def _render_ch(self):
        for ch in self.app.app_state.get('channels', []):
            self._create_list_item(self.ch_scroll, str(ch), lambda c=ch: self.remove_ch(c))

    def _create_list_item(self, parent, text, delete_cmd):
        frame = ctk.CTkFrame(parent, fg_color="#333333", height=30)
        frame.pack(fill="x", pady=2)
        lbl = ctk.CTkLabel(frame, text=text, font=ctk.CTkFont(size=14))
        lbl.pack(side="left", padx=10)
        btn = ctk.CTkButton(frame, text="🗑️", width=30, fg_color="#b83a3a", hover_color="#8c2a2a", command=delete_cmd)
        btn.pack(side="right", padx=5, pady=2)

    def add_kw(self):
        kw = self.kw_entry.get().strip().lower()
        if kw and kw not in self.app.app_state.get('keywords', []):
            if 'keywords' not in self.app.app_state: self.app.app_state['keywords'] = []
            self.app.app_state['keywords'].append(kw)
            save_config(self.app.app_state)
            self.kw_entry.delete(0, "end")
            self.refresh_lists()

    def remove_kw(self, kw):
        if kw in self.app.app_state.get('keywords', []):
            self.app.app_state['keywords'].remove(kw)
            save_config(self.app.app_state)
            self.refresh_lists()

    def add_ch(self):
        ch = self.ch_entry.get().strip()
        if ch:
            try:
                ch = int(ch) if ch.lstrip('-').isdigit() else ch
            except ValueError:
                pass
                
            if 'channels' not in self.app.app_state: self.app.app_state['channels'] = []
            if ch not in self.app.app_state['channels']:
                self.app.app_state['channels'].append(ch)
                save_config(self.app.app_state)
                self.ch_entry.delete(0, "end")
                self.refresh_lists()

    def remove_ch(self, ch):
        if ch in self.app.app_state.get('channels', []):
            self.app.app_state['channels'].remove(ch)
            save_config(self.app.app_state)
            self.refresh_lists()

    def _update_ui_state(self):
        if self.is_running:
            self.btn.configure(text=self.app.t('btn_stop'), fg_color="#b83a3a", hover_color="#8c2a2a")
            self.status_label.configure(text=self.app.t('dash_running'), text_color="#3ab85c")
        else:
            self.btn.configure(text=self.app.t('btn_start'), fg_color="#3ab85c", hover_color="#2a8c42")
            self.status_label.configure(text=self.app.t('dash_stopped'), text_color="gray")

    def toggle_bot(self):
        if not self.is_running:
            import subprocess
            import sys
            self.bot_process = subprocess.Popen([sys.executable, "main_cli.py"])
            self.is_running = True
        else:
            if self.bot_process:
                self.bot_process.terminate()
                self.bot_process = None
            self.is_running = False
            
        self._update_ui_state()

    def logout(self):
        if self.is_running:
            self.toggle_bot() # Stop bot first if running
        
        self.logout_btn.configure(state="disabled", text="...")
        self.app.run_async(self._do_logout())
        
    async def _do_logout(self):
        try:
            if not self.app.client or not self.app.client.is_connected():
                from src.utils.config import load_env
                aid, ahash, _ = load_env()
                from telethon import TelegramClient
                self.app.client = TelegramClient('sesion_monitor', int(aid), ahash)
                await self.app.client.connect()
            
            await self.app.client.log_out()
        except Exception:
            pass
        finally:
            if 'phone' in self.app.app_state:
                del self.app.app_state['phone']
                save_config(self.app.app_state)
            self.app.after(0, lambda: self.app.show_frame(PhoneSetupFrame))
