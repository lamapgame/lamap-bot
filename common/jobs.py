from typing import Callable, Coroutine, Any
from telegram import Update
from telegram.ext import ContextTypes, CallbackContext as CCT

from game import Game


async def start_timer(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    time: int,
    game: Game,
    callback_fn: Callable[[CCT], Coroutine[Any, Any, Any]],
) -> None:
    """sets the start timer for the game"""
    if update.effective_message and context.job_queue:
        chat_id = update.effective_message.chat.id
        passed_data = {"chat_id": chat_id, "game": game, "update": update}
        remove_job_if_exists(str(chat_id), context)
        context.job_queue.run_once(
            callback_fn,
            time,
            passed_data,
            name=str(chat_id),
        )


def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE):
    """Remove job with given name. Returns whether job was removed."""
    if context.job_queue:
        current_jobs = context.job_queue.get_jobs_by_name(name)
        if not current_jobs:
            return
        for job in current_jobs:
            job.schedule_removal()


async def remove_all_jobs(context: ContextTypes.DEFAULT_TYPE):
    """Remove all jobs."""
    if context.job_queue:
        await context.job_queue.stop(False)
