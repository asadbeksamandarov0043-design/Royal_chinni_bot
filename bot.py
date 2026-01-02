from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN = "8485717621:AAFG-uTaq3OBbMis0tBVNxRZVDbKOZos4hA"

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📦 Buyurtma berish"],
        ["ℹ️ Biz haqimizda", "📞 Aloqa"]
    ]
    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_text(
        "Salom 👋\n"
        "Royal Chinni botiga xush kelibsiz!\n"
        "Quyidagi tugmalardan birini tanlang 👇",
        reply_markup=reply_markup
    )

# Tugmalarni ushlash
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📦 Buyurtma berish":
        await update.message.reply_text(
            "🛒 Buyurtma berish bo‘limi.\n"
            "Tez orada mahsulotlar qo‘shiladi."
        )

    elif text == "ℹ️ Biz haqimizda":
        await update.message.reply_text(
            "Royal Chinni — sifatli mahsulotlar va halol savdo 🏪"
        )

    elif text == "📞 Aloqa":
        await update.message.reply_text(
            "📞 Telefon: +998 90 000 00 00\n"
            "📍 Manzil: Bozor ichida"
        )

    else:
        await update.message.reply_text(
            "Iltimos, menyudagi tugmalardan foydalaning 👇"
        )

def main():
    print("BOT ISHGA TUSHDI")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, menu_handler))

    app.run_polling()

if __name__ == "__main__":
    main()