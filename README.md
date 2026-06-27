# 🤖 AI Mock Interview Platform

An AI-powered mock interview platform built with **Python** and **Django** that helps users prepare for technical interviews. The platform generates role-specific interview questions, evaluates responses using AI, provides detailed feedback, and tracks interview performance.

---

## 🚀 Features

* 🔐 User Authentication (Sign Up, Login & Logout)
* ⏳ Auto Logout after Inactivity
* 💼 12 Technical Job Roles
* 🤖 AI-generated Interview Questions
* 📝 AI-powered Answer Evaluation
* 📊 Personalized Feedback & Scoring
* 📈 Performance Dashboard
* 📚 Interview History Tracking
* 🔄 Offline Fallback Question Bank
* 📱 Fully Responsive UI

---

## 🛠️ Tech Stack

| Category       | Technologies                       |
| -------------- | ---------------------------------- |
| **Backend**    | Python, Django                     |
| **Frontend**   | HTML5, CSS3, JavaScript, Bootstrap |
| **AI**         | Groq API (Llama 3.3 70B Versatile) |
| **Database**   | SQLite, PostgreSQL                 |
| **Deployment** | Gunicorn, WhiteNoise, Railway      |

---

## 📂 Project Structure

```text
AI-Mock-Interview/
│── ai_mock/
│── interviews/
│── dashboard/
│── users/
│── templates/
│── static/
│── manage.py
│── requirements.txt
│── Procfile
│── build.sh
└── README.md
```

---

## ⚙️ Installation

### Clone the Repository

```bash
git clone https://github.com/harsh-raj-14/ai-mock_interview.git
cd ai-mock_interview
```

### Create a Virtual Environment

```bash
python -m venv .venv
```

Activate the virtual environment.

**Windows**

```bash
.venv\Scripts\activate
```

**Linux/macOS**

```bash
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
GROQ_API_KEY=your_groq_api_key
DATABASE_URL=your_database_url
DJANGO_DEBUG=True
```

### Apply Migrations

```bash
python manage.py migrate
```

### Run the Project

```bash
python manage.py runserver
```

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

---

## 💼 Supported Interview Roles

* Software Developer
* Full Stack Developer
* Frontend Developer
* Backend Developer
* AI/ML Engineer
* Data Analyst
* Product Data Scientist
* DevOps Engineer
* Cloud Engineer
* Cyber Security Analyst
* Site Reliability Engineer
* Blockchain Developer

---

## 📸 Screenshots

Add screenshots here.

| Home                          | Dashboard                               |
| ----------------------------- | --------------------------------------- |
| ![Home](screenshots/home.png) | ![Dashboard](screenshots/dashboard.png) |

| Interview                               | Result                            |
| --------------------------------------- | --------------------------------- |
| ![Interview](screenshots/interview.png) | ![Result](screenshots/result.png) |

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 🚀 Deployment

The application can be deployed on:

* Railway
* Render
* Heroku
* AWS EC2
* DigitalOcean

Production stack includes:

* Gunicorn
* WhiteNoise
* PostgreSQL

---

## 📌 Future Improvements

* 🎤 Voice Interview
* 🎥 Video Interview
* 📄 Resume Analyzer
* 💻 Coding Interview Support
* 📈 Advanced Analytics
* 🌍 Multi-language Support

---

## 🤝 Contributing

Contributions are welcome.

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to your branch.
5. Open a Pull Request.

---

## 👨‍💻 Author

**Harsh Raj**

* GitHub: https://github.com/harsh-raj-14

---

## ⭐ Support

If you like this project, please consider giving it a **⭐ Star** on GitHub.

---

## 📄 License

This project is licensed under the **MIT License**.
