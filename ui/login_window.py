from __future__ import annotations

from PyQt6.QtWidgets import QFormLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget

from auth.auth_service import AuthService


class LoginWindow(QWidget):
    def __init__(self, auth_service: AuthService, on_login_success):
        super().__init__()
        self.auth_service = auth_service
        self.on_login_success = on_login_success
        self.setWindowTitle("Виртуальный деканат — Вход")
        self.resize(500, 240)

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

        root = QVBoxLayout(self)
        root.addWidget(QLabel("<h2>Вход в систему</h2>"))
        root.addLayout(form)
        root.addWidget(login_btn)
        root.addWidget(QLabel("Тестовые учётные записи: user1/userpass1, dekanat1/dekanatpass1"))
        root.addWidget(self.error_label)

    def _authenticate(self):
        self.error_label.setText("")
        user = self.auth_service.authenticate(
            self.login_input.text().strip(), self.password_input.text()
        )
        if user is None:
            self.error_label.setText("Ошибка входа: неверный логин или пароль.")
            return
        self.on_login_success(user)
