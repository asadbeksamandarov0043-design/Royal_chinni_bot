await update.message.reply_text("Buyurtma qabul qilindi ✅", reply_markup=client_menu())
    return ConversationHandler.END

# ===================== QARZ =====================
async def my_debt(update, context):
    uid = update.effective_user.id
    cur.execute("SELECT SUM(debt) FROM orders WHERE telegram_id=? AND debt>0", (uid,))
    debt = cur.fetchone()[0] or 0
    await update.message.reply_text(f"💳 Jami qarzingiz: {debt:,} so‘m")

async def pay_debt(update, context):
    await update.message.reply_text("Qancha summa to‘ladingiz?")
    return PAY_AMOUNT

async def save_payment(update, context):
    amount = int(update.message.text)
    uid = update.effective_user.id

    cur.execute(
        "SELECT id,debt FROM orders WHERE telegram_id=? AND debt>0 ORDER BY id LIMIT 1",
        (uid,)
    )
    order = cur.fetchone()
    if not order:
        await update.message.reply_text("Qarz topilmadi")
        return ConversationHandler.END

    oid, debt = order
    new_debt = max(debt - amount, 0)

    cur.execute(
        "UPDATE orders SET debt=?, is_closed=? WHERE id=?",
        (new_debt, 1 if new_debt == 0 else 0, oid)
    )
    cur.execute(
        "INSERT INTO payments VALUES (NULL,?,?,?)",
        (oid, amount, datetime.now().strftime("%Y-%m-%d %H:%M"))
    )
    conn.commit()

    await update.message.reply_text("To‘lov qabul qilindi ✅", reply_markup=client_menu())
    return ConversationHandler.END

# ===================== ESLATMA =====================
async def reminders(app):
    if not ENABLE_REMINDERS:
        return

    today = datetime.now().date()
    cur.execute("SELECT telegram_id,debt,due_date FROM orders WHERE debt>0")
    for uid, debt, due in cur.fetchall():
        days = (datetime.strptime(due, "%Y-%m-%d").date() - today).days
        if days in (3, 1, 0):
            await app.bot.send_message(
                uid,
                f"⚠️ Qarzingiz: {debt:,} so‘m\n⏰ {days} kun qoldi"
            )

# ===================== TUG‘ILGAN KUN =====================
async def birthdays(app):
    if not ENABLE_BIRTHDAY:
        return

    today = datetime.now().strftime("%d.%m")
    cur.execute("SELECT telegram_id,first_name FROM users WHERE birthday LIKE ?", (f"{today}%",))
    for uid, name in cur.fetchall():
        await app.bot.send_message(uid, f"🎉 {name}, tug‘ilgan kuningiz bilan!")

# ===================== MAIN =====================
def main():
    print("BOT ISHGA TUSHDI")

    app = ApplicationBuilder().token(TOKEN).build()

    app.job_queue.run_repeating(reminders, interval=86400, first=10)
    app.job_queue.run_repeating(birthdays, interval=86400, first=20)

    app.add_handler(ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            REG_NAME: [MessageHandler(filters.TEXT, reg_name)],
            REG_LAST: [MessageHandler(filters.TEXT, reg_last)],
            REG_BIRTH: [MessageHandler(filters.TEXT, reg_birth)],
            REG_PHONE: [MessageHandler(filters.TEXT, reg_phone)],
            REG_ADDRESS: [MessageHandler(filters.TEXT, reg_address)],
        },
        fallbacks=[]
    ))

    app.add_handler(ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("🛒 Buyurtma berish"), order)],
        states={ORDER_DAYS: [MessageHandler(filters.TEXT, order_days)]},
        fallbacks=[]
    ))

    app.add_handler(MessageHandler(filters.Regex("💳 Mening qarzim"), my_debt))

    app.add_handler(ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("💳 Qarzimni to‘ladim"), pay_debt)],
        states={PAY_AMOUNT: [MessageHandler(filters.TEXT, save_payment)]},
        fallbacks=[]
    ))

    app.run_polling()

if __name__ == "__main__":
    main()