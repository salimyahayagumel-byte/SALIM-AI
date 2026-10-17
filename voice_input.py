"""One-shot speech input for Termux:API."""
import shutil
import subprocess

def listen_once():
    if not shutil.which("termux-speech-to-text"):
        return None, (
            "Ba a samu termux-speech-to-text ba. A Termux ka yi: pkg install termux-api\n"
            "Sannan ka girka Termux:API app daga tushe mai dacewa, ka ba shi izinin microphone."
        )
    try:
        result = subprocess.run(
            ["termux-speech-to-text"], capture_output=True, text=True, timeout=60
        )
        spoken = (result.stdout or "").strip()
        if result.returncode != 0:
            detail = (result.stderr or "").strip()
            return None, detail or "Ba a samu sautin magana ba."
        return (spoken or None), ("Ba a gane abin da ka faɗa ba." if not spoken else "")
    except subprocess.TimeoutExpired:
        return None, "Lokacin sauraro ya ƙare. Ka sake gwadawa."
    except Exception as exc:
        return None, f"Kuskuren microphone: {exc}"
