from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@cryptosaga0"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to Crypto Saga Bot!\n\n"
        "Your source for crypto news, market updates and airdrops."
    )


async def market(context: ContextTypes.DEFAULT_TYPE):
    url = (
        "https://api.coingecko.com/api/v3/simple/price?"
        "ids=bitcoin,ethereum,binancecoin,tron,solana,avalanche-2,"
        "sui,the-open-network,ripple,cardano,dogecoin,chainlink,"
        "aptos,near"
        "&vs_currencies=usd"
        "&include_24hr_change=true"
    )

    data = requests.get(url, timeout=10).json()

    coins = [
        ("🟠 BTC", "bitcoin"),
        ("🔵 ETH", "ethereum"),
        ("🟡 BNB", "binancecoin"),
        ("🔴 TRX", "tron"),
        ("🟣 SOL", "solana"),
        ("🔺 AVAX", "avalanche-2"),
        ("⚫ SUI", "sui"),
        ("🔵 TON", "the-open-network"),
        ("🔷 XRP", "ripple"),
        ("🟢 ADA", "cardano"),
        ("🐶 DOGE", "dogecoin"),
        ("🔗 LINK", "chainlink"),
        ("🟡 APT", "aptos"),
        ("🟢 NEAR", "near")
    ]

    message = "📊 *CRYPTO SAGA MARKET UPDATE*\n\n"

    for label, key in coins:
        price = data[key]["usd"]
        change = data[key]["usd_24h_change"]

        arrow = "🟢 ▲" if change >= 0 else "🔴 ▼"

        message += (
            f"{label}: ${price:,.2f}\n"
            f"{arrow} {change:.2f}% (24h)\n\n"
        )

    message += (
        "━━━━━━━━━━━━━━━━━━\n"
        "🚀 @cryptosaga0\n"
        "Learn • Earn • Grow"
    )

    await context.bot.send_message(
        chat_id=CHANNEL,
        text=message,
        parse_mode="Markdown"
    )


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Automatic market update every hour
    app.job_queue.run_repeating(
        market,
        interval=3600,
        first=10
    )

    print("🚀 Crypto Saga Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
