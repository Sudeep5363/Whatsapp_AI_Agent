"""
WhatsApp AI Agent Bot

This module implements an automated WhatsApp bot that monitors incoming messages
and generates intelligent replies using keyword-based AI responses. It uses Selenium
for browser automation and maintains persistent Chrome sessions.

Author: Sudeep
License: MIT
GitHub: https://github.com/Sudeep5363/Whatsapp_AI_Agent
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from datetime import datetime


# ============================================================================
# CHROME DRIVER CONFIGURATION
# ============================================================================

def setup_chrome_driver():
    """
    Initialize and configure Chrome WebDriver with persistent session management.
    
    Returns:
        webdriver.Chrome: Configured Chrome WebDriver instance
    """
    chrome_options = Options()
    
    # Store persistent session to avoid re-scanning QR code
    if os.getenv('APPDATA'):  # Windows
        user_data_dir = os.path.join(os.getenv('APPDATA'), 'whatsapp_bot_session')
    else:  # Linux/macOS
        user_data_dir = os.path.expanduser('~/.config/whatsapp_bot_session')
    
    chrome_options.add_argument(f"user-data-dir={user_data_dir}")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--remote-debugging-port=9222")
    
    # Initialize driver with automatic ChromeDriver management
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    
    return driver


# Initialize global state
driver = setup_chrome_driver()
driver.get("https://web.whatsapp.com")

input("Scan QR code with your mobile WhatsApp and press Enter to continue...")

attempt = 0
processed_message_signatures = set()  # Track processed messages
bot_initialized = False


# ============================================================================
# REPLY GENERATION
# ============================================================================

def build_reply(message_text: str) -> str:
    """
    Generate context-aware reply based on message keywords.
    
    This function implements keyword matching to generate intelligent responses.
    Keywords are case-insensitive and matched as substrings.
    
    Args:
        message_text (str): Incoming message text
        
    Returns:
        str: Generated reply message
    """
    message_lower = message_text.lower().strip()
    
    # Price inquiries
    if any(word in message_lower for word in ["price", "cost", "charge"]):
        return (
            "Our WhatsApp automation setup starts from Rs 3,000.\n"
            "Includes: Auto replies, lead capture, setup within 24 hours."
        )
    
    # Location inquiries
    if any(word in message_lower for word in ["location", "where"]):
        return "We are based in Bangalore and provide services online across India."
    
    # Service inquiries
    if "service" in message_lower:
        return (
            "We help businesses automate WhatsApp replies, generate leads,\n"
            "and save time using AI automation."
        )
    
    # Availability inquiries
    if any(word in message_lower for word in ["time", "timing", "available"]):
        return "We are available from 9 AM to 8 PM IST (Monday-Saturday)."
    
    # Greetings
    if any(word in message_lower for word in ["hi", "hello", "hey"]):
        return "Hi! Welcome to Sudeep Services! How can I help you today?"
    
    # Demo request
    if "demo" in message_lower:
        return "Sure! I can show you a live demo. Would you like to schedule one?"
    
    # Offer/Discount inquiries
    if any(word in message_lower for word in ["offer", "discount", "discount"]):
        return "Yes! We have special offers for new clients this week."
    
    # Contact/Call request
    if any(word in message_lower for word in ["contact", "call", "phone"]):
        return "Please share your number and preferred time. I will contact you soon."
    
    # Thank you
    if "thank" in message_lower:
        return "You're welcome! Happy to help."
    
    # Goodbye
    if "bye" in message_lower:
        return "Thank you! Have a great day!"
    
    # Default fallback
    return (
        "Hi! I can assist you with:\n"
        "- Pricing information\n"
        "- Services offered\n"
        "- Product demo\n"
        "- Special offers\n\n"
        "Type any of these keywords to get started!"
    )


# ============================================================================
# MESSAGE EXTRACTION & PROCESSING
# ============================================================================

def extract_message_text(container) -> str:
    """
    Extract text content from a message container element.
    
    Args:
        container: Selenium WebElement representing a message container
        
    Returns:
        str: Extracted and normalized message text
    """
    try:
        # Try multiple selectors for text extraction
        text_elements = container.find_elements(
            By.XPATH,
            './/span[contains(@class,"selectable-text")]'
        )
        if text_elements:
            return text_elements[0].text.lower().strip()
    except Exception:
        pass
    
    # Fallback to container text
    return container.text.lower().strip()


def build_message_signature(container, text: str) -> str:
    """
    Create unique signature for message to track if it's already processed.
    
    Args:
        container: Selenium WebElement containing the message
        text (str): Message text content
        
    Returns:
        str: Unique message signature
    """
    try:
        metadata = container.get_attribute("data-pre-plain-text")
    except Exception:
        metadata = ""
    
    return f"{metadata}|{text}"


def find_incoming_messages():
    """
    Find all incoming message containers in the current chat.
    
    Uses multiple XPath selectors for robustness against WhatsApp Web DOM changes.
    
    Returns:
        list: Selenium WebElements representing incoming messages
    """
    selectors = [
        '//div[@id="main"]//div[contains(@class,"message-in")]//div[@data-pre-plain-text]',
        '//div[@id="main"]//div[contains(@class,"message-in") and @data-pre-plain-text]',
        '//div[@id="main"]//div[@data-pre-plain-text and not(contains(@data-pre-plain-text,"You:"))]'
    ]
    
    for selector in selectors:
        found = driver.find_elements(By.XPATH, selector)
        if found:
            return found
    
    return []


def count_outgoing_messages() -> int:
    """
    Count number of outgoing messages sent by the bot.
    
    Returns:
        int: Number of outgoing messages
    """
    outgoing = driver.find_elements(
        By.XPATH,
        '//div[@id="main"]//div[contains(@class,"message-out")]'
    )
    return len(outgoing)


# ============================================================================
# MAIN BOT LOOP
# ============================================================================

def log_message(level: str, message: str):
    """Format and print log messages with timestamps."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def main_loop():
    """
    Main bot execution loop.
    
    Continuously monitors WhatsApp for incoming messages and sends automated replies.
    """
    global attempt, bot_initialized
    
    try:
        while True:
            try:
                time.sleep(3)  # Check for messages every 3 seconds
                attempt += 1
                
                # Get current message counts
                incoming_containers = find_incoming_messages()
                outgoing_count = count_outgoing_messages()
                incoming_count = len(incoming_containers)
                
                log_message("INFO", f"Attempt {attempt} | Incoming: {incoming_count} | Outgoing: {outgoing_count}")
                
                # Initialize on first run - mark all existing messages as processed
                if not bot_initialized:
                    for container in incoming_containers:
                        text = extract_message_text(container)
                        signature = build_message_signature(container, text)
                        processed_message_signatures.add(signature)
                    
                    bot_initialized = True
                    log_message("INFO", "Bot initialized. Waiting for new incoming messages...")
                    continue
                
                # Check for new messages
                new_messages = []
                for container in incoming_containers:
                    text = extract_message_text(container)
                    if not text:
                        continue
                    
                    signature = build_message_signature(container, text)
                    if signature not in processed_message_signatures:
                        new_messages.append((container, text, signature))
                
                # Process new messages
                if not new_messages:
                    log_message("DEBUG", "No new messages...")
                    continue
                
                for _, new_message, signature in new_messages:
                    log_message("RECEIVE", f"{new_message}")
                    
                    # Generate reply
                    reply = build_reply(new_message)
                    log_message("SEND", f"{reply}")
                    
                    # Send reply
                    try:
                        message_box = driver.find_element(
                            By.XPATH,
                            '//footer//div[@contenteditable="true"][@data-tab] | //footer//div[@contenteditable="true"]'
                        )
                        message_box.click()
                        time.sleep(0.5)
                        message_box.send_keys(reply)
                        message_box.send_keys(Keys.ENTER)
                        log_message("SUCCESS", "Reply sent successfully")
                    except Exception as send_error:
                        log_message("ERROR", f"Failed to send reply: {type(send_error).__name__}: {send_error}")
                    
                    processed_message_signatures.add(signature)
                    time.sleep(1)  # Small delay between replies
            
            except KeyboardInterrupt:
                log_message("INFO", "Bot stopped by user")
                break
            except Exception as loop_error:
                log_message("ERROR", f"{type(loop_error).__name__}: {loop_error}")
    
    finally:
        driver.quit()
        log_message("INFO", "Chrome driver closed")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    log_message("INFO", "WhatsApp AI Agent Bot Started")
    log_message("INFO", "Press Ctrl+C to stop the bot")
    main_loop()