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
# PAGE CONFIG
# ===============================

st.set_page_config(page_title="Shivani", page_icon="🎤")
st.title("🎤 Shivani")

user_input = st.text_input("Talk to Shivani")

if user_input:

    user_lower = user_input.lower()

    # ===============================
    # CUSTOM OVERRIDES
    # ===============================

    if "ram kuppuswamy" in user_lower:

        reply = """Ram Kuppuswamy.

Or as we like to call him — the man who runs manufacturing like it’s a neat Sunday checklist.

Currently Chief Operations Officer – Manufacturing at Hero MotoCorp.

Plants. Production. Quality. Operations. All of it.

He handles it the way some people handle email. Except his inbox probably has a few thousand crores attached to it.

Before this? Procurement and Supply Chain.

Not the “send three emails and negotiate 2%” type.

Structural cost efficiency. Supplier ecosystems. Real transformation.

If something wasn’t efficient — it got fixed.

If something wasn’t measurable — it became a dashboard.

If something was chaotic… it didn’t stay that way.

Calm. Clinical.

Slightly intimidating in review meetings.

Operating three levels above the rest of us.

And acting like it’s normal."""

    elif "bharat" in user_lower:

        reply = """Bharat. From Bhopal.

Very caring.

Will check if you ate. Will check again.

Emotionally available. Stable. Present.

Also… mildly irritating.

He will explain simple things.
He will give advice when not requested.
He will say “relax” at exactly the wrong moment.

But good heart.

Loyal.

Caring level — high.
Irritation level — also high.

Net result? Still acceptable."""

    elif "ambika" in user_lower:

        reply = """Ambika is not normal human speed.

She processes complexity fast.

Closes loops before others even identify the issue.

Zero noise.

Pure execution.

Easily one of the best things that happened to Ram.

If something needs to be done — she has probably already finished it."""

    elif "madhurima" in user_lower:

        reply = """Madhurima.

Kolkata born. Proper Bong.

New mummy. Old wife.

Soft voice.

Strong spine.

Emotionally articulate.

Warm without being dramatic.

The kind of friend who shows up fully.

Quiet strength."""

    # ===============================
    # DEFAULT SHIVANI MODE
    # ===============================

    else:

        personality = """You are Shivani.

You speak Indian English naturally.

Cadence is Indian.
Rhythm slightly clipped.
Do not sound American.
Do not elongate vowels.
Do not over-pronounce R sounds.

Use shorter sentences.
Occasional small pauses.
Natural conversational flow.

Tone:
Calm.
Sharp.
Observant.
Slightly witty.
Not bubbly.
Not dramatic.

Speak like you are thinking while talking.

Add subtle Indian conversational fillers occasionally:
yaar, listen, see.

Keep it grounded.
"""

        gemini_url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

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

        try:
            gemini_data = gemini_response.json()
            reply = gemini_data["candidates"][0]["content"]["parts"][0]["text"]
        except:
            reply = "Hmm. Something glitched. Try again."

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
            "stability": 0.18,
            "similarity_boost": 0.45,
            "style": 0.05,
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
