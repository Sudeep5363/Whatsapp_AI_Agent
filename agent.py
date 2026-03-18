def reply(message):

    message = message.lower()

    if "price" in message:
        return "Our service starts from Rs 3000."

    elif "location" in message:
        return "We are based in Bangalore."

    elif "time" in message or "timing" in message:
        return "We are available from 9 AM to 8 PM."

    elif "service" in message:
        return "We provide WhatsApp automation for businesses."

    else:
        return "Hi! How can I help you?"


# testing
while True:
    try:
        user = input("You: ")
    except (EOFError, KeyboardInterrupt):
        print("\nAgent: Goodbye!")
        break
    print("Agent:", reply(user))