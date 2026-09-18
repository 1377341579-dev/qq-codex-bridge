# QQ-Codex Bridge

Chat with Codex remotely via QQ from your phone. Shares the same workspace with the desktop Codex app.

## Requirements

- Windows 10/11
- Python 3.10+
- Codex CLI installed
- A QQ secondary account

## Quick Start

1. `pip install -r requirements.txt`
2. Create a QQ Bot at https://q.qq.com, get AppID + AppSecret
3. Register at https://ngrok.com, get your authtoken
4. Copy `config.yaml` to `config.local.yaml`, fill in your credentials
5. Run `start.bat`
6. Copy the printed ngrok URL to q.qq.com callback URL field
7. Send a message to your bot on QQ!

## Commands

| Message | Effect                    |
| ------- | ------------------------- |
| Hello   | Codex replies on QQ       |
| /new    | Start a fresh conversation |

## Notes

- Use a secondary QQ account to avoid risk
- Keep AppSecret private
- `config.local.yaml` is gitignored, never commit it
