from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone


class AutoLogoutMiddlewareTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="session-user",
            password="StrongPass123!",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_invalid_last_activity_value_does_not_crash(self):
        session = self.client.session
        session["last_activity"] = "invalid"
        session.save()

        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)

    def test_expired_session_logs_user_out(self):
        session = self.client.session
        session["last_activity"] = (
            timezone.now() - timedelta(minutes=11)
        ).isoformat()
        session.save()

        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, reverse("login"))
        self.assertNotIn("_auth_user_id", self.client.session)
