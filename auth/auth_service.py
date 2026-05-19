from __future__ import annotations

from abc import ABC, abstractmethod
from models.entities import User


class AuthService(ABC):
    @abstractmethod
    def request_challenge(self, login: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def authenticate(self, login: str, response: str) -> User | None:
        raise NotImplementedError
