"""Wrapper gọi API OpenAI-compatible — dùng chung cho CLI và Gradio."""
from openai import OpenAI

from config import CONFIG

client = OpenAI(base_url=CONFIG["base_url"], api_key=CONFIG["api_key"])


def _create_stream(messages: list[dict], model: str | None = None):
    return client.chat.completions.create(
        model=model or CONFIG["model"],
        messages=messages,
        stream=True,
    )


def stream_chat(messages: list[dict], echo: bool = True, model: str | None = None) -> str:
    """Stream câu trả lời. echo=True in từng token ra terminal (CLI); echo=False chỉ thu text.

    Trả về toàn bộ câu trả lời.
    """
    parts: list[str] = []
    for chunk in _create_stream(messages, model):
        delta = chunk.choices[0].delta.content
        if delta:
            if echo:
                print(delta, end="", flush=True)  # stream mượt = flush từng mảnh
            parts.append(delta)
    return "".join(parts)


def stream_chat_plain(messages: list[dict], model: str | None = None):
    """Yield từng token — dùng cho UI hiển thị dần (Gradio)."""
    for chunk in _create_stream(messages, model):
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
