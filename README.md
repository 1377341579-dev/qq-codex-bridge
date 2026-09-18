QQ-Codex Bridge
Control desktop Codex remotely from QQ on your phone. Both share the same workspace.

How It Works
Incoming QQ messages are forwarded to Codex via codex exec, and replies are sent back through the QQ API.

Mobile QQ → QQ Server → (WebSocket) → bridge.py → codex exec → Codex Engine
                                                          │
                                              Desktop Codex sees the same workspace
Requirements
Windows 10/11

Python 3.10+ (or use Codex's bundled Python)

Codex CLI installed (codex command available)

A secondary QQ account (do not use your main account — risk of rate limiting)

Setup
1. Install Python dependencies
Run in the project directory:

pip install -r requirements.txt

Or use Codex's bundled Python:

%USERPROFILE%.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pip install -r requirements.txt

If Python is not installed, double-clicking start.bat will usually open the Microsoft Store install page automatically.

2. Create a QQ Bot
Open the QQ Open Platform (q.qq.com) and sign in with a QR code

Create a bot application and get your AppID and AppSecret

In Development Settings:

Message push mode → Webhook

Callback URL → Fill in the ngrok public URL later (after starting the bridge)

In Permission Settings, enable Message Send/Receive and Rich Media Messages

3. Register ngrok (free)
Sign up at ngrok.com

Go to your Authtoken page

Copy your authtoken (looks like 2vC8xxxx...)

4. Configure the bridge
Copy the config template:

copy config.yaml config.local.yaml

Then edit config.local.yaml and fill in your credentials:

qq_bot:
app_id: "1905633576" # your AppID
app_secret: "hKlyxkKgnl..." # your AppSecret
ngrok_token: "2vC8xxxx..." # your ngrok authtoken
webhook_port: 9000

auth:
allowed_users:

"0" # your openid — printed on first run, fill it in afterward

codex:
workspace: "E:/codex" # Codex working directory

If you want to save time, you can let Codex handle the configuration from this step onward.

5. Start
Double-click start.bat, or run:

python bridge.py

On startup, the console will print:

text
QQ-Codex Bridge
[ngrok] >>> https://xxxx.ngrok-free.app/qqbot <<<
[Bot] Ready!
6. Set the callback URL
Copy the ngrok URL printed in the console (e.g. https://xxxx.ngrok-free.app/qqbot) into the Callback URL field on q.qq.com.

7. Usage
Send a message to your bot from mobile QQ:

Message	Effect
hello	Codex processes and replies
/new	Start a new conversation
FAQ
Q: I'm not getting replies.
Check if the console prints [MSG]. If not, your callback URL is not set correctly — verify it matches the ngrok URL on q.qq.com.

Q: "Codex took too long" error.
Codex times out after 90 seconds. Try simplifying your request.

Q: Desktop Codex doesn't show my QQ conversations.
Sessions created by codex exec don't appear in the desktop session list, but the conversation files are stored under ~/.codex/sessions/. You can resume with codex exec resume --last.

Q: The ngrok URL changes every restart.
The free ngrok plan gives a new URL each time. You'll need to update the callback URL on q.qq.com. A paid static domain can fix this.

File Overview
├── bridge.py         Main bridge program
├── config.yaml       Config template (safe to commit)
├── config.local.yaml Your private config (gitignored)
├── requirements.txt  Python dependencies
├── start.bat         Startup script
├── .gitignore        Excludes secret files
└── .gitattributes    Git language detection
Notes
Use a secondary QQ account — main accounts risk rate limiting

Never expose your AppSecret

