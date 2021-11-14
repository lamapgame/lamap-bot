web: python3 bot.py prod
web: gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app