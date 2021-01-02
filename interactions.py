from random import choice

game_interactions = {
    "how_much": [
        "Tu veux jouer combien ?",
        "Je pose combien au terre ?",
        "Je suis ton Katika, tu veux mettre combien ?",
        "L'argent c'est rien, ta mise c'est combien ?",
        "C'est à terre qu'on joue, tu as combien à jéter maintenant ?",
        "Je te connais, tu aimes les petites mises, aujourd'hui tu veux placer combien ?",
        "J'espère que tu ne m'as pas appélé pour jouer les petites mises hein ? Je mets combien ?",
    ],
    "no_understand": [
        "Père, place moi un vrai montant. Je ne comprends pas l'autre là.",
        "Je parle en chiffre. Donne moi un montant que je peux comprendre",
        "C'est quoi ça ? Je te demandes un montant père",
        "Molah, je demande combien tu veux jouer, je suis pressé",
        "On parle en chiffre stp, donnes moi un montant je dépose",
        "Si tu ne veux pas mettre un vrai montant tu /ndem",
        "/ndem si tu ne veux pas placer l'argent.",
        "On est pressé, pose l'argent on lance.",
        "Les gens t'attendent, donnes moi un montant je places.",
    ],
    "just_launched": [
        "{first_name} dépose *{bet}* ! Vient ramasser ta part de Nkap",
        "*{bet}* à été déposé par {first_name} ! Qui a la rage ?",
        "Voilà *{bet}* que {first_name} jette à terre, rejoins si c'est ton jour de chance!",
        "{first_name} vous fait la bise, *{bet}* c'est la mise !",
    ],
    "reminder": [
        "Va jouer dans le groupe [{title}]({link}). La mise c'est {bet}",
        "Ils lancent dans [{title}]({link}) sans toi. La mise c'est {bet}",
        "On vient juste de poser {bet}. Came au terre [{title}]({link}).",
    ],
    "call_me_back": [
        "Go tourner, je te notifie quand on lance.",
        "Si on pose les dos, je viendrais te dire DM",
        "Vas jouer au loup, si jamais ils lancent, je te bip",
        "Dès que ça cuit, je te fais signe",
        "Sois posé, je vais te notifier quand nous allons lancer.",
    ],
    "already_started": [
        "Calme toi! Nous jouons l'argent ici. /call\_me\_back",
        "Tu ne vois pas qu'on a déjà lancé ? /call\_me\_back et je vais te notifier",
        "Ne nous embrouilles pas, on est déjà entrain de jouer ici",
        "On a déjà lancé, /call\_me\_back, si tu veux que je te notifie pour le prochain",
    ],
    "count_down": [
        "Je partage les cartes dans **{time} secondes**...",
        "Le terre s'enflame dans **{time} secondes**...",
        "Les carottes cuisent dans exactement **{time} secondes**",
        "Dans **{time} secondes** ça cuit",
    ],
    "not_enough": [
        "Les gars ne sont pas chauds, je tue le way. Utilise /call\_me\_back et je vais te notifier quand on va lancer ici.",
        "Personne n'a repondu à l'appel. Ils sont surement entrain de jouer au loup.\nUtilise /call\_me\_back et je vais te notifier quand on va lancer ici.",
        "Les gars ont laissé l'argent. Ils ne sont pas chaud",
        "Ils ne veulent pas jouer, ils ont peur du terre",
        "Ils te fuient tous. T'inquiète utilise /call\_me\_back et je vais te notifier quand on va lancer.",
        "Ils ont peur de champy. T'inquiète utilise /call\_me\_back et je vais te notifier quand on va lancer ici.",
        "Ils ne sont pas chaud, vas d'abord faire un tour avant de venir relancer.",
        "Ils ne sont pas prêts pour toi. Utilise /call\_me\_back et je vais te notifier quand on va lancer ici.",
        "Molah, all le mot est alors déconnecté en vrai. Utilise /call\_me\_back et je vais te notifier quand on va lancer ici.",
    ],
    "no_money": [
        "Molah, {user}, tu n'as pas l'argent.\nCe n'est pas le ndoshi ici.",
        "{user}, soit tu me dois, soit tu n'as rien, vas d'abord jouer au loup",
        "{user}, la santé est fini en 2020, on garde les vrais joueurs",
        "{user}, je vais lancer ta part dimanche, tu vas jouer seul",
        "STP {user}, ne fais pas je t'affiches.",
        "{user} vérifie d'abord ton porte-monnaie",
        "{user} on t'a foiré, attends dimanche midi",
        "{user} même dans l'argent virtuel, tu n'as rien ?",
        "{user} on ne joue pas le check-games içi",
        "{user} tu n'as rien. Tu pensais qu'on jouait avec les points ?",
    ],
    "max_reached": [
        "Désolé {user}, le terre est plein, tu ne peux pas joindre. /call\_me\_back pour être notifié lorsque une nouvelle partie sera lancée dans ce groupe."
        "{user}, nous sommes déjà 4, ce n'est pas le check games ici",
        "{user}, tu es malheureusement en retard, on est plein",
        "{user} qui vient en retard perd son nkap",
        "{user} c'est plein, /call\_me\_back et je te bip quand on lance",
        "oups! Partie pleine. {user} /call\_me\_back seulement pour jouer plus tard",
    ],
    "no_game": [
        "Aucun argent au terre, pose ta part avec /nkap",
        "Il n'y a aucune partie en cours, crée une nouvelle avec /nkap",
        "Je n'ai encore rien reçu, je vous le jure... /nkap pour lancer une partie",
        "Aucune partie n'est lancé, ouvre le terre avec /nkap",
        "Il n'y a rien au feu. Place une marmite avec /nkap",
        "Ca ne joue pas encore. /nkap pour une nouvelle partie",
    ],
    "already_joined": [
        "{user}, calme toi, j'ai déjà coupé tes cartes.",
        "{user}, tu as déjà rejoint.",
        "{user}, ton argent est à terre, ne t'inquiète pas",
        "{user}, t'inquiète tes cartes sont déjà dans placées",
        "{user}, tes dos sont dans ma poche",
        "{user}, calme toi, je gère ta position",
        "{user}, tu es parmi mes titulaires",
        "{user}, t'inquète jamais sur le banc de touche",
        "{user}, tu es au terre, titulaire à mort",
        "{user}, ton nom est déjà dans le cahier, tu bouffes le prémier",
        "{user}, j'ai déjà coupé tes 5 cartes, calme toi",
    ],
    "joining": [
        "{user} a réjoint la partie !"
        "{user} mon korateur préféré a réjoint !",
        "{user} vient de poser sa mise",
        "{user} toujours en formation !",
        "{user} présent !",
        "{user} placé au chaud !",
        "{user} mon PDT a rejoint !",
        "{user} toujours très professionel.",
        "{user} tu es là ?! J'ai placé tes dos",
        "Ca fait comme ci {user} à rejoint",
        "Il fait chaud, {user} vient de rejoindre",
        "{user} ta mise est posé !",
        "Il y a pas l'homme pour {user}",
        "Mon chef de terre {user} à rejoint !",
        "Tueur de taureaux {user} à rejoint !",
        "{user} j'ai gardé tes 5 bonnes cartes !",
        "{user} a placé l'argent de sa pension !",
        "{user} a mis le cœur !",
        "{user} a mis les organes !",
        "{user} est consentant !",
        "{user} vient de joum !",
        "{user} il fait chaud, c'est toi qui est entré là !?",
        "Ah maf ! {user} a posé sa mise !",
        "Champion d'afrique {user} est déjà là !",
        "{user} est venu pour falla le nyama !",
        "{user} a rempli les conditions pour rejoindre !",
        "Yeessss... {user} a déposé ses dos !",
        "Mon meilleur pro {user} a rejoint la partie !",
        "{user} est présent !",
        "{user} a soif !",
        "{user} est venu pour gagner !",
        "TREMBLEZ DE JOIE ! {user} est présent !",
        "{user} chef de terre a repondu présent !",
        "{user} le 10 fois koraman est présent !",
        "Le pro {user} a rejoint, mais dit que la mise est trop petite !",
    ],
}


def t_tu_joue_combien():
    return choice(game_interactions.get('how_much'))


def t_i_do_not_understand():
    return choice(game_interactions.get('no_understand'))


def t_just_launched(first_name, bet):
    return choice(game_interactions.get('just_launched')).format(first_name=first_name, bet=bet)


def t_reminder(title, link, bet):
    return choice(game_interactions.get('reminder')).format(title=title, link=link, bet=bet)


def t_call_me_back():
    return choice(game_interactions.get('call_me_back'))


def t_already_started():
    return choice(game_interactions.get('already_started'))


def t_count_down(time):
    return choice(game_interactions.get('count_down')).format(time=time)


def t_not_enough():
    return choice(game_interactions.get('not_enough'))


def t_no_money(user):
    return choice(game_interactions.get("no_money")).format(user=user)


def t_max_reached(user):
    return choice(game_interactions.get("max_reached")).format(user=user)


def t_already_joined(user):
    return choice(game_interactions.get("already_joined")).format(user=user)


def t_joining(user):
    return choice(game_interactions.get("joining")).format(user=user)


def t_no_game():
    return choice(game_interactions.get('no_game'))
