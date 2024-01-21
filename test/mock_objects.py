from telegram.ext import ContextTypes
from telegram.ext import ApplicationBuilder, Defaults
from telegram.constants import ParseMode
from telegram import Update, User
from player import Player

from test.conftest import TEST_TOKEN


app = (
    ApplicationBuilder()
    .defaults(Defaults(ParseMode.MARKDOWN))
    .token(TEST_TOKEN)
    .build()
)

mocked_message_update = Update(update_id=12345)

mocked_context = ContextTypes.DEFAULT_TYPE(app)

mocked_user = User(id=123, first_name="Test", is_bot=False)


# Dummy data
user1 = User(id=1, first_name="Ateba", is_bot=False)
user2 = User(id=2, first_name="Bassogog", is_bot=False)
user3 = User(id=3, first_name="Chokote", is_bot=False)
user4 = User(id=3, first_name="Donfack", is_bot=False)
user5 = User(id=3, first_name="Essani", is_bot=False)
player1 = Player(user1)
player2 = Player(user2)
player3 = Player(user3)
player4 = Player(user4)
player5 = Player(user5)
