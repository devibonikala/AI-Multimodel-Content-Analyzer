# AI-Multimodel-Content-Analyzer
An intelligent Streamlit-based application that analyzes and extracts information from multiple content formats including PDF documents, Images, and Audio files using advanced AI models powered by Groq Cloud.
# 🎯 AI Multimodel Content Analyzer

> A powerful multimodal AI application that analyzes PDFs, Images, and Audio files using Groq LLM, Whisper AI, and Vision OCR to generate summaries, quizzes, and intelligent conversations.

---

## 🚀 Project Overview

AI Multimodel Content Analyzer is an AI-powered content processing platform that allows users to upload and analyze multiple content formats from a single interface.

The application extracts information from:

- 📄 PDF Documents
- 🖼️ Images
- 🎙️ Audio Files

and converts them into a unified AI-readable context.

Using Groq Cloud's high-speed inference models, the application can:

- Extract information
- Generate summaries
- Create quizzes
- Answer user questions
- Provide intelligent insights

through a single interactive dashboard.

---

# 🎯 Problem Statement

In today's digital world, information exists in multiple formats such as documents, images, and audio recordings.

Analyzing each file separately is time-consuming and inefficient.

This project solves that problem by:

- Extracting text from PDFs
- Performing OCR on images
- Converting speech to text
- Combining all extracted data into one context
- Using AI to generate meaningful insights

---

# ✨ Features

## 📄 PDF Document Analysis

- Upload PDF documents
- Extract text from multiple pages
- Parse large documents
- Store extracted information for AI processing

---

## 🖼️ Image OCR Analysis

- Upload PNG, JPG, JPEG images
- Extract text using OCR
- Identify visual content
- Analyze diagrams and screenshots

---

## 🎙️ Audio Transcription

- Upload MP3, WAV, M4A files
- Convert speech into text
- Generate accurate transcripts
- Analyze spoken content

---

## 🤖 AI Executive Summary

Generate:

- Detailed summaries
- Key insights
- Important highlights
- Topic understanding

---

## 📝 AI Quiz Generator

Automatically creates:

- Multiple Choice Questions
- Knowledge Assessments
- Learning Evaluations

from uploaded content.

---

## 💬 AI Chat Assistant

Ask questions about uploaded files.

Examples:

- Summarize this PDF
- What is discussed in the audio?
- Explain the image content
- Give important points

The assistant answers using uploaded file context.

---

# 🏗️ System Architecture

```text
                    USER
                      │
                      ▼
           ┌──────────────────┐
           │ Streamlit UI     │
           └────────┬─────────┘
                    │
     ┌──────────────┼──────────────┐
     │              │              │
     ▼              ▼              ▼

 PDF Upload    Image Upload    Audio Upload

     │              │              │
     ▼              ▼              ▼

 PyPDF2        Vision OCR      Whisper AI

     │              │              │
     └──────────────┼──────────────┘
                    │
                    ▼

         Shared Context Builder

                    │
                    ▼

             Groq LLM Engine

                    │
      ┌─────────────┼─────────────┐
      ▼             ▼             ▼

 Executive      Quiz         Chatbot
 Summary      Generator
```

---

# 📂 Project Structure

```text
AI-Multimodel-Content-Analyzer/
│
├── app.py
│
├── .env
│
├── requirements.txt
│
├── README.md
│
├── utils/
│   ├── ai_helper.py
│   ├── audio_processor.py
|   ├── image_processor.py
│   ├── text_processor.py
|   
│
├── screenshots/
│   ├── home.png
│   ├── pdf_analysis.png
│   ├── image_analysis.png
│   └── audio_analysis.png
│
└── sample_files/
    ├── sample.pdf
    ├── sample.jpg
    └── sample.mp3
```

---

# ⚙️ Complete Working Flow

## Step 1: User Uploads Content

The user uploads:

- PDF
- Image
- Audio

using Streamlit file uploaders.

```python
uploaded_pdf = st.file_uploader()
uploaded_image = st.file_uploader()
uploaded_audio = st.file_uploader()
```

---

## Step 2: PDF Text Extraction

When a PDF is uploaded:

