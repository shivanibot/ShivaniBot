import streamlit as st
import os
import requests
import uuid
from pydub import AudioSegment
from dotenv import load_dotenv

load_dotenv()

st.title("🎙 Shivani Voice Bot")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

# =========================
# Personality Prompt
# =========================

PERSONALITY = """
You are Shivani.

- From Mussoorie originally.
- Fast-talking.
- Slightly bossy.
- Very savage.
- Very expressive and voice modulation is on point.
- Playful and dramatic.
- Indian English tone only.
- No American slang.
- No British tone.
- Use mild fillers like: "arre yaar", "listen", "honestly".
- Keep Indian rhythm.

If asked about Ram Kuppuswamy:
Give a detailed, sassy but respectful description:
Ram Kuppuswamy - or as we call him, the man who runs manufacturing like a Sunday checklist.
Currently COO - Manufacturing at Hero MotoCorp.
Previously ruled Procurement and Supply Chain.
Structural cost efficiencies, dashboards everywhere, chaos doesn’t survive around him.
Calm. Clinical. Slightly intimidating in reviews.
Operating three levels above everyone else.

If asked about Bharat:
Bharat - husband from Bhopal.
Very caring.
Very grounding.
Also slightly irritating in the cutest way.
Balances Shivani’s chaos perfectly.

If asked about Ambika:
Ambika is a superhuman.
Can do everything in a blink.
Extremely efficient.
Best thing that happened to Ram’s ecosystem.
Silent force multiplier.

If asked about Madhurima:
Madhurima - proper Kolkata Bong.
New mummy.
Old wife.
Amazing friend.
Warm but sharp.
Emotionally intelligent with solid sarcasm.
"""

# =========================
# User Input
# =========================

user_input = st.text_input("Talk to Shivani:")

if user_input:

    full_prompt = PERSONALITY + "\nUser: " + user_input

    # =========================
    # GEMINI TEXT GENERATION
    # =========================

    gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={GEMINI_API_KEY}"

    gemini_payload = {
        "contents": [
            {
                "parts": [
                    {"text": full_prompt}
                ]
            }
        ]
    }

    gemini_response = requests.post(gemini_url, json=gemini_payload)
    gemini_data = gemini_response.json()

    try:
        reply = gemini_data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        st.error("Gemini Error")
        st.write(gemini_data)
        st.stop()

    st.write("Shivani:", reply)

    # =========================
    # ELEVENLABS TTS
    # =========================

    eleven_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": reply,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.30,
            "similarity_boost": 0.75,
            "style": 0.20,
            "use_speaker_boost": True
        }
    }

    audio_response = requests.post(eleven_url, headers=headers, json=payload)
if audio_response.status_code == 200:
    filename = f"response_{uuid.uuid4()}.mp3"

    with open(filename, "wb") as f:
        f.write(audio_response.content)

    audio_html = f"""
    <audio controls autoplay>
        <source src="{filename}" type="audio/mp3">
    </audio>

    <script>
        const audio = document.querySelector('audio');
        if (audio) {{
            audio.playbackRate = 1.5;
        }}
    </script>
    """

    st.markdown(audio_html, unsafe_allow_html=True)

else:
    st.error("ElevenLabs Error")
    st.write(audio_response.text)


