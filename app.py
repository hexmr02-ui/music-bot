import os
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, AudioPiped
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING")
RADIO_URL = os.getenv("RADIO_URL")

# সাপোর্টিং ইউজার (MTProto client)
user_client = Client("assistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
pytg = PyTgCalls(user_client)

# বট (Bot API)
app = ApplicationBuilder().token(BOT_TOKEN).build()

async def start_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎵 /play দিয়ে রেডিও চালু করো, /stop দিয়ে বন্ধ করো।")

async def play_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        await pytg.join_group_call(
            chat_id,
            InputStream(
                AudioPiped(RADIO_URL)
            )
        )
        await update.message.reply_text(f"▶️ রেডিও চালু: {RADIO_URL}")
    except Exception as e:
        await update.message.reply_text(f"⚠️ সমস্যা: {e}")

async def stop_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    try:
        await pytg.leave_group_call(chat_id)
        await update.message.reply_text("⏹️ রেডিও বন্ধ।")
    except Exception as e:
        await update.message.reply_text(f"⚠️ সমস্যা: {e}")

async def main():
    await user_client.start()
    await pytg.start()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("play", play_cmd))
    app.add_handler(CommandHandler("stop", stop_cmd))
    await app.initialize()
    await app.start()
    print("✅ Bot & Assistant চলছে...")
    await app.updater.start_polling()
    await app.updater.idle()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
