"""
Some utils shared amoung the app module
"""

from telegram import Update


async def send_reply_message(update: Update, message: str):
    """util function way to reply to a user"""
    if update.message:
        return await update.message.reply_text(
            message, reply_to_message_id=update.message.message_id
        )


def mention(title, link):
    """mention (tag) a telegram user"""
    if link:
        return f"[{title}]({link})"
    else:
        return f"{title}"


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
