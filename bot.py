import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from groq import Groq

# ── إعدادات ──────────────────────────────────────────────
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN", "YOUR_TELEGRAM_TOKEN")
GROQ_API_KEY   = os.environ.get("GROQ_API_KEY",   "YOUR_GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# ── سيرفر وهمي لإرضاء Render ─────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
    def log_message(self, format, *args):
        pass

def run_server():
    port = int(os.environ.get("PORT", 10000))
    HTTPServer(('', port), Handler).serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# ── سياق كل مستخدم (ذاكرة المحادثة) ─────────────────────
user_histories: dict[int, list[dict]] = {}

SYSTEM_PROMPT = """أنت NexusAI، مساعد ذكي ومفيد يتحدث العربية والإنجليزية بطلاقة.
كن ودوداً، موجزاً، ودقيقاً في إجاباتك."""

# ── /start ────────────────────────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.first_name
    await update.message.reply_text(
        f"مرحباً {user}! 👋\n"
        "أنا *NexusAI* — مساعدك الذكي.\n"
        "ابعتلي أي سؤال وأنا هنا! 🚀",
        parse_mode="Markdown"
    )

# ── /clear  تصفير المحادثة ────────────────────────────────
async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_histories.pop(user_id, None)
    await update.message.reply_text("✅ تم مسح سجل المحادثة.")

# ── /help ─────────────────────────────────────────────────
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "*أوامر البوت:*\n"
        "/start — تشغيل البوت\n"
        "/clear — مسح سجل المحادثة\n"
        "/help  — هذه المساعدة\n\n"
        "أو ببساطة ابعت أي رسالة وسأرد عليك! 💬",
        parse_mode="Markdown"
    )

# ── معالج الرسائل النصية ──────────────────────────────────
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id  = update.effective_user.id
    user_msg = update.message.text

    history = user_histories.get(user_id, [])
    history.append({"role": "user", "content": user_msg})

    if len(history) > 20:
        history = history[-20:]

    try:
        await context.bot.send_chat_action(
            chat_id=update.effective_chat.id, action="typing"
        )

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": SYSTEM_PROMPT}] + history,
            max_tokens=1024,
            temperature=0.7,
        )

        ai_reply = response.choices[0].message.content
        history.append({"role": "assistant", "content": ai_reply})
        user_histories[user_id] = history

        await update.message.reply_text(ai_reply)

    except Exception as e:
        logging.error(f"Groq error: {e}")
        await update.message.reply_text(
            "⚠️ حدث خطأ، حاول مرة ثانية بعد لحظة."
        )

# ── تشغيل البوت ───────────────────────────────────────────
def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(CommandHandler("help",  help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logging.info("NexusAI Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
