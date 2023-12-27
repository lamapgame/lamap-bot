from random import choice

# ruff: noqa: E501 # pylint: disable=line-too-long disable=anomalous-backslash-in-string

IMAGES = {
    "START": "https://i.imgur.com/GwMcZVr.png",
    "START0": "https://i.imgur.com/nCQ6Ams.png",
    "NORMAL": "https://i.imgur.com/ITeg26s.png",
    "KORA": "https://i.imgur.com/AEXG4Dp.png",
    "AFK": "https://i.imgur.com/hoeRJV2.png",
    "DBL_KORA": "https://i.imgur.com/SYUpiF6.png",
    "SPECIAL": "https://i.imgur.com/EQRc66n.png",
}

TEXTS = {
    "NEW_GAME": [
        "{user} veut nous mettre bien. Il a déposé *{bet}*.\n\nQui est chaud?",
        "Ça va être chaud, {user} a mis *{bet}*.\n\nQui est chaud?",
        "Kior décor, kior encore. Le génie {user} a mis *{bet}*.\n\nAppuie 'joindre' et je coupe tes cartes",
        "Le génie {user} dépose *{bet}*.",
        "Wooooookoooooh, un gros *{bet}* comme ça. On voit ça seulement dans la casa de papel.",
        "Oyé oyé! {user} lance le défi avec {bet}! À vos marques!",
        "{user} propose *{bet}* en quinquonce, qui est chaud?",
        "{user} vous fait la bise *{bet}* c'est la mise.",
        "Qui a soif, {user} propose *{bet}*. Je te vois, tu as soif.",
        "Venez jouer, {user} propose *{bet}*. Ce mieux que le 2-0 à Nkoulouloun",
        "On dirait que {user} a mis *{bet}*. Qui est chaud?",
        "Le groupe ci dort trop, voici *{bet}* chaud chaud!",
        "La moula c'est *{bet}*, le moulatier c'est {user}. Qui est chaud?",
        "*{bet}* est posé, tu n'auras jamais ça a 1xBet !",
        "*{bet}* à été déposé par {user} ! Qui a la rage ?",
    ],
    "CANNOT_START_NEG": [
        "Tu ne peux pas commencer avec un nombre négatif",
        "Ta maman te donnes l'argent en négatif ?",
        "Chez ta grand-mère, vous utilisez l'argent négatif ?",
        "Tu es le fils de qui pour poser un nombre négatif?",
        "Tu fais ça dans un vrai terre on te tappes",
        "Respecte moi, c'est pas parce que on est ici sur Telegram on joue aux cartes.",
        "Tu veux jouer au malin? Tu vas voir",
        "Tu fais encore ça, je te bannis, propre !",
        "Tu carbures à quoi? T'es déjà en jeu!"
        "Pas la peine de pousser, tu es déjà sur le terrain!"
        "Garde ton calme, tu fais déjà partie de l'aventure!",
    ],
    "NOT_ENOUGH_PLAYERS": [
        "Pas assez de joueurs pour lancer.\nInvite les autres à rejoindre avant de lancer",
        "Il faut au moins 2 joueurs pour lancer une partie",
        "Je ne peux pas lancer une partie avec un seul joueur",
        "Tu n'as pas les amis ? Il faut au moins 2 joueurs pour lancer une partie",
        "Tu es seul ? Il faut au moins 2 joueurs pour lancer une partie",
        "Va dans le groupe du loup, dit leurs que j'ai dit qu'ils viennent jouer avec toi",
        "Waaaah, je t'ai déjà dit de ne plus venir lancer seul, tu ne m'écoutes pas",
        "Weeeeh, tu vas alors jouer avec qui ?",
        "Vas un peu tourner stp.",
        "Tu n'as pas d'amis ?, il faut au moins 2 joueurs pour lancer une partie",
        "Les gars ont peur de toi, Raaaaambo ?!",
        "Le terre est sec, revient après, il y aura plus de joueurs",
    ],
    "ALREADY_IN_GAME": [
        "Be cool, tes cartes sont posés",
        "Tu es déjà dans la partie",
        "Tu es déjà dans la partie, calme toi",
        "J'ai déjà coupé tes cartes",
        "Tu es déjà dans la partie, tu veux join 2 fois ?",
        "C'est posé, tu es déjà dans la partie",
        "C'est posé mon pétit. Tu es déjà dans la partie",
        "Calme toi, j'ai déjà coupé tes cartes.",
        "Tu as déjà rejoint.",
        "Ton argent est à terre, ne t'inquiète pas",
        "T'inquiète tes cartes sont déjà dans placées",
        "Tes dos sont dans ma poche",
        "Calme toi, je gère ta position",
        "Arrête un peu ça. Tu es déjà là",
        "Tu veux seulement forcer ? tu es déjà dedans",
        "Tu es parmi mes titulaires",
        "T'inquète jamais sur le banc de touche",
        "Tu es au terre, titulaire à mort",
        "Ton nom est déjà dans le cahier, tu bouffes le prémier",
        "J'ai déjà coupé tes 5 cartes, calme toi",
    ],
    "FULL_GAME": [
        "Le terre est plein, tu vas jouer après",
        "C'est plein, concentre toi.",
        "Nous sommes full, va jouer dans un autre groupe.",
        "Nous sommes full, attends un peu qu'on finisse.",
        "C'est dead bro. Nous sommes full.",
        "Ca a cuit, on va lancer sans toi !",
        "Laisse nous un peu stp, on t'as appelé, tu n'étais pas là.",
    ],
    "BANNED_PLAYER": [
        "Tu es banni, tu ne joues pas.",
        "Tu ne joue pas, contact @lamapsupport",
        "Tara, laisse nous tranquille.",
        "Va jouer autre chose stp.",
        "Tu n'as pas un autre groupe ? Vas t'amuser sur whatsapp, tu es ban.",
        "Malheureusement tu n'as pas le droit de jouer",
        "Accès refusé! Va voir ailleurs si j'y suis.",
        "T'es dans la liste noire, désolé! Pas de jeu pour toi.",
        "Fiches moi le camps stp. Tu es banni",
    ],
    "POOR_PLAYER": [
        "Tu es pauvre, tu ne joues pas.",
        "Tu n'as pas assez d'argent pour jouer",
        "Tu sais bien que ce n'est pas ton niveau ici, tu es pauvre",
        "Tu as vu ton argent ? Tu ne joues pas",
        "Mola, fiches le camps stp.",
        "Joues ton niveau mon petit. Ici ca joue gros",
        "Tu n'as pas l'argent",
        "Ekieh, tu n'as pas l'argent ?",
        "Ici, c'est le grand jeu! Reviens quand tu seras plus... fourni.",
        "On joue en grand ici. Va remplir ton coffre et reviens!",
    ],
    "PLAYER_JOINED": [
        "{user}, tu es dans la partie. Je coupe tes cartes.",
        "{user} le genie à rejoint, les koras vont pleuvoir.",
        "{user} le tu nous a manqué dans le terre, je coupe tes cartes.",
        "{user} le génie, je coupe tes cartes.",
        "{user} est venu pour falla le nyama !",
        "{user} a rejoint en quinquonce.",
        "{user} Popol c'est qui devant toi.",
        "{user} le PR est là !",
        "{user} si tu ne gagnes pas, on change mon nom.",
        "Ateeeeh, {user} est là ! On a perdu les dos",
        "Mon meilleur pro {user} a rejoint la partie !",
        "{user} 🔥🔥🔥🔥🔥🔥🔥🔥🔥",
        "{user} ⚡️ un pro",
        "{user} a mis le cœur !",
        "{user} a mis les organes !",
        "{user} est consentant !",
        "{user} j'ai gardé tes 5 bonnes cartes !",
        "{user} a placé l'argent de sa pension !",
        "Mon chef de terre {user} à rejoint !",
        "{user} toujours très professionel.",
        "{user} tu es là ?! J'ai placé tes dos",
        "{user} ton coubi ne cherche jamais son bro",
        "{user} tu gagnes même ?",
        "{user} me sô a ya ! Je coupe tes cartes.",
        "Le plus gros korateur {user}",
        "Le barman, le distributeur de 33, {user} vient de rejoindre.",
        "Ah maf, {user} est joum",
        "C'est un oiseau? C'est un avion? Non, c'est {user} qui atterrit dans le jeu",
        "Mazembe dey for mboko ! {user} a rejoint.",
        "le 12 fois koraman, {user} a rejoint.",
    ],
    "FIRST_CARD": [
        "{user} tu joues en premier.",
        "{user} c'est toi qui joues en premier.",
        "{user} tu es le premier à jouer.",
        "{user} tu es le premier à jouer, dégage la partie.",
        "Fouette nous la première carte {user}",
        "C'est à toi de jouer {user}",
        "Tu es le premier à jouer {user}",
    ],
    "WARN_AFK": [
        "{user} si tu ne joues pas dans les prochaines {time_to_play} secondes, tu perds.",
        "{user} je croyais que les AFK c'était seulement sur la v1. Joue avant {time_to_play} secondes ou tu perds.",
        "{user} tu as {time_to_play} secondes pour jouer, sinon tu perds.",
        "{user}, en vrai on a pas le temps, tu as {time_to_play} secondes pour jouer",
        "Si tu joues dans 7 groupes c'est ton pb, tu as {time_to_play} secondes pour jouer",
        "Stp, ne vient pas pleurer la connexion ici. Tu as {time_to_play} secondes pour jouer {user}",
        "{user}, dans {time_to_play} secondes, tu ne joue pas tu loss. Propre !",
    ],
    "COUNT_DOWN": [
        "Je partage les cartes dans **{time_to_play} secondes**...",
        "Le terre s'enflame dans **{time_to_play} secondes**...",
        "Les carottes cuisent dans exactement **{time_to_play} secondes**",
        "Dans **{time_to_play} secondes** ça cuit",
        "Dans **{time_to_play} secondes** j'ai partagé",
        "**{time_to_play} secondes** pour lancer",
        "Est-ce que c'est bon dans la salle ? {time_to_play} secondes pour lancer les gars",
        "On a pas le temps, dans **{time_to_play} secondes** j'ai partagé",
        "Je partage bientôt",
        "Je lance bientôt, je veux rien entendre",
        "Je pense qu'on est bon, dans **{time_to_play} secondes** je coupes vos cartes",
    ],
    "WRONG_CARD_CONTROL": [
        "🤦🏾‍♂️ Ok tara, on a vu, mais ce n'est pas le {card} qui contrôle ce tour. C'est le {controlling} \n\nJe sais que tu a la carte, joue la!",
        "🤦🏾‍♂️ Stp, cache ton petit {card}. C'est le {controlling} qui contrôle \n\nJe sais que tu a la carte, joue la!",
        "🤦🏾‍♂️ Si tu ne sais pas jouer, va d'abord lire. Le {controlling} contrôle actuellement",
        "🤦🏾‍♂️ Je me demandes comment tu gagnes, tu n'es pas concentré bro. Le {controlling} contrôle actuellement",
        "🤦🏾‍♂️ Joue mieux stp, tu n'es pas concentré. Le {controlling} contrôle actuellement",
        "🤦🏾‍♂️ Tu ne sais pas jouer ? Le {controlling} contrôle actuellement",
        "🤦🏾‍♂️ Arrête de jouer sans suivre le jeu ? Le {controlling} contrôle actuellement",
        "🤦🏾‍♂️ Tu n'effraie personne ici avec ton {card}. On sait tous que le {controlling} contrôle actuellement",
        "🤦🏾‍♂️ Tu affiche ton {card} là et pourtant c'est le {controlling} qui contrôle en ce moment",
        "🤦🏾‍♂️ Joue mieux mon petit tu affiche ton {card}. On est dans le {controlling} actuellement",
    ],
    "WRONG_CARD_TURN": [
        "🤦🏾‍♂️ Ce n'est pas toi qui joue, {user}. Attends ton tour",
        "🤦🏾‍♂️ Tu ne peux pas jouer, {user}. Attends ton tour",
        "🤦🏾‍♂️ {user} C'est moi ou ce n'est pas moi le katika ? Laisse moi te dire quand c'est ton tour de jouer.",
        "🤦🏾‍♂️ {user}, merci on a vu!\n Mais ce n'est pas ton tour de jouer",
        "🤦🏾‍♂️ waahaa, j'ai remarqué que le mboutman ci ne m'écoute pas!\nCe n'est pas ton tour de jouer",
        "🤦🏾‍♂️ {user}, stp be cool, tu vas jouer quand je vais te dire, cache ta carte, les gars vont voir",
        "🤦🏾‍♂️ {user}, tu fais encore ça je te banque, laisse moi te dire quand tu dois jouer",
        "🤦🏾‍♂️ On joue même avec qui comme ça ? Tu dois jouer quand je te dis que c'est ton tour.",
    ],
    "NOT_ADMIN": [
        "Fiches moi la paix stp, tu n'es pas admin",
        "Tu n'es pas admin, ne me parle pas",
        "Vas jouer loin stp, tu n'es pas admin",
        "Ça ne te concerne pas, et ça ne va jamais te concerner",
        "Tara, tu n'as pas les accréditations pour faire ça.",
        "Mola reste à ta place, tu n'es pas admin",
        "Be cool tara. Tu n'es pas admin",
    ],
    "QUIT_GAME": [""],
}


