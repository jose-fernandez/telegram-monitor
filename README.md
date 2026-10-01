# Telegram Monitor Bot

Un "Userbot" de Telegram diseñado para escuchar canales específicos en tiempo real, buscar palabras clave definidas por el usuario, y enviarte una notificación Push a tu teléfono a través de un Bot de Telegram Oficial. Todo ello gestionado de forma interactiva y preparado para ser desplegado mediante Docker (ej. en un servidor TrueNAS, Raspberry Pi, VPS, etc.).

## Características

- **Monitorización Silenciosa:** Utiliza tu cuenta de Telegram (Userbot) para escuchar canales de los que eres miembro, sin necesidad de ser administrador.
- **Notificaciones Push:** Utiliza la API de Bots Oficiales de Telegram para enviarte las alertas, asegurando que recibas una notificación con sonido en tu teléfono móvil.
- **Configuración Interactiva:** No hace falta tocar el código ni reiniciar el servidor. Controla el bot directamente desde tus **Mensajes Guardados (Saved Messages)** en Telegram usando comandos.
- **Protección Antispam:** Evita saturar tu teléfono limitando las notificaciones (por defecto, máximo 3 alertas por minuto).
- **Despliegue Sencillo:** Incluye `Dockerfile` y `docker-compose.yml` para un despliegue rápido y seguro.

## Prerrequisitos

Necesitarás obtener tres claves de Telegram antes de empezar:

1. **`TELEGRAM_API_ID`** y **`TELEGRAM_API_HASH`**:
   - Ve a [my.telegram.org](https://my.telegram.org) e inicia sesión con tu número de teléfono.
   - Ve a **API development tools**.
   - Crea una nueva aplicación (puedes inventarte el nombre) y copia el `api_id` y `api_hash`.
2. **`TELEGRAM_BOT_TOKEN`**:
   - Abre Telegram y busca a **@BotFather**.
   - Envíale el comando `/newbot` y sigue los pasos.
   - Copia el token que te proporciona al final (ej. `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`).
   - **Importante:** Inicia un chat con tu nuevo bot (dale a "Start" o envíale `/start`) para que este tenga permiso de enviarte mensajes.

## Instalación y Uso Local

Es **obligatorio** ejecutar el bot localmente la primera vez para poder iniciar sesión con tu cuenta de Telegram y generar el archivo de sesión (`sesion_monitor.session`).

1. **Clona o descarga este repositorio.**
2. **Prepara las variables de entorno:**
   - Crea un archivo llamado `.env` en la raíz del proyecto.
   - Añade tus credenciales:
     ```env
     TELEGRAM_API_ID=tu_api_id
     TELEGRAM_API_HASH=tu_api_hash
     TELEGRAM_BOT_TOKEN=tu_bot_token
     ```
3. **Prepara el archivo de configuración:**
   - Copia o renombra `config.json.example` a `config.json`.
4. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
5. **Ejecuta el bot:**
   ```bash
   python3 main_cli.py
   ```
   *La consola te pedirá tu número de teléfono y el código de inicio de sesión que te llegará por Telegram. Una vez introducido, se generará el archivo `sesion_monitor.session`.*

## Despliegue con Docker

Una vez que tengas tu archivo `.env`, tu `config.json` y hayas generado el archivo `sesion_monitor.session` (paso vital), puedes desplegarlo fácilmente:

```bash
docker-compose up -d
```

## Comandos Interactivos

Para gestionar el bot, ve al chat de **Mensajes Guardados (Saved Messages)** de tu propia cuenta de Telegram. Puedes usar los siguientes comandos:

- `/start` - Inicia/reanuda la monitorización.
- `/stop` - Pausa la monitorización.
- `/status` - Muestra si el bot está activo y la lista actual de canales y palabras clave.
- `/add_kw <palabra>` - Añade una nueva palabra clave.
- `/rm_kw <palabra>` - Elimina una palabra clave.
- `/add_ch <canal>` - Añade un canal (puedes usar el ID numérico como `-1001234567890` o el usuario como `@nombre_canal`).
- `/rm_ch <canal>` - Elimina un canal.
- `/lang <en|es>` - Cambia el idioma de los mensajes del bot a Inglés (`en`) o Español (`es`).

Toda la configuración se guarda automáticamente en `config.json` y persistirá tras los reinicios.

## Privacidad y Git

El archivo `.gitignore` ya está configurado para evitar que subas credenciales por accidente. Archivos como `.env`, `config.json`, y los archivos de sesión `*.session` serán ignorados por Git.
