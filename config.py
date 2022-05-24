# yooo guiz Herox 
import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "𝑾𝑶𝑹𝑳𝑫 𝑴𝑼𝑺𝑰𝑪 💗ˣ")
API_ID = int(getenv("API_ID", "13382519"))
API_HASH = getenv("API_HASH", "3c852e55d6ef31f7acd8e4a666465e07")
OWNER_NAME = getenv("OWNER_NAME", "𝑾𝑶𝑹𝑳𝑫 𝑴𝑼𝑺𝑰𝑪 💗ˣ")
ALIVE_NAME = getenv("ALIVE_NAME", "𝑾𝑶𝑹𝑳𝑫 𝑴𝑼𝑺𝑰𝑪 💗ˣ")
BOT_USERNAME = getenv("BOT_USERNAME", "WorldMusicly_Bot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "World_Musicly")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "Gr_World_Music")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "Ch_World_Music")
SUDO_USERS = list(map(int, getenv("SUDO_USERS", "1491415522 1419419100 2112059230").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/a322550bfdbbc3caf4f55.jpg")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "300"))
UPSTREAM_REPO = getenv("UPSTREAM_REPO", "https://github.com/ScolzeWA/World1")
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/d6f92c979ad96b2031cba.png")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/596f75a52ea9bf0109644.png")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/f02efde766160d3ff52d6.png")
IMG_4 = getenv("IMG_4", "https://telegra.ph/file/be5f551acb116292d15ec.png")
IMG_5 = getenv("IMG_5", "https://telegra.ph/file/92e8c83e9148c6fea5f3b.png")
IMG_6 = getenv("IMG_6", "https://telegra.ph/file/92e8c83e9148c6fea5f3b.png")

