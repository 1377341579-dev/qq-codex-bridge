# QQ-Codex Bridge

用手机 QQ 远程与桌面端 Codex 交流，对话共享同一工作区。

## 原理

```
手机QQ ──→ QQ官方服务器 ──(WebSocket)──→ bridge.py ──→ codex exec ──→ Codex 引擎
                                                    │
                                        桌面板 Codex 可见同一工作区目录
```

收到的 QQ 消息通过 `codex exec` 交给 Codex 处理，回复通过 QQ API 发回。

## 环境要求

- Windows 10/11
- Python 3.10+（或直接用 Codex 自带的 Python）
- 已安装 [Codex CLI](https://codex.openai.com)（`codex` 命令可用）
- 一个 QQ 小号（不要用主号，有风控风险）

## 安装步骤

### 1. 安装 Python 依赖（若未安装一般在启动start.bat时会自动跳出微软商店安装页面）

```cmd
pip install -r requirements.txt
```

如果用 Codex 自带的 Python：

```cmd
%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe -m pip install -r requirements.txt
```

### 2. 创建 QQ 机器人

1. 打开 [QQ 开放平台](https://q.qq.com)，扫码登录
2. 创建机器人应用，获取 **AppID** 和 **AppSecret**
3. 在「开发设置」中：
   - 消息推送模式 → **Webhook**
   - 回调地址 → 后面启动 bridge 后填写 ngrok 公网 URL
4. 在「权限配置」中勾选「消息收发」和「富媒体消息」

### 3. 注册 ngrok（免费）

1. 打开 [ngrok 官网](https://ngrok.com) 注册免费账号
2. 进入 [Your Authtoken](https://dashboard.ngrok.com/get-started/your-authtoken) 页面
3. 复制你的 authtoken（类似 `2vC8xxxx...`）

### 4. 配置桥接（嫌麻烦在此步开始让codex帮你完成）

复制配置模板：

```cmd
copy config.yaml config.local.yaml
```

编辑 `config.local.yaml`，填入你的凭据：

```yaml
qq_bot:
  app_id: "1905633576"          # 你的 AppID
  app_secret: "hKlyxkKgnl..."   # 你的 AppSecret
  ngrok_token: "2vC8xxxx..."    # 你的 ngrok authtoken
  webhook_port: 9000

auth:
  allowed_users:
    - "0"                       # 首次运行后控制台会打印你的 openid，再回来填

codex:
  workspace: "E:/codex"         # Codex 工作目录
```

### 5. 启动

双击 `start.bat`，或命令行运行：

```cmd
python bridge.py
```

启动后控制台会显示：

```
QQ-Codex Bridge
[ngrok] >>> https://xxxx.ngrok-free.app/qqbot <<<
[Bot] Ready!
```

### 6. 设置回调地址

把控制台打印的 ngrok URL（如 `https://xxxx.ngrok-free.app/qqbot`）填到 q.qq.com 的「回调地址」中。

### 7. 使用

用手机 QQ 给机器人发消息：

| 消息     | 效果          |
| ------ | ----------- |
| `你好`   | Codex 处理并回复 |
| `/new` | 开启新对话       |

## 常见问题

**Q: 收不到回复？**
检查控制台是否打印了 `[MSG]`，没打印说明回调地址没配好。重新检查 q.qq.com 的回调地址是否为 ngrok URL。

**Q: 回复说"Codex took too long"？**
Codex 处理超过 90 秒自动超时，简化问题重试即可。

**Q: 桌面端看不到 QQ 对话？**
`codex exec` 创建的会话不会显示在桌面端会话列表，但对话文件存在 `~/.codex/sessions/` 里，可用 `codex exec resume --last` 在终端继续。

**Q: ngrok URL 每次重启会变？**
免费版 ngrok 每次启动 URL 不同，需同步更新 q.qq.com 回调地址。可购买 ngrok 静态域名固定 URL。

## 文件说明

```
├── bridge.py         主桥接程序
├── config.yaml       配置模板（可提交 Git）
├── config.local.yaml 你的私密配置（已 gitignore）
├── requirements.txt  Python 依赖
├── start.bat         启动脚本
├── .gitignore        排除密钥文件
└── .gitattributes    Git 语言识别
```

## 注意事项

- 建议用小号，大号有风控风险
- AppSecret 不要泄露

