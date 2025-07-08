from twilio_sender.rest import Client
from dotenv import load_dotenv
from rag_ques import llama_generate_response  # Your Groq wrapper
import os

load_dotenv()

# Twilio credentials
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_phone_number = os.getenv("TWILIO_PHONE_NUMBER")

twilioClient = Client(twilio_account_sid, twilio_auth_token)

def notify_influencer_with_ai(phone_number, raw_text):
    # Generate polished message using Groq/LLaMA
    refined_message = llama_generate_response(raw_text)

    # Send SMS via Twilio
    twilioClient.messages.create(
        body=refined_message,
        from_=twilio_phone_number,
        to=phone_number
    )

    return refined_message  # Optional: return the final message
