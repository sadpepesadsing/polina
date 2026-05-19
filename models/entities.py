from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional, Set


@dataclass(frozen=True)
class Permission:
    code: str
    description: str = ""


@dataclass
class Role:
    name: str
    permissions: Set[str] = field(default_factory=set)
    parent: Optional["Role"] = None


@dataclass
class User:
    login: str
    role: Role
    full_name: str = ""


@dataclass
class ScheduleItem:
    day: str
    pair_number: int
    group_name: str
    discipline: str
    teacher: str
    auditorium: str
    published: bool = True


@dataclass
class Group:
    code: str
    curator: str


@dataclass
class TeacherAssignment:
    teacher: str
    discipline: str
    group_name: str


@dataclass
class Auditorium:
    building: str
    room: str
    capacity: int
