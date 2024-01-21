# How to Contribute

## Getting Started

1. Talk with [@BotFather](https://t.me/botfather) on telegram.
1. Create a new bot and generate a Token
1. Enable `/setinline` and `/setinlinefeedback` on @BotFather
1. Enter your Token in your `.env` file.

## Development

### CodeSpaces (Easier & Faster) 🚀
1. Open the Codespace from the Github Repository. Code -> Codespaces -> Create Codespace
2. Everything is already setup in the codespace config.
3. Install recommended extensions (OPTIONAL, but good to have)

### Local
1. Clone this repo
2. Make sure you have Poetry (if not `pip install poetry`)
3. Install dependencies with `poetry install --no-root`

Copy `.env.example` in a `.env` file. Fill in your tokens and variables.

### Debugging the bot

The app is already perfectly setup for VSCode debuggers

VSCode debuggers works well in this case, you may use it. To further ease debugging experience, you'd set up a debug configuration like the one below. It'll help you reload just by pressing `CTRL+SHIFT+F5`

## Running the bot

1. Run `python bot.py` in prod.
2. <kbd>CTRL</kbd> <kbd>SHIFT</kbd> <kbd>F5</kbd>

ping [@panachaud](https:t.me/panachaud) in case you need any help in getting setup
