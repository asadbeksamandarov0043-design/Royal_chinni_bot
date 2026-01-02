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
ADMIN_ID = 5234451700  

PRODUCT, QUANTITY = range(2)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["📦 Buyurtma berish"],
        ["ℹ️ Biz haqimizda", "📞 Aloqa"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "Salom 👋 Royal Chinni botiga xush kelibsiz!\n"
        "Buyurtma berish uchun tugmani bosing 👇",
        reply_markup=reply_markup
    )

async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Qaysi mahsulotni olmoqchisiz?")
    return PRODUCT

async def product_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["product"] = update.message.text
    await update.message.reply_text("Nechta dona olmoqchisiz?")
    return QUANTITY

async def quantity_step(update: Update, context: ContextTypes.DEFAULT_TYPE):
    product = context.user_data["product"]
    quantity = update.message.text

    user = update.message.from_user
    username = user.username or "username yo‘q"
    user_id = user.id

    # Mijozga javob
    await update.message.reply_text(
        "✅ Buyurtmangiz qabul qilindi!\n"
        "Tez orada siz bilan bog‘lanamiz."
    )

    # ADMIN ga yuborish
    admin_text = (
        "🛎 YANGI BUYURTMA!\n\n"
        f"👤 Foydalanuvchi: @{username}\n"
        f"🆔 ID: {user_id}\n"
        f"📦 Mahsulot: {product}\n"
        f"🔢 Soni: {quantity}"
    )

    await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text)

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

if name == "main":
    main()