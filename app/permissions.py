from abc import ABC, abstractmethod


class PermissionManager:
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

    def permissions(self, user):
        if user in self.permissions:
            return self.permissions[user]
        else:
            return set()


class HasPermissions(ABC):
    @abstractmethod
    def permissions(self, user):
        pass

class Require:
    def __init__(self, permission):
        self.permission = permission

    def __call__(self, handler):
        async def wrapper(controller, interaction, *args, **kwargs):
            if not isinstance(controller, HasPermissions):
                raise Exception("Can't use Require decorator on a controller that doesn't implement HasPermissions")
            else:
                user_permissions = controller.permissions(interaction.user)
                if self.permission in user_permissions:
                    await handler(controller, interaction, *args, **kwargs)
                else:
                    await interaction.response.send_message("You can't do that 🐸")
        return wrapper
        