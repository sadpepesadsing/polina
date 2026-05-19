from __future__ import annotations

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from services.schedule_service import ScheduleService
from ui.common import set_table_headers


class UserMainWindow(QWidget):
    def __init__(self, schedule_service: ScheduleService):
        super().__init__()
        self.schedule_service = schedule_service
        self.setWindowTitle("Электронное расписание — Пользователь")
        self.resize(900, 500)

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Например: ИВТ-101")
        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(self.load_table)

        self.table = QTableWidget()
        set_table_headers(self.table, ["День", "Пара", "Группа", "Дисциплина", "Преподаватель", "Аудитория"])

        top = QHBoxLayout()
        top.addWidget(QLabel("Фильтр по группе:"))
        top.addWidget(self.filter_input)
        top.addWidget(refresh_btn)

        root = QVBoxLayout(self)
        root.addWidget(QLabel("<h2>Просмотр опубликованного расписания</h2>"))
        root.addLayout(top)
        root.addWidget(self.table)

        self.load_table()

    def load_table(self):
        data = self.schedule_service.get_published_schedule(self.filter_input.text())
        self.table.setRowCount(len(data))
        for i, item in enumerate(data):
            self.table.setItem(i, 0, QTableWidgetItem(item.day))
            self.table.setItem(i, 1, QTableWidgetItem(str(item.pair_number)))
            self.table.setItem(i, 2, QTableWidgetItem(item.group_name))
            self.table.setItem(i, 3, QTableWidgetItem(item.discipline))
            self.table.setItem(i, 4, QTableWidgetItem(item.teacher))
            self.table.setItem(i, 5, QTableWidgetItem(item.auditorium))
