# Multimodal Data Processing System

A modular system to extract text from multiple file types (pdf, docx, pptx, md, txt, images, audio, YouTube),
store the extracted content in a SQLite DB, and answer natural language queries using Google's Gemini API (optional).

## Setup
1. Create and activate a virtualenv:
```
python -m venv venv
source venv/bin/activate  # mac/linux
venv\Scripts\activate   # windows
```
2. Install requirements:
```
pip install -r requirements.txt
```
3. Install Tesseract OCR on your OS (required for image OCR with pytesseract):
- Ubuntu: `sudo apt-get install tesseract-ocr`
- Mac (Homebrew): `brew install tesseract`

4. (Optional) Add a `.env` file with:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Usage (CLI)
- To ingest a file:
```
python main.py ingest path/to/file.pdf
```
- To ingest a YouTube URL:
```
python main.py ingest-youtube "https://www.youtube.com/watch?v=VIDEOID"
```
- To ask a question:
```
python main.py query "What is said about AI?"
```

## Usage (Streamlit UI)
```
streamlit run ui/streamlit_app.py
```

## Notes
- If GEMINI_API_KEY is not provided, the system uses a local extractive fallback to return answers from context.
- Whisper is optional; if not installed, audio transcription falls back to SpeechRecognition+pydub, which may need internet.
