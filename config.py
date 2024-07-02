import os
from typing import cast
from dotenv import load_dotenv

from common.types import DesignType

# Load the stored environment variables
load_dotenv()

# Base values
# ----------------
# Telegram token
TOKEN = os.getenv("TOKEN")

# Bot Id
BOT_ID = int(os.getenv("BOT_ID") or 1397177261)

# Connection url to db
DATABASE_URL = os.getenv("DATABASE_URL")

# Gameplay values
# ----------------
# time to start game after being initiated
GAME_START_TIMEOUT = int(os.getenv("GAME_START_TIMEOUT") or 40)
TIME_TO_AFK = int(os.getenv("TIME_TO_AFK") or 50)
LOGGING_CHAT_ID = int(os.getenv("LOGGING_CHAT_ID") or 0)
BASE_POINTS = int(os.getenv("BASE_POINTS") or 10)
SUPER_ADMIN_LIST = str(os.getenv("SUPER_ADMIN_LIST") or "223627873,1077515995").split(
    ","
)
CARDS_DESIGN = cast(DesignType, str(os.getenv("CARDS_DESIGN") or "DEFAULT"))

# ruff: noqa: E501

# Achievements
# ----------------
ACHIEVEMENTS = {
    "ACH_LE_PATRON": {
        "name": "Chef de Terre",
        "emoji": "🧬",
        "description": "C'est le mbom ci même qui m'a créé.\n"
        "C'est mon papa, je dois le soulever jusqu'au ciel.",
    },
    "ACH_SUPER_QUEEN": {
        "name": "Katika Queen",
        "emoji": "👩🏽‍⚖️",
        "description": "La patronne du bot, elle gère toute vos parties\n"
        "Même si elle est pas la, elle est la.",
    },
    "CHAMP_LAMAP_2024": {
        "name": "Champion Lamap Printemps 2024",
        "emoji": "⚡",
        "description": "Au tournoi de juillet 2024, Wilfried nous a montré une masterclass.\n"
        "C'est un pro. Il connaît la carte.",
    },
    "ACH_SUPER_CHOUCHOU": {
        "name": "Katika Chouchou",
        "emoji": "🧑🏽‍⚖️",
        "description": "Meilleur Katika depuis 2020.\n"
        "Ce n'est pas l'atalaku, c'est inscrit au Guiness Book.",
    },
    "ACH_NEW_PLAYER": {
        "name": "Un Bleu",
        "emoji": "🌱",
        "description": "Tu viens de commencer à jouer.\n"
        "Reste concentré, ça va vite ici.",
    },
    "ACH_NOVICE_PLAYER": {
        "name": "Un Novice",
        "emoji": "☘️",
        "description": "Jouer 150 parties.\n"
        "Ca fait un bon moment que tu joues, je te remarque dans le terre çi.",
    },
    "ACH_MID_PLAYER": {
        "name": "Un Jongleur",
        "emoji": "🍀",
        "description": "Jouer 1 500 parties.\n"
        "Ca commence a venir. Les coubis sont tes amis."
        "Les gars ont peur de toi quand tu join la table.",
    },
    "ACH_PRO_PLAYER": {
        "name": "Un Pro",
        "emoji": "🌿",
        "description": "Jouer 5 000 parties.\n"
        "Massah ! 5 000 ? On peut te laisser avec si tu veux.",
    },
    "ACH_GOD_PLAYER": {
        "name": "Un Génie",
        "emoji": "🍁",
        "description": "Tu as joué 50 000 parties.\n"
        "Tu n'as pas de vie."
        "Tu joues matin midi soir. "
        "Gagner ou perdre n'a plus d'importance pour toi",
    },
    "ACH_SLEEPER_PRO": {
        "name": "Le Dormeur Pro",
        "emoji": "💤",
        "description": "Tu dors, ton argent rentre.\n"
        "Tu as bien mérité un petit somme. Tu as gagné 100 parties en dormant.",
    },
    "ACH_LE_NOOB": {
        "name": "Bien faible",
        "emoji": "🤡",
        "description": "Tu as perdu 20 parties de suite.\n"
        "Tu sais qu'on ne te force pas à jouer ?"
        "Tu peux aussi aller jouer au loup garou.",
    },
    "ACH_LE_DON_MAN": {
        "name": "Le Don Man / La Don Nga",
        "emoji": "👑",
        "description": "Gagner 20 parties de suite.\n"
        "Tu es sur que tu ne triches pas ?",
    },
    "ACH_LE_NDEM_MAN": {
        "name": "Le Ndem Man",
        "emoji": "🏦",
        "description": "Fuire 500 parties.\n"
        "Tu fais comment pour fuire jusqu'a 500 parties."
        "Tu fais comment dans la vraie vie tara?",
    },
    "ACH_EL_PEQUENO": {
        "name": "El Pequeno",
        "emoji": "🎩",
        "description": "*Gagner avec 21/22.\n" "Jouer petit, c'est jouer malin.",
    },
    "ACH_LA_FAMILLE": {
        "name": "Reunion de famille",
        "emoji": "🃏",
        "description": "Gagner avec les cartes d'une même famille ♠️♠️♠️♠️♠️.\n",
    },
    "ACH_LE_BOBO": {
        "name": "Le Boboh",
        "emoji": "💸",
        "description": "Avoir 500 batons\n"
        "L'argent ne fait pas le bonheur, mais il y contribue fortement.",
    },
    "ACH_LE_PAUVRE": {
        "name": "Le Pauvre",
        "emoji": "⛔",
        "description": "Avoir -500 batons\n"
        "Ca fait un bon moment que tu joues les arachides.",
    },
    "ACH_LE_NTONG_MAN": {
        "name": "Le Ntong Man",
        "emoji": "🎰",
        "description": "Gagner 200 parties avec les cartes speciales\n"
        "Tu joues avec les écorces?",
    },
    "ACH_LE_TETE": {
        "name": "Le Tété",
        "emoji": "🤑",
        "description": "Avoir 1 myondo\n"
        "L'argent ne fait pas le bonheur, mais il y contribue fortement.",
    },
    "ACH_LE_KORATEUR": {
        "name": "Le Korateur",
        "emoji": "👺",
        "description": "Kora 200 fois.\n"
        "Les 3 ne cherchent plus leurs frère, tu es un vrai korateur.",
    },
    "ACH_LE_SNACKBAR": {
        "name": "Le Snackbar",
        "emoji": "🍺",
        "description": "Distribuer 200 trente-trois.\n"
        "Tu sers les 33s comme chez Pacho à Bastos. C'est pas bon pour la santé.",
    },
    "ACH_LE_KORATE": {
        "name": "Le Koraté",
        "emoji": "🤕",
        "description": "Payer 200 koras.\n" "Comment tu peux payer 200 koras ?",
    },
    "ACH_LE_SAOULARD": {
        "name": "Le Saoulard",
        "emoji": "😵",
        "description": "Boire 200 trente-trois.\n"
        "On a compris que ton goût c'est la 33. Ne bois pas seulement ton cerveau aussi.",
    },
    "ACH_L'ANCIEN_RICHE": {
        "name": "L'ancien Riche",
        "emoji": "📉",
        "description": "Un Ancien bobo desormais dans le négatif\n"
        "Tu es comme les petits de 24ans qui disent qu'ils étaient bon aux ballon avant.",
    },
    "ACH_LA_REMONTADA": {
        "name": "L'ancien Pauvre",
        "emoji": "🚀",
        "description": "Un ancien pauvre qui est devenu riche\n"
        "Chapeau mollah, tu es comme le Barca face a Paris.",
    },
}


# Logging
# ----------------
THREAD_IDS = {"TRANSFERT": 41027, "BLOCKS": 41026, "RETREM": 41023, "OTHER": None}
