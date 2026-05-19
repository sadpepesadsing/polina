from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from models.entities import Auditorium, Group, TeacherAssignment


class DataService(ABC):
    @abstractmethod
    def get_groups(self) -> List[Group]:
        raise NotImplementedError

    @abstractmethod
    def get_teacher_assignments(self) -> List[TeacherAssignment]:
        raise NotImplementedError

    @abstractmethod
    def get_auditoriums(self) -> List[Auditorium]:
        raise NotImplementedError
