import discord

from permissions import *
from user_roles import *

class SubjectRoles(HasPermissions):
    class Permission(Enum):
        MANAGE = auto()
        USE = auto()

    def __init__(self, bot, subjects):
        self.bot = bot
        self.subjects = subjects


        bot.tree.command(name="load-subjects", description="Load subjects from a file")(self.load_subjects)
        bot.tree.command(name="add-subject", description="Add a subject to the list of available subjects")(self.add_existing_subject)
        bot.tree.command(name="add-me-to", description="Add yourself to a subject")(self.add_me_to)
        bot.tree.command(name="remove-me-from", description="Remove yourself from a subject")(self.remove_me_from)
        bot.tree.command(name="list-subjects", description="List all subjects you can get access to")(self.list_subjects)

    async def load_subjects(self, interaction):
        await self._load_subjects(interaction)

    async def add_existing_subject(self, interaction, name: str):
        await self._add_existing_subject(interaction, name)

    async def add_me_to(self, interaction, role_name: str):
        await self._add_me_to(interaction, role_name)

    async def remove_me_from(self, interaction, role_name: str):
        await self._remove_me_from(interaction, role_name)

    async def list_subjects(self, interaction):
        await self._list_subjects(interaction)

    def is_name_stupid(self, name):
        return len(name) >= 30

    def permissions(self, user):
        roles = user_roles(user)
        permissions = set()
        if DiscordRoles.HIHAL in roles or DiscordRoles.MUDERATOR in roles:
            permissions.add(self.Permission.MANAGE)
        if DiscordRoles.VERIFIED in roles:
            permissions.add(self.Permission.USE)
        return permissions

    async def validate(self, interaction, name):
        if self.is_name_stupid(name):
            await interaction.response.send_message("That's a stupid name for a subject 🐸")
            return False
        return True

    async def create_subject_if_not_exists(self, guild, name):
        # Create a role for the subject
        role = discord.utils.get(guild.roles, name=name)
        if role is None:
            role = await guild.create_role(name=name)

        # Create a channel for the subject
        channel = discord.utils.get(guild.channels, name=name)
        if channel is None:
            channel = await guild.create_text_channel(name)

        # remove all permissions from the channel
        await channel.set_permissions(guild.default_role, read_messages=False, send_messages=False)
        await channel.set_permissions(role, read_messages=True, send_messages=True)

    @Require(Permission.MANAGE)
    async def _load_subjects(self, interaction):
        await interaction.response.send_message("Subjects loading")
        for subject in self.subjects:
            await self.create_subject_if_not_exists(interaction.guild, subject)

    @Require(Permission.USE)
    async def _add_me_to(self, interaction, role_name: str):
        if await self.validate(interaction, role_name):
            role_name = self.to_kebab_case(role_name)
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role is None or role_name not in self.subjects:
                await interaction.response.send_message(f"Subject {role_name} doesn't exist")
                return
            else:
                message = f"Added <@{interaction.user.id}> to {role_name}"
                await interaction.user.add_roles(role)
                await interaction.response.send_message(message)


    @Require(Permission.USE)
    async def _remove_me_from(self, interaction, role_name: str):
        if await self.validate(interaction, role_name):
            role_name = self.to_kebab_case(role_name)
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role is None or role_name not in self.subjects:
                await interaction.response.send_message(f"Subject {role_name} doesn't exist")
                return
            else:
                message = f"Removed <@{interaction.user.id}> from {role_name}"
                await interaction.user.remove_roles(role)
                await interaction.response.send_message(message)


    @Require(Permission.USE)
    async def _list_subjects(self, interaction):
        if len(self.subjects) == 0:
            await interaction.response.send_message("There are currently no subjects :(")
        else:
            result = "Subjects:\n" + "\n".join("- " + s for s in self.subjects)
            await interaction.response.send_message(result)

    def to_kebab_case(self, string):
        return string.lower().strip().replace(" ", "-")