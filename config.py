"""Module config backend — mọi thứ "đổi được" nằm ở đây.

Đổi backend = đổi env var LLM_BASE_URL (hoặc file .env), không sửa code logic.
"""
import os

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

CONFIG = {
    "base_url": os.getenv("LLM_BASE_URL", "http://localhost:11434/v1"),
    "api_key": os.getenv("LLM_API_KEY", "ollama"),
    "model": os.getenv("LLM_MODEL", "qwen3.5:9b"),
    "system": os.getenv("LLM_SYSTEM", "Bạn là trợ lý hữu ích, trả lời bằng tiếng Việt."),
}
