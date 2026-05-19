from __future__ import annotations

from abc import ABC, abstractmethod

from models.entities import User


class AuthService(ABC):
    @abstractmethod
    def authenticate(self, login: str, password: str) -> User | None:
        raise NotImplementedError
