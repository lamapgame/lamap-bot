# Change log

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/) and this project adheres to Semantic Versioning.

## 1.0.0 - yyyy-mm-dd

### Added

Update 1.0.0: Le terre oublie, mais le Katika sauvegarde.

* Statistiques: Aucun Kora ne sera perdu, toute partie gagné/perdue/non-terminée est compté et les plus bon joueurs seront affichés dans un classement global.
* Nouvelle interface pour jouer:
  👑 - c'est celui qui contrôle.
  🤙🏾 - celui qui doit jouer.
  🎴 - cartes à jouer.
  🃏 - cartes jouées.
* Nouvelle commande /game_status : pendant la partie, vous aurez la possibilité de savoir quelles cartes ont controlées les tours d'avant.
* Commande /tchoko: pour donner une bière au bot.
* Commande /apprendre: pour apprendre à jouer LaMap.
* 18 nouveaux GIFS qui vont vous mettre bien 😱.
* Comme d'habitude un bot 2x plus insolent et intélligent.

### Changed

* Il n'est plus possible de lancer plus d'une partie dans un groupe
* Les joueurs sont mentionnés par le bot avec leurs prénoms, mais pour que le bot puisse vous tagger, écrivez lui en DM.
* Un meilleur aléa, permettant aux joueurs d'avoir de meilleurs cartes.

### Fixed

* Le double KORA fonctionne maintenant correctement.
* Bugs de début de partie, de suivie de jeu et de fin de parties.

N'oubliez pas de BIEN travailler vos points.

### DX

* Add tests
* Add databases

## 0.8.0 - 12-06-2020

### Added

* La 33 (Double Korat).
* La famille.
* Le Tia (3x3 et 3x7).
* La commande /chasser
* Un bot encore plus intelligent et insolent.

### Changed

* Les commande /join et /start ont été retirées on peut joindre et commencer avec les boutons.
* Le droit de /tuer_le_way n'est octroyé qu'a l'admin et le créateur de la partie en cours.
* Lorsque les joueurs se banquent, le dernier gagne.
* Les messages d'organisation de parties sont supprimés lorsqu'elle est lancée.
* Lorsque les joueurs se banquent, le dernier gagne.
* Les parties se lancent seules après 60 secondes.
* Seul le créateur de la partie ou un admin peut faire commencer la partie.
* Les cartes sont désormais toujours accessible (mais pour jouer il faut attendre son tour, les fermer et les rouvrir). **EXPERIMENTAL**

### Fixed

* Plus de 4 joueurs ne peuvent plus rejoindre la partie.

### DX

* Better logging
