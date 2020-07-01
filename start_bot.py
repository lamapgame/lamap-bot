from config import TOKEN, HEROKU_URL, HEROKU_PORT
import sys


def start_bot(updater):
    if sys.argv[1] == "prod":
        updater.start_webhook(
            listen="0.0.0.0", port=HEROKU_PORT, url_path=TOKEN)
        updater.bot.setWebhook(HEROKU_URL + TOKEN)
    else:
        updater.start_polling()
