import discord
from discord.ext import commands

import ping
from color_roles import ColorRoles

# Create intents for managing reactions and channels
intents = discord.Intents.default()
intents.reactions = True
intents.members = True
intents.message_content = True

bot = commands.Bot(intents=intents, command_prefix="!")

async def on_ready():
    print("bot is ready")
    await bot.tree.sync()

def load_token(path):
    with open(path, "r") as f:
        return f.read()
    
ping.add_ping(bot)
ColorRoles(bot)
bot.event(on_ready)
bot.run(load_token("secrets/TOKEN"))