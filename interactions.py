from random import choice

game_interactions = {
    "how_much": [
        "Tu veux jouer combien ?",
        "Je pose combien au terre ?",
        "Je suis ton Katika, tu veux mettre combien ?",
        "L'argent c'est rien, ta mise c'est combien ?",
        "Combien ?",
        "Je pose combien ?",
        "C'est à terre qu'on joue, tu as combien à jéter maintenant ?",
        "Je te connais, tu aimes les petites mises, aujourd'hui tu veux placer combien ?",
        "J'espère que tu ne m'as pas appélé pour jouer les petites mises hein ? Je mets combien ?",
        "J'espère que tu ne m'as pas appélé pour rien ? Donnes le montant ?",
        "Ici on ne s'amuse plus, donne moi le montant je pose"
    ],
    "no_understand": [
        "Père, place moi un vrai montant. Je ne comprends pas l'autre là.",
        "Je parle en chiffre. Donne moi un montant que je peux comprendre",
        "C'est quoi ça ? Je te demandes un montant père",
        "Molah, je demande combien tu veux jouer, je suis pressé",
        "On parle en chiffre stp, donnes moi un montant je dépose",
        "Si tu ne veux pas mettre un vrai montant tu /ndem",
        "/ndem si tu ne veux pas placer l'argent.",
        "/ndem si ton argent est petit.",
        "On est pressé, pose l'argent on lance.",
        "Les gens t'attendent, donnes moi un montant je places.",
    ],
    "just_launched": [
        "{first_name} dépose *{bet}* ! Vient ramasser ta part de Nkap",
        "{first_name} veut lancer *{bet}* ! J'écris le nom de qui ?",
        "{first_name} a placé l'argent de sa pension *{bet}* ! Qui prends ?",
        "{first_name} taxe *{bet}* ! Attention aux koras",
        "{first_name} a jété *{bet}* ! No money no work ?",
        "{first_name} - *{bet}* ! C'est l'argent des beignets de qui ?",
        "*{bet}* posé au feu, qui a faim ?",
        "*{bet}* est posé, tu n'auras jamais ça au PMUC ?",
        "*{bet}* à été déposé par {first_name} ! Qui a la rage ?",
        "Voilà *{bet}* que {first_name} jette à terre, rejoins si c'est ton jour de chance!",
        "{first_name} vous fait la bise, *{bet}* c'est la mise !",
    ],
    "reminder": [
        "Va jouer dans le groupe [{title}]({link}). La mise c'est {bet}",
        "Viens jouer dans [{title}]({link}). La mise c'est {bet}",
        "C'est entrain de cuire dans [{title}]({link}). La mise c'est {bet}",
        "Ils lancent dans [{title}]({link}) sans toi. La mise c'est {bet}",
        "On vient juste de poser {bet}. Came au terre [{title}]({link}).",
    ],
    "call_me_back": [
        "Go tourner, je te notifie quand on lance.",
        "Désolé, il n'y a personne dans les parrages, je vais te faire signe après.",
        "Il n y a pas les joueurs, je te fais signe quand on lance.",
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
        "Dans **{time} secondes** j'ai partagé",
        "**{time} secondes** pour lancer",
        "On a pas le temps, dans **{time} secondes** j'ai partagé",
        "Je partage bientôt",
        "Je pense qu'on est bon, dans **{time} secondes** je coupes vos cartes",
    ],
    "not_enough": [
        "Les gars ne sont pas chauds, je tue le way. Utilise /call\_me\_back et je vais te notifier quand on va lancer ici.",
        "Personne n'a repondu à l'appel. Ils sont surement entrain de jouer au loup.\nUtilise /call\_me\_back et je vais te notifier quand on va lancer ici.",
        "Les gars ont laissé l'argent. Ils ne sont pas chaud",
        "Ils ne veulent pas jouer, ils ont peur du terre",
        "Il n y a personne pour jouer avec toi, je suis sur que tu es même faible.",
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
        "{user}, laisse nous stp",
        "{user}, vas jouer le check games",
        "{user}, ce n'est pas le terre de ta maman ici",
        "{user}, tu peux aller faire un tour stp ?",
        "{user}, attends on fini ça, tu vas jouer ta part après",
        "{user}, vérifie ton compte.",
        "{user}, j'espère que tu as au moins l'argent dans la vraie vie.",
        "{user}, non! tu ne joueras point.",
        "{user}, maff! Pauvre.",
        "{user}, je vais lancer ta part dimanche, tu vas jouer seul",
        "STP {user}, ne fais pas je t'affiches.",
        "{user} vérifie d'abord ton porte-monnaie",
        "{user} on t'a foiré, attends dimanche midi",
        "{user} demande un peu l'argent des beignets et tu reviens",
        "{user} même dans l'argent virtuel, tu n'as rien ?",
        "{user} on ne joue pas le check-games içi",
        "{user} tu n'as rien. Tu pensais qu'on jouait avec les points ?",
    ],
    "game_run": [
        "Molah, {user}, ne joint pas pour fuir. J'ai une place libre",
        "{user} est parti",
        "{user} a abandonné ses fonctions, une place s'est libéré",
        "{user}, comme tu fuis là, ne reviens plus",
        "STP {user} prochainement ne joins pas.",
        "{user} je n'aime pas faire l'atalaku pour rien",
        "{user} a fui. Une place s'est libéré",
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
        "/nkap pour déposer, lamap pour partagé",
        "fouette /nkap et je te mets bien",
        "/nkap suivi du montant, c'est ça le code secrèt",
        "Il n y a pas de partie ici, pose tes dos je lance direct",
        "Je sais que tu es lourd, lance avec /nkap on joue",
        "Pose les dos on lance tara /nkap",
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
        "{user}, arrête un peu ça. Tu es déjà là",
        "{user}, tu veux seulement forcer ? tu es déjà dedans",
        "{user}, tu es parmi mes titulaires",
        "{user}, t'inquète jamais sur le banc de touche",
        "{user}, tu es au terre, titulaire à mort",
        "{user}, ton nom est déjà dans le cahier, tu bouffes le prémier",
        "{user}, j'ai déjà coupé tes 5 cartes, calme toi",
    ],
    "unverified": [
        "{user}, non tu ne joues pas.",
    ],
    "joining": [
        "{user} a réjoint la partie !"
        "{user} mon korateur préféré a réjoint !",
        "{user} vient de poser sa mise",
        "{user} toujours en formation !",
        "{user} présent !",
        "{user} placé au chaud !",
        "{user} a sortie le porte-monnaie magique !",
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
        "{user} n'as plus besoin d'atalaku",
        "{user} est donc là, faites venir les koras",
        "{user} souhaite se suliver jusqu'au ciel",
        "{user} le règne des règnes",
        "{user} la gloire des gloires",
        "Méfier vous de {user}, trop tranchant",
        "{user}, j'ai coupé tes cartes, assieds toi tu attends que je lance",
        "{user} sois posé. en tout cas ta place est sécurisé",
        "{user} est là pour gâter",
        "Ohh!! {user} le PR est joum",
        "{user} 🔥🔥🔥🔥🔥🔥🔥🔥🔥",
        "{user} ⚡️ un pro",
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


def t_tu_joue_combien() -> str:
    return choice(game_interactions.get('how_much'))


def t_i_do_not_understand() -> str:
    return choice(game_interactions.get('no_understand'))


def t_just_launched(first_name, bet) -> str:
    return choice(game_interactions.get('just_launched')).format(first_name=first_name, bet=bet)


def t_reminder(title, link, bet) -> str:
    return choice(game_interactions.get('reminder')).format(title=title, link=link, bet=bet)


def t_call_me_back() -> str:
    return choice(game_interactions.get('call_me_back'))


def t_already_started() -> str:
    return choice(game_interactions.get('already_started'))


def t_count_down(time) -> str:
    return choice(game_interactions.get('count_down')).format(time=time)


def t_not_enough() -> str:
    return choice(game_interactions.get('not_enough'))


def t_no_money(user) -> str:
    return choice(game_interactions.get("no_money")).format(user=user)


def t_unverified(user) -> str:
    return choice(game_interactions.get("unverified")).format(user=user)


def t_game_run(user) -> str:
    return choice(game_interactions.get("game_run")).format(user=user)


def t_max_reached(user) -> str:
    return choice(game_interactions.get("max_reached")).format(user=user)


def t_already_joined(user) -> str:
    return choice(game_interactions.get("already_joined")).format(user=user)


def t_joining(user) -> str:
    return choice(game_interactions.get("joining")).format(user=user)


def t_no_game() -> str:
    return choice(game_interactions.get('no_game'))
