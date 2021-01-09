'''
game manager
'''
import logging
from game import Game
from player import Player
from errors import AlreadyJoinedError, LobbyClosedError, NoGameInChatError, NotEnoughPlayersError, GameAlreadyStartedError, MaxPlayersReached, AlreadyGameInChat, NotEnoughNkap
from stats import get_nkap
from nkap import has_enough_nkap


class GameManager(object):
    def __init__(self):
        super().__init__()
        self.chatid_games = dict()
        self.userid_players = dict()
        self.userid_current = dict()
        self.remind_dict = dict()
        self.start_gm_msgs = dict()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def new_game(self, chat):
        """Create new game in chat"""
        chat_id = chat.id
        game = Game(chat)
        if chat_id not in self.chatid_games:
            self.chatid_games[chat_id] = list()
            self.start_gm_msgs[chat_id] = list()

        # do not start another if there's already one going on
        if len(self.chatid_games[chat_id]) >= 1:
            raise AlreadyGameInChat()

        # remove old games
        self.chatid_games[chat_id] = []
        self.start_gm_msgs[chat_id].clear()
        self.chatid_games[chat_id].append(game)

        self.logger.info(f"NEW GAME in chat {chat_id}")
        return game

    def join_game(self, user, chat):
        """Create a player from the Telegram user info and add to current game"""
        try:
            game = self.chatid_games[chat.id][-1]
        except (KeyError, IndexError):
            raise NoGameInChatError()
        if game.nkap:
            if not has_enough_nkap(get_nkap(user.id), game.bet):
                raise NotEnoughNkap()
        if not game.open:
            raise LobbyClosedError()
        if game.started:
            raise GameAlreadyStartedError()

        # Don't add a player if the max is reached
        if len(game.players) == game.max_players:
            raise MaxPlayersReached()

        # Don't re-add a player if he is already one of them
        for user_player in list(map(lambda x: x.user, game.players)):
            if user.id == user_player.id:
                raise AlreadyJoinedError()

        player = Player(game, user)
        game.players.append(player)

        self.userid_current[user.id] = player
        self.logger.info(
            f"NEW PLAYER - {user.id} on game in the group: {chat.id}")

        # start game when the max no of players joined
        if len(game.players) == game.max_players:
            self.logger.info(f"MAX PLAYERS ({game.max_players}) in {chat.id}")

    def end_game(self, chat, user):
        """
        End a game
        """
        # Find the correct game instance to end
        try:
            self.userid_current.clear()  # todo! make remove player possible
            self.chatid_games[chat.id].clear()
        except ValueError:
            pass

        if not self.chatid_games[chat.id]:
            del self.chatid_games[chat.id]

        self.logger.info("END GAME in chat " + str(chat.id))

    def leave_game(self, user, chat):
        """ Remove a player from its current game """

        player = self.player_for_user_in_chat(user, chat)

        try:
            game = self.chatid_games[chat.id][-1]
        except (KeyError, IndexError):
            raise NoGameInChatError()

        players = game.players

        if not player:
            games = self.chatid_games[chat.id]
            for g in games:
                for p in g.players:
                    if p.user.id == user.id:
                        if p is g.current_player:
                            g.turn()
                        g.players.remove(p)
                        return

            raise NoGameInChatError()

        if len(game.players) < 2:
            raise NotEnoughPlayersError()

        if player is game.current_player:
            if game.next_player == 0:
                game.turn_to_controler()
            else:
                game.turn()

        players.remove(player)

    def player_for_user_in_chat(self, user, chat):
        try:
            game = self.chatid_games[chat.id][-1]
        except (KeyError, IndexError):
            raise NoGameInChatError()
        players = game.players
        for player in players:
            if player.game.chat.id == chat.id:
                return player
        return None
