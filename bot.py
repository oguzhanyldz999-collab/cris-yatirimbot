
import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

COINS = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "qubic": "QUBIC",
    "solana": "SOL",
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 CRISYATIRIM bot aktif!\n\n"
        "/piyasa - Güncel piyasa fiyatlarını gösterir."
    )

async def piyasa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        
        params = {
            "ids": ",".join(COINS.keys()),
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        mesaj = "📊 CRISYATIRIM PİYASA\n\n"

        for coin_id, sembol in COINS.items():
            coin = data.get(coin_id)

            if not coin:
                continue

            fiyat = coin.get("usd", 0)
            degisim = coin.get("usd_24h_change", 0) or 0

            emoji = "🟢" if degisim >= 0 else "🔴"

            mesaj += (
                f"{emoji} {sembol}: ${fiyat:,.6f}\n"
                f"24S: {degisim:+.2f}%\n\n"
            )

        await update.message.reply_text(mesaj)

    except Exception as e:
        await update.message.reply_text(
            f"❌ Veri alınırken hata oluştu:\n{e}"
        )

def main():
    if not TOKEN:
        raise ValueError("BOT_TOKEN bulunamadı!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("piyasa", piyasa))

    print("🤖 CRISYATIRIM bot başlatıldı...")
    app.run_polling()

if __name__ == "__main__":
    main()
