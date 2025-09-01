#pip install python-telegram-bot 
#pip install requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
import requests

TG_TOKEN = "???"    # Replace with your Telegram bot token
#AGENT_URL = "http://localhost:8002/chat" this will not work after Dockerization
AGENT_URL = "http://python-agent_service:8002/chat"

# Store chat histories
chat_histories = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! 🤖 I’m your MCP-powered AI bot.\n"
        "Type /help to see what I can do."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/start – Start the conversation\n"
        "/help – Show this help message\n"
        "/sentiment <text> – Analyze sentiment\n"
        "/bio <query> – Search in bio dataset\n"
        "/reset – Clear conversation history\n"
        "/memory – Show last 5 messages in history\n"
        "/clear_chat – ⚠️ WARNING: Permanently delete ALL stored messages for this chat.\n"
        "   Usage: /clear_chat confirm"
    )

async def sentiment_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("Please provide text after /sentiment")
        return
    tool_instruction = "Use the sentiment_tool. Inform that sentiment tool was used. Return sentiment and score. "
    text = f"{tool_instruction}\n\nUser text: {text}"
    await send_to_agent(update, text)

async def bio_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text("Please provide a query after /bio")
        return
    tool_instruction = "Use the rag_tool for this query. Return most suitable information from document or say that there is no info about in a document. Write in the end of your response: 'RAG tool was used'."
    query = f"{tool_instruction}\n\nUser query: {query}"
    await send_to_agent(update, query)

async def reset_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_histories[str(update.effective_chat.id)] = []
    await update.message.reply_text("✅ Conversation history cleared!")

async def clear_chat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)

    # Step 1: Require confirmation
    if not context.args or context.args[0].lower() != "confirm":
        await update.message.reply_text(
            "⚠️ This will permanently delete ALL stored messages for this chat.\n"
            "❌ This action cannot be undone.\n\n"
            "If you are sure, type:\n"
            "/clear_chat confirm"
        )
        return

    # Step 2: Delete history
    if chat_id in chat_histories:
        del chat_histories[chat_id]
        await update.message.reply_text("✅ All stored messages for this chat have been deleted.")
    else:
        await update.message.reply_text("ℹ️ No stored messages found for this chat.")


async def memory_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = str(update.effective_chat.id)
    history = chat_histories.get(chat_id, [])
    if not history:
        await update.message.reply_text("💭 No history yet.")
        return

    # Get last 5 messages
    last_messages = history[-5:]
    formatted = "\n".join(
        [f"{msg['role'].capitalize()}: {msg['content']}" for msg in last_messages]
    )
    await update.message.reply_text(f"🧠 Last {len(last_messages)} messages:\n{formatted}")

async def send_to_agent(update: Update, user_text: str):
    chat_id = str(update.effective_chat.id)
    history = chat_histories.get(chat_id, [])
    history.append({"role": "user", "content": user_text})

    mcp_payload = {
        "context": {
            "conversation_id": chat_id,
            "history": history
        },
        "input": {"query": user_text}
    }

    try:
        response = requests.post(AGENT_URL, json=mcp_payload)
        result = response.json().get("output", {}).get("result", "⚠️ No answer")
    except Exception as e:
        result = f"Error: {e}"

    history.append({"role": "assistant", "content": result})
    chat_histories[chat_id] = history

    await update.message.reply_text(result)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_to_agent(update, update.message.text)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TG_TOKEN).build()

    # Command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("sentiment", sentiment_command))
    app.add_handler(CommandHandler("bio", bio_command))
    app.add_handler(CommandHandler("reset", reset_command))
    app.add_handler(CommandHandler("clear_chat", clear_chat_command))
    app.add_handler(CommandHandler("memory", memory_command))

    # Regular text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running... Press Ctrl+C to stop.")
    app.run_polling()
