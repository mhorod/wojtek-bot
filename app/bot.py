import os
import discord
import random

with open("secrets/TOKEN", "r") as f:
    token = f.read()

# Create intents for managing reactions and channels
intents = discord.Intents.default()
intents.reactions = True
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

def can_manage_roles(user):
    return user.guild_permissions.manage_roles

def is_dzban(user):
    return any(role.name == "dzban" for role in user.roles)

def is_licestarosta(user):
    return any(role.name == "Licestarosta" for role in user.roles)

@client.event
async def on_ready():
    await tree.sync()

@client.event
async def on_message(message):
    actions = {
        '!ping': pong,
    }

    for action in actions:
        if message.content.startswith(action):
            await actions[action](message)

async def pong(message):
    await message.channel.send("pong")
    # react with frog emoji
    await message.add_reaction("🐸")


@tree.command(name="ping", description="ping the bot")
async def self(interaction):
    await interaction.response.send_message("pong")

def to_kebab_case(string):
    return string.lower().strip().replace(" ", "-")

@tree.command(name="create-subject", description="Create a subject")
async def create_subject(interaction, name: str):
    if is_name_stupid(name):
        await interaction.response.send_message("nie psuć mi bota")
        return

    if not can_manage_roles(interaction.user):
        if is_dzban(interaction.user):
            await interaction.response.send_message("Nawet nie próbuj 🔫🐸")
        else:
            await interaction.response.send_message("You can't to that 🐸")
        return

    channel_name = to_kebab_case(name)
    role_name = to_kebab_case(name)

    # check if channel or role already exists
    if discord.utils.get(interaction.guild.roles, name=role_name):
        await interaction.response.send_message(f"Role {role_name} already exists")
        return
    if discord.utils.get(interaction.guild.channels, name=channel_name):
        await interaction.response.send_message(f"Channel {channel_name} already exists")
        return

    category = discord.utils.get(interaction.guild.categories, name="fakultety")
    role = await interaction.guild.create_role(name=role_name)
    channel = await interaction.guild.create_text_channel(channel_name, category=category)

    # set role color to be blue
    await role.edit(color=discord.Colour.blue())

    # set channel to be only visible to role and the bot
    await channel.set_permissions(role, view_channel=True)
    await channel.set_permissions(interaction.guild.me, view_channel=True)
    await channel.set_permissions(interaction.guild.default_role, view_channel=False)

    
    add_role(role_name)
    await interaction.response.send_message(f"Subject {role_name} created")

@tree.command(name="delete-subject", description="Delete a subject")
async def delete_subject(interaction, name: str):
    if is_name_stupid(name):
        await interaction.response.send_message("nie psuć mi bota")
        return

    if not can_manage_roles(interaction.user):
        if is_dzban(interaction.user):
            await interaction.response.send_message("Nawet nie próbuj 🔫🐸")
        else:
            await interaction.response.send_message("You can't to that 🐸")
        return

    channel_name = to_kebab_case(name)
    role_name = to_kebab_case(name)
    
    if not can_delete(role_name):
        await interaction.response.send_message("Wyluzuj, jeszcze coś popsujesz")
        return

    # check if channel or role already doesn't exist
    if not discord.utils.get(interaction.guild.roles, name=role_name):
        await interaction.response.send_message(f"Subject {role_name} doesn't exist")
        return

    role = discord.utils.get(interaction.guild.roles, name=role_name)
    channel = discord.utils.get(interaction.guild.channels, name=channel_name)
    
    remove_role(role_name)
    if role:
        await role.delete()
    if channel:
        await channel.delete()

    await interaction.response.send_message(f"Subject {role_name} deleted")

@tree.command(name="add-me-to", description="Add yourself to a subject")
async def add_me_to(interaction, name: str):
    if is_name_stupid(name):
        await interaction.response.send_message("nie psuć mi bota")
        return

    role_name = to_kebab_case(name)
    role = discord.utils.get(interaction.guild.roles, name=role_name)

    if role_name not in load_roles() or not role:
        await interaction.response.send_message(f"Subject {role_name} doesn't exist")
        return

    await interaction.user.add_roles(role)
    response = f"{interaction.user.name} was added to {role_name}"
    if is_licestarosta(interaction.user):
        response = "Our mighty Licestarosta " + response
    await interaction.response.send_message(response)

@tree.command(name="remove-me-from", description="Remove yourself from a subject")
async def remove_me_from(interaction, name: str):
    if is_name_stupid(name):
        await interaction.response.send_message("nie psuć mi bota")
        return

    role_name = to_kebab_case(name)
    role = discord.utils.get(interaction.guild.roles, name=role_name)

    if role_name not in load_roles() or not role:
        await interaction.response.send_message(f"Subject {role_name} doesn't exist")
        return

    await interaction.user.remove_roles(role)
    response = f"{interaction.user.name} was removed from {role_name}"
    if is_licestarosta(interaction.user):
        response = "Our mighty Licestarosta " + response
    await interaction.response.send_message(response)

@tree.command(name="list-subjects", description="List all subjects you can get access to")
async def list_subjects(interaction):
    result = "\n".join(load_roles())
    if len(result) == 0:
        result = "There are currently no subjects :("

    await interaction.response.send_message(result)


def can_delete(role):
    roles = load_roles()
    return role in roles

def load_roles():
    try:
        f = open("roles.txt", "r")
        return set(f.read().split(' '))
    except:
        return set()

def save_roles(roles):
    with open("roles.txt", "w") as f:
        f.write(" ".join(roles))

def add_role(role):
    roles = load_roles()
    roles.add(role)
    save_roles(roles)

def remove_role(role):
    roles = load_roles()
    if role in roles:
        roles.remove(role)
    save_roles(roles)

def is_name_stupid(name):
    return len(name) >= 30

def is_unforgivable_bonk(member):
    return is_joasia(member) or is_starosta(member)

def is_joasia(user):
    return any(role.name == "Joasia" for role in user.roles)

def is_starosta(user):
    return any(role.name == "Starosta" for role in user.roles)

@tree.command(name="bonk", description="ping the bot")
async def self(interaction, member: discord.Member):
        if interaction.channel.category.id != 895765200228216913:
            await interaction.response.send_message("illegal bonk")
            await interaction.delete_original_response()
        elif interaction.user.id == member.id:
            with open("self-bonk.png", "rb") as f:
                bonk = discord.File(f)
                await interaction.response.send_message(f"<@{interaction.user.id}> bonks themself", file=bonk)
        elif is_unforgivable_bonk(member):
            with open("unforgivable-bonk.jpg", "rb") as f:
                bonk = discord.File(f)
                await interaction.response.send_message(f"<@{interaction.user.id}> tried to bonk someone who shouldn't even be bonked. Shame.", file=bonk)
        elif is_licestarosta(member):
            with open("no-bonk.png", "rb") as f:
                bonk = discord.File(f)
                await interaction.response.send_message(f"<@{interaction.user.id}> tried to bonk our mighty Licestarosta but our mighty Licestarosta is unbonkable", file=bonk)
        elif is_dzban(interaction.user) or random.randint(1, 10) == 1:
            with open("self-bonk.png", "rb") as f:
                bonk = discord.File(f)
                await interaction.response.send_message(f"<@{interaction.user.id}> tried to bonk someone but ended up bonking themself", file=bonk)
        else:
            with open("bonk.jpg", "rb") as f:
                bonk = discord.File(f)
                await interaction.response.send_message(f"<@{interaction.user.id}> bonks <@{member.id}>", file=bonk)

client.run(token)