def t_new_game(user: str, bet: str):
    return choice(TEXTS["NEW_GAME"]).format(user=user, bet=bet)


def t_cannot_start_neg():
    return choice(TEXTS["CANNOT_START_NEG"])


def t_not_enough_players():
    return choice(TEXTS["NOT_ENOUGH_PLAYERS"])


def t_already_in_game():
    return choice(TEXTS["ALREADY_IN_GAME"])


def t_full_game():
    return choice(TEXTS["FULL_GAME"])


def t_banned_player():
    return choice(TEXTS["BANNED_PLAYER"])


def t_poor_player():
    return choice(TEXTS["POOR_PLAYER"])


def t_player_joined(user: str):
    return choice(TEXTS["PLAYER_JOINED"]).format(user=user)


def t_first_card(user: str):
    return choice(TEXTS["FIRST_CARD"]).format(user=user)


def t_warn_afk(user: str, time_to_play: int):
    return choice(TEXTS["WARN_AFK"]).format(user=user, time_to_play=time_to_play)


def t_count_down(time_to_play: int):
    return choice(TEXTS["COUNT_DOWN"]).format(time_to_play=time_to_play)


def t_wrong_card_control(card: str, controlling: str):
    return choice(TEXTS["WRONG_CARD_CONTROL"]).format(
        card=card, controlling=controlling
    )


def t_wrong_card_turn(user: str):
    return choice(TEXTS["WRONG_CARD_TURN"]).format(user=user)


def t_not_admin():
    return choice(TEXTS["NOT_ADMIN"])


def t_quit_game():
    return choice(TEXTS["QUIT_GAME"])
