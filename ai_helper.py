from groq import Groq
from dotenv import load_dotenv
import os

# Explicitly search for your project .env config file
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)

api_key_value = os.getenv("GROQ_API_KEY")

if not api_key_value:
    raise ValueError("⚠️ Cannot find GROQ_API_KEY inside your .env configuration container.")

client = Groq(api_key=api_key_value)

# High-speed model declarations mapping
TEXT_MODEL = "llama-3.1-8b-instant"
AUDIO_MODEL = "whisper-large-v3"

def ask_groq_cloud(prompt):
    """Sends text structures directly to Llama 3 on Groq LPUs"""
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a professional multimedia data parsing analyzer."},
                {"role": "user", "content": prompt}
            ],
            model=TEXT_MODEL,
            temperature=0.2,
        )
        return chat_completion.choices.message.content
    except Exception as e:
        return f"⚠️ Groq Text Engine Error: {str(e)}"

def transcribe_audio_via_groq(file_path):
    """Uploads any raw local audio file to Groq's cloud supercomputer for instant transcription"""
    try:
        with open(file_path, "rb") as audio_file:
            transcription = client.audio.transcriptions.create(
                file=audio_file,
                model=AUDIO_MODEL,
                response_format="text"
            )
        return transcription
    except Exception as e:
        return f"⚠️ Groq Whisper Cloud Error: {str(e)}"
