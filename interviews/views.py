import logging
import os
import random
import re

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import never_cache
from groq import Groq

from .models import JobRole, InterviewSession, Answer

MAX_QUESTIONS = 8
logger = logging.getLogger(__name__)

FALLBACK_QUESTIONS = {

    "Software Developer": [
        "Explain REST architecture.",
        "What is dependency injection?",
        "Explain microservices architecture.",
        "What is database indexing?",
        "Difference between SQL and NoSQL?",
        "Explain caching strategies.",
        "What is JWT authentication?",
        "Explain SOLID principles."
    ],

    "Cyber Security Analyst": [
        "What is a SIEM?",
        "Explain XSS and CSRF.",
        "What is OWASP Top 10?",
        "Explain brute force attack prevention.",
        "What is privilege escalation?",
        "Difference between IDS and IPS?",
        "Explain Zero Trust security.",
        "What is a SOC workflow?"
    ],

    "Data Analyst": [
        "Explain data normalization.",
        "What is EDA?",
        "Difference between supervised and unsupervised learning?",
        "Explain data cleaning techniques.",
        "What is regression analysis?",
        "Explain SQL joins.",
        "What is data visualization best practice?",
        "Explain correlation vs causation."
    ],

    "AI / ML Engineer": [
        "Explain overfitting and underfitting.",
        "What is gradient descent?",
        "Difference between CNN and RNN?",
        "Explain model evaluation metrics.",
        "What is feature engineering?",
        "Explain bias vs variance.",
        "What is transfer learning?",
        "Explain hyperparameter tuning."
    ],

    "DevOps Engineer": [
        "Explain CI/CD pipeline design.",
        "What is Infrastructure as Code?",
        "How does Docker differ from virtual machines?",
        "Explain Kubernetes architecture.",
        "What is blue-green deployment?",
        "How do you monitor distributed systems?",
        "Explain container orchestration.",
        "How would you secure a CI/CD pipeline?"
    ],

    "Cloud Engineer": [
        "Explain IAM in cloud platforms.",
        "What is auto scaling?",
        "How does load balancing work?",
        "Explain VPC architecture.",
        "How do you secure cloud storage?",
        "Difference between IaaS, PaaS, and SaaS?",
        "Explain cloud cost optimization strategies.",
        "How do you design high availability systems?"
    ],

    "Frontend Developer": [
        "What is virtual DOM?",
        "Explain state management in React.",
        "How does browser rendering work?",
        "What is lazy loading?",
        "Explain responsive design principles.",
        "How do you optimize frontend performance?",
        "What are web accessibility best practices?",
        "Explain CORS."
    ],

    "Backend Engineer": [
        "Explain RESTful API design principles.",
        "How do you implement authentication in Django?",
        "What is database indexing?",
        "Explain caching in backend systems.",
        "How would you design a scalable backend?",
        "What are message queues?",
        "Explain rate limiting.",
        "How do you handle concurrency?"
    ],

    "Site Reliability Engineer": [
        "What is observability?",
        "Explain incident response workflow.",
        "How do you handle system outages?",
        "What is SLA, SLO, and SLI?",
        "Explain load testing.",
        "How do you monitor microservices?",
        "What is root cause analysis?",
        "Explain reliability engineering principles."
    ],

    "Blockchain Developer": [
        "What is a smart contract?",
        "Explain consensus mechanisms.",
        "What is gas in Ethereum?",
        "How do you secure a smart contract?",
        "Difference between public and private blockchain?",
        "Explain token standards like ERC-20.",
        "What is Web3?",
        "How do you prevent reentrancy attacks?"
    ],

    "Product Data Scientist": [
        "Explain A/B testing.",
        "How do you measure product success?",
        "What is cohort analysis?",
        "Explain hypothesis testing.",
        "How do you design experiments?",
        "What are business KPIs?",
        "Explain churn prediction.",
        "How do you communicate data insights?"
    ],

    "Full Stack Web Developer": [
        "Explain how frontend and backend communicate.",
        "What is JWT authentication?",
        "How would you design a scalable web app?",
        "Explain database normalization.",
        "How do you deploy a web application?",
        "What is CORS?",
        "Explain MVC architecture.",
        "How do you secure a web application?"
    ],
}

groq_api_key = os.environ.get("GROQ_API_KEY")
if groq_api_key:
    groq_client = Groq(api_key=groq_api_key)
else:
    groq_client = None


def fallback_questions_for_role(role_name, count=MAX_QUESTIONS):
    questions = FALLBACK_QUESTIONS.get(
        role_name,
        FALLBACK_QUESTIONS["Software Developer"],
    )
    return list(questions[:count])


def generate_ai_questions_logic(role, count=8):
    if not groq_client:
        return fallback_questions_for_role(role.name, count)

    prompt = f"""
Generate {count} different advanced technical interview questions.

Role: {role.name}
Description: {role.description}

Return only numbered questions.
"""

    try:
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.9
        )

        text = response.choices[0].message.content.strip()

        questions = []
        for line in text.split("\n"):
            line = re.sub(r"^\s*\d+[\.\)]\s*", "", line)
            line = line.lstrip("-* ").strip()
            if line and line not in questions:
                questions.append(line)

        for question in fallback_questions_for_role(role.name, count):
            if len(questions) >= count:
                break
            if question not in questions:
                questions.append(question)

        return questions[:count]

    except Exception:
        logger.exception("Groq question generation failed; using fallback questions.")
        return fallback_questions_for_role(role.name, count)


