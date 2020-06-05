# How to Contribute

## Setup

1. `git clone --this-repo`
1. Talk with [@BotFather](https://t.me/botfather) on telegram.
1. Create a new bot and generate a Token
1. activate /setinline and /setinlinefeedback on @BotFather
1. Enter your token in your `config.json` file.
1. Install requirements (usage of virtualenv is recommended): `pip install -r requirements.txt`

## Development

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
	"console": "internalConsole"
}
```
