from __future__ import annotations

from PyQt6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from auth.auth_service import AuthService


class LoginWindow(QWidget):
    def __init__(self, auth_service: AuthService, on_login_success):
        super().__init__()
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        self.setWindowTitle("Виртуальный деканат — Вход")
        self.resize(500, 260)

        self.login_input = QLineEdit()
        self.challenge_input = QLineEdit()
        self.challenge_input.setReadOnly(True)
        self.response_input = QLineEdit()
        self.error_label = QLabel()
        self.error_label.setStyleSheet("color: #c62828;")

        get_challenge_btn = QPushButton("Получить challenge")
        login_btn = QPushButton("Войти")
        get_challenge_btn.clicked.connect(self._request_challenge)
        login_btn.clicked.connect(self._authenticate)

        form = QFormLayout()
        form.addRow("Login:", self.login_input)
        form.addRow("Challenge:", self.challenge_input)
        form.addRow("Response:", self.response_input)

        root = QVBoxLayout(self)
        root.addWidget(QLabel("<h2>Mock-вход по схеме рукопожатия</h2>"))
        root.addLayout(form)

        buttons = QHBoxLayout()
        buttons.addWidget(get_challenge_btn)
        buttons.addWidget(login_btn)
        buttons.addStretch()
        root.addLayout(buttons)
        root.addWidget(self.error_label)

    def _request_challenge(self):
        self.error_label.setText("")
        try:
            challenge = self.auth_service.request_challenge(self.login_input.text().strip())
            self.challenge_input.setText(challenge)
        except ValueError as exc:
            self.error_label.setText(str(exc))

    def _authenticate(self):
        self.error_label.setText("")
        user = self.auth_service.authenticate(
            self.login_input.text().strip(), self.response_input.text().strip()
        )
        if user is None:
            self.error_label.setText("Ошибка входа: неверный response или challenge не получен.")
            return
        self.on_login_success(user)
