import os
PORT = int(os.environ.get('PORT', 5000))
HEROKU = 'https://afternoon-meadow-46045.herokuapp.com/'


def start_bot(updater):
    updater.start_webhook(listen="0.0.0.0", port=int(PORT), url_path=TOKEN)
    updater.bot.setWebhook(HEROKU + TOKEN)
