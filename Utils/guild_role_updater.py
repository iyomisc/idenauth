import json

from discord.utils import get

from idena_auth.auth import auth


async def update_guild_roles(guilds, CONFIG, ROLES, check_last_status=True):
    data = auth.db.get_all_status()
    with open(CONFIG["status_file"]) as f:
        STATUS = json.load(f)

    for user_id, address, userstatus in data:
        state = ""
        if address in STATUS:
            state = STATUS[address]
        if check_last_status and state == userstatus:
            continue
        auth.db.set_address_status(address, state)
        for guild in guilds:
            member = guild.get_member(int(user_id))
            if member is not None:
                await member.remove_roles(get(guild.roles, name=ROLES[userstatus]))
                await member.add_roles(get(guild.roles, name=ROLES[state]))
    return STATUS
