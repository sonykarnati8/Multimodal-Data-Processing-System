# Multimodal Data Processing System

The **Multimodal Data Processing System** is a Python-based project that extracts and processes text from multiple file formats such as documents, images, audio, video, and YouTube videos. It stores all extracted content in a local database and allows users to ask natural language questions about the stored data. Answers are generated using the **Google Gemini AI API** or a local fallback method if the API key is not available.

---

## Features
- Extracts text from `.pdf`, `.docx`, `.pptx`, `.txt`, and `.md` files  
- Performs OCR (Optical Character Recognition) on image files  
- Transcribes audio and video into text  
- Extracts YouTube video transcripts automatically  
- Stores data using **TinyDB** (lightweight database)  
- Supports natural language queries through the **Gemini AI API**  
- Provides both **CLI** and optional **Streamlit UI**

---

## Technologies Used
**Language:** Python  
**Libraries:**  
`pdfplumber`, `python-docx`, `python-pptx`, `pytesseract`, `Pillow`,  
`SpeechRecognition`, `Whisper`, `youtube-transcript-api`, `TinyDB`,  
`google-generativeai`, `Streamlit`, `python-dotenv`

---

## System Workflow
1. **Ingestion:** User provides a file or YouTube link.  
2. **Extraction:** The system detects file type and extracts text using the appropriate extractor.  
3. **Storage:** Extracted data and metadata are saved in TinyDB.  
4. **Querying:** User asks a question; relevant documents are retrieved.  
5. **Answer Generation:** Gemini API (or fallback method) generates a response.

---

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/multimodal-data-processing-system.git
   cd multimodal-data-processing-system
