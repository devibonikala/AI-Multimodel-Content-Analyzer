import streamlit as st
import tempfile
import os
import base64
from PyPDF2 import PdfReader
from groq import Groq
from dotenv import load_dotenv

# ==============================================================================
# 1. PAGE CONFIGURATION SETUP
# ==============================================================================
st.set_page_config(
    page_title="🎯 AI Multimodel Content Analyzer",
    layout="wide"
)

# ==============================================================================
# 2. ENTERPRISE SAAS DESIGN SYSTEM (CUSTOM CSS)
# ==============================================================================
st.markdown("""
    <style>
    .stApp {
        background-color: #FAFAFA;
    }
    .section-title {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        color: #0F172A;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        margin-bottom: 12px !important;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .metric-badge {
        display: inline-block;
        background: #F1F5F9;
        color: #475569;
        font-size: 0.75rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        border: 1px solid #E2E8F0;
        margin-bottom: 16px;
    }
    .stAlert {
        border-radius: 10px !important;
        border: 1px solid rgba(0,0,0,0.05) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. GLOBAL STREAMLIT SESSION STATE INITIALIZATION
# ==============================================================================
if "shared_context_tokens" not in st.session_state:
    st.session_state.shared_context_tokens = ""

if "studio_chat_history" not in st.session_state:
    st.session_state.studio_chat_history = []

# ==============================================================================
# 4. ENVIRONMENT ENVIRONMENT INFRASTRUCTURE
# ==============================================================================
project_root = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path=dotenv_path)

api_key_value = os.getenv("GROQ_API_KEY")

if not api_key_value:
    st.error("⚠️ System Configuration Error: GROQ_API_KEY not found in your hidden .env file path configuration.")
    st.stop()

client = Groq(api_key=api_key_value)

# Core Model Endpoints
TEXT_MODEL = "qwen/qwen3.6-27b"
WHISPER_MODEL = "whisper-large-v3-turbo"
VISION_MODEL = "qwen/qwen3.6-27b"

# ==============================================================================
# 5. CORE INFERENCE FUNCTIONS
# ==============================================================================
def ask_groq_llm(prompt, system_instruction="You are a professional multi-format digital asset analysis system."):
    """Sends compiled textual asset contexts to Groq LPUs for instant results."""
    try:
        safe_prompt = prompt if len(prompt) < 15000 else prompt[:15000] + "\n[Text truncated due to size limits...]"
        
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": safe_prompt}
            ],
            model=TEXT_MODEL,
            temperature=0.4
        )
        
        raw_content = chat_completion.choices[0].message.content
        
        # --- CHATGPT-LIKE FILTER: REMOVE THINKING TAGS ---
        if "<think>" in raw_content and "</think>" in raw_content:
            # Splits the text at the closing tag and takes everything after it
            clean_content = raw_content.split("</think>")[-1].strip()
            return clean_content
        elif "<think>" in raw_content:
            # Backup safety if the model forgets to close the tag
            clean_content = raw_content.split("<think>")[0].strip()
            return clean_content
            
        return raw_content
        
    except Exception as e:
        return f"⚠️ Cloud AI Error: Failed to evaluate text components. Details: {str(e)}"


def transcribe_audio_cloud(audio_file_path):
    """Processes audio binaries directly using Groq's high-speed Whisper cloud instance."""
    try:
        with open(audio_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=file,
                model=WHISPER_MODEL,
                response_format="text"
            )
        return transcription
    except Exception as e:
        return f"⚠️ Cloud Audio Error: Transcription pipeline disconnected. Details: {str(e)}"

def process_image_vision_cloud(image_bytes, mime_type):
    """Encodes images to base64 strings and uses active models to read text natively."""
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        response = client.chat.completions.create(
            model=VISION_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Extract and transcribe all readable text from this image exactly as it appears. If there is a diagram, describe it briefly."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Cloud Vision Error: Image OCR pipeline failed. Details: {str(e)}"

# ==============================================================================
# 6. GLOBAL LAYOUT FRAMEWORK
# ==============================================================================
st.title("🎯 AI Multimodel Content Analyzer")
st.caption("⚡ Enterprise Hybrid Architecture: Sub-Second Content Extractions powered by Groq Cloud LPUs")

ui_left, ui_right = st.columns(2, gap="large")

# ==============================================================================
# 7. UI LEFT: ACCESSIBLE & CLEAN UPLOAD CENTER
# ==============================================================================
with ui_left:
    st.subheader("📤 Document & Media Upload Center")
    st.caption("Select your media asset type below to extract its text matrix.")

    tab_pdf, tab_img, tab_audio = st.tabs(["📄 PDF Documents", "🖼️ Graphic Images", "🎵 Voice Audio"])

    # --- PDF PIPELINE ---
    with tab_pdf:
        st.markdown("#### Parse Document Assets")
        uploaded_pdf = st.file_uploader("Drop your PDF here:", type=["pdf"], key="pdf_uploader_unique")
        if uploaded_pdf:
            with st.spinner("Extracting PDF token matrices..."):
                extracted_pdf_text = ""
                pdf_reader = PdfReader(uploaded_pdf)
                for page in pdf_reader.pages:
                    page_string = page.extract_text()
                    if page_string:
                        extracted_pdf_text += page_string + "\n"
                
                if extracted_pdf_text:
                    st.session_state.shared_context_tokens += f"\n[PDF Content Source Data]:\n{extracted_pdf_text}\n"
                    st.toast("✅ PDF parsed successfully!", icon="📄")
                    
                    with st.expander("🔍 Preview Extracted PDF Content Data", expanded=True):
                        st.text_area("PDF Source Mirror", extracted_pdf_text, height=300, disabled=False)

    # --- IMAGE PIPELINE ---
    with tab_img:
        st.markdown("#### Visual Parsing Engine")
        uploaded_image = st.file_uploader("Drop your image here (PNG, JPG, JPEG):", type=["png", "jpg", "jpeg"], key="img_uploader_unique")
        if uploaded_image:
            col_preview, col_ocr_info = st.columns(2, gap="small")
            with col_preview:
                st.image(uploaded_image, caption="Uploaded Source Asset", use_container_width=True)
            
            with col_ocr_info:
                with st.spinner("Processing Image through Cloud Vision Engine..."):
                    img_bytes = uploaded_image.read()
                    img_ext = uploaded_image.name.split('.')[-1].lower()
                    mime_type = f"image/{'jpeg' if img_ext == 'jpg' else img_ext}"
                    
                    extracted_image_text = process_image_vision_cloud(img_bytes, mime_type)
                    if extracted_image_text:
                        st.session_state.shared_context_tokens += f"\n[Extracted Image Data/Text]:\n{extracted_image_text}\n"
                        st.toast("✅ Vision OCR tracking complete!", icon="🖼️")
                        
                        st.markdown("**Vision OCR Output Mirror**")
                        st.info(extracted_image_text if len(extracted_image_text) < 300 else extracted_image_text[:300] + "...")

    # --- AUDIO PIPELINE ---
    with tab_audio:
        st.markdown("#### Cloud Voice Audio Pipeline")
        uploaded_audio = st.file_uploader("Drop speech audio here (MP3, WAV, M4A):", type=["mp3", "wav", "m4a"], key="audio_uploader_unique")
        if uploaded_audio:
            st.audio(uploaded_audio)
            with st.spinner("Streaming voice stream bytes to Groq Whisper LPUs..."):
                suffix_mapping = f".{uploaded_audio.name.split('.')[-1]}"
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix_mapping) as tmp:
                    tmp.write(uploaded_audio.read())
                    audio_temp_path = tmp.name
                    
                speech_transcript_string = transcribe_audio_cloud(audio_temp_path)
                if speech_transcript_string:
                    st.session_state.shared_context_tokens += f"\n[Audio Transcript Context]:\n{speech_transcript_string}\n"
                    st.toast("✅ Audio transcription complete!", icon="🎵")
                    
                    with st.expander("📝 View Full Whisper Audio Transcript", expanded=True):
                        st.text_area("Whisper Output Mirror", speech_transcript_string, height=150, disabled=False)
                
                os.unlink(audio_temp_path)

    # --- RESET MECHANISM ---
    st.divider()
    # --- RESET MECHANISM ---
    if st.button("🔄 Clear App Context Cache", use_container_width=True, type="secondary"):
        st.session_state.shared_context_tokens = ""
        st.session_state.studio_chat_history = []
        if "cached_summary" in st.session_state: 
            del st.session_state["cached_summary"]
        if "cached_quiz" in st.session_state: 
            del st.session_state["cached_quiz"]
        st.toast("Context cache successfully wiped clean!", icon="🧹")
        st.rerun()

# ==============================================================================
# 8. UI RIGHT: RESPONSIVE LIGHTNING INFERENCE STUDIO
# ==============================================================================
with ui_right:
    st.subheader("⚡ Analysis Workspace", anchor=False)
    st.markdown("Extract insights from documents, images, and audio instantly", unsafe_allow_html=True)
    
    if st.session_state.shared_context_tokens:
        st.success("🟢 Pipeline Active: Source data verified and securely tokenized.")
        
                # --- ROW 1: GRID LAYOUT ---
        col_summary, col_quiz = st.columns(2, gap="medium")
        
        with col_summary:
            with st.container(border=True):
                st.markdown('<div class="section-title">📄 Synthesize Context</div>', unsafe_allow_html=True)
                
                if st.button("✨ Generate Executive Summary", use_container_width=True, type="primary"):
                    with st.spinner("Compiling structural vectors..."):
                        llm_response = ask_groq_llm(
                            f"Provide a comprehensive, factual executive summary based on the given multimedia context blocks:\n{st.session_state.shared_context_tokens}"
                        )
                        st.session_state["cached_summary"] = llm_response
                
                if "cached_summary" in st.session_state:
                    with st.container(height=240, border=True):
                        st.markdown(st.session_state["cached_summary"])
                else:
                    st.info("Click the compile button to trigger semantic processing.")
                    
        with col_quiz:
            with st.container(border=True):
                st.markdown('<div class="section-title">🎯 Knowledge Evaluation</div>', unsafe_allow_html=True)
                
                if st.button("📝 Generate Assessment Quiz", use_container_width=True):
                    with st.spinner("Drafting validated schemas..."):
                        llm_response = ask_groq_llm(
                            f"Generate exactly 5 challenging multiple-choice questions with answer parameters strictly testing content from this input asset:\n{st.session_state.shared_context_tokens}"
                        )
                        st.session_state["cached_quiz"] = llm_response
                
                if "cached_quiz" in st.session_state:
                    with st.container(height=240, border=True):
                        st.markdown(st.session_state["cached_quiz"])
                else:
                    st.info("Click button to instantiate testing.")

                # --- ROW 2: CHAT STUDIO LAYOUT ---
                # --- ROW 2: CHAT STUDIO LAYOUT (Locked Input Bar Structure) ---
        st.write("")
        with st.container(border=True):
            chat_header_col, chat_clear_col = st.columns([4, 1.5], gap="small")
            
            with chat_header_col:
                st.markdown('<div class="section-title" style="margin-bottom:0px;">💬 Chat Assistant</div>', unsafe_allow_html=True)
                
            with chat_clear_col:
                if st.button("🗑️ Clear Chat", use_container_width=True):
                    st.session_state.studio_chat_history = []
                    st.rerun()

            # 1. FIXED VIEWPORT: This window will contain message logs only
            with st.container(height=180, border=True):
                if not st.session_state.studio_chat_history:
                    st.caption("Hi there! Ask me anything about your uploaded files, or just say hello! 😊")
                else:
                    for msg in st.session_state.studio_chat_history:
                        with st.chat_message(msg["role"]):
                            st.markdown(msg["content"])

            # 2. SEPARATED WIDGET BLOCK: Placing this here keeps the bar locked at the card footer
            if chat_prompt := st.chat_input("Type your message here...", key="fixed_chat_bar"):
                st.session_state.studio_chat_history.append({"role": "user", "content": chat_prompt})
                
                friendly_system_prompt = (
                    "You are a helpful, warm, and highly conversational AI assistant. "
                    "Keep casual conversation natural, brief, and friendly. Use occasional emojis. "
                    "If the user says 'hi' or greets you, reply naturally with a warm greeting like "
                    "'Hello! How can I help you today? 😊'. "
                    "If they ask about the uploaded files, use the provided context to answer clearly and helpfully."
                )
                
                with st.spinner("Thinking..."):
                    llm_response = ask_groq_llm(
                        prompt=f"Context Elements:\n{st.session_state.shared_context_tokens}\n\nQuestion:\n{chat_prompt}",
                        system_instruction=friendly_system_prompt
                    )
                    st.session_state.studio_chat_history.append({"role": "assistant", "content": llm_response})
                
                st.rerun()


                    
    else:
        st.warning("⚠️ System Offline: The cloud LPU architecture is currently un-allocated. Upload matching multimedia files in the left module to engage analytics.")
