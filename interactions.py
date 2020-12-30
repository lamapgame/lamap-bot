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
        "Voilà *{bet}* à terre, rejoins si c'est ton jour de chance !",
    ],
    "reminder": [
        "Va jouer dans le groupe [{title}]({link}). La mise c'est {bet}",
        "Ils lancent dans [{title}]({link}) sans toi. La mise c'est {bet}",
        "On vient juste de poser {bet}. Came au terre [{title}]({link}).",
    ]
}


def tu_joue_combien_txt():
    return choice(game_interactions.get('how_much'))


def i_do_not_understand():
    return choice(game_interactions.get('no_understand'))


def just_launched(first_name, bet):
    return choice(game_interactions.get('just_launched')).format(first_name=first_name, bet=bet)


def reminder(title, link, bet):
    return choice(game_interactions.get('reminder')).format(title=title, bet=bet)
