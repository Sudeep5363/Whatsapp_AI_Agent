"""
WhatsApp Bot Agent Module

This module provides utility functions for conversation management and reply generation.
It serves as a helper module for the main whatsapp_bot.py script.

Author: Sudeep
License: MIT
"""


def reply(message: str) -> str:
    """
    Generate a contextual reply based on message keywords.
    
    This is a simplified version of the reply generation logic.
    Use this for testing or as a reference implementation.
    
    Args:
        message (str): The input message text
        
    Returns:
        str: Generated reply message
        
    Example:
        >>> reply("What is your price?")
        "Our service starts from Rs 3000."
    """
    message = message.lower().strip()
    
    # Price inquiries
    if "price" in message or "cost" in message:
        return "💰 Our service starts from Rs 3,000."
    
    # Location inquiries
    elif "location" in message or "where" in message:
        return "📍 We are based in Bangalore."
    
    # Availability inquiries
    elif "time" in message or "timing" in message:
        return "⏰ We are available from 9 AM to 8 PM."
    
    # Service inquiries
    elif "service" in message:
        return "🤖 We provide WhatsApp automation for businesses."
    
    # Default response
    else:
        return "👋 Hi! How can I help you?"


# ============================================================================
# TESTING/DEMO
# ============================================================================

def test_agent():
    """
    Simple test function to demonstrate the agent's reply capabilities.
    
    Run this to test the bot offline without needing WhatsApp Web.
    """
    print("WhatsApp AI Agent - Test Mode")
    print("=" * 50)
    print("Type your message (or 'quit' to exit):\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ["quit", "exit", "bye"]:
                print("Agent: Goodbye! Have a great day!")
                break
            
            if not user_input:
                continue
            
            agent_reply = reply(user_input)
            print(f"Agent: {agent_reply}\n")
        
        except KeyboardInterrupt:
            print("\n\nAgent: Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}\n")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    test_agent()