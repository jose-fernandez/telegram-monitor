TRANSLATIONS = {
    'en': {
        # Bot Core
        'monitoring_started_cmd': "✅ Monitoring started.",
        'monitoring_stopped_cmd': "⏸ Monitoring stopped.",
        'bot_status': "**Bot Status**",
        'monitoring': "Monitoring:",
        'active': "✅ Active",
        'paused': "⏸ Paused",
        'keywords': "**Keywords:**",
        'channels': "**Channels:**",
        'none': "None",
        'kw_added': "✅ Keyword added:",
        'kw_exists': "⚠️ Keyword already exists.",
        'usage_add_kw': "⚠️ Usage: `/add_kw <keyword>`",
        'kw_removed': "✅ Keyword removed:",
        'kw_not_found': "⚠️ Keyword not found.",
        'usage_rm_kw': "⚠️ Usage: `/rm_kw <keyword>`",
        'ch_added': "✅ Channel added:",
        'ch_exists': "⚠️ Channel already exists.",
        'invalid_ch': "⚠️ Invalid channel ID/username.",
        'usage_add_ch': "⚠️ Usage: `/add_ch <channel_id_or_username>`",
        'ch_removed': "✅ Channel removed:",
        'ch_not_found': "⚠️ Channel not found.",
        'usage_rm_ch': "⚠️ Usage: `/rm_ch <channel_id_or_username>`",
        'unknown_cmd': "⚠️ Unknown command. Available: `/start`, `/stop`, `/status`, `/add_kw`, `/rm_kw`, `/add_ch`, `/rm_ch`, `/lang <en|es>`",
        'alert': "🚨 **Alert in {chat_title}**\n\n{text}",
        'bot_started_msg': "🤖 **Bot Started**\nType `/status` to see current configuration.",
        'lang_changed': "✅ Language changed to English.",
        'usage_lang': "⚠️ Usage: `/lang <en|es>`",
        
        # UI - General
        'back': "〈 Back",
        'next': "Next",
        'start_now': "Start Now",
        
        # UI - Welcome
        'welcome_title': "Welcome to\nTelegram Monitor",
        'welcome_desc': "Let's set up your automated alerts\nin just a few simple steps.",
        
        # UI - API Keys
        'api_title': "API Credentials",
        'api_desc': "We need these to connect to Telegram safely.",
        'api_id_ph': "API ID (e.g. 1234567)",
        'api_hash_ph': "Your API HASH",
        'bot_token_ph': "Your BOT TOKEN",
        'next': "Next",
        'checking': "Checking...",
        'tut_api_title': "How to get API ID & Hash",
        'tut_api_1': "1. Click the button below to open my.telegram.org",
        'tut_api_2': "2. Log in using your Telegram phone number.",
        'tut_api_3': "3. Click on 'API development tools'.",
        'tut_api_4': "4. Create a new application (any name). You will then see your 'App api_id' and 'App api_hash'.",
        'tut_api_btn': "Open my.telegram.org",
        'tut_bot_title': "How to get the Bot Token",
        'tut_bot_1': "1. Click the button below to open @BotFather in Telegram.",
        'tut_bot_2': "2. Send the message /newbot",
        'tut_bot_3': "3. Follow the steps to choose a name and username.",
        'tut_bot_4': "4. BotFather will give you a long HTTP API Token. Copy it.",
        'tut_bot_btn': "Open @BotFather",
        
        # UI - Phone
        'phone_title': "Telegram Login",
        'phone_desc': "Please enter your phone number\nwith your country code.",
        'phone_ph': "+34 600 123 456",
        'send_code': "Send Code",
        'sending': "Sending...",
        'invalid_phone': "Error: Number must start with '+' and contain 8-15 digits.",
        
        # UI - Code
        'code_title': "Verification Code",
        'code_desc': "We sent a code to your Telegram app.\nEnter it below:",
        'code_ph': "12345",
        'verify': "Verify",
        'verifying': "Verifying...",
        'invalid_code': "Error: The code must be 5 digits long.",
        
        # UI - Dashboard
        'dash_title': "Dashboard",
        'dash_running': "The Bot is RUNNING",
        'dash_stopped': "The Bot is STOPPED",
        'btn_start': "START BOT",
        'btn_stop': "STOP BOT",
        'dash_kw_title': "My Keywords",
        'dash_ch_title': "My Channels",
        'dash_kw_ph': "New keyword...",
        'dash_ch_ph': "Channel ID or @user...",
        'dash_add': "Add",
        'dash_tab_status': "Status",
        'dash_tab_kw': "Keywords",
        'dash_tab_ch': "Channels",
        'btn_logout': "Log out (Change Phone)",
        'tut_kw_title': "What are Keywords?",
        'tut_kw_desc': "Add the words or phrases you want to monitor. The bot will send you a notification whenever anyone mentions them.",
        'tut_ch_title': "What are Channels?",
        'tut_ch_desc': "You can monitor channels using two formats:\n\n1. By Username: If the channel is public, just type its username (e.g., @AppleDeals).\n2. By Numeric ID: For private groups, you need the ID. It always starts with '-100' (e.g., -1001234567890).\n\nTo find a hidden Numeric ID, you can forward any message from that private group to a bot like @JsonDumpBot."
    },
    'es': {
        # Bot Core
        'monitoring_started_cmd': "✅ Monitorización iniciada.",
        'monitoring_stopped_cmd': "⏸ Monitorización pausada.",
        'bot_status': "**Estado del Bot**",
        'monitoring': "Monitorización:",
        'active': "✅ Activa",
        'paused': "⏸ Pausada",
        'keywords': "**Palabras clave:**",
        'channels': "**Canales:**",
        'none': "Ninguno",
        'kw_added': "✅ Palabra clave añadida:",
        'kw_exists': "⚠️ La palabra clave ya existe.",
        'usage_add_kw': "⚠️ Uso: `/add_kw <palabra>`",
        'kw_removed': "✅ Palabra clave eliminada:",
        'kw_not_found': "⚠️ Palabra clave no encontrada.",
        'usage_rm_kw': "⚠️ Uso: `/rm_kw <palabra>`",
        'ch_added': "✅ Canal añadido:",
        'ch_exists': "⚠️ El canal ya existe.",
        'invalid_ch': "⚠️ ID/usuario de canal no válido.",
        'usage_add_ch': "⚠️ Uso: `/add_ch <id_canal_o_usuario>`",
        'ch_removed': "✅ Canal eliminado:",
        'ch_not_found': "⚠️ Canal no encontrado.",
        'usage_rm_ch': "⚠️ Uso: `/rm_ch <id_canal_o_usuario>`",
        'unknown_cmd': "⚠️ Comando desconocido. Disponibles: `/start`, `/stop`, `/status`, `/add_kw`, `/rm_kw`, `/add_ch`, `/rm_ch`, `/lang <en|es>`",
        'alert': "🚨 **Alerta en {chat_title}**\n\n{text}",
        'bot_started_msg': "🤖 **Bot Iniciado**\nEscribe `/status` para ver la configuración actual.",
        'lang_changed': "✅ Idioma cambiado a Español.",
        'usage_lang': "⚠️ Uso: `/lang <en|es>`",
        
        # UI - General
        'back': "〈 Atrás",
        'next': "Siguiente",
        'start_now': "Empezar ahora",
        
        # UI - Welcome
        'welcome_title': "Bienvenido a\nTelegram Monitor",
        'welcome_desc': "Vamos a configurar tus alertas automatizadas\nen muy pocos pasos.",
        
        # UI - API Keys
        'api_title': "Credenciales API",
        'api_desc': "Necesitamos esto para conectar con Telegram de forma segura.",
        'api_id_ph': "API ID (ej. 1234567)",
        'api_hash_ph': "Tu API HASH",
        'bot_token_ph': "Tu BOT TOKEN",
        'next': "Siguiente",
        'checking': "Comprobando...",
        'tut_api_title': "Cómo obtener API ID y Hash",
        'tut_api_1': "1. Haz clic en el botón de abajo para abrir my.telegram.org",
        'tut_api_2': "2. Inicia sesión con tu número de teléfono de Telegram.",
        'tut_api_3': "3. Haz clic en 'API development tools'.",
        'tut_api_4': "4. Crea una aplicación (incluso con datos inventados). Al terminar, verás tu 'App api_id' y 'App api_hash'.",
        'tut_api_btn': "Abrir my.telegram.org",
        'tut_bot_title': "Cómo obtener el Bot Token",
        'tut_bot_1': "1. Haz clic en el botón de abajo para hablar con @BotFather.",
        'tut_bot_2': "2. Envíale el mensaje /newbot",
        'tut_bot_3': "3. Sigue sus pasos para darle un nombre a tu bot.",
        'tut_bot_4': "4. Al final, te dará un Token rojo muy largo. Ese es el Bot Token.",
        'tut_bot_btn': "Abrir @BotFather",
        
        # UI - Phone
        'phone_title': "Inicia Sesión",
        'phone_desc': "Introduce tu número de teléfono\ncon prefijo internacional.",
        'phone_ph': "+34 600 123 456",
        'send_code': "Enviar Código",
        'sending': "Enviando...",
        'invalid_phone': "Error: El número debe empezar por '+' y tener 8-15 números.",
        
        # UI - Code
        'code_title': "Código de Verificación",
        'code_desc': "Te hemos enviado un código a Telegram.\nIntrodúcelo a continuación:",
        'code_ph': "12345",
        'verify': "Verificar",
        'verifying': "Verificando...",
        'invalid_code': "Error: El código debe tener 5 dígitos exactos.",
        
        # UI - Dashboard
        'dash_title': "Panel de Control",
        'dash_running': "El Bot está FUNCIONANDO",
        'dash_stopped': "El Bot está DETENIDO",
        'btn_start': "ARRANCAR BOT",
        'btn_stop': "DETENER BOT",
        'dash_kw_title': "Mis Palabras Clave",
        'dash_ch_title': "Mis Canales",
        'dash_kw_ph': "Nueva palabra...",
        'dash_ch_ph': "ID de canal o @usuario...",
        'dash_add': "Añadir",
        'dash_tab_status': "Estado",
        'dash_tab_kw': "Palabras Clave",
        'dash_tab_ch': "Canales",
        'btn_logout': "Cerrar sesión (Cambiar Teléfono)",
        'tut_kw_title': "¿Qué son las Palabras Clave?",
        'tut_kw_desc': "Añade las palabras o frases que quieres monitorizar. El bot te enviará una notificación cada vez que alguien las mencione.",
        'tut_ch_title': "¿Qué son los Canales?",
        'tut_ch_desc': "Puedes monitorizar canales usando dos formatos:\n\n1. Por Usuario: Si el canal es público, escribe su @usuario (ej: @OfertasApple).\n2. Por ID Numérico: Para grupos privados necesitas el ID. Siempre empieza por '-100' (ej: -1001234567890).\n\nPara descubrir el ID de un grupo privado, simplemente reenvía cualquier mensaje de ese grupo a un bot como @JsonDumpBot."
    }
}

def get_translation(lang_code, key, **kwargs):
    if lang_code not in TRANSLATIONS:
        lang_code = 'en'
    text = TRANSLATIONS[lang_code].get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text
