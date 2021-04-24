from discord.ext import commands
from discord.ext.commands import Context

from Utils.guild_role_updater import update_guild_roles


class Admin(commands.Cog, name="ADMIN ONLY"):
    """
    Cog with Commands that are only available for Admins
    """

    def __init__(self, b):
        self.b = b
        print("Admin Commands succesfully added to the bot!")

    @commands.command(name="update_roles",
                      brief="ADMIN ONLY",
                      help="Updates Roles",
                      aliases=["updateroles", "update roles"])
    async def update_roles(self, ctx:Context):
        """Admin command"""
        if ctx.message.author.id not in self.b.CONFIG["admins"]:
            print("The User with the id {} tried to do update_roles".format(str(ctx.author.id)))
            await ctx.reply("Thats Admin only!")
            return
        self.b.Status = await update_guild_roles(self.b.guilds, self.b.CONFIG, self.b.Roles)
        await ctx.message.add_reaction("👍")

