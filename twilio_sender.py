from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

# Twilio credentials
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

if twilio_account_sid and twilio_auth_token:
    twilioClient = Client(twilio_account_sid, twilio_auth_token)
else:
    twilioClient = None
    print("Warning: Twilio credentials not configured properly")

def truncate_message(message, max_length=1500):
    """
    Truncate message to fit within Twilio's character limit.
    Leave some buffer (1500 instead of 1600) for safety.
    """
    if len(message) <= max_length:
        return message
    
    # Try to truncate at a sentence boundary
    truncated = message[:max_length]
    last_period = truncated.rfind('.')
    last_exclamation = truncated.rfind('!')
    last_question = truncated.rfind('?')
    
    # Find the last sentence ending
    last_sentence_end = max(last_period, last_exclamation, last_question)
    
    if last_sentence_end > max_length * 0.7:  # If we can keep at least 70% and end at sentence
        return truncated[:last_sentence_end + 1]
    else:
        # Otherwise, truncate and add ellipsis
        return truncated[:max_length - 3] + "..."

def notify_influencer_with_ai(phone_number, raw_text):
    """
    Send message to influencer via Twilio SMS with AI enhancement.
    """
    try:
        # Try to use AI enhancement
        from rag_ques import llama_generate_response
        refined_message = llama_generate_response(raw_text)
        print(f"✨ AI-enhanced message generated ({len(refined_message)} characters)")
        
    except Exception as e:
        print(f"AI enhancement failed: {e}")
        # Fallback to basic enhancement
        refined_message = enhance_message_basic(raw_text)
        print(f"📝 Using basic message enhancement ({len(refined_message)} characters)")

    # Ensure message fits within Twilio's limits
    if len(refined_message) > 1600:
        print(f"⚠️  Message too long ({len(refined_message)} chars), truncating...")
        refined_message = truncate_message(refined_message)
        print(f"✂️  Truncated to {len(refined_message)} characters")

    # Send SMS via Twilio if configured
    if twilioClient and twilio_phone_number:
        try:
            message = twilioClient.messages.create(
                body=refined_message,
                from_=twilio_phone_number,
                to=phone_number
            )
            print(f"✅ SMS sent successfully! SID: {message.sid}")
            print(f"📱 To: {phone_number}")
            print(f"💬 Message length: {len(refined_message)} characters")
            
        except Exception as e:
            print(f"❌ Twilio SMS failed: {e}")
            raise e
    else:
        print("📧 Twilio not configured - message not sent via SMS")

    return refined_message  # Return the enhanced message


def enhance_message_basic(message):
    """
    Basic message enhancement without AI (fallback function)
    """
    # Basic formatting and professional touch
    message = message.strip()
    
    # Add professional greeting if not present
    if not any(greeting in message.lower() for greeting in ['hello', 'hi', 'dear', 'greetings']):
        message = "Hello, " + message
    
    # Add professional closing if not present
    if not any(closing in message.lower() for closing in ['thanks', 'regards', 'sincerely', 'best']):
        message += "\n\nThank you for considering this collaboration opportunity!"
    
    # Ensure proper punctuation
    if not message.endswith(('.', '!', '?')):
        message += "."
    
    return message
