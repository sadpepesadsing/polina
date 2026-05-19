from __future__ import annotations

from models.entities import Role, User


class AccessManager:
    def __init__(self, current_user: User):
        self.current_user = current_user

    def has_permission(self, permission_code: str) -> bool:
        return self._role_has_permission(self.current_user.role, permission_code)

    def _role_has_permission(self, role: Role, permission_code: str) -> bool:
        if permission_code in role.permissions:
            return True
        if role.parent is None:
            return False
        return self._role_has_permission(role.parent, permission_code)
