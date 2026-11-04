"""Entrypoint CLI — chat loop đọc stdin, in streaming, giữ lịch sử hội thoại."""
import argparse
import sys

# Windows console mặc định cp1252 → crash khi in tiếng Việt; chuẩn hoá UTF-8.
for stream in (sys.stdout, sys.stdin):
    try:
        stream.reconfigure(encoding="utf-8")
    except (AttributeError, ValueError):
        pass

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
        try:
            answer = stream_chat(history, echo=True, model=model)
        except Exception as exc:  # API chết / sai key / model không tồn tại
            print(f"\n[Lỗi: {exc}]")
            history.pop()  # bỏ lượt user chưa có câu trả lời, hỏi lại được
            continue
        print()
        history.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Chatbot GĐ1 — CLI streaming, 2 backend.")
    parser.add_argument("--system", default=CONFIG["system"], help="System prompt tùy chỉnh")
    parser.add_argument("--model", default=None, help="Override model (mặc định: LLM_MODEL)")
    args = parser.parse_args()
    chat_loop(args.system, args.model)
