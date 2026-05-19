from __future__ import annotations

import hashlib
import secrets

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
        self._active_challenges: dict[str, str] = {}
        self._challenge_counter: dict[str, int] = {}

    def authenticate(self, login: str, password: str) -> User | None:
        """
        Mock handshake-based authentication with one-time dynamic password.
        1) Identify user by login.
        2) Build one-time challenge.
        3) Client computes dynamic response from password + challenge.
        4) Server verifies expected response and invalidates challenge.
        """
        user = self._users.get(login)
        if user is None:
            return None

        challenge = self._issue_challenge(login)
        client_response = self._build_client_response(password, challenge)
        expected_response = self._build_expected_response(login, challenge)
        self._active_challenges.pop(login, None)

        if client_response == expected_response:
            return user
        return None

    def _issue_challenge(self, login: str) -> str:
        counter = self._challenge_counter.get(login, 0) + 1
        self._challenge_counter[login] = counter
        challenge = f"{login}:{counter}:{secrets.token_hex(8)}"
        self._active_challenges[login] = challenge
        return challenge

    def _build_client_response(self, password: str, challenge: str) -> str:
        password_hash = self._hash_password(password)
        return self._hash_password(f"{password_hash}:{challenge}")

    def _build_expected_response(self, login: str, challenge: str) -> str:
        stored_hash = self._password_hashes[login]
        return self._hash_password(f"{stored_hash}:{challenge}")

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode("utf-8")).hexdigest()
