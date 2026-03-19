# WhatsApp AI Agent Bot

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python)
![Selenium](https://img.shields.io/badge/Selenium-4.15-green?style=flat-square&logo=selenium)
![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)

An intelligent WhatsApp automation bot that replies to incoming messages using keyword-based AI responses and Selenium web automation. Perfect for businesses looking to automate customer service on WhatsApp Web.

## Overview

This bot monitors WhatsApp Web for incoming messages and automatically generates contextual replies based on predefined keywords. It leverages Selenium for browser automation and maintains persistent Chrome sessions for seamless operation.

**Use Cases:**
- Automated customer support responses
- Lead generation and qualification
- Out-of-office auto-replies
- Business inquiry automation
- Availability information delivery

## Prerequisites

Before running this project, ensure you have the following installed:

### System Requirements
- Python: 3.8 or higher
- Google Chrome: Latest version (required for Selenium)
- pip: Python package manager

### Verify Installation
```bash
python --version  # Should be 3.8+
pip --version     # Should be pip 20.0+
```

## Quick Start

### 1. Clone & Setup
```bash
# Clone the repository
git clone https://github.com/Sudeep5363/Whatsapp_AI_Agent.git
cd Whatsapp_AI_Agent

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Running the Bot

```bash
python whatsapp_bot.py
```

#### Execution Steps

1. Start the script - Chrome opens WhatsApp Web
2. Scan QR Code - Use your mobile WhatsApp
3. Press Enter - Bot starts monitoring
4. Auto-Reply - Bot responds to messages
5. Check Console - View message logs

## Configuration & Customization

### Customizing Replies

Edit the `build_reply()` function in [whatsapp_bot.py](whatsapp_bot.py) to add/modify automatic responses:

```python
def build_reply(message_text: str) -> str:
    """Generate AI-powered response based on message content."""
    if "price" in message_text or "cost" in message_text:
        return "Our pricing: Rs 3000 startup + Rs 500/month"
    if "available" in message_text:
        return "We're available 9 AM - 8 PM IST"
    if "hello" in message_text or "hi" in message_text:
        return "Hello! How can I assist you?"
    return "Thanks for your message. We'll get back to you soon!"
```

### Session Management

The bot automatically persists Chrome sessions:
- **Windows**: `%APPDATA%\whatsapp_bot_session`
- **Linux/Mac**: `~/.config/whatsapp_bot_session`

This means you don't need to scan the QR code on every restart.

## Features

- Real-time monitoring of incoming messages
- Keyword-based intelligent reply generation
- Session persistence across restarts
- Robust error handling and logging
- Cross-platform browser automation
- Message tracking and console logging
- Easy configuration and customization

## Keyword Reference

| Keyword(s) | Response Type |
|------------|---------------|
| price, cost, charge | Pricing details |
| location, where | Location information |
| service | Service description |
| time, timing | Availability hours |
| hi, hello | Greeting |
| demo | Demo request |
| offer, discount | Special offers |
| contact, call | Contact info |
| thanks | Thank you |
| bye | Goodbye |

**Note**: Keywords are case-insensitive and checked as substring matches.

## Dependencies

| Package | Version | Purpose |
|---------|---------|----------|
| selenium | 4.15.2 | Web browser automation |
| webdriver-manager | 4.0.1 | Automatic Chrome driver management |

All dependencies are specified in [requirements.txt](requirements.txt)

## Troubleshooting

### ChromeDriver Issues
```bash
pip install --upgrade webdriver-manager
```

### QR Code Not Appearing
- Ensure Google Chrome is fully updated
- Check Chrome version via `chrome://version`
- Try using a fresh Chrome profile

### Bot Not Replying
- Verify keywords in `build_reply()` match your test messages
- Check WhatsApp Web loads correctly
- Ensure you're logged in before continuing
- WhatsApp DOM structure changes may require XPath updates

### Import Errors
```bash
pip install -r requirements.txt --force-reinstall
```

## Project Structure

```
Whatsapp_AI_Agent/
├── whatsapp_bot.py       # Main bot script
├── agent.py              # Agent utilities
├── requirements.txt      # Dependencies
├── README.md             # Documentation
├── LICENSE               # MIT License
├── CONTRIBUTING.md       # Contribution guidelines
└── .github/              # GitHub templates
```

## Important Notes

1. WhatsApp ToS - Use responsibly and check WhatsApp's Terms of Service
2. Browser Window - Keep Chrome open while the bot is running
3. Persistent Sessions - Login sessions are automatically saved
4. Message Polling - Bot checks for messages every 3 seconds
5. Error Recovery - Errors are logged and bot continues
6. Single Instance - Run only one bot instance to avoid conflicts

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Links

- GitHub: [github.com/Sudeep5363/Whatsapp_AI_Agent](https://github.com/Sudeep5363/Whatsapp_AI_Agent)
- Issues: [Report a bug](https://github.com/Sudeep5363/Whatsapp_AI_Agent/issues)

---

Created by Sudeep | March 2026
