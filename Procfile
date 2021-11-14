web: python3 bot.py prod
api: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app