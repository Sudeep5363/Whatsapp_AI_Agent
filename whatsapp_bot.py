from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

# Setup Chrome options
chrome_options = Options()

# Persistent session folder
user_data_dir = os.path.join(os.getenv('APPDATA'), 'whatsapp_bot_session')

chrome_options.add_argument(f"user-data-dir={user_data_dir}")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--remote-debugging-port=9222")

# Start driver (ONLY ONCE ✅)
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=chrome_options
)

driver.get("https://web.whatsapp.com")

input("Scan QR code and press Enter...")

attempt = 0
processed_signatures = set()
initialized = False


def build_reply(message_text: str) -> str:
    if "price" in message_text or "cost" in message_text or "charge" in message_text:
        return "Our WhatsApp automation setup starts from Rs 3000. It includes auto replies, lead capture, and setup within 1 day."
    if "location" in message_text or "where" in message_text:
        return "We are based in Bangalore and provide services online across India."
    if "service" in message_text:
        return "We help businesses automate WhatsApp replies, generate leads, and save time using AI automation."
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

    return (
        "Hi! I can help you with:\n"
        "1) Price\n"
        "2) Services\n"
        "3) Demo\n"
        "4) Offer\n\n"
        "Just type your query!"
    )


def extract_message_text(container):
    text_elements = container.find_elements(
        By.XPATH,
        './/span[contains(@class,"selectable-text")]'
    )
    if text_elements:
        return text_elements[0].text.lower().strip()
    return container.text.lower().strip()


def build_signature(container, text):
    try:
        meta = container.get_attribute("data-pre-plain-text")
    except Exception:
        meta = ""
    return f"{meta}|{text}"


def find_incoming_messages():
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


def count_outgoing_messages():
    outgoing = driver.find_elements(
        By.XPATH,
        '//div[@id="main"]//div[contains(@class,"message-out")]'
    )
    return len(outgoing)


while True:
    try:
        time.sleep(3)
        attempt += 1

        incoming_containers = find_incoming_messages()
        outgoing_count = count_outgoing_messages()
        incoming_count = len(incoming_containers)

        print(
            f"[Attempt {attempt}] Incoming: {incoming_count} | Outgoing: {outgoing_count}"
        )

        if not initialized:
            for container in incoming_containers:
                text = extract_message_text(container)
                signature = build_signature(container, text)
                processed_signatures.add(signature)

            initialized = True
            print("Watcher initialized. Waiting for new incoming messages...")
            continue

        new_items = []
        for container in incoming_containers:
            text = extract_message_text(container)
            if not text:
                continue

            signature = build_signature(container, text)
            if signature not in processed_signatures:
                new_items.append((container, text, signature))

        if not new_items:
            print(f"[Attempt {attempt}] No new incoming messages yet...")
            continue

        for _, new_message, signature in new_items:
            print(f"Received: {new_message}")
            reply = build_reply(new_message)
            print(f"Sending reply: {reply}")

            try:
                box = driver.find_element(
                    By.XPATH,
                    '//footer//div[@contenteditable="true"][@data-tab] | //footer//div[@contenteditable="true"]'
                )
                box.click()
                time.sleep(0.5)
                box.send_keys(reply)
                box.send_keys(Keys.ENTER)
                print("Reply sent successfully!")
            except Exception as send_err:
                print(f"Error sending reply: {type(send_err).__name__}: {send_err}")

            processed_signatures.add(signature)
            time.sleep(1)

    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")