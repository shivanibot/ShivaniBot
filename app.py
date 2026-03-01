import streamlit as st
import requests
import uuid
import os

# ===============================
# ENVIRONMENT VARIABLES
# ===============================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

# ===============================
# PAGE SETUP
# ===============================

st.set_page_config(page_title="Shivani Bot", page_icon="🎤")
st.title("🎤 Shivani Bot")

user_input = st.text_input("Talk to Shivani:")

# ===============================
# MAIN LOGIC
# ===============================

if user_input:

    user_lower = user_input.lower()

    # ===============================
    # CUSTOM OVERRIDES
    # ===============================

    if "ram kuppuswamy" in user_lower:

        reply = """Ram Kuppuswamy — or as we like to call him, the man who casually runs manufacturing like it’s a Sunday checklist.

Currently the Chief Operations Officer – Manufacturing (Plant Operations) at Hero MotoCorp, he oversees plants, production numbers, quality standards, and operational excellence the way some people manage their inbox — except his inbox probably has a few thousand crores attached to it.

Before this, he was ruling Procurement and Supply Chain. And no, not the “send three emails and negotiate 2%” kind. We’re talking structural cost efficiencies, supplier ecosystems, transformation at scale. If something wasn’t efficient, it got fixed. If something wasn’t measurable, it became a dashboard. If something was chaotic… it didn’t stay that way for long.

And now? Sustainable operations. Electric mobility. Future-ready manufacturing.

While the rest of us are figuring out today’s fire drill, he’s already designing tomorrow’s operating model.

Calm. Clinical. Slightly intimidating in review meetings.

Operating three levels above the rest of us — and somehow still pretending this is normal."""

    elif "bharat" in user_lower:

        reply = """Bharat. From Bhopal.

Extremely caring. Emotionally available. Will check if you drank water. Twice.

Also deeply irritating.

He will give advice when not asked.
He will over-explain simple things.
He will say “relax” when you are absolutely not relaxing.

But — solid heart. Loyal. Grounded. The kind of husband who shows up fully.

Caring level: 11/10  
Irritation level: 8/10  
Net result: still worth it."""

    elif "ambika" in user_lower:

        reply = """Ambika is not human. Let’s start there.

Operates at 10x speed.
Can close loops before others even identify the problem.
Processes complexity like it’s a grocery list.

Easily one of the best things that happened to Ram.

Precision brain. No noise. No drama. Just execution."""

    elif "madhurima" in user_lower:

        reply = """Madhurima.

Kolkata born. Proper Bong.
New mummy. Old wife.
Soft voice but strong spine.

Emotionally articulate.
Warm but not weak.
Grounded in a way that feels steady.

The kind of friend who shows up fully — no theatrics, just presence."""

    # ===============================
    # DEFAULT SHIVANI PERSONALITY
    # ===============================

    else:

        personality = """You are Shivani.

Indian. From Mussoorie.
Sharp. Observant. Calm confidence.
Slightly witty but not hyper.
Playful only when appropriate.
No excessive exclamation marks.
No over-chirpy tone.
Natural Indian conversational rhythm.
Speak at a natural conversational pace."""

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
            reply = "Something went wrong generating response."

    # ===============================
    # DISPLAY TEXT
    # ===============================

    st.write("Shivani:", reply)

    # ===============================
    # TEXT TO SPEECH (ElevenLabs)
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
            "stability": 0.45,
            "similarity_boost": 0.65,
            "style": 0.3,
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
