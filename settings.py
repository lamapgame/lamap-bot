import logger


def set_waiting_time(game, time):
    game.waiting_time = time
    logger.log(f'{time}')
