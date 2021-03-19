from utils import loss_by_afk, mention, n_format
from game import Game
from config import TIME_TO_PLAY
from global_variables import gm
from telegram import Update
from telegram.ext import CallbackContext


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def end_of_play_time(context: CallbackContext):
    ''' The time is over '''
    job = context.job
    game: Game = job.context['game_ob']
    gm.end_game(game.chat, game.current_player.user)
    loss_by_afk(context.bot, game, game.chat, "n")


def reminder(context: CallbackContext):
    ''' The time is over '''
    job = context.job
    game = job.context['game_ob']
    bet = game.bet
    players = game.players
    context.bot.send_message(
        game.chat.id, text=f"{mention(game.current_player.user)}. Tu as **{round(TIME_TO_PLAY/2)} secondes** pour jouer")
    context.bot.send_message(
        game.current_player.user.id, text=f"Tu as **{round(TIME_TO_PLAY/2)} secondes** pour jouer dans {game.chat.title}.\nFaute de quoi tu te feras prélèvé {n_format(bet * (len(players)-1))}.")
    context.job_queue.run_once(
        end_of_play_time, TIME_TO_PLAY/2, context=job.context, name=context.job.name)


def set_job(name: str, context: CallbackContext, update: Update, game: Game):
    ''' Create a job with a given name '''
    obj = {}
    obj["update_ob"] = update
    obj["game_ob"] = game

    remove_job_if_exists(name, context)
    context.job_queue.run_once(
        reminder, TIME_TO_PLAY/2, context=obj, name=name)
