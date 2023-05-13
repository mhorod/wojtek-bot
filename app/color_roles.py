import discord

class ColorRoles:
    def __init__(self, bot):
        self.bot = bot
        bot.tree.command(name="set-color", description="Set your color")(self.set_color)
        bot.tree.command(name="unset-color", description="Unet your color")(self.unset_color)
        bot.tree.command(name="add-color", description="Add a color to the list of available colors")(self.add_color)
        bot.tree.command(name="remove-color", description="Remove a color from the list of available colors")(self.remove_color)
        bot.tree.command(name="list-colors", description="List all available colors")(self.list_colors)

        self.name_to_role = {}

    def is_stupid_name(self, name):
        return len(name) >= 30

    async def add_color(self, interaction, color_name: str, role_name: str):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("You can't do that 🐸")
            return
        elif self.is_stupid_name(color_name):
            await interaction.response.send_message("That's a stupid name for a color 🐸")
            return
        elif self.is_stupid_name(role_name):
            await interaction.response.send_message("That's a stupid name for a role 🐸")
            return
        else:
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role:
                self.name_to_role[color_name] = role
                await interaction.response.send_message(f"Color {color_name} bound to role {role_name}")
            else:
                await interaction.response.send_message(f"Role {role_name} doesn't exist")

    async def remove_color(self, interaction, color_name: str):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("You can't do that 🐸")
            return
        elif self.is_stupid_name(color_name):
            await interaction.response.send_message("That's a stupid name for a color 🐸")
            return
        else:
            del self.name_to_role[color_name]
            await interaction.response.send_message(f"Color {color_name} unbound.")
        

    async def list_colors(self, interaction):
        colors = "\n".join(self.name_to_role.keys())
        await interaction.response.send_message(f"Available colors:\n{colors}")
    
    async def set_color(self, interaction, color_name: str):
        if not self.color_exists(color_name):
            await interaction.response.send_message("No such color")
        else:
            role = self.name_to_role[color_name]
            await self.clear_user_colors(interaction.user)
            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Color set to {color_name}")

    async def unset_color(self, interaction):
        await self.clear_user_colors(interaction.user)
        await interaction.response.send_message("Color unset")

    async def clear_user_colors(self, user):
        roles = [role for role in user.roles if role.name in self.name_to_role]
        if roles:
            await user.remove_roles(*roles)

    def color_exists(self, color_name):
        return color_name in self.name_to_role