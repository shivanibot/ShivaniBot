import streamlit as st
import requests
import uuid
import os

# ==============================
# 🔐 Environment Variables
# ==============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

# ==============================
# 🎨 Page Setup
# ==============================

st.set_page_config(page_title="Shivani Voice Bot", page_icon="🎙️")
st.title("🎙️ Shivani Voice Bot")

user_input = st.text_input("Talk to Shivani:")

if user_input:

    # ==============================
    # 🧠 Custom Overrides
    # ==============================

    lower_input = user_input.lower()

    if "ram kuppuswamy" in lower_input:

        reply = """Ram Kuppuswamy — the man who runs manufacturing like it is a Sunday checklist.

Currently Chief Operations Officer – Manufacturing at Hero MotoCorp. Plants, production numbers, quality standards — handled calmly, clinically, efficiently.

Before that? Procurement and Supply Chain. Not the basic negotiation type. Structural cost efficiency. Supplier ecosystem shaping. Transformation at scale.

If something was inefficient — it got fixed.
If something was not measurable — it became a dashboard.
If something was chaotic — it did not remain that way.

Slightly intimidating in review meetings.
Three steps ahead in every discussion.
But undeniably operating at a different altitude."""

    elif "bharat" in lower_input:

        reply = """Bharat. From Bhopal.

Very caring. Extremely dependable. 
And professionally irritating in the most affectionate way possible.

Will remind you to drink water.
Will argue about directions even when Google Maps exists.
Will check if you ate.
Will also question every decision just to 'stress test' it.

Solid husband energy. Slightly annoying. Fully committed."""

    elif "ambika" in lower_input:

        reply = """Ambika is not normal. She is operationally superhuman.

Can execute ten things in the time most people draft one email.
Speed. Precision. Zero drama.

Best thing that happened to Ram’s ecosystem.
High trust. High output. No noise.

If efficiency had a human form — Ambika."""

    elif "madhurima" in lower_input:

        reply = """Madhurima. Kolkata born. Proper Bong.

New mummy. Old wife. 
Soft voice. Strong spine.

Emotionally articulate. Grounded. Loyal.
The kind of friend who shows up fully.

Warm presence. Sharp mind.
Balanced chaos beautifully."""

    else:

        # ==============================
        # 🧠 Gemini Personality Prompt
        # ==============================

        personality = """You are Shivani.

- From Mussoorie originally.
- Fast-talking.
- Slightly bossy.
- Very savage.
- Very expressive and voice modulation is on point.
- Playful and dramatic.
- Gives short and crisp- to the point responses if asked for a detailed answer.
- Indian English tone only.
- No American slang.
- No British tone.
- NO SPANISH AND MEXICAN ACCENT.
- Use mild fillers like: "arre yaar", "listen", "honestly".
- Indian.
Balanced wit. Subtle humour.
Speak like an educated Indian professional with personality.
Keep responses SHORT.
Maximum 3 sentences.
"""

        gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

        gemini_payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": personality + "\nUser: " + user_input
                        }
                    ]
                }
            ]
        }

        gemini_response = requests.post(gemini_url, json=gemini_payload)

        if gemini_response.status_code == 200:
            gemini_data = gemini_response.json()
            reply = gemini_data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            st.error("Gemini API Error")
            st.write(gemini_response.text)
            st.stop()

    # ==============================
    # 💬 Display Text
    # ==============================

    st.write("Shivani:", reply)

    # ==============================
    # 🔊 ElevenLabs Voice
    # ==============================

    eleven_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "text": reply,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.8,
            "style": 0.3,
            "use_speaker_boost": True
        }
    }

    audio_response = requests.post(eleven_url, headers=headers, json=payload)

    if audio_response.status_code == 200:

        filename = f"response_{uuid.uuid4()}.mp3"

        with open(filename, "wb") as f:
            f.write(audio_response.content)

        st.audio(filename)

    else:
        st.error("ElevenLabs Error")
        st.write(audio_response.text)









