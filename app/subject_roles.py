import discord

import enum

class Permission(enum.Enum):
    MANAGE = 1
    CREATE = 2
    DELETE = 3
    ADD = 4
    REMOVE = 5

class BasicPermissions:
    def __init__(self):
        self.permissions = {}

    def add_permission(self, user, permission):
        if user not in self.permissions:
            self.permissions[user] = set()
        self.permissions[user].add(permission)

    def remove_permission(self, user, permission):
        if user in self.permissions:
            self.permissions[user].remove(permission)

    def has_permission(self, user, permission):
        return user in self.permissions and permission in self.permissions[user]

class SubjectRoles:
    def __init__(self, bot, subjects, permissions):
        self.bot = bot
        self.permissions = permissions
        self.subjects = subjects
        bot.tree.command(name="add-subject", description="Add a subject to the list of available subjects")(self.add_exisiting_subject)
        bot.tree.command(name="add-me-to", description="Add yourself to a subject")(self.add_me_to)
        bot.tree.command(name="remove-me-from", description="Remove yourself from a subject")(self.remove_me_from)
        bot.tree.command(name="list-subjects", description="List all subjects you can get access to")(self.list_subjects)

    def is_name_stupid(self, name):
        return len(name) >= 30

    async def authorize(self, interaction, name, permission):
        if not self.permissions.has_permission(interaction.user, permission):
            await interaction.response.send_message("You can't do that 🐸")
            return False
        return True

    async def validate(self, interaction, name):
        if self.is_name_stupid(name):
            await interaction.response.send_message("That's a stupid name for a subject 🐸")
            return False

        return True

    async def create_subject(self, interaction, name: str):
        pass
    
    async def add_exisiting_subject(self, interaction, name: str):
        if await self.validate(interaction, name) and await self.authorize(interaction, name, Permission.CREATE):
            role_name = self.to_kebab_case(name)
            self.subjects.add(role_name)
            await interaction.response.send_message(f"Subject {role_name} created")


    async def add_me_to(self, interaction, role_name: str):
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


    async def remove_me_from(self, interaction, role_name: str):
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


    async def list_subjects(self, interaction):
        if len(self.subjects) == 0:
            await interaction.response.send_message("There are currently no subjects :(")
        else:
            result = "Subjects:\n" + "\n".join("- " + s for s in self.subjects)
            await interaction.response.send_message(result)

    def to_kebab_case(self, string):
        return string.lower().strip().replace(" ", "-")