# Chatbot GĐ1 — Chatbot CLI + Demo

> Project **giai đoạn 1** của [AI Engineer Roadmap](https://github.com/nkthienai-lucky/AI-Engineer-Roadmap):
> chatbot CLI streaming chạy được **2 backend** (Ollama local ↔ API thật) — đổi 1 dòng config,
> kèm demo web Gradio deploy lên Hugging Face Spaces.

## ✨ Tính năng (4 yêu cầu GĐ1)

1. **CLI chat streaming** — in từng token khi model sinh, giữ lịch sử hội thoại qua các lượt.
2. **2 backend, đổi 1 dòng config** — Ollama local hoặc bất kỳ API OpenAI-compatible nào (ví dụ xkiro/MiMo); không sửa code logic.
3. **System prompt tùy chỉnh** — qua biến môi trường `LLM_SYSTEM` hoặc flag `--system`.
4. **Demo web public** — Gradio ChatInterface, deploy lên HF Spaces có URL gửi cho bạn bè.

## 🚀 Chạy nhanh (5 phút)

```bash
git clone <repo-này> && cd chatbot-cli
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env     # chỉnh config nếu cần
python chat.py
```

Yêu cầu: Python 3.14+ (đã test), và [Ollama](https://ollama.com/) đang chạy với model `qwen3.5:9b`
(`ollama pull qwen3.5:9b`) nếu dùng backend local.

## ⚙️ Cấu hình — "đổi 1 dòng config"

Tất cả nằm trong env vars (file `.env` — **không commit**, xem `.env.example`):

| Biến | Backend local (mặc định) | Backend API thật |
|---|---|---|
| `LLM_BASE_URL` | `http://localhost:11434/v1` | `https://api.xkiro.com/v1` |
| `LLM_API_KEY` | `ollama` (không cần key thật) | key của bạn |
| `LLM_MODEL` | `qwen3.5:9b` | `xiaomi/mimo-v2.6-pro` |
| `LLM_SYSTEM` | `Bạn là trợ lý hữu ích, trả lời bằng tiếng Việt.` | tùy chỉnh |

```bash
python chat.py                                  # backend trong .env
python chat.py --system "Bạn là cướp biển"      # đổi persona
python chat.py --model qwen3.5:9b               # override model
```

## 🌐 Demo web (Gradio)

```bash
python app.py           # chạy local tại http://127.0.0.1:7860
```

Deploy public (Render free — xem `render.yaml`):

1. Đẩy project lên GitHub (Render/Koyeb deploy qua kết nối Git — không upload trực tiếp được).
2. Tạo **Web Service** trên [render.com](https://render.com) → kết nối repo → Render tự đọc `render.yaml`.
3. Vào **Environment** của service, đặt `LLM_BASE_URL`, `LLM_API_KEY`, `LLM_MODEL`
   (secret **không** commit; server không chạy được Ollama local → trỏ tới API thật).
4. Deploy xong → lấy **URL public** gửi cho bạn bè.

> Lưu ý: HF Spaces (chọn gốc của spec GĐ1) đã chặn Space Gradio trên free tier từ 2026
> (cần HF Pro) → đổi sang Render free, cùng code, chỉ đổi nền tảng.

## 📸 Screenshot

```
$ python chat.py
[backend: http://localhost:11434/v1 | model: qwen3.5:9b]
Nhập câu hỏi (exit/quit để thoát).

Bạn: Tên tôi là Nam, nhớ nhé.
Bot: Vâng, tôi đã ghi nhớ tên của bạn là Nam rồi ạ. Rất vui được đồng hành cùng bạn!
Bạn: tên tôi là gì?
Bot: Tên của bạn là **Nam** ạ! Tôi đã nhớ rõ rồi đấy, Nam ơi! 😊
```

> Ảnh chụp UI demo web sẽ được thêm vào sau khi deploy HF Spaces (bước cuối).

## ✅ Checklist nghiệm thu (DoD GĐ1)

- [x] `python chat.py` chạy được, stream mượt (flush từng token)
- [x] Đổi model/backend không sửa code logic (chỉ đổi env var)
- [x] System prompt tùy chỉnh (`LLM_SYSTEM` / `--system`)
- [x] Lịch sử hội thoại giữ đúng ("câu trước tôi hỏi gì?")
- [ ] Demo URL hoạt động, gửi được cho bạn bè xem *(sau khi deploy)*
- [x] README có hướng dẫn chạy
- [ ] Ảnh screenshot UI demo *(sau khi deploy)*
- [x] Không hard-code API key (key chỉ nằm trong `.env` gitignored / HF Secrets)

## 📁 Cấu trúc

```
chatbot-cli/
├── chat.py          # entrypoint CLI: chat loop, streaming, flag --system/--model
├── config.py        # config qua env vars (đổi backend = đổi env)
├── llm.py           # wrapper OpenAI-compatible: stream_chat + stream_chat_plain
├── app.py           # Gradio ChatInterface cho HF Spaces
├── requirements.txt # openai, gradio>=6.0, python-dotenv
├── .env.example     # template cấu hình (không chứa key thật)
└── README.md
```
