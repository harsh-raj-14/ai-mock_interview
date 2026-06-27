from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from interviews.models import InterviewSession, JobRole


class DashboardTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="dashboard-user",
            password="StrongPass123!",
        )
        cls.other_user = get_user_model().objects.create_user(
            username="dashboard-other",
            password="StrongPass123!",
        )
        cls.role = JobRole.objects.create(
            name="Dashboard Test Role",
            description="Used by dashboard tests.",
        )
        cls.first_session = InterviewSession.objects.create(
            user=cls.user,
            job_role=cls.role,
            total_score=60,
        )
        cls.second_session = InterviewSession.objects.create(
            user=cls.user,
            job_role=cls.role,
            total_score=80,
        )
        cls.other_session = InterviewSession.objects.create(
            user=cls.other_user,
            job_role=cls.role,
            total_score=100,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_dashboard_uses_only_current_users_sessions(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["total_interviews"], 2)
        self.assertEqual(response.context["average_score"], 70)
        self.assertEqual(response.context["highest_score"], 80)
        self.assertEqual(response.context["lowest_score"], 60)
        self.assertEqual(response.context["performance_level"], "Intermediate")

    def test_user_cannot_view_another_users_session(self):
        response = self.client.get(
            reverse("session_detail", args=[self.other_session.id])
        )

        self.assertEqual(response.status_code, 404)
