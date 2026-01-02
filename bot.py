import sqlite3
from datetime import datetime, timedelta
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    ConversationHandler, ContextTypes, filters
)

# ===================== SOZLAMALAR =====================
TOKEN = "8485717621:AAFG-uTaq3OBbMis0tBVNxRZVDbKOZos4hA"   
ADMINS = [5234451700]

# ===================== DATABASE ======================
conn = sqlite3.connect("database.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
    telegram_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    birthday TEXT,
    phone TEXT,
    address TEXT
)
""")

conn.commit()

# ===================== STATES ========================
FIRST_NAME, LAST_NAME, BIRTHDAY, PHONE, ADDRESS = range(5)

# ===================== MENYU =========================
def client_menu():
    return ReplyKeyboardMarkup(
        [["🛒 Buyurtma berish"], ["💳 Mening qarzim"]],
        resize_keyboard=True
    )

# ===================== START =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    cur.execute("SELECT first_name FROM users WHERE telegram_id=?", (uid,))
    user = cur.fetchone()

    if user:
        await update.message.reply_text(
            f"Assalomu alaykum, {user[0]} 😊",
            reply_markup=client_menu()
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("Ismingizni kiriting:")
        return FIRST_NAME

# ===================== REGISTRATSIYA =================
async def reg_first(update, context):
    context.user_data["first_name"] = update.message.text
    await update.message.reply_text("Familiyangizni kiriting:")
    return LAST_NAME

async def reg_last(update, context):
    context.user_data["last_name"] = update.message.text
    await update.message.reply_text("Tug‘ilgan sana (DD.MM.YYYY):")
    return BIRTHDAY

async def reg_birth(update, context):
    context.user_data["birthday"] = update.message.text
    await update.message.reply_text("Telefon raqam:")
    return PHONE

async def reg_phone(update, context):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Manzil:")
    return ADDRESS

async def reg_address(update, context):
    d = context.user_data
    cur.execute(
        "INSERT INTO users VALUES (?,?,?,?,?,?)",
        (
            update.effective_user.id,
            d["first_name"],
            d["last_name"],
            d["birthday"],
            d["phone"],
            update.message.text
        )
    )
    conn.commit()

    await update.message.reply_text(
        "Ro‘yxatdan o‘tdingiz ✅",
        reply_markup=client_menu()
    )
    return ConversationHandler.END

# ===================== MAIN ==========================
def main():
    print("BOT ISHGA TUSHDI")

    app = ApplicationBuilder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_first)],
            LAST_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_last)],
            BIRTHDAY: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_birth)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_phone)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_address)],
        },
        fallbacks=[]
    )

    app.add_handler(conv)
    app.run_polling()

# ===================== RUN ===========================
if __name__ == "__main__":
    main()