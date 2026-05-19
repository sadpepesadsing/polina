from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFormLayout, QFrame, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from auth.auth_service import AuthService


class LoginWindow(QWidget):
    def __init__(self, auth_service: AuthService, on_login_success):
        super().__init__()
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        self.setWindowTitle("Виртуальный деканат — Вход")
        self.resize(520, 300)
        self.setStyleSheet(
            """
            QWidget { background-color: #f2f5fa; font-size: 14px; }
            QFrame#card { background: white; border: 1px solid #dce4f0; border-radius: 12px; }
            QLineEdit { background: white; border: 1px solid #cfd8e6; border-radius: 8px; padding: 7px; }
            QPushButton { background: #2f80ed; color: white; border: none; border-radius: 8px; padding: 9px 14px; }
            QPushButton:hover { background: #1d6fe0; }
            """
        )

        self.login_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #c62828;")

        login_btn = QPushButton("Войти")
        login_btn.clicked.connect(self._authenticate)

        form = QFormLayout()
        form.addRow("Логин:", self.login_input)
        form.addRow("Пароль:", self.password_input)

        card = QFrame()
        card.setObjectName("card")
        card_layout = QVBoxLayout(card)
        title = QLabel("<h2 style='margin: 0;'>Вход в систему</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        card_layout.addWidget(title)
        card_layout.addLayout(form)
        card_layout.addWidget(login_btn)
        card_layout.addWidget(QLabel("Тестовые учётные записи: user1/userpass1, dekanat1/dekanatpass1"))
        card_layout.addWidget(self.error_label)

        root = QVBoxLayout(self)
        root.addStretch()
        root.addWidget(card)
        root.addStretch()

    def _authenticate(self):
        self.error_label.setText("")
        user = self.auth_service.authenticate(
            self.login_input.text().strip(), self.password_input.text()
        )
        if user is None:
            self.error_label.setText("Ошибка входа: неверный логин или пароль.")
            return
        self.on_login_success(user)
