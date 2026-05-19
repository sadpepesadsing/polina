from __future__ import annotations

from auth.auth_service import AuthService
from models.entities import Role, User


class MockAuthService(AuthService):
    def __init__(self, user_role: Role, dean_staff_role: Role):
        self.user_role = user_role
        self.dean_staff_role = dean_staff_role
        self._challenges: dict[str, str] = {}
        self._users = {
            "user1": User(login="user1", role=user_role, full_name="Обычный пользователь"),
            "dekanat1": User(login="dekanat1", role=dean_staff_role, full_name="Сотрудник деканата"),
        }

    def request_challenge(self, login: str) -> str:
        if login not in self._users:
            raise ValueError("Пользователь не найден")
        challenge = f"mock_challenge_for_{login}"
        self._challenges[login] = challenge
        return challenge

    def authenticate(self, login: str, response: str) -> User | None:
        challenge = self._challenges.get(login)
        if not challenge:
            return None
        expected_response = f"response:{challenge}"
        if response.strip() == expected_response:
            return self._users[login]
        return None
