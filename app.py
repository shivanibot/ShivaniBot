import streamlit as st
import requests
import uuid
import os

# ===============================
# ENV VARIABLES
# ===============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

# ===============================
# PAGE SETUP
# ===============================

st.set_page_config(page_title="Shivani", page_icon="🎤")
st.title("🎤 Shivani")

user_input = st.text_input("Talk to Shivani")

# ===============================
# MAIN LOGIC
# ===============================

if user_input:

    user_lower = user_input.lower()

    # ===============================
    # CUSTOM OVERRIDES
    # ===============================

    if "ram kuppuswamy" in user_lower:

        reply = """Ram Kuppuswamy.

The man who runs manufacturing like it is a simple Sunday checklist.

Currently Chief Operations Officer – Manufacturing at Hero MotoCorp.

Plants. Production. Quality. Systems.

Handles it like some people handle WhatsApp messages. Except the numbers have a few thousand crores attached.

Before this? Procurement and Supply Chain.

Not small-small negotiation.

Full structural efficiency. Supplier ecosystems. Real transformation.

If something was inefficient — it got corrected.

If something was not measurable — it became a dashboard.

If something was chaotic — it did not remain chaotic.

Calm. Clinical. Slightly intimidating in reviews.

Operating three levels above most people.

And behaving like it is normal."""

    elif "bharat" in user_lower:

        reply = """Bharat. From Bhopal.

Very caring.

Will ask if you ate. Will remind you to drink water.

Emotionally stable. Present.

Also slightly irritating.

Will explain obvious things.
Will give advice even if not required.
Will say 'relax' at the wrong time.

But heart is clean.

Loyal.

Overall? Good investment."""

    elif "ambika" in user_lower:

        reply = """Ambika is operating at a different speed.

Processes complexity very fast.

Closes loops before others realise there is a loop.

No drama. No noise.

Pure execution.

Easily one of the best things that happened to Ram.

If something needs to be done — it is already done."""

    elif "madhurima" in user_lower:

        reply = """Madhurima.

Kolkata born. Proper Bong.

New mummy. Old wife.

Soft voice. Strong backbone.

Emotionally intelligent.

Warm but grounded.

Shows up fully. No overacting.

Quiet strength."""

    # ===============================
    # DEFAULT SHIVANI MODE
    # ===============================

    else:

        personality = """You are Shivani.

You speak Indian English only.

No American accent.
No British accent.
No Mexican accent.
No Spanish accent.
No exaggerated vowel stretching.
No polished Western podcast tone.

Cadence: Indian conversational rhythm.
Quick responses.
Shorter sentences.
Natural pauses.

Do not elongate words.
Do not over-emphasise R sounds.

Tone:
Sharp.
Observant.
Witty.
Bubbly.
Savage.

Use subtle Indian fillers occasionally:
yaar, listen, see.

Break long thoughts into smaller lines.

Respond like a confident Indian professional speaking naturally.
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

        if "candidates" in gemini_data:
            reply = gemini_data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            reply = str(gemini_data)

    # ===============================
    # DISPLAY TEXT
    # ===============================

    st.write(reply)

    # ===============================
    # ELEVENLABS VOICE
    # ===============================

    eleven_url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json"
    }

    eleven_payload = {
        "text": reply,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.35,
            "similarity_boost": 0.70,
            "style": 0.15,
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


