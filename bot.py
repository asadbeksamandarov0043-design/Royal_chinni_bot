# ===================== QARZ ==========================
async def qarz_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    cur.execute(
        "SELECT SUM(debt) FROM orders WHERE telegram_id=? AND is_closed=0",
        (uid,)
    )
    debt = cur.fetchone()[0]

    if debt and debt > 0:
        await update.message.reply_text(f"💳 Sizning qarzingiz: {debt} so‘m")
    else:
        await update.message.reply_text("✅ Sizda qarz yo‘q")

# ===================== MAIN ==========================
def main():
    print("BOT ISHGA TUSHDI")

    app = ApplicationBuilder().token(TOKEN).build()

    reg_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_name)],
            LAST: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_last)],
            BIRTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_birth)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_phone)],
            ADDRESS: [MessageHandler(filters.TEXT & ~filters.COMMAND, reg_address)],
        },
        fallbacks=[]
    )

    app.add_handler(reg_handler)

    app.add_handler(MessageHandler(
        filters.Regex("^🛒 Buyurtma berish$"),
        buyurtma_handler
    ))

    app.add_handler(MessageHandler(
        filters.Regex("^📄 Mening qarzim$"),
        qarz_handler
    ))

    app.run_polling()

if __name__ == "__main__":
    main()