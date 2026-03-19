# 🚀 Quick Start Guide

Get the WhatsApp AI Agent Bot running in **5 minutes**!

## Prerequisites Check
```bash
# Verify Python installation (3.8+)
python --version

# Verify pip
pip --version

# Verify Chrome browser is installed
chrome --version  # or google-chrome --version on Linux
```

## Installation (5 steps)

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/Sudeep5363/Whatsapp_AI_Agent.git
cd Whatsapp_AI_Agent
```

### 2️⃣ **Create Virtual Environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/macOS
python -m venv .venv
source .venv/bin/activate
```

### 3️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 4️⃣ **Run the Bot**
```bash
python whatsapp_bot.py
```

### 5️⃣ **Scan QR Code**
- A Chrome window will open
- Scan the QR code with your mobile WhatsApp
- Press Enter in the terminal

**That's it! Your bot is now running! 🎉**

---

## Quick Tips

### Test Bot Offline
```bash
python agent.py
```

### Customize Replies
Edit the `build_reply()` function in `whatsapp_bot.py`

### Stop the Bot
Press `Ctrl+C` in the terminal

### Remove Cached Session
Delete: `%APPDATA%\whatsapp_bot_session` (Windows)
or: `~/.config/whatsapp_bot_session` (Linux/Mac)

---

## Common Issues

| Issue | Solution |
|-------|----------|
| Chrome driver fails | `pip install --upgrade webdriver-manager` |
| QR code doesn't appear | Update Chrome to latest version |
| Bot doesn't reply | Check keywords in `build_reply()` function |
| Port 9222 in use | Run `netstat -ano \| find "9222"` to find process |

---

## Next Steps

1. Read [README.md](README.md) for full documentation
2. Check [CONTRIBUTING.md](CONTRIBUTING.md) to contribute
3. Review [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
4. Open an [Issue](https://github.com/Sudeep5363/Whatsapp_AI_Agent/issues) if you have questions

---

**Happy automating! 🤖**
