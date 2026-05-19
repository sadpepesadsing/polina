from __future__ import annotations

import hashlib

from auth.auth_service import AuthService
from models.entities import Role, User


class MockAuthService(AuthService):
    def __init__(self, user_role: Role, dean_staff_role: Role):
        self._users = {
            "user1": User(login="user1", role=user_role, full_name="Обычный пользователь"),
            "dekanat1": User(login="dekanat1", role=dean_staff_role, full_name="Сотрудник деканата"),
        }
        # Mock credential storage: login -> sha256(password)
        self._password_hashes = {
            "user1": self._hash_password("userpass1"),
            "dekanat1": self._hash_password("dekanatpass1"),
        }

    def authenticate(self, login: str, password: str) -> User | None:
        user = self._users.get(login)
        if user is None:
            return None
        if self._password_hashes.get(login) == self._hash_password(password):
            return user
        return None

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
