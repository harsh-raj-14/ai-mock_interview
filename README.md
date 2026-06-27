# AI Mock Interview Platform

An AI-powered technical interview practice platform built with Django. It generates role-specific questions, evaluates answers, provides actionable feedback, and tracks performance across multiple interview sessions.

![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![Groq](https://img.shields.io/badge/AI-Groq-F55036)

## Features

- User registration, login, logout, and automatic logout after inactivity
- 12 preconfigured technical job roles
- Eight dynamically generated questions per interview
- AI-based answer scoring and personalized feedback
- Built-in questions and local evaluation when the AI service is unavailable
- Interview result pages with answer-by-answer feedback
- Personal dashboard with average, highest, and lowest scores
- Performance history and progress visualization
- User-specific session privacy and protected routes
- Responsive dark-themed interface

## Supported Roles

- Software Developer
- Cyber Security Analyst
- Data Analyst
- AI / ML Engineer
- DevOps Engineer
- Cloud Engineer
- Frontend Developer
- Backend Engineer
- Site Reliability Engineer
- Blockchain Developer
- Product Data Scientist
- Full Stack Web Developer

## How It Works

1. Create an account or log in.
2. Select a job role.
3. Answer eight technical interview questions.
4. Receive a score and feedback for each response.
5. Review the final result and track progress from the dashboard.

When `GROQ_API_KEY` is configured, the platform uses the `llama-3.3-70b-versatile` model to generate questions and evaluate responses. If the key is missing or the API is unavailable, the application automatically uses its built-in question bank and local evaluation logic.

## Tech Stack

- **Backend:** Python, Django
- **AI:** Groq Python SDK
- **Frontend:** Django templates, HTML, CSS, JavaScript, Bootstrap
- **Database:** SQLite for local development; PostgreSQL-compatible through `DATABASE_URL`
- **Production:** Gunicorn and WhiteNoise

## Getting Started

### Prerequisites

- Python 3.11 or later
- Git
- A Groq API key (optional)

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd <repository-folder>
```

Replace the placeholders with your GitHub repository URL and local folder name.

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Environment variables can be set in your terminal or loaded through your preferred environment-management tool.

Windows PowerShell:

```powershell
$env:SECRET_KEY = "replace-with-a-secure-secret"
$env:GROQ_API_KEY = "your-groq-api-key"
$env:DJANGO_DEBUG = "True"
```

macOS or Linux:

```bash
export SECRET_KEY="replace-with-a-secure-secret"
export GROQ_API_KEY="your-groq-api-key"
export DJANGO_DEBUG="True"
```

`GROQ_API_KEY` is optional during local development because the application includes fallback questions and scoring.

### 5. Apply database migrations

```bash
python manage.py migrate
```

The migrations automatically add the supported job roles to the database.

### 6. Run the development server

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Environment Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `SECRET_KEY` | Production | Development-only value | Django cryptographic signing key |
| `GROQ_API_KEY` | No | None | Enables AI question generation and evaluation |
| `DATABASE_URL` | No | Local SQLite database | Database connection URL |
| `DJANGO_DEBUG` | No | Enabled locally | Enables or disables Django debug mode |
| `ALLOWED_HOSTS` | Production | `127.0.0.1,localhost` | Comma-separated allowed host names |
| `AUTO_LOGOUT_MINUTES` | No | `10` | Inactivity period before automatic logout |
| `CORS_ALLOWED_ORIGINS` | No | Empty | Comma-separated trusted CORS origins |
| `CORS_ALLOW_ALL_ORIGINS` | No | Same as debug mode | Allows requests from all origins |
| `CORS_ALLOW_CREDENTIALS` | No | `False` | Allows credentials in cross-origin requests |
| `SECURE_SSL_REDIRECT` | No | Enabled on Railway | Redirects HTTP traffic to HTTPS |

Never commit API keys, passwords, or production secrets to the repository.

## Running Tests

Run the full automated test suite with:

```bash
python manage.py test
```

The tests cover authentication, interview completion, fallback question generation, answer validation, dashboard calculations, session privacy, and automatic logout.

## Admin Panel

Create an administrator account:

```bash
python manage.py createsuperuser
```

Start the server and open [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) to manage job roles, interview sessions, and answers.

## Project Structure

```text
.
|-- ai_mock/          # Project settings, root URLs, and middleware
|-- dashboard/        # Performance dashboard and session history
|-- interviews/       # Interview flow, AI integration, models, and tests
|-- templates/        # Shared and page-specific Django templates
|-- users/            # User application
|-- build.sh          # Production build and migration commands
|-- manage.py         # Django command-line utility
|-- Procfile          # Gunicorn production process
|-- requirements.txt  # Python dependencies
`-- runtime.txt       # Python runtime version
```

## Deployment

The repository includes a `build.sh` script and `Procfile` suitable for platforms such as Railway.

For a production deployment:

1. Provision a PostgreSQL database and set `DATABASE_URL`.
2. Set `SECRET_KEY` to a strong, unique value.
3. Set `GROQ_API_KEY` if AI-powered behavior is required.
4. Set `ALLOWED_HOSTS` to the deployment domain.
5. Set `DJANGO_DEBUG=False`.
6. Deploy the application. The build script installs dependencies, collects static files, and applies migrations.

The production process starts Gunicorn using the command defined in `Procfile`.

## Contributing

Contributions are welcome. Fork the repository, create a feature branch, make your changes, run the tests, and open a pull request with a clear description.

## Author

Conceptualized and developed by **Gaddam Likhitha Raj**.

## Disclaimer

This project is intended for interview practice and educational use. AI-generated questions, scores, and feedback should be treated as guidance rather than as a definitive assessment of a candidate's ability.
