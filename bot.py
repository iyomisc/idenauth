
import json
import discord
from discord.ext import commands
from discord.utils import get
from idena_auth.auth import auth

with open("bot_config.json") as f:
    CONFIG = json.load(f)
    
with open(CONFIG["status_file"]) as f:
    STATUS = json.load(f)
ROLES = {"": "Logged", "Candidate": "Candidate", "Newbie": "Newbie", "Verified": "Verified", "Human": "Human", "Suspended": "Suspended", "Zombie": "Zombie"}

PREFIX = "auth/"
bot = commands.Bot(command_prefix=PREFIX)


async def remove_roles(user, is_id=False):
    if is_id:
        user_id = user
    else:
        user_id = user.id
    for guild in bot.guilds:
        member = guild.get_member(user_id)
        if member is not None:
            await member.remove_roles(*[get(guild.roles, name=role) for _, role in ROLES.items()])

@bot.command()
async def update_roles(ctx):
    """Admin command"""
    if ctx.message.author.id not in CONFIG["admins"]:
        return
    await update_guild_roles(bot.guilds)
    await ctx.message.add_reaction("👍")
    

async def update_guild_roles(guilds, check_last_status=True):
    global STATUS
    data = auth.db.get_all_status()
    with open(CONFIG["status_file"]) as f:
        STATUS = json.load(f)
        
    for user_id, address, status in data:
        state = ""
        if address in STATUS:
            state = STATUS[address]
        if check_last_status and state == status:
            continue
        auth.db.set_address_status(address, state)
        for guild in guilds:
            member = guild.get_member(int(user_id))
            if member is not None:
                await member.remove_roles(get(guild.roles, name=ROLES[status]))
                await member.add_roles(get(guild.roles, name=ROLES[state]))

@bot.command()
async def login(ctx):
    """Gives a link to login"""
    if auth.db.is_token_auth(str(ctx.message.author.id)):
        address = auth.db.get_address(str(ctx.message.author.id))
        await ctx.message.author.send("You are already logged with {} ({})\nYou can logout using `!logout`".format(address, auth.db.get_address_status(address)))
        return
    auth.get_dna_url(token=str(ctx.message.author.id))
    await ctx.message.author.send("Login with {}{}\nThen update your status with `{}status`".format("https://discordauth.idena.site/auth/", ctx.message.author.id, PREFIX))
    await ctx.message.add_reaction("👍")
    
@bot.command()
async def status(ctx):
    """Updates your status after you logged in"""
    if not auth.db.is_token_auth(str(ctx.message.author.id)):
        await login(ctx)
        return
    await remove_roles(ctx.message.author)
    user_id = ctx.message.author.id
    address = auth.db.get_address(str(user_id))
    state = ""
    if address in STATUS:
        state = STATUS[address]
        auth.db.set_address_status(address, status=state)
        
    for guild in bot.guilds:
        member = guild.get_member(user_id)
        if member is not None:
            await member.add_roles(get(guild.roles, name=ROLES[state]))
    await ctx.message.author.send("Your status has been updated to '{}'".format(ROLES[state]))
    await ctx.message.add_reaction("👍")

@bot.command()
async def logout(ctx):
    """Unlinks your address from this account"""
    auth.db.remove_token(str(ctx.message.author.id))
    await remove_roles(ctx.message.author)
    await ctx.message.add_reaction("👍")

@bot.event
async def on_guild_join(guild):
    for _, role in ROLES.items():
        await guild.create_role(name=role)
    await update_guild_roles([guild], check_last_status=False)
        
@bot.event
async def on_member_join(member):
    status = auth.db.get_token_status(member.id)
    if status is None:
        return
    await member.add_roles(get(member.guild.roles, name=ROLES[status]))

"""
@bot.event
async def on_ready():
    await remove_roles(, is_id=True)
"""
bot.run(CONFIG["token"])
