# QQ-Codex Bridge

**Control Codex from QQ — no ChatGPT account required.**

Most Codex remote tools assume you have an official OpenAI login. This bridge doesn't. It connects to **any OpenAI-compatible API** (Aliyun DashScope, DeepSeek, Moonshot, local vLLM, etc.), so you can drive your desktop Codex CLI from mobile QQ without ever touching ChatGPT's login flow.

Both sides share the same workspace. Send a message on QQ, get Codex's response back on QQ.

## Why This Exists

If you're in a region where ChatGPT sign-up is painful, or you simply prefer pay-as-you-go APIs over a monthly subscription, most "remote Codex" tools are useless to you. This project fixes that gap:

- **No ChatGPT account** — works with any third-party API key
- **No VPN** — QQ + ngrok, both accessible in mainland China
- **No complex setup** — single config file, one Python script

## How It Works
Mobile QQ → QQ Server → (WebSocket) → bridge.py → codex exec → Codex Engine
│
Desktop Codex sees the same workspace

text

Incoming QQ messages are forwarded to Codex via `codex exec`. Replies are sent back through the QQ Bot API.

## Requirements

- Windows 10/11
- Python 3.10+ (or Codex's bundled Python)
- Codex CLI installed (`codex` command works)
- Any OpenAI-compatible API key (Aliyun, DeepSeek, local model, etc.)
- A secondary QQ account (avoid your main account)

## Setup

### 1. Install Python dependencies

Run in the project directory:

pip install -r requirements.txt

Or use Codex's bundled Python:

%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pip install -r requirements.txt

> If Python isn't installed, double-clicking `start.bat` usually opens the Microsoft Store install page.

### 2. Create a QQ Bot

1. Open the QQ Open Platform (q.qq.com) and scan to log in
2. Create a bot application, get your **AppID** and **AppSecret**
3. In **Development Settings**:
   - Message push mode → **Webhook**
   - Callback URL → fill in the ngrok URL later
4. In **Permission Settings**, enable **Message Send/Receive** and **Rich Media Messages**

### 3. Register ngrok (free)

1. Sign up at ngrok.com
2. Go to your **Authtoken** page
3. Copy your authtoken (looks like `2vC8xxxx...`)

### 4. Configure the bridge

Copy the config template:

copy config.yaml config.local.yaml

Edit `config.local.yaml`:

qq_bot:
  app_id: "your_app_id"
  app_secret: "your_app_secret"
  ngrok_token: "your_ngrok_token"
  webhook_port: 9000

auth:
  allowed_users:
    - "0"                 # your openid — printed on first run

codex:
  workspace: "E:/codex"   # Codex working directory

> Don't want to do this manually? You can ask Codex to fill it in for you.

### 5. Start

Double-click `start.bat`, or run:

python bridge.py

Console output:
QQ-Codex Bridge
[ngrok] >>> https://xxxx.ngrok-free.app/qqbot <<<
[Bot] Ready!

text

### 6. Set the callback URL

Copy the ngrok URL (e.g. `https://xxxx.ngrok-free.app/qqbot`) into the **Callback URL** field on q.qq.com.

### 7. Usage

Send a message to your bot on mobile QQ:

| Message | Effect |
| ------- | ------ |
| `hello` | Codex processes and replies |
| `/new`  | Start a new conversation |

## FAQ

**Q: I'm not getting replies.**
Check if the console prints `[MSG]`. If not, your callback URL is wrong — verify it matches the ngrok URL on q.qq.com.

**Q: "Codex took too long" error.**
Codex times out after 90 seconds. Try simplifying your request.

**Q: Desktop Codex doesn't show my QQ conversations.**
Sessions created by `codex exec` don't appear in the desktop session list, but files are stored under `~/.codex/sessions/`. You can resume with `codex exec resume --last`.

**Q: The ngrok URL changes every restart.**
Free ngrok gives a new URL each time. Update the callback URL on q.qq.com, or buy a static domain.

**Q: Which API should I use?**
Any OpenAI-compatible endpoint works. Aliyun DashScope (`https://dashscope.aliyuncs.com/compatible-mode/v1`) and DeepSeek (`https://api.deepseek.com/v1`) are both verified to work.

## File Overview
├── bridge.py Main bridge program
├── config.yaml Config template
├── config.local.yaml Your private config (gitignored)
├── requirements.txt Python dependencies
├── start.bat Startup script
├── .gitignore Excludes secret files
└── .gitattributes Git language detection

text

## Notes

- Use a secondary QQ account — main accounts risk rate limiting
- Never expose your AppSecret
- Third-party API keys are loaded from `config.local.yaml` and never committed
