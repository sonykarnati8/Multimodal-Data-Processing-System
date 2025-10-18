# main.py
import argparse
from pathlib import Path
from utils import text_extractor, image_extractor, audio_video_extractor, youtube_extractor
from database.db_handler import DBHandler
from llm.gemini_interface import query_gemini

def ingest_file(db: DBHandler, path: str):
    p = Path(path)
    if not p.exists():
        print(f"[ERROR] File not found: {path}")
        return
    suf = p.suffix.lower()
    try:
        if suf in [".pdf", ".docx", ".pptx", ".txt", ".md"]:
            content = text_extractor.extract_text_generic(path)
            db.add_document(str(p.name), "text", content, {"source": str(p)})
            print(f"[OK] Ingested text file: {p.name} (len={len(content)})")
            return
        if suf in [".png", ".jpg", ".jpeg", ".bmp", ".tiff"]:
            content = image_extractor.extract_text_from_image(path)
            db.add_document(str(p.name), "image", content, {"source": str(p)})
            print(f"[OK] Ingested image file: {p.name} (len={len(content)})")
            return
        if suf in [".mp3", ".wav", ".m4a", ".mp4", ".mov", ".aac", ".ogg"]:
            content = audio_video_extractor.extract_text_from_audio_or_video(path)
            db.add_document(str(p.name), "audio", content, {"source": str(p)})
            print(f"[OK] Ingested audio/video file: {p.name} (len={len(content)})")
            return
        # fallback
        print(f"[WARN] Unsupported file type: {suf}")
    except Exception as e:
        print(f"[ERROR] Failed to ingest {path}: {e}")

def ingest_youtube(db: DBHandler, url: str):
    try:
        txt = youtube_extractor.extract_transcript_from_youtube(url)
        db.add_document(url, "youtube", txt, {"source": url})
        print(f"[OK] Ingested YouTube: {url} (len={len(txt)})")
    except Exception as e:
        print(f"[ERROR] YouTube ingest failed: {e}")

def query_db_and_answer(db: DBHandler, question: str, top_k: int = 5):
    results = db.search_documents(question, limit=top_k)
    if not results:
        print("No matching documents found. Try a broader query or ingest more documents.")
        return
    context_parts = []
    for r in results:
        header = f"--- Document: {r['filename']} (type: {r['filetype']}) ---\n"
        context_parts.append(header + r["content"][:4000])
    context = "\n\n".join(context_parts)
    answer = query_gemini(context, question)
    print("\n=== Answer ===\n")
    print(answer)
    print("\n=== Sources ===\n")
    for r in results:
        print(f"- {r['filename']} (id={r['id']})")

def main():
    parser = argparse.ArgumentParser(description="Multimodal Data Processing CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_ingest = sub.add_parser("ingest", help="Ingest a file")
    p_ingest.add_argument("path", help="Path to file to ingest")

    p_yt = sub.add_parser("ingest-youtube", help="Ingest a YouTube URL transcript")
    p_yt.add_argument("url", help="YouTube URL")

    p_query = sub.add_parser("query", help="Ask a question over ingested content")
    p_query.add_argument("question", help="Natural language question")
    p_query.add_argument("--top", type=int, default=5, help="Top-K docs to retrieve")

    args = parser.parse_args()
    db = DBHandler()

    if args.cmd == "ingest":
        ingest_file(db, args.path)
    elif args.cmd == "ingest-youtube":
        ingest_youtube(db, args.url)
    elif args.cmd == "query":
        query_db_and_answer(db, args.question, top_k=args.top)

if __name__ == "__main__":
    main()
