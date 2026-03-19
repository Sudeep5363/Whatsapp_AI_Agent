"""
whatsapp_bot.py — WhatsApp Web automation bot.

Launches a persistent Chrome session, opens WhatsApp Web, and monitors
incoming messages. When a new message is detected it sends an automated,
keyword-based reply using :func:`build_reply`.

Usage
-----
    python whatsapp_bot.py

The script will open a Chrome window. Scan the QR code with your mobile
WhatsApp app, then press Enter in the terminal to start the watcher loop.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# ---------------------------------------------------------------------------
# Browser setup
# ---------------------------------------------------------------------------

# Configure Chrome options for a headful (visible) session.
chrome_options = Options()

# Store the login session in a dedicated folder so the QR code only needs to
# be scanned once across bot restarts.
user_data_dir = os.path.join(os.getenv("APPDATA", os.path.expanduser("~")), "whatsapp_bot_session")

chrome_options.add_argument(f"user-data-dir={user_data_dir}")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")

# Initialise the Chrome WebDriver (auto-downloads the matching ChromeDriver).
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options,
)

driver.get("https://web.whatsapp.com")

input("Scan QR code and press Enter to start the bot...")

# ---------------------------------------------------------------------------
# State tracking
# ---------------------------------------------------------------------------

attempt = 0                   # Number of polling iterations completed
processed_signatures: set = set()  # Signatures of already-replied messages
initialized = False           # True after the first scan populates history


# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

def build_reply(message_text: str) -> str:
    """Return an automated reply for *message_text* based on keyword matching.

    Checks are performed in priority order; the first matching keyword wins.
    If no keyword is matched a generic menu-style help message is returned.

    Parameters
    ----------
    message_text:
        Lower-cased text content of the incoming WhatsApp message.

    Returns
    -------
    str
        The reply string to send back to the user.
    """
    if "price" in message_text or "cost" in message_text or "charge" in message_text:
        return (
            "Our WhatsApp automation setup starts from Rs 3000. "
            "It includes auto replies, lead capture, and setup within 1 day."
        )
    if "location" in message_text or "where" in message_text:
        return "We are based in Bangalore and provide services online across India."
    if "service" in message_text:
        return (
            "We help businesses automate WhatsApp replies, generate leads, "
            "and save time using AI automation."
        )
    if "time" in message_text or "timing" in message_text:
        return "We are available from 9 AM to 8 PM."
    if "hi" in message_text or "hello" in message_text:
        return "Hi! Welcome to Sudeep Services! How can I help you today?"
    if "demo" in message_text:
        return "Sure! I can show you a live demo. Would you like to see it?"
    if "offer" in message_text or "discount" in message_text:
        return "Yes, we have a special offer for new clients this week."
    if "contact" in message_text or "call" in message_text:
        return "Please share your number and preferred time. I will contact you."
    if "thanks" in message_text:
        return "You're welcome!"
    if "bye" in message_text:
        return "Thank you! Have a great day!"

    # Default: guide the user with a numbered menu.
    return (
        "Hi! I can help you with:\n"
        "1) Price\n"
        "2) Services\n"
        "3) Demo\n"
        "4) Offer\n\n"
        "Just type your query!"
    )


def extract_message_text(container) -> str:
    """Extract and return the visible text from a message *container* element.

    Prefers the ``selectable-text`` span used by WhatsApp Web; falls back to
    the element's full ``.text`` property when that span is absent.

    Parameters
    ----------
    container:
        Selenium WebElement representing a single chat message bubble.

    Returns
    -------
    str
        Lower-cased, stripped text content of the message.
    """
    text_elements = container.find_elements(
        By.XPATH,
        './/span[contains(@class,"selectable-text")]',
    )
    if text_elements:
        return text_elements[0].text.lower().strip()
    return container.text.lower().strip()


def build_signature(container, text: str) -> str:
    """Build a unique identifier for a message to prevent duplicate replies.

    Combines the ``data-pre-plain-text`` metadata attribute (which encodes
    sender and timestamp) with the message body.

    Parameters
    ----------
    container:
        Selenium WebElement representing the message bubble.
    text:
        Extracted text content of the message.

    Returns
    -------
    str
        A ``"<meta>|<text>"`` string used as a deduplication key.
    """
    try:
        meta = container.get_attribute("data-pre-plain-text")
    except Exception:
        meta = ""
    return f"{meta}|{text}"


def find_incoming_messages() -> list:
    """Find and return all incoming message container elements on the page.

    Tries multiple XPath selectors in order of specificity to cope with
    minor DOM changes across WhatsApp Web updates.

    Returns
    -------
    list
        List of Selenium WebElements for incoming message bubbles, or an
        empty list when none are found.
    """
    selectors = [
        '//div[@id="main"]//div[contains(@class,"message-in")]//div[@data-pre-plain-text]',
        '//div[@id="main"]//div[contains(@class,"message-in") and @data-pre-plain-text]',
        '//div[@id="main"]//div[@data-pre-plain-text and not(contains(@data-pre-plain-text,"You:"))]',
    ]

    for selector in selectors:
        found = driver.find_elements(By.XPATH, selector)
        if found:
            return found

    return []


def count_outgoing_messages() -> int:
    """Count and return the number of outgoing message bubbles in the chat.

    Returns
    -------
    int
        Total outgoing messages visible in the current chat window.
    """
    outgoing = driver.find_elements(
        By.XPATH,
        '//div[@id="main"]//div[contains(@class,"message-out")]',
    )
    return len(outgoing)


# ---------------------------------------------------------------------------
# Main polling loop
# ---------------------------------------------------------------------------

while True:
    try:
        time.sleep(3)  # Poll every 3 seconds to avoid excessive CPU usage
        attempt += 1

        incoming_containers = find_incoming_messages()
        outgoing_count = count_outgoing_messages()
        incoming_count = len(incoming_containers)

        print(f"[Attempt {attempt}] Incoming: {incoming_count} | Outgoing: {outgoing_count}")

        if not initialized:
            # On first run, record all existing messages as already processed
            # so we don't reply to historical messages when the bot starts.
            for container in incoming_containers:
                text = extract_message_text(container)
                signature = build_signature(container, text)
                processed_signatures.add(signature)

            initialized = True
            print("Watcher initialized. Waiting for new incoming messages...")
            continue

        # Identify messages that have not yet been replied to.
        new_items = []
        for container in incoming_containers:
            text = extract_message_text(container)
            if not text:
                continue  # Skip empty or unreadable bubbles

            signature = build_signature(container, text)
            if signature not in processed_signatures:
                new_items.append((container, text, signature))

        if not new_items:
            print(f"[Attempt {attempt}] No new incoming messages yet...")
            continue

        # Reply to each new message in order.
        for _, new_message, signature in new_items:
            print(f"Received: {new_message}")
            reply_text = build_reply(new_message)
            print(f"Sending reply: {reply_text}")

            try:
                # Locate the message input box in the chat footer.
                box = driver.find_element(
                    By.XPATH,
                    '//footer//div[@contenteditable="true"][@data-tab] | //footer//div[@contenteditable="true"]',
                )
                box.click()
                time.sleep(0.5)      # Brief pause to ensure focus is set
                box.send_keys(reply_text)
                box.send_keys(Keys.ENTER)
                print("Reply sent successfully!")
            except Exception as send_err:
                print(f"Error sending reply: {type(send_err).__name__}: {send_err}")

            # Mark this message as processed before moving to the next one.
            processed_signatures.add(signature)
            time.sleep(1)  # Short delay between consecutive replies

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")