```python
pdf_reader = PdfReader(uploaded_pdf)

for page in pdf_reader.pages:
    text += page.extract_text()
```

### What Happens?

✅ Reads every page

✅ Extracts all text

✅ Stores extracted text

✅ Sends content to AI pipeline

---

## Step 3: Image OCR Processing

When an image is uploaded:

```python
process_image_vision_cloud()
```

### What Happens?

✅ Converts image to Base64

✅ Sends image to Vision Model

✅ Extracts text

✅ Detects visual information

✅ Returns OCR results

---

## Step 4: Audio Transcription

When audio is uploaded:

```python
transcribe_audio_cloud()
```

### What Happens?

✅ Uploads audio to Whisper

✅ Converts speech into text

✅ Creates transcript

✅ Stores transcript

---

## Step 5: Context Aggregation

All extracted information is combined into:

```python
st.session_state.shared_context_tokens
```

Example:

```text
PDF Text

+

Image Text

+

Audio Transcript

=

Unified AI Context
```

This allows the AI model to understand all uploaded content together.

---

## Step 6: AI Processing

The unified context is sent to Groq LLM.

```python
ask_groq_llm()
```

The model performs:

- Context Understanding
- Content Analysis
- Summarization
- Question Generation
- Conversational Reasoning

---

## Step 7: Executive Summary Generation

When the user clicks:

```text
Generate Executive Summary
```

The application:

1. Sends extracted content to Groq
2. Generates summary
3. Displays important information

---

## Step 8: Quiz Generation

When the user clicks:

```text
Generate Assessment Quiz
```

The application:

1. Reads uploaded content
2. Creates MCQs
3. Generates answers

---

## Step 9: Chat Assistant

When the user asks:

```text
What is this document about?
```

The chatbot:

1. Uses uploaded content as context
2. Sends context + question to LLM
3. Returns intelligent response

---

# 🔧 Core Functions Used

## ask_groq_llm()

Purpose:

- Connects with Groq API
- Sends prompts
- Receives AI responses

---

## process_image_vision_cloud()

Purpose:

- OCR extraction
- Image understanding

---

## transcribe_audio_cloud()

Purpose:

- Audio transcription
- Speech-to-text conversion

---

# 🛠️ Technologies Used

| Technology | Purpose |
|------------|----------|
| Python | Programming Language |
| Streamlit | Web Application |
| Groq API | AI Inference |
| Qwen LLM | Text Analysis |
| Whisper AI | Speech Recognition |
| PyPDF2 | PDF Extraction |
| dotenv | API Key Management |
| HTML/CSS | UI Styling |

---

# 📦 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/AI-Multimodel-Content-Analyzer.git
```

```bash
cd AI-Multimodel-Content-Analyzer
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Create Environment File

Create:

```env
.env
```

Add:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## Run Application

```bash
streamlit run app.py
```

---

# 📈 Future Improvements

- Video Analysis Support
- RAG Integration
- ChromaDB / FAISS
- Multi-Language Translation
- User Authentication
- PDF Report Generation
- Cloud Deployment
- Analytics Dashboard
- Voice Chat Assistant

---

# 🎓 Learning Outcomes

Through this project I learned:

- Multimodal AI Systems
- OCR Technology
- Speech Recognition
- Large Language Models
- Prompt Engineering
- Streamlit Development
- API Integration
- Session State Management
- AI Product Design
- Cloud-Based AI Deployment

---

# 💼 Resume Project Description

### AI Multimodel Content Analyzer

Developed a multimodal AI application using Streamlit, Groq LLM, Whisper AI, and OCR technologies to process PDF documents, images, and audio files. Implemented automated text extraction, speech transcription, executive summary generation, quiz creation, and context-aware conversational AI. Designed a unified content-processing pipeline that combines multiple data formats into a shared AI context for intelligent analysis and user interaction.

---

# 👨‍💻 Author

**Devi**

Aspiring Data Scientist | Machine Learning Engineer | Python Developer

### Skills

- Python
- Machine Learning
- Deep Learning
- NLP
- Generative AI
- Streamlit
- Data Science

---

## ⭐ Star this repository if you found it useful!
