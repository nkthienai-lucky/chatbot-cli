"""Entrypoint CLI — chat loop đọc stdin, in streaming, giữ lịch sử hội thoại."""
import argparse

from config import CONFIG
from llm import stream_chat


def chat_loop(system: str, model: str | None = None) -> None:
    history: list[dict] = [{"role": "system", "content": system}]
    print(f"[backend: {CONFIG['base_url']} | model: {model or CONFIG['model']}]")
    print("Nhập câu hỏi (exit/quit để thoát).\n")
    while True:
        try:
            question = input("Bạn: ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not question:
            continue
        if question.lower() in {"exit", "quit"}:
            break
        history.append({"role": "user", "content": question})
        print("Bot: ", end="", flush=True)
        answer = stream_chat(history, echo=True, model=model)
        print()
        history.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot GĐ1 — CLI streaming, 2 backend.")
    parser.add_argument("--system", default=CONFIG["system"], help="System prompt tùy chỉnh")
    parser.add_argument("--model", default=None, help="Override model (mặc định: LLM_MODEL)")
    args = parser.parse_args()
    chat_loop(args.system, args.model)
