"""Gradio demo — deploy lên Hugging Face Spaces.

Spaces không chạy được Ollama local → trỏ LLM_BASE_URL tới API thật
(xem .env.example và Settings → Secrets của Space).
"""
import gradio as gr

from config import CONFIG
from llm import stream_chat_plain


def respond(message: str, history: list[dict]):
    messages = [{"role": "system", "content": CONFIG["system"]}]
    messages += history
    messages.append({"role": "user", "content": message})
    partial = ""
    for token in stream_chat_plain(messages):
        partial += token
        yield partial


demo = gr.ChatInterface(
    respond,
    title="Chatbot GĐ1",
    description="Chatbot streaming — demo project GĐ1 (AI Engineer Roadmap).",
    type="messages",
)

if __name__ == "__main__":
    demo.launch()
