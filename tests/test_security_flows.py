import unittest

from access.access_manager import AccessManager
from auth.mock_auth_service import MockAuthService
from models.entities import Role, User


class SecurityFlowsTest(unittest.TestCase):
    def setUp(self):
        self.user_role = Role(name="user", permissions={"schedule.read"})
        self.dean_role = Role(
            name="dean_staff",
            parent=self.user_role,
            permissions={
                "groups.edit",
                "assignments.edit",
                "auditoriums.edit",
                "schedule.generate",
                "schedule.approve",
                "schedule.publish",
            },
        )
        self.auth = MockAuthService(self.user_role, self.dean_role)

    def test_handshake_authentication_success(self):
        user = self.auth.authenticate("user1", "userpass1")
        self.assertIsNotNone(user)
        self.assertEqual(user.login, "user1")

    def test_handshake_authentication_rejects_bad_password(self):
        user = self.auth.authenticate("user1", "wrong")
        self.assertIsNone(user)

    def test_access_matrix_user_permissions(self):
        user = User(login="user1", role=self.user_role)
        access = AccessManager(user)
        self.assertTrue(access.has_permission("schedule.read"))
        self.assertFalse(access.has_permission("groups.edit"))

    def test_hierarchical_role_inheritance(self):
        dean = User(login="dekanat1", role=self.dean_role)
        access = AccessManager(dean)
        self.assertTrue(access.has_permission("groups.edit"))
        self.assertTrue(access.has_permission("schedule.read"))


if __name__ == "__main__":
    unittest.main()
