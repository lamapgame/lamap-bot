"""
Some utils shared amoung the app module
"""
from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError

from config import LOGGING_CHAT_ID


async def send_reply_message(update: Update, message: str):
    """util function way to reply to a user"""
    if update.message:
        return await update.message.reply_text(
            message, reply_to_message_id=update.message.message_id
        )


async def log_admin(
    message: str,
    context: ContextTypes.DEFAULT_TYPE,
    thread_id: int | None = None,
) -> None:
    """Logs the message to the logging chat"""
    try:
        await context.bot.send_message(
            chat_id=LOGGING_CHAT_ID,
            text=message,
            disable_web_page_preview=True,
            parse_mode="MarkdownV2",
            message_thread_id=thread_id,
        )
    except TelegramError as e:
        print(e)
        # bot might not be able to message admin group
        # its alright, we will just ignore it
        # it will work in prod ;)
        # pass


def mention(title, link, v2: bool = False):
    """mention (tag) a telegram user"""
    if v2:
        v2ize(title)
    if link:
        return f"[{title}]({link})"
    else:
        return f"{title}"


def v2ize(text: str) -> str:
    """escape invalid markdown characters"""
    for char in [
        "_",
        "*",
        "[",
        "]",
        "(",
        ")",
        "~",
        "`",
        ">",
        "#",
        "+",
        "-",
        "=",
        "|",
        "{",
        "}",
        ".",
        "!",
    ]:
        text = text.replace(char, f"\\{char}")
    return text


def n_format(num):
    """transform numbers to n format (3k = 3 kolos, 1M = baton... and so on)"""
    # pylint: disable=consider-using-f-string
    num = float("{:.3g}".format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return "{}{}".format(
        "{:f}".format(num).rstrip("0").rstrip("."),
        ["", " kolos", " bâtons", " myondos", " mitoumba"][magnitude],
    )


def ascii_art() -> None:
    """print the ascii art logo"""
    print("""""")
