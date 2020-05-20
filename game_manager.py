'''
game manager
'''
import logging
from game import Game
from player import Player
from errors import AlreadyJoinedError, LobbyClosedError, NoGameInChatError, NotEnoughPlayersError


class GameManager(object):
    def __init__(self):
        super().__init__()
        self.chatid_games = dict()
        self.userid_players = dict()
        self.userid_current = dict()
        self.remind_dict = dict()

        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.DEBUG)

    def new_game(self, chat):
        """Create new game in chat"""
        chat_id = chat.id
        self.logger.debug(f"Creating new game in chat {chat_id}")
        game = Game(chat)
        if chat_id not in self.chatid_games:
            self.chatid_games[chat_id] = list()

        # remove old games
        for g in list(self.chatid_games[chat_id]):
            if not g.players:
                self.chatid_games[chat_id].remove(g)

        self.chatid_games[chat_id].append(game)
        return game

    def join_game(self, user, chat):
        """Create a player from the Telegram user info and add to current game"""

        try:
            game = self.chatid_games[chat.id][-1]

        except (KeyError, IndexError):
            raise NoGameInChatError()

        if not game.open:
            raise LobbyClosedError()

        if user.id not in self.userid_players:
            self.userid_players[user.id] = list()

        players = self.userid_players[user.id]

        if len(players) == game.max_players:
            raise MaxPlayersReached()

        # Don't re-add a player and remove the player from previous games in
        # this chat, if he is in one of them
        for player in players:
            if player in game.players:
                raise AlreadyJoinedError()

        try:
            self.leave_game(user, chat)
        except NoGameInChatError:
            pass
        except NotEnoughPlayersError:
            self.end_game(chat, user)

            if user.id not in self.userid_players:
                self.userid_players[user.id] = list()

            players = self.userid_players[user.id]

        player = Player(game, user)
        if game.started:
            player.draw_first_hand()

        players.append(player)
        self.userid_current[user.id] = player
        self.logger.debug(
            f"NEW PLAYER - {user.id} on game in the group: {chat.id}")

    def end_game(self, chat, user):
        """
        End a game
        """

        self.logger.debug("Game in chat " + str(chat.id) + " ended")

        # Find the correct game instance to end
        player = self.player_for_user_in_chat(user, chat)

        if not player:
            raise NoGameInChatError

        game = player.game

        # Clear game
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
            self.chatid_games[chat.id].remove(game)
        except ValueError:
            pass
        if not self.chatid_games[chat.id]:
            del self.chatid_games[chat.id]

    def leave_game(self, user, chat):
        """ Remove a player from its current game """

        player = self.player_for_user_in_chat(user, chat)
        players = self.userid_players.get(user.id, list())

        if not player:
            games = self.chatid_games[chat.id]
            for g in games:
                for p in g.players:
                    if p.user.id == user.id:
                        if p is g.current_player:
                            g.turn()
                        p.leave()
                        return

            raise NoGameInChatError()

        game = player.game

        if len(game.players) < 3:
            raise NotEnoughPlayersError()

        if player is game.current_player:
            game.turn(None)

        player.leave()
        players.remove(player)

        # If this is the selected game, switch to another
        if self.userid_current.get(user.id, None) is player:
            if players:
                self.userid_current[user.id] = players[0]
            else:
                del self.userid_current[user.id]
                del self.userid_players[user.id]

    def player_for_user_in_chat(self, user, chat):
        players = self.userid_players.get(user.id, list())
        for player in players:
            if player.game.chat.id == chat.id:
                return player
        return None
