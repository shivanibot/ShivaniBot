import streamlit as st
import requests
import uuid
import os

# 🔐 Paste your keys here (temporary for local testing)
import os

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

st.set_page_config(page_title="Shivani Bot", page_icon="🎙")
st.title("🎙 Shivani Bot")

user_input = st.text_input("Talk to Shivani:")

if user_input:

    # 🔥 Custom overrides
    if "ram kuppuswamy" in user_input.lower():
        reply = """Ram Kuppuswamy — calm, clinical, and running manufacturing like it's a Sunday checklist."""
    elif "bharat" in user_input.lower():
        reply = """Bharat — very caring. Very loving. Also professionally irritating."""
    else:
        personality = """You are Shivani.
Indian. Fast-talking. Slightly savage. Playful.
Use yaar, arre, bro naturally.
Keep responses conversational and energetic.
"""

        gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

        gemini_payload = {
            "contents": [
                {
                    "parts": [
                        {"text": personality + "\nUser: " + user_input}
                    ]
                }
            ]
        }

        gemini_response = requests.post(gemini_url, json=gemini_payload)
        gemini_data = gemini_response.json()

        reply = gemini_data["candidates"][0]["content"]["parts"][0]["text"]

    st.write("Shivani:", reply)

    # 🔊 ElevenLabs TTS
    eleven_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
        "accept": "audio/mpeg"
    }

    eleven_payload = {
        "text": reply,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.2,
            "similarity_boost": 0.9,
            "style": 0.7,
            "use_speaker_boost": True
        }
    }

    audio_response = requests.post(eleven_url, headers=headers, json=eleven_payload)

    if audio_response.status_code == 200:
        filename = f"response_{uuid.uuid4()}.mp3"
        with open(filename, "wb") as f:
            f.write(audio_response.content)

        st.audio(filename)
    else:
        st.error("Audio generation failed.")