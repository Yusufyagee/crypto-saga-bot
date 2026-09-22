from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from datetime import time
import requests
import os
import feedparser

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@cryptosaga0"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 Welcome to Crypto Saga Bot!\n\n"
        "Your source for crypto news, market updates and airdrops."
    )


# 📊 Market Update
async def market(context: ContextTypes.DEFAULT_TYPE):

    url = (
        "https://api.coingecko.com/api/v3/simple/price?"
        "ids=bitcoin,ethereum,binancecoin,tron,solana,avalanche-2,"
        "sui,the-open-network,ripple,cardano,dogecoin,chainlink,"
        "aptos,near"
        "&vs_currencies=usd"
        "&include_24hr_change=true"
    )

    try:
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

        message = "📊 *CRYPTO SAGA MARKET UPDATE* 🚀\n\n"

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

    except Exception as e:
        print("Market Error:", e)



# 📰 Crypto News
async def crypto_news(context: ContextTypes.DEFAULT_TYPE):

    try:
        news = feedparser.parse(
            "https://cointelegraph.com/rss"
        )

        message = "📰 *CRYPTO SAGA NEWS UPDATE* 🚀\n\n"

        for item in news.entries[:5]:
            message += f"🔹 {item.title}\n\n"

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

    except Exception as e:
        print("News Error:", e)



# 🎁 Airdrop & Testnet Alerts
async def airdrop_alerts(context: ContextTypes.DEFAULT_TYPE):

    try:
        feed = feedparser.parse(
            "https://coinmarketcap.com/community/rss/latest/"
        )

        message = "🎁 *CRYPTO SAGA AIRDROP & TESTNET ALERTS* 🚀\n\n"

        found = 0

        for item in feed.entries:

            title = item.title.lower()

            if (
                "airdrop" in title
                or "testnet" in title
                or "mainnet" in title
            ):
                message += f"🔹 {item.title}\n\n"
                found += 1

            if found == 5:
                break

        if found == 0:
            message += "No major alerts found today 🔍"

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

    except Exception as e:
        print("Airdrop Error:", e)



def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))


    # 📊 Market Updates
    app.job_queue.run_daily(
        market,
        time=time(hour=8, minute=0)
    )

    app.job_queue.run_daily(
        market,
        time=time(hour=14, minute=0)
    )

    app.job_queue.run_daily(
        market,
        time=time(hour=20, minute=0)
    )


    # 📰 News
    app.job_queue.run_daily(
        crypto_news,
        time=time(hour=12, minute=0)
    )


    # 🎁 Airdrops/Testnets
    app.job_queue.run_daily(
        airdrop_alerts,
        time=time(hour=16, minute=0)
    )


    print("🚀 Crypto Saga Bot is running...")
    app.run_polling()



if __name__ == "__main__":
    main()
