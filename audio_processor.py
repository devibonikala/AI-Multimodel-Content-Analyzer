from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

MODEL = "gemini-2.5-flash"


def transcribe_audio(audio_bytes):

    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(
                data=audio_bytes,
                mime_type="audio/mp3"
            ),
            "Transcribe this audio."
        ]
    )

    return response.text