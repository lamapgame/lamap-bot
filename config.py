import os
from dotenv import load_dotenv

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
LOGGING_CHAT_ID = os.getenv("LOGGING_CHAT_ID")
BASE_POINTS = int(os.getenv("BASE_POINTS") or 10)
SUPER_ADMIN_LIST = str(os.getenv("SUPER_ADMIN_LIST") or "223627873, 1077515995").split(
    ","
)
CARDS_DESIGN = os.getenv("CARDS_DESIGN") or "DEFAULT"


# Achievements
# ----------------
ACHIEVEMENTS = {
    "ACH_LE_PATRON": {
        "name": "Chef de Terre",
        "emoji": "🧬",
        "description": "C'est le mbom ci même qui m'a créé.\n"
        "C'est mon papa, je dois le soulever jusqu'au ciel.",
    },
    "ACH_NEW_PLAYER": {
        "name": "Un Bleu",
        "emoji": "🌱",
        "description": "Tu viens de commencer à jouer.\n"
        "Reste concentré, ça va vite ici.",
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
    "ACH_LE_TETE": {
        "name": "Le Tété",
        "emoji": "🤑",
        "description": "Avoir 1 myondo\n"
        "L'argent ne fait pas le bonheur, mais il y contribue fortement.",
    },
    "ACH_LE_KORATEUR": {
        "name": "Le Korateur",
        "emoji": "👺",
        "description": "Kora 1000 fois.\n"
        "Les 3 ne cherchent plus leurs frère, tu es un vrai korateur.",
    },
    "ACH_LE_SNACKBAR": {
        "name": "Le Snackbar",
        "emoji": "👺",
        "description": "Distribuer 1000 trente-trois.\n"
        "Tu sers les 33s comme chez Pacho à Bastos. C'est pas bon pour la santé.",
    },
}
