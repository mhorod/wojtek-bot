import discord

async def ping(ctx: discord.ext.commands.Context):
    await ctx.send("pong")
    await ctx.message.add_reaction("🐸")

def add_ping(bot: discord.Client):
    bot.command()(ping)
    print("ping added")