# How to Contribute

## Getting Started

1. Talk with [@BotFather](https://t.me/botfather) on telegram.
1. Create a new bot and generate a Token
1. activate /setinline and /setinlinefeedback on @BotFather
1. Enter your token in your `config.json` file.

## Development

1. Clone this repo
2. Create your virtual environment using `python3 -m venv venv`
3. Activate your venv `venv\Scripts\activate` (on windows) check out [venv](https://docs.python.org/3/library/venv.html#module-venv) for UNIX.
4. Import the necessary packages using `pip install -r requirements.txt`

Most of the gameplay parameters would be preferably changed in `config.json`, it is recommended to check this file to get yours updated. I prepared a sample file which you could copy from.

## Debugging the bot

On VSCode you may go to `./bot.py` and tap `F5`.

VSCode debuggers works well in this case, you may use it. To further ease debugging experience, you'd set up a debug configuration like the one below. It'll help you reload just by pressing `CTRL+SHIFT+F5`

```json
{
 "name": "Python: Launch bot",
 "type": "python",
 "request": "launch",
 "program": "./bot.py",
 "console": "internalConsole",
 "args": ["dev"]
}
```

## Env Variables

The bot uses environment variables as token and reads two files, `.env.local` when in local dev and `.env.prod` when in prod. This helps the bot know what TOKEN to use.

It should contain `DATABASE_URL` which is the url to your Postgres db for example: `DATABASE_URL=postgresql://user:password@localhost:5432/lamapbot`
and `TOKEN` which is your telegram bot token

## Running the bot

1. Run `python bot.py prod` in prod.
2. `python bot.py dev` in local (with your own TOKEN in your .env.local file).

ping [@panachaud](https:t.me/panachaud) in case you need any help getting setup
