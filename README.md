# WhatsApp AI Agent Bot

An automated WhatsApp bot that replies to incoming messages using AI-powered responses with Selenium web automation.

## Prerequisites

Before running this project, ensure you have the following installed on your system:

### System Requirements
- **Python**: Version 3.8 or higher
- **Google Chrome**: Latest version (required for Selenium automation)
- **pip**: Python package manager (usually comes with Python)

### Verify Installation
```bash
python --version
pip --version
```

## Installation & Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Sudeep5363/Whatsapp_AI_Agent.git
cd Whatsapp_AI_Agent
```

### Step 2: Create a Virtual Environment (Recommended)
```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python -m venv .venv
source .venv/bin/activate
```

### Step 3: Install Required Dependencies
```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install selenium
pip install webdriver-manager
```

## Usage

### Running the WhatsApp Bot

```bash
# Make sure your virtual environment is activated
python whatsapp_bot.py
```

### Steps to Execute:

1. **Run the script**:
   ```bash
   python whatsapp_bot.py
   ```

2. **Scan QR Code**:
   - A Chrome browser window will open with WhatsApp Web
   - Scan the QR code with your mobile WhatsApp
   - You will be logged in to your WhatsApp account

3. **Press Enter**:
   - After scanning, press Enter in the terminal to continue

4. **Bot is Now Active**:
   - The bot will monitor incoming messages
   - It will automatically reply based on the keywords in the `build_reply()` function
   - Messages will be logged in the console

## Configuration

### Customizing Bot Replies

Edit the `build_reply()` function in `whatsapp_bot.py` to change the automated responses:

```python
def build_reply(message_text: str) -> str:
    if "price" in message_text:
        return "Your custom price response here"
    if "hello" in message_text:
        return "Your custom greeting here"
    # Add more conditions as needed
```

### Chrome Session Persistence

The bot uses a persistent Chrome session stored at:
- **Windows**: `%APPDATA%\whatsapp_bot_session`

This allows the bot to maintain login sessions across restarts.

## Features

✅ Automatic message detection  
✅ AI-powered keyword-based replies  
✅ Session persistence  
✅ Error handling and logging  
✅ Real-time incoming message monitoring  
✅ Outgoing message count tracking  

## Supported Keywords

The bot automatically replies to messages containing:
- **price, cost, charge** - Pricing information
- **location, where** - Location details
- **service** - Service information
- **time, timing** - Availability information
- **hi, hello** - Greeting response
- **demo** - Demo request
- **offer, discount** - Special offers
- **contact, call** - Contact information
- **thanks** - Thank you response
- **bye** - Goodbye message

## Dependencies

| Package | Purpose |
|---------|---------|
| selenium | Web browser automation |
| webdriver-manager | Automatic Chrome driver management |

## Troubleshooting

### Issue: "Chrome driver not found"
**Solution**: The `webdriver-manager` package should auto-download it. If it fails:
```bash
pip install --upgrade webdriver-manager
```

### Issue: "QR code window doesn't appear"
**Solution**: Ensure Chrome is installed and up-to-date. Check:
```bash
chrome://version
```

### Issue: "Bot doesn't reply to messages"
**Solution**: 
- Check the XPath selectors in `find_incoming_messages()` function
- WhatsApp Web updates may change the DOM structure
- Verify the message keywords match your custom shortcuts

### Issue: "Module not found" errors
**Solution**: Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

## File Structure

```
Whatsapp_AI_Agent/
├── whatsapp_bot.py       # Main bot script
├── agent.py              # Agent configuration (if applicable)
├── README.md             # This file
└── requirements.txt      # Python dependencies
```

## Important Notes ⚠️

1. **WhatsApp Web Compliance**: This bot automates WhatsApp Web. Ensure you comply with WhatsApp's Terms of Service.

2. **Keep Browser Open**: Do not close the Chrome window while the bot is running.

3. **Session Persistence**: The bot saves your login session automatically.

4. **Message Queue**: The bot checks for new messages every 3 seconds.

5. **Error Recovery**: If an error occurs, the script logs it and continues running.

## Support & Contributions

For issues, feature requests, or contributions, visit:
https://github.com/Sudeep5363/Whatsapp_AI_Agent

## License

This project is provided as-is for educational and personal use.

---

**Last Updated**: March 18, 2026
