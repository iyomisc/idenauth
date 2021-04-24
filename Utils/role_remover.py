from discord.utils import get


async def remove_roles(user, bot, roles, is_id=False):
    if is_id:
        user_id = user
    else:
        user_id = user.id
    for guild in bot.guilds:
        member = guild.get_member(user_id)
        if member is not None:
            await member.remove_roles(*[get(guild.roles, name=role) for _, role in roles.items()])
