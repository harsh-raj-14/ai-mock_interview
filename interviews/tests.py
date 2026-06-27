from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Answer, InterviewSession, JobRole
from .views import FALLBACK_QUESTIONS, generate_ai_questions_logic


class InterviewFlowTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="interviewer",
            password="StrongPass123!",
        )
        cls.other_user = get_user_model().objects.create_user(
            username="other-user",
            password="StrongPass123!",
        )
        cls.role = JobRole.objects.create(
            name="Test Engineer",
            description="Tests software systems.",
            skills_required="Testing",
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_public_and_protected_pages(self):
        self.client.logout()

        self.assertEqual(self.client.get(reverse("home")).status_code, 200)
        self.assertEqual(self.client.get(reverse("login")).status_code, 200)
        self.assertEqual(self.client.get(reverse("register")).status_code, 200)
        self.assertRedirects(
            self.client.get(reverse("select_role")),
            f"{reverse('login')}?next={reverse('select_role')}",
        )

    def test_invalid_role_and_result_ids_return_404(self):
        self.assertEqual(
            self.client.get(reverse("start_interview", args=[999999])).status_code,
            404,
        )
        self.assertEqual(
            self.client.get(reverse("interview_result", args=[999999])).status_code,
            404,
        )

    def test_question_api_requires_login_and_returns_fallback(self):
        self.client.logout()
        response = self.client.get(reverse("generate_ai_questions"))
        self.assertEqual(response.status_code, 302)

        self.client.force_login(self.user)
        response = self.client.get(
            reverse("generate_ai_questions"),
            {"role": "Unknown Role"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["questions"]), 8)

    @patch("interviews.views.groq_client", None)
    def test_fallback_questions_are_copied_and_complete(self):
        original = list(FALLBACK_QUESTIONS["Software Developer"])
        role = JobRole(name="Software Developer", description="Builds software")

        questions = generate_ai_questions_logic(role)
        questions.reverse()

        self.assertEqual(len(questions), 8)
        self.assertEqual(FALLBACK_QUESTIONS["Software Developer"], original)

    @patch("interviews.views.evaluate_answer_with_ai", return_value=(8, "Good answer."))
    @patch(
        "interviews.views.generate_ai_questions_logic",
        return_value=[f"Question {number}?" for number in range(1, 9)],
    )
    def test_complete_interview_is_saved(self, generate_questions, evaluate_answer):
        url = reverse("start_interview", args=[self.role.id])
        self.assertEqual(self.client.get(url).status_code, 200)

        for _ in range(8):
            response = self.client.post(
                url,
                {"answer": "A detailed technical answer with reasoning and examples."},
            )
            self.assertEqual(response.status_code, 302)

        response = self.client.get(url)
        session = InterviewSession.objects.get(user=self.user, job_role=self.role)

        self.assertRedirects(
            response,
            reverse("interview_result", args=[session.id]),
        )
        self.assertEqual(session.total_score, 80)
        self.assertEqual(Answer.objects.filter(session=session).count(), 8)
        self.assertEqual(generate_questions.call_count, 1)
        self.assertEqual(evaluate_answer.call_count, 8)

    @patch(
        "interviews.views.generate_ai_questions_logic",
        return_value=[f"Question {number}?" for number in range(1, 9)],
    )
    def test_whitespace_only_answer_is_rejected(self, generate_questions):
        url = reverse("start_interview", args=[self.role.id])
        response = self.client.post(url, {"answer": "   "})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Please answer before submitting.")
        self.assertEqual(generate_questions.call_count, 1)

    def test_user_cannot_view_another_users_result(self):
        session = InterviewSession.objects.create(
            user=self.other_user,
            job_role=self.role,
            total_score=90,
        )

        response = self.client.get(reverse("interview_result", args=[session.id]))
        self.assertEqual(response.status_code, 404)

    def test_registration_creates_user(self):
        self.client.logout()
        response = self.client.post(
            reverse("register"),
            {
                "username": "new-user",
                "password1": "AnotherStrongPass123!",
                "password2": "AnotherStrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("login"))
        self.assertTrue(get_user_model().objects.filter(username="new-user").exists())
