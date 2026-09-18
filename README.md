好的，你直接复制这段到 GitHub 网页编辑 README.md 就行：
# QQ-Codex Bridge

Chat with Codex remotely via QQ from your phone. Shares the same workspace with the desktop Codex app.

## Architecture

Phone QQ ──→ QQ Official Server ──(WebSocket)──→ bridge.py ──→ codex exec ──→ Codex Engine
                                                       │
                                            Desktop Codex sees the same workspace

## Requirements

- Windows 10/11
- Python 3.10+ (or use the Python bundled with Codex)
- Codex CLI installed (`codex` command available)
- A QQ secondary account (not recommended to use your main account)

## Setup

### 1. Install Python dependencies

```cmd
pip install -r requirements.txt
Or with Codex bundled Python:
%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pip install -r requirements.txt
2. Create a QQ Bot
1. Open QQ Open Platform, scan QR code to login
2. Create a bot application, get your AppID and AppSecret
3. In Development Settings:
   - Message push mode → Webhook
   - Callback URL → Fill in the ngrok URL later (step 6)
4. In Permission Settings, enable "Message Sending/Receiving" and "Rich Media Messages"
3. Register ngrok (free)
1. Sign up at ngrok.com
2. Get your authtoken from dashboard
4. Configure the bridge
Copy the config template:
copy config.yaml config.local.yaml
Edit config.local.yaml with your credentials:
qq_bot:
  app_id: "your_app_id"
  app_secret: "your_app_secret"
  ngrok_token: "your_ngrok_authtoken"
  webhook_port: 9000

auth:
  allowed_users:
    - "0"                       # Your QQ openid (printed on first run)

codex:
  workspace: "E:/codex"         # Codex working directory
5. Start the bridge
Double-click start.bat, or run:
python bridge.py
You will see:
QQ-Codex Bridge
[ngrok] >>> https://xxxx.ngrok-free.app/qqbot <<<
[Bot] Ready!
6. Set the callback URL
Copy the ngrok URL (e.g. https://xxxx.ngrok-free.app/qqbot) and paste it into the Callback URL field on q.qq.com.
7. Use it
Send a message to your bot on QQ:
Message	Effect
Hello	Codex processes and replies
/new	Start a new conversation


FAQ
Q: No reply received?
Check if [MSG] appears in the console. If not, the callback URL is not configured correctly on q.qq.com.
Q: Got "Codex took too long"?
Codex processing exceeded 90 seconds. Try a simpler question.
Q: Can't see QQ conversations in desktop Codex?
Sessions created by codex exec don't appear in the desktop sidebar, but the files are stored in ~/.codex/sessions/. Use codex exec resume --last in terminal to continue them.
Q: ngrok URL changes on restart?
Free ngrok assigns a different URL each time. Purchase a static domain or update the callback URL in q.qq.com each restart.
File Structure
├── bridge.py          Main bridge program
├── config.yaml        Config template (safe to commit)
├── config.local.yaml  Your credentials (gitignored)
├── requirements.txt   Python dependencies
├── start.bat          Startup script
├── .gitignore         Excludes secret files
└── .gitattributes     Git language detection
Notes
- Use a secondary QQ account to avoid risk to your main account
- Keep your AppSecret private and never commit it
