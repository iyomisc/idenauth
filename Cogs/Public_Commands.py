import discord.ext.commands
from discord.ext import commands
from discord.utils import get

from idena_auth.auth import auth
from Utils.guild_role_updater import update_guild_roles
import Utils.role_remover


class Public(commands.Cog, name="Available for everyone"):
    """
    Cog with Commands that are available for all
    """

    def __init__(self, b):
        self.b = b
        print("General Commands succesfully added to the bot!")

    @commands.command(name="status",
                      brief="Updates your status",
                      help="If you are logged in it retrieves new data from the api to update your status",
                      aliases=["state","update","refresh"])
    async def status(self, ctx):
        """Updates your status after you logged in"""
        if not auth.db.is_token_auth(str(ctx.message.author.id)):
            await self.login(ctx)
            return
        await Utils.role_remover.remove_roles(ctx.message.author, self.b, self.b.Roles)
        user_id = ctx.message.author.id
        address = auth.db.get_address(str(user_id))
        state = ""
        if address in self.b.Status:
            state = self.b.Status[address]
            auth.db.set_address_status(address, status=state)

        for guild in self.b.guilds:
            member = guild.get_member(user_id)
            if member is not None:
                await member.add_roles(get(guild.roles, name=self.b.Roles[state]))
        await ctx.message.author.send("Your status has been updated to '{}'".format(self.b.Roles[state]))
        await ctx.message.add_reaction("👍")

    @commands.command(name="logout",
                      brief="Logs you out",
                      help="Unlinks your address from this account",
                      aliases=["lo","lgout","logou"])
    async def logout(self, ctx):
        """Unlinks your address from this account"""
        auth.db.remove_token(str(ctx.message.author.id))
        await Utils.role_remover.remove_roles(ctx.message.author, self.b, self.b.Roles)
        await ctx.message.add_reaction("👍")

    @commands.command(name="login",
                      brief="Logs you in",
                      help="Sends you a link to authenticate yourself",
                      aliases=["li","lgin","logi","validate"])
    async def login(self, ctx:discord.ext.commands.Context):
        """Gives a link to login"""
        if auth.db.is_token_auth(str(ctx.message.author.id)):
            address = auth.db.get_address(str(ctx.message.author.id))
            await ctx.message.author.send(
                "You are already logged with {} ({})\nYou can logout using `{}logout`".format(address,
                                                                                              auth.db.get_address_status(
                                                                                                  address), ctx.prefix))
            return
        auth.get_dna_url(token=str(ctx.message.author.id))
        await ctx.message.author.send(
            "Login with {}{}\nThen update your status with `{}status`".format("https://idenauth.dragginator.com/auth/",
                                                                              ctx.message.author.id, ctx.prefix))
        await ctx.message.add_reaction("👍")


