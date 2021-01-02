# Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to Semantic Versioning.

## 3.0.0.0 - Trois Kolos

La Map #Update #3_0_0_0 🏷 Live.

3 Kolos

🔑 **Que le Nkap**: Désormais on ne joue qu'une partie misé, il n'y a plus la Santé

📌 Un nouveau flow pour lancer nouvelle partie, envoyez /nkap (seulement la commande) pour essayer !

📌 Désormais tout le monde ayant un montant supérieur à 0 peuvent rejoindre une partie. Mais sachez que la dette sera payé au moment du chargement

📌 La paye tombe désormais Mercredi et Dimanche à 10h pile (j'avais remarqué que avant mardi vous étiez déjà tous foiré).

📌 Puis que nous ne jouons que les gros montants ici, désormais le bot appellera l'argent de façon commune `100 kolos`, `2 batons`, `3 myondos`, `6 mitoumbas` (correspondant à mille, million, milliard, billion).

🔑 **Transparence**: Nous sommes comme la CONAC, contre la corruption, alors:

📌 Tout gains, pertes ou mises vous séront envoyés en DM après une partie (faut DM le bot, ceux qui ne l'ont pas fait).

📌 Les points sont désormais très régulés pour éviter les grosses pertes (parce qu'il est plus facile de perdre que de gagner).

🔑 **Expérience de jeu**: On travaille toujours pour donner une meilleure expérience aux joueurs:

📌 Le lancement d'une partie a été entièrement refaite.

📌 Ajout de la possibilité de notifier (via ping), les potentiels joueurs

📌 Le délai de départ d'une partie reduite (90s -> 30 secondes), on a plus le temps d'attendre–On veut déjà lancer.

📌 Le bot a desormais beaucoup de mots que vous lui avez appris en jouant (il parle aussi mal que vous).

🔑 **Le transfert de nkap**: On concurrence les Orange et MTN avec la possibilité de transférer l'argent d'un compte à un autre.

📌 Il suffit de répondre au méssage de celui à qui vous voulez transférer avec /transfert <montant>

📌 Bien évidemment, vous ne pouvez pas vous transférer de l'argent à vous même.

🔑 **Les statistiques**: Rien ne se perd sur internet et vous le savez: Désormais, les joueurs auront accès des statistiques tels que;

Les meilleurs 10:

📌 /top10: Basé sur les points

📌 /top10nkap: Basé sur le nkap

📌 /top10koras: Basé sur le nombre de koras

📌 /top10_2koras: Basé sur le nombre de 33 offertes

🔑 **Le retour (EXPERIMENTALE)**: Si il y a un problème dans une partie (ou un joueur ne veut pas payer): Expliquez et ping @panachaud , le bot va gérer le retour.

🔑 Le Katika 2035 fois plus insolent

**Petits Changements**
📌 Plus d'interface pour recommencer la partie directement après une partie finie.

📌 Le bot calcule vos temps de jeu pour permettre l'implémentation dans une version très prochaine la possibilité de rétirer un joueur qui est AFK

📌 Les nouveaux joueurs qui n'arrivaient pas à rejoindre une partie pourront désormais le faire.

📌 L'aléa à été rajouté dans le partage des cartes (il y aura légerement moins de 333, 777 et familles).

@lamapdevs: Venez et jouez...

## 1.0.0 - yyyy-mm-dd

### Added

Update 1.0.0: Le terre oublie, mais le Katika sauvegarde.

- Statistiques: Aucun Kora ne sera perdu, toute partie gagné/perdue/non-terminée est compté et les plus bon joueurs seront affichés dans un classement global.
- Nouvelle interface pour jouer:
  👑 - c'est celui qui contrôle.
  🤙🏾 - celui qui doit jouer.
  🎴 - cartes à jouer.
  🃏 - cartes jouées.
- Nouvelle commande /game_status : pendant la partie, vous aurez la possibilité de savoir quelles cartes ont controlées les tours d'avant.
- Commande /tchoko: pour donner une bière au bot.
- Commande /apprendre: pour apprendre à jouer LaMap.
- 18 nouveaux GIFS qui vont vous mettre bien 😱.
- Comme d'habitude un bot 2x plus insolent et intélligent.

### Changed

- Il n'est plus possible de lancer plus d'une partie dans un groupe
- Les joueurs sont mentionnés par le bot avec leurs prénoms, mais pour que le bot puisse vous tagger, écrivez lui en DM.
- Un meilleur aléa, permettant aux joueurs d'avoir de meilleurs cartes.

### Fixed

- Le double KORA fonctionne maintenant correctement.
- Bugs de début de partie, de suivie de jeu et de fin de parties.

N'oubliez pas de BIEN travailler vos points.

### DX

- Add tests
- Add databases

## 0.8.0 - 12-06-2020

### Added

- La 33 (Double Korat).
- La famille.
- Le Tia (3x3 et 3x7).
- La commande /chasser
- Un bot encore plus intelligent et insolent.

### Changed

- Les commande /join et /start ont été retirées on peut joindre et commencer avec les boutons.
- Le droit de /tuer_le_way n'est octroyé qu'a l'admin et le créateur de la partie en cours.
- Lorsque les joueurs se banquent, le dernier gagne.
- Les messages d'organisation de parties sont supprimés lorsqu'elle est lancée.
- Lorsque les joueurs se banquent, le dernier gagne.
- Les parties se lancent seules après 60 secondes.
- Seul le créateur de la partie ou un admin peut faire commencer la partie.
- Les cartes sont désormais toujours accessible (mais pour jouer il faut attendre son tour, les fermer et les rouvrir). **EXPERIMENTAL**

### Fixed

- Plus de 4 joueurs ne peuvent plus rejoindre la partie.

### DX

- Better logging
