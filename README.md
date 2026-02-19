# 💬 Q&A AI Telegram Bot: Intelligent Assistant

![Python](https://img.shields.io/badge/Python-3.11%2B-blue?logo=python&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI-Gemini%202.5%20Flash-8E75B2?logo=google&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-PTB%20Framework-26A5E4?logo=telegram&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success)

## 📌 Overview
**Q&A AI Telegram Bot** is an interactive, real-time chatbot powered by Google's latest **Gemini 2.5 Flash** model, built natively for Telegram.

Unlike basic bots using raw HTTP requests, this project utilizes the robust **`python-telegram-bot` (PTB)** framework. It features an asynchronous architecture capable of handling multiple users concurrently, personalizing responses based on sender metadata, and providing a highly structured, global error-handling mechanism that alerts the developer directly if a critical failure occurs.

> **🎯 Perfect for Beginners:** This repository is an excellent starting point for developers who are just starting to learn the Python Telegram Bot (PTB) framework. By focusing strictly on the core integration between Python Telegram Bot (PTB) and Google Gemini, it provides a clean, easy-to-understand codebase without the distraction of unnecessary libraries or overly complex architectures.

## ✨ Key Features
### 🧠 Advanced Contextual AI
* **Gemini SDK Integration:** Uses the new `google-genai` client to connect with the lightning-fast `gemini-2.5-flash` model.
* **Personalized Prompts:** Dynamically injects the user's Telegram First Name into the system prompt, allowing the AI to address users personally and naturally.
* **Graceful Degradation:** If the AI returns an empty response (e.g., due to safety filters), the bot automatically replies with a polite fallback message.

### 🛡️ Enterprise-Grade Architecture
* **Asynchronous Handlers:** Built with `async/await` syntax, ensuring the bot remains responsive even when the LLM takes time to generate long answers.
* **Command & Message Routing:** Cleanly separates the `/start` command logic from standard conversational text processing using PTB's `CommandHandler` and `MessageHandler`.
* **Centralized Error Ambulance:** Features a Global Error Handler (`app.add_error_handler`). If the bot crashes, it prevents silent failures by sending a detailed error report directly to the Developer's Telegram DM.

### 📨 Smart Delivery
* **Markdown Support:** All AI responses are formatted using Telegram's Markdown parsing, allowing for bold text, lists, and structured outputs.
* **Intelligent Error Feedback:** Catches specific Google API exceptions (Quota limits 429, Invalid Keys 403) and sends user-friendly, non-technical warning messages back to the chat.

## 🛠️ Tech Stack
* **Core:** Python 3.11+
* **AI Provider:** Google GenAI SDK (`google-genai`)
* **Framework:** Python Telegram Bot (`python-telegram-bot`)
* **Config:** Python-Dotenv (`python-dotenv`)
* **Logging:** Standard Python `logging` module

## 🚀 The Workflow
1.  **Initialize:** The `ApplicationBuilder` constructs the bot and attaches the required handlers.
2.  **Listen:** The bot uses `app.run_polling()` to continuously and asynchronously listen for updates from Telegram.
3.  **Route:**
    * If `/start` is received -> Triggers `start_command()` -> Sends a welcome message.
    * If Text is received -> Triggers `handle_message()` -> Processes through Gemini.
4.  **Process (AI):** The bot extracts the user's name and text, formats the prompt, and queries the Gemini API.
5.  **Reply:** The generated text is safely sent back to the specific `chat_id`.
6.  **Rescue (Error):** If any step raises an unhandled exception, `error_handler()` catches it, logs it, and alerts the Developer.

## ⚙️ Configuration (Environment Variables)
Create a `.env` file in the root directory:
```ini
TELEGRAM_TOKEN_JawabAja_Bot=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_developer_chat_id_for_error_alerts
GOOGLE_API_KEY=your_gemini_api_key
```

## 📦 Local Installation
1. **Clone the Repository**
```bash
git clone [https://github.com/viochris/qna-telegram-bot-ptb.git](https://github.com/viochris/qna-telegram-bot-ptb.git)
cd qna-telegram-bot-ptb
```

2. **Install Dependencies**
```bash
pip install python-telegram-bot google-genai python-dotenv
```

3. **Run the Bot**
```bash
python bot_main.py
```

### 🖥️ Expected Output
You will see the system logging initialize and the bot enter its polling state:
```text
2026-02-19 14:05:00 - httpx - INFO - HTTP Request: GET [https://api.telegram.org/bot](https://api.telegram.org/bot)<TOKEN>/getMe "HTTP/1.1 200 OK"
2026-02-19 14:05:01 - telegram.ext.Application - INFO - Application started
🚀 Gemini Q&A Telegram Bot is currently online and listening...
```

## 🚀 Deployment
This script uses Long Polling (`app.run_polling()`) and is designed to be **Always On**. It is best deployed on:
* **VPS** (Virtual Private Server) like DigitalOcean, Linode, or AWS EC2 running via `tmux` or `systemd`.
* **Docker Container** for isolated, continuous execution.
* **Railway / Render** (PaaS) as a background worker process.

---

**Author:** [Silvio Christian, Joe](https://www.linkedin.com/in/silvio-christian-joe)
*"Connecting minds, automating conversations."*
