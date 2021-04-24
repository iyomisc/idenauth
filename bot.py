import json

import discord
from discord.ext import commands

from Cogs.Listeners import Listeners
from Cogs.Admin_Commands import Admin
from Cogs.Public_Commands import Public



try:
    with open("bot_config.json") as f:
        CONFIG = json.load(f)
except FileNotFoundError:
    with open("bot_config.json", "w") as f:
        json.dump({"token": "bot_token", "admins": [429902990594539524], "status_file": "data/status.json"}, f)
    raise Exception("missing bot_config.json. I added it, please fill it out yourself! (Should only happen on first "
                    "load)")

try:
    with open(CONFIG["status_file"]) as f:
        STATUS = json.load(f)
    ROLES = {"": "Logged", "Candidate": "Logged", "Newbie": "Newbie", "Verified": "Verified", "Human": "Human",
             "Suspended": "Suspended", "Zombie": "Zombie"}
except FileNotFoundError:
    with open(CONFIG["status_file"], "w") as f:
        json.dump({}, f)
    print("Missing status file. Starting from scratch!")

PREFIX = "auth/"
intents = discord.Intents.none()
intents.messages = True  # read and write messages. Change to intents.guild_messages to disable dm commands
intents.guilds = True  # This is needed to have the Guild Object to send messages
# This ensures the bot gets as minimal information and rights as possible to function
bot = commands.Bot(commands.when_mentioned_or(PREFIX), case_insensitive=True, intents=intents)
bot.Status = STATUS
bot.CONFIG = CONFIG
bot.Roles = ROLES
Cogs = [Admin(bot), Public(bot), Listeners(bot)]

for i in Cogs:
    bot.add_cog(i)

print("""
<<---------->>
Added all Cogs. Now starting
<<---------->>
""")


@bot.event
async def on_ready():
    print("Started!")


bot.run(CONFIG["token"])
