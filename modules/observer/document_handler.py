import asyncio
import glob
import os
from pypdf import PdfReader


# ── PDF finder ────────────────────────────────────────────────────────────────

def find_latest_pdf() -> str | None:
    """Find most recently modified PDF in common locations."""
    search_paths = [
        os.path.expanduser("~/Downloads/*.pdf"),
        os.path.expanduser("~/Documents/*.pdf"),
        os.path.expanduser("~/Desktop/*.pdf"),
        os.path.expanduser("~/Pictures/*.pdf"),
    ]
    all_pdfs = []
    for pattern in search_paths:
        all_pdfs.extend(glob.glob(pattern))

    if not all_pdfs:
        return None

    latest = max(all_pdfs, key=os.path.getmtime)
    print(f"[Documents] Latest PDF: {latest}")
    return latest


def extract_pdf_text(path: str, max_pages: int = 10) -> str | None:
    """Extract plain text from PDF — first N pages."""
    try:
        reader = PdfReader(path)
        total = len(reader.pages)
        pages = min(total, max_pages)
        print(f"[Documents] Reading {pages} of {total} pages")

        text = ""
        for i in range(pages):
            page_text = reader.pages[i].extract_text() or ""
            text += page_text

        if not text.strip():
            print("[Documents] No text extracted — may be scanned/image PDF")
            return None

        print(f"[Documents] Extracted {len(text)} characters")
        return text

    except Exception as e:
        print(f"[Documents] PDF read error: {e}")
        return None


def summarize_text(text: str, brain, instruction: str = None) -> str:
    """Summarize document text using Mistral."""
    # truncate if too long
    max_chars = 8000
    truncated = False
    if len(text) > max_chars:
        text = text[:max_chars]
        truncated = True
        print(f"[Documents] Truncated to {max_chars} chars")

    focus = f"\nFocus on: {instruction}" if instruction else ""
    trunc_note = "\n(Note: document was truncated due to length)" if truncated else ""

    prompt = f"""Summarize this document concisely for a voice assistant.
    3-5 sentences max. Plain text only. No markdown. End with 'sir'.{focus}{trunc_note}
    
    Document:
    {text}
    
    Summary:"""

    try:
        return brain.query(
            prompt,
            model_key="orchestrator",
            num_ctx_override=8192,
            max_tokens_override=300
        )
    except Exception as e:
        print(f"[Documents] Summary error: {e}")
        return "I had trouble summarizing that document, sir."


# ── Main handler ──────────────────────────────────────────────────────────────

async def handle_document_command(text: str, face, mouth, brain, debug: bool = False) -> bool:
    """
    Handle document commands. Returns True if handled.
    """

    # ── PDF summarization ─────────────────────────────────────────────────
    if any(phrase in text for phrase in [
        "summarize pdf", "summarize the pdf", "read the pdf",
        "what does the pdf say", "summarize last pdf",
        "what's in the pdf", "read this pdf", "summarize document",
        "what's in the document", "read the document"
    ]):
        face.set_caption("finding PDF...")

        path = await asyncio.to_thread(find_latest_pdf)
        if not path:
            await _say(face, mouth, "No PDF files found, sir. Try putting one in Downloads or Documents.")
            return True

        face.set_caption("reading PDF...")
        pdf_text = await asyncio.to_thread(extract_pdf_text, path)
        if not pdf_text:
            await _say(face, mouth,
                "Couldn't extract text from that PDF, sir. It may be a scanned image — try a text-based PDF.")
            return True

        # extract focus instruction if any
        instruction = None
        for phrase in ["focus on", "looking for", "about", "find"]:
            if phrase in text:
                instruction = text.split(phrase)[-1].strip()
                break

        face.set_caption("summarizing...")
        summary = await asyncio.to_thread(summarize_text, pdf_text, brain, instruction)
        await _say(face, mouth, summary, next_state="listening")
        return True

    # ── Specific PDF question ─────────────────────────────────────────────
    if any(phrase in text for phrase in [
        "what does the document say about",
        "find in the pdf", "search the pdf",
        "look for in the document"
    ]):
        face.set_caption("searching PDF...")

        path = await asyncio.to_thread(find_latest_pdf)
        if not path:
            await _say(face, mouth, "No PDF files found, sir.")
            return True

        pdf_text = await asyncio.to_thread(extract_pdf_text, path)
        if not pdf_text:
            await _say(face, mouth, "Couldn't read that PDF, sir.")
            return True

        face.set_caption("searching...")
        summary = await asyncio.to_thread(summarize_text, pdf_text, brain, text)
        await _say(face, mouth, summary, next_state="listening")
        return True

    return False


async def _say(face, mouth, text: str, next_state: str = "listening") -> None:
    """Minimal say for document handler."""
    from modules.utils import timer
    face.set_caption(text)
    face.set_state("speaking")
    with timer("TTS doc", True):
        await mouth.speak(text)
    face.set_state(next_state)