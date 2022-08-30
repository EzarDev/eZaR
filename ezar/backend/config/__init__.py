from os import environ

from disnake import Permissions
from dotenv import load_dotenv
from motor.core import Collection as MotorCollection
from motor.core import Database as MotorDatabase
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

__all__ = (
    "Bot",
    "Config",
    "Colors",
    "Emojis",
    "Database",
)


class Bot:
    name = "eZaR"
    version = "3.0.0a"
    gh_repo = "https://github.com/eZaR-Bot/3Z4R"
    pp_gist = ""
    ppal_link = "https://paypal.me/realShamlol"
    pat_link = "https://patreon.com/ezarbot"
    invite_perms = Permissions(
        attach_files=True,
        ban_members=True,
        embed_links=True,
        external_emojis=True,
        kick_members=True,
        manage_channels=True,
        manage_guild=True,
        manage_messages=True,
        manage_roles=True,
    )
    support_inv_url = "2Usu8E5KK4"


class Config:
    main_token = environ.get("MAIN_TOKEN")
    beta_token = environ.get("BETA_TOKEN")
    mongo_uri = environ.get("MONGO_URI")
    owner_ids = [int(id_) for id_ in environ["OWNER_IDS"].strip("[]").split(", ")]
    test_guilds = int(environ["TEST_GUILDS"])


class Colors:
    purple = 0x8449CA
    green = 0x27A027
    white = 0xFFFFFF
    grey = 0x5B5959
    red = 0xFE4D4D
    yellow = 0xFEFE4D


class Emojis:
    cross = "<:eZaR_cross:911561593811271741>"
    tick = "<:eZaR_tick:911561509677727764>"


class Database:
    _cluster = AsyncIOMotorClient(Config.mongo_uri)
    _db: MotorDatabase = _cluster["eZaR"]
    guild_logs: MotorCollection = _db["guild_logs"]
    economy: MotorCollection = _db["economy"]
