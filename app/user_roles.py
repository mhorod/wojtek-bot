from enum import Enum, auto
from secrets.role_ids import *

class DiscordRoles(Enum):
    HIHAL = auto()
    MUDERATOR = auto()
    JOASIA = auto()
    GOCHA = auto()
    LICESTAROSTA = auto()
    DZBAN = auto()
    VERIFIED = auto()

ROLE_MAP = {
    HIHAL_ID : DiscordRoles.HIHAL,
    MUDERATOR_ID : DiscordRoles.MUDERATOR,
    JOASIA_ID : DiscordRoles.JOASIA,
    GOCHA_ID : DiscordRoles.GOCHA,
    LICESTAROSTA_ID : DiscordRoles.LICESTAROSTA,
    DZBAN_ID : DiscordRoles.DZBAN,
    VERIFIED_ID : DiscordRoles.VERIFIED
}


def user_roles(user):
    return [ROLE_MAP[r.id] for r in user.roles if r.id in ROLE_MAP]
    