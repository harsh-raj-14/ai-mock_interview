from django.db import migrations


JOB_ROLES = [
    (
        "Software Developer",
        "Builds, tests, and maintains reliable software applications.",
        "Programming, APIs, databases, testing, system design",
    ),
    (
        "Cyber Security Analyst",
        "Protects systems and data by identifying and responding to security threats.",
        "Network security, SIEM, OWASP, incident response, risk analysis",
    ),
    (
        "Data Analyst",
        "Turns raw data into useful business insights and recommendations.",
        "SQL, statistics, data cleaning, visualization, business analysis",
    ),
    (
        "AI / ML Engineer",
        "Designs, trains, evaluates, and deploys machine learning systems.",
        "Python, machine learning, deep learning, model evaluation, MLOps",
    ),
    (
        "DevOps Engineer",
        "Automates software delivery and improves infrastructure reliability.",
        "CI/CD, containers, infrastructure as code, monitoring, cloud platforms",
    ),
    (
        "Cloud Engineer",
        "Designs and operates secure, scalable cloud infrastructure.",
        "IAM, networking, compute, storage, high availability, cost optimization",
    ),
    (
        "Frontend Developer",
        "Builds accessible and responsive user interfaces for the web.",
        "HTML, CSS, JavaScript, browser APIs, accessibility, performance",
    ),
    (
        "Backend Engineer",
        "Builds APIs, services, and data systems that power applications.",
        "API design, databases, authentication, caching, scalability",
    ),
    (
        "Site Reliability Engineer",
        "Improves the reliability, observability, and operation of production systems.",
        "Observability, incident response, SLOs, automation, performance",
    ),
    (
        "Blockchain Developer",
        "Builds and secures decentralized applications and smart contracts.",
        "Smart contracts, consensus, Web3, token standards, security",
    ),
    (
        "Product Data Scientist",
        "Uses experiments and data models to guide product decisions.",
        "Experimentation, statistics, product metrics, modeling, communication",
    ),
    (
        "Full Stack Web Developer",
        "Builds complete web applications across frontend and backend systems.",
        "Frontend, backend, databases, APIs, deployment, web security",
    ),
]


def seed_job_roles(apps, schema_editor):
    JobRole = apps.get_model("interviews", "JobRole")

    for name, description, skills_required in JOB_ROLES:
        if not JobRole.objects.filter(name=name).exists():
            JobRole.objects.create(
                name=name,
                description=description,
                skills_required=skills_required,
            )


class Migration(migrations.Migration):
    dependencies = [
        ("interviews", "0004_alter_answer_id_alter_interviewsession_id_and_more"),
    ]

    operations = [
        migrations.RunPython(seed_job_roles, migrations.RunPython.noop),
    ]
