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

ENABLE_REMINDERS = True
ENABLE_BIRTHDAY = True

# ===================== DATABASE ======================
conn = sqlite3.connect("database.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS users(
    telegram_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    birthday TEXT,
    phone TEXT,
    address TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    total INTEGER,
    debt INTEGER,
    due_date TEXT,
    is_closed INTEGER DEFAULT 0,
    created_at TEXT
)""")

cur.execute("""CREATE TABLE IF NOT EXISTS payments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    amount INTEGER,
    created_at TEXT
)""")

conn.commit()

# ===================== MENYULAR ======================
def client_menu():
    return ReplyKeyboardMarkup([
        ["🛒 Buyurtma berish"],
        ["💳 Mening qarzim"],
        ["💳 Qarzimni to‘ladim"]
    ], resize_keyboard=True)

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
        await update.message.reply_text("Ismingizni yozing:")
        return 1

# ===================== RO‘YXAT ======================
async def reg_name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Familiyangiz:")
    return 2

async def reg_last(update, context):
    context.user_data["last"] = update.message.text
    await update.message.reply_text("Tug‘ilgan sana (DD.MM.YYYY):")
    return 3

async def reg_birth(update, context):
    context.user_data["birth"] = update.message.text
    await update.message.reply_text("Telefon raqam:")
    return 4

async def reg_phone(update, context):
    context.user_data["phone"] = update.message.text
    await update.message.reply_text("Manzil:")
    return 5

async def reg_address(update, context):
    d = context.user_data
    cur.execute(
        "INSERT INTO users VALUES (?,?,?,?,?,?)",
        (update.effective_user.id, d["name"], d["last"], d["birth"], d["phone"], update.message.text)
    )
    conn.commit()
    await update.message.reply_text("Ro‘yxatdan o‘tdingiz ✅", reply_markup=client_menu())
    return ConversationHandler.END

# ===================== BUYURTMA ======================
async def order(update, context):
    context.user_data["total"] = 100_000  # test summa
    context.user_data["debt"] = context.user_data["total"]
    await update.message.reply_text("Qarz muddati? (5 yoki 10)")
    return 6

async def order_days(update, context):
    days = int(update.message.text)
    due = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
    cur.execute("""
        INSERT INTO orders (telegram_id,total,debt,due_date,created_at)
        VALUES (?,?,?,?,?)
    """, (
        update.effective_user.id,
        context.user_data["total"],
        context.user_data["debt"],
        due,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()
    await update.message.reply_text("Buyurtma qabul qilindi ✅", reply_markup=client_menu())
    return ConversationHandler.END
if __name__ == "__main__":
    main()