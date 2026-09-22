from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@cryptosaga0"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to Crypto Saga Bot!\n\n"
        "Your source for crypto news, market updates, and airdrops."
    )


async def trending(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.coingecko.com/api/v3/search/trending"

    try:
        data = requests.get(url).json()

        message = "🔥 Trending Coins\n\n"

        for i, coin in enumerate(data["coins"], start=1):
            item = coin["item"]
            message += f"{i}. {item['name']} ({item['symbol']})\n"

        message += "\n🚀 Powered by Crypto Saga"

        await update.message.reply_text(message)

    except Exception:
        await update.message.reply_text(
            "❌ Unable to fetch trending coins right now."
        )


async def market(context: ContextTypes.DEFAULT_TYPE):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"

    data = requests.get(url).json()

    btc = data["bitcoin"]["usd"]
    eth = data["ethereum"]["usd"]

    text = (
        "📊 *Crypto Market Update*\n\n"
        f"🟠 Bitcoin: ${btc:,}\n"
        f"🔵 Ethereum: ${eth:,}\n\n"
        "🚀 Powered by Crypto Saga"
    )

    await context.bot.send_message(
        chat_id=CHANNEL,
        text=text,
        parse_mode="Markdown"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("trending", trending))

    app.job_queue.run_repeating(
        market,
        interval=3600,
        first=10
    )

    print("Crypto Saga Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
