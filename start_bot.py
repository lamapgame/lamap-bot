from config import TOKEN, HEROKU_URL
import os
import sys
PORT = int(os.environ.get('PORT', 5000))


def start_bot(updater):
    if sys.argv[1] == "prod":
        updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
        updater.bot.setWebhook(HEROKU_URL + TOKEN)
    else:
        updater.start_polling()
