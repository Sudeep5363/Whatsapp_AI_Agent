"""
agent.py — Standalone command-line interface for testing the AI reply logic.

Run this file directly to interactively test keyword-based responses
without launching the full WhatsApp bot:

    python agent.py

Type any message and the agent will reply based on recognised keywords.
Press Ctrl+C or send EOF (Ctrl+D) to quit.
"""


def reply(message: str) -> str:
    """Return an automated reply based on keywords found in *message*.

    Parameters
    ----------
    message:
        Raw text received from the user.

    Returns
    -------
    str
        A canned response string that matches the first recognised keyword,
        or a generic help message when no keyword matches.
    """
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


# ---------------------------------------------------------------------------
# Interactive test loop – only runs when the script is executed directly.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Agent is running. Type a message to test replies (Ctrl+C to quit).\n")
    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nAgent: Goodbye!")
            break
        print("Agent:", reply(user))