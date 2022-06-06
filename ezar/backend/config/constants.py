from os import environ
from disnake import Permissions
from dotenv import load_dotenv

load_dotenv()


class Bot:
    name = "eZaR"
    version = "3.1.0"
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


class Config:
    main_token = environ.get("MAIN_TOKEN")
    beta_token = environ.get("BETA_TOKEN")
    mongo_uri = environ.get("MONGO_URI")
    owner_ids = environ["OWNER_IDS"]
    test_guilds = int(environ["TEST_GUILDS"])


class Colors:
    purple = 0x8704C8
    green = 0x27A027
    white = 0xFFFFFF
    grey = 0x5B5959
    red = 0xFE4D4D
    yellow = 0xFEFE4D


class Emojis:
    edit = ""
