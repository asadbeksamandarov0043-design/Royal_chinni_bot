import sqlite3
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

TOKEN = "8485717621:AAFG-uTaq3OBbMis0tBVNxRZVDbKOZos4hA"

# ====== DATABASE ======
conn = sqlite3.connect("database.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    birthday TEXT,
    phone1 TEXT,
    phone2 TEXT,
    address TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    product TEXT,
    quantity TEXT,
    payment TEXT
)
""")
conn.commit()

# ====== STATES ======
(
    FIRST_NAME, LAST_NAME, BIRTHDAY,
    PHONE1, PHONE2, ADDRESS,
    PRODUCT, QUANTITY, PAYMENT, DEBT_TIME
) = range(10)

# ====== START ======
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    cur.execute("SELECT first_name FROM users WHERE telegram_id=?", (user_id,))
    user = cur.fetchone()

    if user:
        await update.message.reply_text(
            f"Assalomu alaykum, {user[0]} 😊\n"
            "Bugun sizga qanday yordam bera olaman?",
            reply_markup=main_menu()
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "Assalomu alaykum 😊\n"
            "Avval tanishib olaylik.\n\n"
            "Ismingizni kiriting:"
        )
        return FIRST_NAME

# ====== REGISTRATION ======
async def first_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["first_name"] = update.message.text
    await update.message.reply_text("Familiyangizni kiriting:")
    return LAST_NAME

async def last_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["last_name"] = update.message.text
    await update.message.reply_text("Tug‘ilgan sanangizni kiriting (DD.MM.YYYY):")
    return BIRTHDAY

async def birthday(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["birthday"] = update.message.text
    await update.message.reply_text("Telefon raqamingizni kiriting:")
    return PHONE1

async def phone1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone1"] = update.message.text
    await update.message.reply_text("Ikkinchi telefon raqam (bo‘sh qoldirsa bo‘ladi):")
    return PHONE2

async def phone2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone2"] = update.message.text
    await update.message.reply_text("Manzilingizni kiriting:")
    return ADDRESS

async def address(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = context.user_data
    cur.execute("""
        INSERT INTO users VALUES (?,?,?,?,?,?,?)
    """, (
        update.effective_user.id,
        data["first_name"],
        data["last_name"],
        data["birthday"],
        data["phone1"],
        data["phone2"],
        update.message.text
    ))
    conn.commit()

    await update.message.reply_text(
        f"Rahmat, {data['first_name']} 😊\n"
        "Ma’lumotlaringiz saqlandi.",
        reply_markup=main_menu()
    )
    return ConversationHandler.END

# ====== MENU ======
def main_menu():
    return ReplyKeyboardMarkup(
        [["🛒 Buyurtma berish"]],
        resize_keyboard=True
    )

# ====== ORDER ======
async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Qaysi mahsulotni olmoqchisiz?")
    return PRODUCT

async def product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["product"] = update.message.text
    await update.message.reply_text("Nechta dona?")
    return QUANTITY

async def quantity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["quantity"] = update.message.text