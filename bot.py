from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import interactions

from tlgrm.utils import send_reply_message
from config import token


async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if (update.effective_user):
      await send_reply_message(update, f'Hello {update.effective_user.first_name}')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await interactions.INIT_USER(update)

async def learn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  await interactions.LEARN(update)

app = ApplicationBuilder().token(token).build()


# Bot command handlers
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("learn", learn))
app.add_handler(CommandHandler("hello", hello))

app.run_polling()