import random

import discord.ext.commands
from discord.ext import commands
from discord.utils import get

import Utils.role_remover
from idena_auth.auth import auth


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
                      aliases=["state", "update", "refresh"])
    @commands.cooldown(3, 60, commands.BucketType.user)
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
                      aliases=["lo", "lgout", "logou"])
    @commands.cooldown(2, 60, commands.BucketType.user)
    async def logout(self, ctx):
        """Unlinks your address from this account"""
        auth.db.remove_token(str(ctx.message.author.id))
        await Utils.role_remover.remove_roles(ctx.message.author, self.b, self.b.Roles)
        await ctx.message.add_reaction("👍")

    @commands.command(name="login",
                      brief="Logs you in",
                      help="Sends you a link to authenticate yourself",
                      aliases=["li", "lgin", "logi", "validate"])
    @commands.cooldown(3, 60, commands.BucketType.user)
    async def login(self, ctx: discord.ext.commands.Context):
        """Gives a link to login"""
        if auth.db.is_token_auth(str(ctx.message.author.id)):
            address = auth.db.get_address(str(ctx.message.author.id))
            await ctx.message.author.send(
                "You are already logged with {} ({})\n"
                "You can logout using `{}logout`".format(address,
                                                         auth.db.get_address_status(
                                                             address), ctx.prefix))
            return
        auth.get_dna_url(token=str(ctx.message.author.id))
        await ctx.message.author.send(
            "Login with {}{}\nThen update your status with `{}status`".format("https://idenauth.dragginator.com/auth/",
                                                                              ctx.message.author.id, ctx.prefix))
        await ctx.message.add_reaction("👍")

    @login.error
    async def spam_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Stop Spamming! Try again in {error.retry_after:.2f}s.",
                            delete_after=15)

    @logout.error
    async def spam_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Stop Spamming! Try again in {error.retry_after:.2f}s.",
                            delete_after=15)

    @status.error
    async def spam_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.reply(f"Stop Spamming! Try again in {error.retry_after:.2f}s.",
                            delete_after=15)

    @commands.command(name="website",
                      brief="Offical Website",
                      help="Sends you a link to the offical webpage",
                      aliases=["link", "page", "webpage", "donate"])
    async def website(self, ctx: commands.Context):
        embed = discord.Embed(color=discord.Colour(random.randint(0, 16777215)))
        embed.title = "Links"
        embed.add_field(name="Website", value="https://www.idena.io/", inline=True)
        embed.add_field(name="Discord", value="https://discord.gg/96Sw2e6", inline=True)
        embed.add_field(name="Bots Github", value="https://github.com/iyomisc/idenauth", inline=True)
        embed.add_field(name="Donate to bot devs",
                        value="iyomisc: 0xf2cc549874f366b66b11eb7bb3ad5a66343ce369 \n "
                              "The_Bow_Hunter: 0x590a5c6002f45e26cf8d818299ce35925e5f6732")
        await ctx.reply(embed=embed, delete_after=40)
