from __future__ import annotations

from PyQt6.QtWidgets import (
    QFrame,
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
    def __init__(self, schedule_service: ScheduleService, on_logout):
        super().__init__()
        self.schedule_service = schedule_service
        self.on_logout = on_logout
        self.setWindowTitle("Электронное расписание — Пользователь")
        self.resize(900, 500)
        self.setStyleSheet(
            """
            QWidget { background-color: #f7f9fc; font-size: 14px; }
            QPushButton { background: #2f80ed; color: white; border: none; border-radius: 8px; padding: 8px 14px; }
            QPushButton:hover { background: #1d6fe0; }
            QLineEdit { background: white; border: 1px solid #d3d9e2; border-radius: 8px; padding: 7px; }
            QTableWidget { background: white; border: 1px solid #e1e6ef; border-radius: 8px; gridline-color: #edf1f7; }
            """
        )

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Например: ИВТ-101")
        refresh_btn = QPushButton("Обновить")
        refresh_btn.clicked.connect(self.load_table)
        logout_btn = QPushButton("Выйти")
        logout_btn.clicked.connect(self.on_logout)

        self.table = QTableWidget()
        set_table_headers(self.table, ["День", "Пара", "Группа", "Дисциплина", "Преподаватель", "Аудитория"])

        header_card = QFrame()
        header_card.setStyleSheet("QFrame { background: white; border: 1px solid #e1e6ef; border-radius: 10px; }")
        header_layout = QVBoxLayout(header_card)
        header_layout.addWidget(QLabel("<h2 style='margin: 0;'>Просмотр опубликованного расписания</h2>"))

        top = QHBoxLayout()
        top.addWidget(QLabel("Фильтр по группе:"))
        top.addWidget(self.filter_input)
        top.addWidget(refresh_btn)
        top.addWidget(logout_btn)

        root = QVBoxLayout(self)
        root.addWidget(header_card)
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
