from __future__ import annotations

from PyQt6.QtWidgets import QHBoxLayout, QMainWindow, QPushButton, QTabWidget, QVBoxLayout, QWidget

from access.access_manager import AccessManager
from services.data_service import DataService
from services.schedule_service import ScheduleService
from ui.common import StubPage


def _apply_permission(button: QPushButton, allowed: bool):
    button.setEnabled(allowed)


class DeanStaffMainWindow(QMainWindow):
    def __init__(
        self, access_manager: AccessManager, data_service: DataService, schedule_service: ScheduleService, on_logout
    ):
        super().__init__()
        self.access_manager = access_manager
        self.data_service = data_service
        self.schedule_service = schedule_service
        self.on_logout = on_logout
        self.setWindowTitle("Электронное расписание — Деканат")
        self.resize(1080, 640)
        self.setStyleSheet(
            """
            QMainWindow, QWidget { background-color: #f7f9fc; font-size: 14px; }
            QPushButton { background: #2f80ed; color: white; border: none; border-radius: 8px; padding: 8px 14px; }
            QPushButton:hover { background: #1d6fe0; }
            QPushButton:disabled { background: #a8b7cc; color: #eef3fb; }
            QTabWidget::pane { border: 1px solid #dbe3ef; background: white; border-radius: 8px; }
            QTabBar::tab { background: #ebf1fb; border: 1px solid #d6deea; padding: 8px 12px; margin-right: 4px; border-top-left-radius: 6px; border-top-right-radius: 6px; }
            QTabBar::tab:selected { background: #ffffff; }
            """
        )

        tabs = QTabWidget()
        tabs.addTab(self._groups_page(), "Группы")
        tabs.addTab(self._assignments_page(), "Назначения преподавателей")
        tabs.addTab(self._auditoriums_page(), "Аудитории и корпуса")
        tabs.addTab(self._schedule_project_page(), "Проект расписания")
        tabs.addTab(self._schedule_approval_page(), "Согласование расписания")
        tabs.addTab(self._schedule_publish_page(), "Публикация расписания")
        tabs.addTab(self._published_schedule_page(), "Просмотр опубликованного расписания")
        logout_btn = QPushButton("Выйти")
        logout_btn.clicked.connect(self.on_logout)
        top_row = QHBoxLayout()
        top_row.addStretch()
        top_row.addWidget(logout_btn)

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.addLayout(top_row)
        layout.addWidget(tabs)
        self.setCentralWidget(central)

    def _groups_page(self):
        rows = [[g.code, g.curator] for g in self.data_service.get_groups()]
        add = QPushButton("Добавить")
        edit = QPushButton("Изменить")
        delete = QPushButton("Удалить")
        allowed = self.access_manager.has_permission("groups.edit")
        for btn in (add, edit, delete):
            _apply_permission(btn, allowed)
        return StubPage("GroupsPage", ["Группа", "Куратор"], rows, [add, edit, delete])

    def _assignments_page(self):
        rows = [[a.teacher, a.discipline, a.group_name] for a in self.data_service.get_teacher_assignments()]
        add, edit, delete = QPushButton("Добавить"), QPushButton("Изменить"), QPushButton("Удалить")
        allowed = self.access_manager.has_permission("assignments.edit")
        for btn in (add, edit, delete):
            _apply_permission(btn, allowed)
        return StubPage("TeacherAssignmentsPage", ["Преподаватель", "Дисциплина", "Группа"], rows, [add, edit, delete])

    def _auditoriums_page(self):
        rows = [[a.building, a.room, str(a.capacity)] for a in self.data_service.get_auditoriums()]
        add, edit, delete = QPushButton("Добавить"), QPushButton("Изменить"), QPushButton("Удалить")
        allowed = self.access_manager.has_permission("auditoriums.edit")
        for btn in (add, edit, delete):
            _apply_permission(btn, allowed)
        return StubPage("AuditoriumsPage", ["Корпус", "Аудитория", "Вместимость"], rows, [add, edit, delete])

    def _schedule_project_page(self):
        generate = QPushButton("Сформировать проект")
        _apply_permission(generate, self.access_manager.has_permission("schedule.generate"))
        return StubPage("ScheduleProjectPage", ["Статус", "Комментарий"], [["Черновик", "Mock-проект доступен"]], [generate])

    def _schedule_approval_page(self):
        approve = QPushButton("Согласовать")
        _apply_permission(approve, self.access_manager.has_permission("schedule.approve"))
        return StubPage("ScheduleApprovalPage", ["Этап", "Статус"], [["Проверка", "Ожидает решения"]], [approve])

    def _schedule_publish_page(self):
        publish = QPushButton("Опубликовать")
        _apply_permission(publish, self.access_manager.has_permission("schedule.publish"))
        return StubPage("SchedulePublishPage", ["Версия", "Статус"], [["v1-mock", "Готово к публикации"]], [publish])

    def _published_schedule_page(self):
        rows = [[s.day, str(s.pair_number), s.group_name, s.discipline] for s in self.schedule_service.get_published_schedule()]
        refresh = QPushButton("Обновить")
        _apply_permission(refresh, self.access_manager.has_permission("schedule.read"))
        return StubPage("PublishedSchedulePage", ["День", "Пара", "Группа", "Дисциплина"], rows, [refresh])
