from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters
)

TOKEN = "8485717621:AAFG-uTaq3OBbMis0tBVNxRZVDbKOZos4hA"

# Buyurtma bosqichlari
PRODUCT, QUANTITY = range(2)

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

async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📦 Buyurtma berish boshlandi.\n"
        "Qaysi mahsulotni olmoqchisiz?"
    )
    return PRODUCT

async def product_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["product"] = update.message.text
    await update.message.reply_text(
        "Nechta dona olmoqchisiz?"
    )
    return QUANTITY

async def quantity_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quantity"] = update.message.text

    product = context.user_data["product"]
    quantity = context.user_data["quantity"]

    await update.message.reply_text(
        "✅ Buyurtma qabul qilindi!\n\n"
        f"📦 Mahsulot: {product}\n"
        f"🔢 Soni: {quantity}\n\n"
        "Tez orada operator siz bilan bog‘lanadi."
    )

    return ConversationHandler.END

def main():
    print("BOT ISHGA TUSHDI")

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^📦 Buyurtma berish$"), order_start)],
        states={
            PRODUCT: [MessageHandler(filters.TEXT & ~filters.COMMAND, product_step)],
            QUANTITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, quantity_step)],
        },
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv_handler)

    app.run_polling()

if __name__ == "__main__":
    main()