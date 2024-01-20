import os
from twilio.rest import Client
from flask import render_template, request
from twilio.twiml.voice_response import VoiceResponse
from dotenv import load_dotenv
load_dotenv()

# Your Twilio account SID and auth token
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")

# OpenAI API key

# Create a new Twilio client object
client = Client(account_sid, auth_token)


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code



def make_call(phone_number, greeting):
    # Make a call to the phone number with Gather speech
    call = client.calls.create(
        twiml=f"<Response><Gather language=\"en-US\" input=\"speech\" action=\"{request.url_root+'gather'}\" method=\"GET\"><Say language=\"en-US\" voice=\"Google.en-US-Neural2-C\">{greeting}</Say></Gather></Response>",
        to="+917760735073",
        from_="+12393448454"
    )
    # Return the call sid
    return call.sid


def update_call(call_sid, text):
    # Update the call with Gather speech
    call = client.calls(call_sid).update(
        twiml=f"<Response><Gather language=\"en-US\" input=\"speech\" action=\"{request.url_root+'gather'}\" method=\"GET\"><Say language=\"en-US\" voice=\"Google.en-US-Neural2-C\">{text}</Say></Gather></Response>"
    )
    # Return the call sid
    return call.sid

def end_call(call_sid):
    # End the call
    response = VoiceResponse()
    response.say("Thank you for your time. Goodbye!", language="en-US", voice="Google.en-US-Neural2-C")
    call = client.calls(call_sid).update(
        twiml=response
    )
    # Return the call sid
    return call.sid