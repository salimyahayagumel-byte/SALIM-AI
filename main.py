"""SALIM AI TERMINAL 3.1 — direct command prompt, no menu required."""
import os
import sys
from dotenv import load_dotenv
from ai_client import ask_gemini
from browser_actions import handle_command
from voice_input import listen_once

load_dotenv()
SYSTEM = os.getenv(
    "SYSTEM_PROMPT",
    "You are SALIM AI, a capable bilingual assistant fluent in natural Hausa and English, including Nigerian Hausa phrasing and mixed Hausa-English. "
    "Reply in the same language as the user; if they mix languages, understand both and reply naturally. "
    "Ask a short clarifying question if the request is unclear. Be accurate and honest; never invent facts. "
    "Do not claim to open apps or websites unless the local command handler confirms the action."
)
messages = [{"role": "system", "content": SYSTEM}]

def process(text):
    handled, result = handle_command(text)
    if handled:
        print(f"\nSALIM: {result}\n")
        return
    messages.append({"role": "user", "content": text})
    answer = ask_gemini(messages)
    print(f"\nSALIM: {answer}\n")
    messages.append({"role": "assistant", "content": answer})
    # Keep recent context bounded.
    if len(messages) > 21:
        messages[:] = [messages[0]] + messages[-20:]

def main():
    print("=" * 48)
    print(" SALIM AI TERMINAL 3.1")
    print("Rubuta umarni kai tsaye. Ba sai ka shiga menu ba.")
    print("Misali: SALIM, open YouTube")
    print("Rubuta 'help' don misalai, 'voice' don magana, 'exit' don fita.")
    print("=" * 48)
    while True:
        try:
            text = input("\nKai > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSALIM AI ya tsaya.")
            break
        if not text:
            continue
        cleaned = text.lower().strip()
        if cleaned in ("exit", "quit", "bye", "fita", "stop"):
            print("SALIM: Sai an jima.")
            break
        if cleaned in ("voice", "speak", "murya", "yi magana"):
            print("SALIM: Ina sauraronka yanzu. Ka faɗi umarni...")
            spoken, error = listen_once()
            if spoken:
                print(f"An ji: {spoken}")
                process(spoken)
            else:
                print(f"\nSALIM: {error}\n")
            continue
        process(text)

if __name__ == "__main__":
    main()
