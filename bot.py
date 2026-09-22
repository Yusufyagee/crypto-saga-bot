
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
        "aptos,near&vs_currencies=usd"
    )

    data = requests.get(url).json()

    text = f"""
📊 *CRYPTO SAGA MARKET UPDATE*

🟠 BTC : ${data['bitcoin']['usd']:,}
🔵 ETH : ${data['ethereum']['usd']:,}
🟡 BNB : ${data['binancecoin']['usd']:,}
🔴 TRX : ${data['tron']['usd']:,}
🟣 SOL : ${data['solana']['usd']:,}
🔺 AVAX : ${data['avalanche-2']['usd']:,}
⚫ SUI : ${data['sui']['usd']:,}
🔵 TON : ${data['the-open-network']['usd']:,}
🔷 XRP : ${data['ripple']['usd']:,}
🟢 ADA : ${data['cardano']['usd']:,}
🐶 DOGE : ${data['dogecoin']['usd']:,}
🔗 LINK : ${data['chainlink']['usd']:,}
🟡 APT : ${data['aptos']['usd']:,}
🟢 NEAR : ${data['near']['usd']:,}

━━━━━━━━━━━━━━━━━━
🚀 @cryptosaga0
Learn • Earn • Grow
"""

    await context.bot.send_message(
        chat_id=CHANNEL,
        text=text,
        parse_mode="Markdown"
    )

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    # Post every hour
    app.job_queue.run_repeating(
        market,
        interval=3600,
        first=10
    )

    print("Crypto Saga Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
