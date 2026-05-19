from __future__ import annotations

import sys

from PyQt6.QtWidgets import QApplication

from access.access_manager import AccessManager
from auth.mock_auth_service import MockAuthService
from models.entities import Role
from services.mock_services import MockReferenceDataService, MockScheduleService
from ui.dean_staff_window import DeanStaffMainWindow
from ui.login_window import LoginWindow
from ui.user_main_window import UserMainWindow


class AppController:
    def __init__(self):
        self.app = QApplication(sys.argv)

        user_role = Role(name="user", permissions={"schedule.read"})
        dean_role = Role(
            name="dean_staff",
            parent=user_role,
            permissions={
                "groups.edit",
                "assignments.edit",
                "auditoriums.edit",
                "schedule.generate",
                "schedule.approve",
                "schedule.publish",
            },
        )

        self.auth_service = MockAuthService(user_role=user_role, dean_staff_role=dean_role)
        self.schedule_service = MockScheduleService()
        self.data_service = MockReferenceDataService()

        self.login_window = LoginWindow(self.auth_service, self._on_login_success)
        self.main_window = None

    def _on_login_success(self, user):
        access_manager = AccessManager(user)
        if user.role.name == "dean_staff":
            self.main_window = DeanStaffMainWindow(
                access_manager, self.data_service, self.schedule_service, self._logout
            )
        else:
            self.main_window = UserMainWindow(self.schedule_service, self._logout)
        self.main_window.show()
        self.login_window.close()

    def _logout(self):
        if self.main_window is not None:
            self.main_window.close()
            self.main_window = None
        self.login_window.login_input.clear()
        self.login_window.password_input.clear()
        self.login_window.error_label.clear()
        self.login_window.show()

    def run(self):
        self.login_window.show()
        return self.app.exec()


if __name__ == "__main__":
    sys.exit(AppController().run())
