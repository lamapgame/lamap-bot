from config import TOKEN
import os
import sys
PORT = int(os.environ.get('PORT', 5000))
HEROKU = 'https://afternoon-meadow-46045.herokuapp.com/'


def start_bot(updater):
    if sys.argv[1] == "prod":
        updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
        updater.bot.setWebhook(HEROKU + TOKEN)
    else:
        updater.start_polling()
