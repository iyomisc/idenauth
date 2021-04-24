from discord.ext import commands
from discord.utils import get

from Utils.guild_role_updater import update_guild_roles
from idena_auth.auth import auth


class Listeners(commands.Cog, name="Event Listeners"):
    """
    Cog with Listeners
    """

    def __init__(self, b):
        self.b = b
        print("Listeners succesfully added to the bot!")

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for _, role in self.b.Roles.items():
            await guild.create_role(name=role)
        self.b.status = await update_guild_roles([guild], self.b.CONFIG, self.b.Roles, check_last_status=False)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        memberstatus = auth.db.get_token_status(member.id)
        if memberstatus is None:
            return
        await member.add_roles(get(member.guild.roles, name=self.b.Roles[memberstatus]))
