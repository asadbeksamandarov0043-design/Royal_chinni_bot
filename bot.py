cur.execute("""
        INSERT INTO orders (telegram_id, total, debt, due_date, created_at)
        VALUES (?,?,?,?,?)
    """, (
        update.effective_user.id,
        total,
        total,
        due,
        datetime.now().strftime("%Y-%m-%d %H:%M")
    ))
    conn.commit()

    await update.message.reply_text(
        "Buyurtma qabul qilindi ✅",
        reply_markup=client_menu()
    )
    return ConversationHandler.END

# ===================== QARZ ======================
async def my_debt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    cur.execute(
        "SELECT SUM(debt) FROM orders WHERE telegram_id=?",
        (uid,)
    )
    debt = cur.fetchone()[0] or 0

    await update.message.reply_text(f"Jami qarzingiz: {debt} so‘m")

# ===================== MAIN ======================
def main():
    print("BOT ISHGA TUSHDI")

    app = ApplicationBuilder().token(TOKEN).build()

    reg_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            FIRST_NAME: [MessageHandler(filters.TEXT, reg_first)],
            LAST_NAME: [MessageHandler(filters.TEXT, reg_last)],
            BIRTHDAY: [MessageHandler(filters.TEXT, reg_birth)],
            PHONE: [MessageHandler(filters.TEXT, reg_phone)],
            ADDRESS: [MessageHandler(filters.TEXT, reg_address)],
        },
        fallbacks=[]
    )

    order_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("🛒 Buyurtma berish"), order_start)],
        states={
            DEBT_DAYS: [MessageHandler(filters.TEXT, order_days)]
        },
        fallbacks=[]
    )

    app.add_handler(reg_handler)
    app.add_handler(order_handler)
    app.add_handler(MessageHandler(filters.Regex("💳 Mening qarzim"), my_debt))

    app.run_polling()

# ===================== RUN =======================
if __name__ == "__main__":
    main()