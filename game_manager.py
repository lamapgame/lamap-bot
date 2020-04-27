'''
game manager
'''
import logging


class GameManager(object):
    def __init__(self):
        super().__init__()
        self.chatid_games = dict()
        self.userid_players = dict()
        self.userid_current = dict()
        self.remind_dict = dict()

        self.logger = logging.getLogger(__name__)

        def new_game(self, chat):
            """Create new game in chat"""
            chat_id = chat.id

            self.logger.debug(f"Creating new game in chat {chatid}")
            game = "a game starts"
            if chat_id not in self.chatid_games:
                self.chatid_games[chat_id] = list()

            # remove old games
            for g in list(self.chatid_games[chat_id]):
                if not g.players:
                    self.chatid_games[chat_id].remove(g)

            self.chatid_games[chat_id].append(game)
            return game
