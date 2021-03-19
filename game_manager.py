'''
game manager
'''
import logging
from game import Game
from player import Player
from errors import AlreadyJoinedError, LobbyClosedError, NoGameInChatError, NotEnoughPlayersError, GameAlreadyStartedError, MaxPlayersReached, AlreadyGameInChat, NotEnoughNkap
from stats import has_enough_nkap


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

        if not has_enough_nkap(user.id, game.bet):
            raise NotEnoughNkap()

        if not game.open:
            raise LobbyClosedError()
        if game.started:
            raise GameAlreadyStartedError()

        if user.id not in self.userid_players:
            self.userid_players[user.id] = list()

        players = self.userid_players[user.id]

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
        player = self.player_for_user_in_chat(user, chat)

        if not player:
            raise NoGameInChatError

        game = player.game

        # Find the correct game instance to end
        for player_in_game in game.players:
            this_users_players = self.userid_players.get(
                player_in_game.user.id, list())

            try:
                this_users_players.remove(player_in_game)
            except ValueError:
                pass

            if this_users_players:
                try:
                    self.userid_current[player_in_game.user.id] = this_users_players[0]
                except KeyError:
                    pass
            else:
                try:
                    del self.userid_players[player_in_game.user.id]
                except KeyError:
                    pass

                try:
                    del self.userid_current[player_in_game.user.id]
                except KeyError:
                    pass
        try:
            self.chatid_games[chat.id].clear()
        except ValueError:
            pass

        if not self.chatid_games[chat.id]:
            del self.chatid_games[chat.id]

        game.end()
        self.logger.info("END GAME in chat " + str(chat.id))

    def leave_game(self, user, chat):
        """ Remove a player from its current game """

        player = self.player_for_user_in_chat(user, chat)

        try:
            game = self.chatid_games[chat.id][-1]
        except (KeyError, IndexError):
            raise NoGameInChatError()

        game.remove_player(player)

        ''' if player:
            games = self.chatid_games[chat.id]
            for g in games:
                for p in g.players:
                    if p.user.id == user.id:
                        if p is g.current_player:
                            g.turn()
                        g.players.remove(p)
                        return '''

        if len(game.players) < 2:
            raise NotEnoughPlayersError()

        ''' if player is game.current_player:
            if game.next_player == 0:
                game.turn_to_controler()
            else:
                game.turn() '''

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