@login_required
def generate_ai_question(request):
    role_name = request.GET.get("role", "Software Developer")
    role = JobRole.objects.filter(name=role_name).first()

    if role is None:
        return JsonResponse({
            "questions": fallback_questions_for_role(role_name)
        })

    questions = generate_ai_questions_logic(role)

    return JsonResponse({"questions": questions})


@never_cache
@login_required
def select_role(request):

    # Clear ALL interview sessions when coming to role selection
    keys_to_remove = [key for key in request.session.keys() if key.startswith("interview_role_")]

    for key in keys_to_remove:
        request.session.pop(key, None)

    roles = JobRole.objects.all()
    return render(request, 'select_role.html', {'roles': roles})

@never_cache
@login_required
def start_interview(request, role_id):
    role = get_object_or_404(JobRole, id=role_id)
    session_key = f"interview_role_{role_id}"

    # Restart only if explicitly requested
    if request.GET.get("restart") == "true":
        request.session.pop(session_key, None)
        return redirect("start_interview", role_id=role.id)

    # Initialize only if session doesn't exist
    if session_key not in request.session:
        questions = generate_ai_questions_logic(role, MAX_QUESTIONS)
        random.shuffle(questions)

        request.session[session_key] = {
            "question_number": 1,
            "questions": questions,
            "total_score": 0,
            "answers": []
        }

    interview_data = request.session[session_key]
    question_number = interview_data["question_number"]
    questions = interview_data["questions"]
    if not questions:
        questions = fallback_questions_for_role(role.name)
        random.shuffle(questions)
        interview_data["questions"] = questions
        request.session[session_key] = interview_data

    question_count = len(questions)

    # Finish interview
    if question_number > question_count:

        total_score = interview_data["total_score"]
        percentage = round((total_score / (question_count * 10)) * 100)
        percentage = max(0, min(100, percentage))

        interview_session = InterviewSession.objects.create(
            user=request.user,
            job_role=role,
            total_score=percentage
        )

        for ans in interview_data["answers"]:
            Answer.objects.create(
                session=interview_session,
                question_text=ans["question"],
                response=ans["user_answer"],
                score=ans["score"],
                feedback=ans["feedback"]
            )

        request.session.pop(session_key, None)

        return redirect("interview_result", session_id=interview_session.id)

    question = questions[question_number - 1]

    if request.method == "POST":

        user_answer = (request.POST.get("answer") or "").strip()

        if not user_answer:
            return render(request, "interview.html", {
                "role": role,
                "question": question,
                "question_number": question_number,
                "question_count": question_count,
                "progress_percentage": int(((question_number - 1) / question_count) * 100),
                "error": "Please answer before submitting."
            })

        score, feedback = evaluate_answer_with_ai(
            question,
            user_answer,
            role.name,
        )

        interview_data["answers"].append({
            "question": question,
            "user_answer": user_answer,
            "score": score,
            "feedback": feedback
        })

        interview_data["total_score"] += score
        interview_data["question_number"] += 1

        request.session[session_key] = interview_data

        return redirect(request.path)

    progress_percentage = int(((question_number - 1) / question_count) * 100)

    return render(request, "interview.html", {
        "role": role,
        "question": question,
        "question_number": question_number,
        "question_count": question_count,
        "progress_percentage": progress_percentage
    })


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})



def evaluate_answer_locally(user_answer):
    word_count = len(user_answer.split())

    if word_count < 8:
        return 1, "Add more detail and explain the reasoning behind your answer."
    if word_count < 25:
        return 4, "The answer is relevant but needs more technical depth and examples."
    if word_count < 60:
        return 6, "Good foundation. Add trade-offs or a practical example for a stronger answer."
    return 7, "Detailed answer. Improve it further by making the key points more concise."


def evaluate_answer_with_ai(question_text, user_answer, role_name):
    if not groq_client:
        return evaluate_answer_locally(user_answer)

    try:
        prompt = f"""
You are a STRICT senior technical interviewer.

If the answer is incomplete, vague, off-topic, or less than 2 meaningful sentences,
you MUST give 0 to 3 score.

If the answer is a single sentence or generic like "using django",
you MUST give 0.

Role: {role_name}

Question:
{question_text}

Answer:
{user_answer}

Be strict and realistic like a FAANG interviewer.

Return exactly:

Score: X/10
Feedback: short explanation.
"""

        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )

        text = response.choices[0].message.content

        match = re.search(r"(\d+)/10", text)

        if match:
            score = max(0, min(10, int(match.group(1))))
        else:
            score = 5

        feedback_match = re.search(r"Feedback:\s*(.*)", text, re.DOTALL)
        feedback = feedback_match.group(1).strip() if feedback_match else "Answer evaluated."

        return score, feedback

    except Exception:
        logger.exception("Groq answer evaluation failed; using local evaluation.")
        return evaluate_answer_locally(user_answer)


def home(request):
    if request.user.is_authenticated:
        return redirect('select_role')  

    return render(request, 'home.html') 

def about(request):
    return render(request, "about.html")



@login_required
def interview_result(request, session_id):
    session = get_object_or_404(InterviewSession, id=session_id, user=request.user)
    answers = session.answer_set.all()

    return render(request, "result.html", {
        "role": session.job_role,
        "percentage": session.total_score,
        "answers": answers
    })
