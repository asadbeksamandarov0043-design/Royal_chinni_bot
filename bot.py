from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN="8485717621:AAFG-uTaq3OBbMis0tBVNxRZVDbKOZos4hA"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("START keldi")
    await update.message.reply_text("Royal Chinni bot ishlayapti ✅")

def main():
    print("BOT ISHGA TUSHDI")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if__name__=="__main__": 





    main()