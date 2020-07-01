from random import choice

# starting game
start_game_GIF = [
    "https://media.giphy.com/media/Y2buJBCkGdkfJV41X4/giphy-downsized.gif", "https://media.giphy.com/media/TGQoUSuNBNEOACAIGv/giphy-downsized.gif", "https://media.giphy.com/media/kDOJumTGGTSYw2zNwJ/giphy-downsized.gif", "https://media.giphy.com/media/JmCOTovHMQ2OCifNIV/giphy-downsized.gif", "https://media.giphy.com/media/Z9nPjqX1vDIgSPrGGX/giphy-downsized.gif", "https://media.giphy.com/media/U4jfvnw81uHeQNs9rO/giphy-downsized.gif"
]

# won
win_game_GIF = [
    "https://media.giphy.com/media/h3u7jI6xHzAA7ElwII/giphy-downsized.gif", "https://media.giphy.com/media/QzADrVlEiuV3fS1dFi/giphy-downsized.gif", "https://media.giphy.com/media/mCEC1BxCIJv2sQmFNP/giphy-downsized.gif", "https://media.giphy.com/media/W9WSk4tEU1aJW/giphy.gif", "https://media.giphy.com/media/dxn6nOILy3OixVA1FY/giphy-downsized.gif", "https://media.giphy.com/media/NG6dWJC9wFX2/giphy.gif"]
# won by kora
win_kora_game_GIF = [
    "https://media.giphy.com/media/Q7FEPREUzLJoy16WFu/giphy-downsized.gif", "https://media.giphy.com/media/Jmfq3XfBo2RJsaskm0/giphy-downsized.gif", "https://media.giphy.com/media/IeoL0iD3eUrEibN6fm/giphy-downsized.gif"]
# won by double kora
win_double_kora_game_GIF = [
    "https://media.giphy.com/media/zrj0yPfw3kGTS/giphy.gif", "https://media.giphy.com/media/dxn6nOILy3OixVA1FY/giphy-downsized.gif", "https://media.giphy.com/media/NG6dWJC9wFX2/giphy.gif"]
# won by forfeit
win_forfeit_game_GIF = [
    "https://media.giphy.com/media/dxn6nOILy3OixVA1FY/giphy-downsized.gif", "https://media.giphy.com/media/NG6dWJC9wFX2/giphy.gif"
]
# won by quick win
win_qw_game_GIF = []


def start_Anim():
    return choice(start_game_GIF)


def win_Anim():
    return choice(win_game_GIF)


def win_kora_Anim():
    return choice(win_kora_game_GIF)


def win_forfeit_Anim():
    return choice(win_forfeit_game_GIF)


def win_dbl_kora_Anim():
    return choice(win_double_kora_game_GIF)


def win_qw_Anim():
    return choice(win_game_GIF)
