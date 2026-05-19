from __future__ import annotations

from typing import List

from models.entities import Auditorium, Group, ScheduleItem, TeacherAssignment
from services.data_service import DataService
from services.schedule_service import ScheduleService


class MockScheduleService(ScheduleService):
    def __init__(self):
        self._schedule = [
            ScheduleItem("Понедельник", 1, "ИВТ-101", "Математика", "Иванов И.И.", "A-101", True),
            ScheduleItem("Понедельник", 2, "ИВТ-102", "Физика", "Петров П.П.", "B-202", True),
            ScheduleItem("Вторник", 3, "ИВТ-101", "Информатика", "Сидоров С.С.", "C-301", True),
        ]

    def get_published_schedule(self, group_filter: str = "") -> List[ScheduleItem]:
        if not group_filter.strip():
            return self._schedule
        normalized = group_filter.strip().lower()
        return [item for item in self._schedule if normalized in item.group_name.lower()]


class MockReferenceDataService(DataService):
    def get_groups(self) -> List[Group]:
        return [
            Group("ИВТ-101", "Иванова А.А."),
            Group("ИВТ-102", "Кузнецов Д.Д."),
        ]

    def get_teacher_assignments(self) -> List[TeacherAssignment]:
        return [
            TeacherAssignment("Иванов И.И.", "Математика", "ИВТ-101"),
            TeacherAssignment("Петров П.П.", "Физика", "ИВТ-102"),
        ]

    def get_auditoriums(self) -> List[Auditorium]:
        return [
            Auditorium("Корпус A", "101", 30),
            Auditorium("Корпус B", "202", 50),
        ]
