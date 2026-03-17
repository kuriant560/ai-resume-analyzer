"""
skills_db.py
------------
Master list of technical and soft skills used for skill extraction.

WHY THIS EXISTS:
    Instead of guessing skills from text, we match against this known list.
    This gives consistent, reliable skill detection.
    You can grow this list over time to improve accuracy.
"""

TECHNICAL_SKILLS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c++", "c#", "r", "scala",
    "go", "rust", "kotlin", "swift", "php", "ruby", "matlab",

    # Data Science & ML
    "machine learning", "deep learning", "natural language processing", "nlp",
    "computer vision", "data science", "data analysis", "statistical modeling",
    "feature engineering", "model deployment", "mlops",

    # ML Libraries & Frameworks
    "tensorflow", "pytorch", "keras", "scikit-learn", "xgboost", "lightgbm",
    "hugging face", "transformers", "spacy", "nltk", "opencv",

    # Data Tools
    "pandas", "numpy", "matplotlib", "seaborn", "plotly", "tableau", "power bi",

    # Databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "sqlite", "oracle", "cassandra", "dynamodb",

    # Cloud & DevOps
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
    "ci/cd", "jenkins", "git", "github", "gitlab", "terraform",

    # Web Frameworks
    "flask", "django", "fastapi", "streamlit", "react", "node.js",
    "express", "spring boot", "rest api", "graphql",

    # Data Engineering
    "apache spark", "hadoop", "kafka", "airflow", "etl", "data pipeline",
    "data warehouse", "dbt", "snowflake", "bigquery",

    # Other Technical
    "linux", "bash", "shell scripting", "excel", "jupyter", "agile",
    "scrum", "jira", "microservices", "object oriented programming",
]

SOFT_SKILLS = [
    "communication", "teamwork", "leadership", "problem solving",
    "critical thinking", "time management", "adaptability", "creativity",
    "collaboration", "project management", "attention to detail",
    "analytical thinking", "presentation skills", "mentoring",
]

# Combined for easy import elsewhere
ALL_SKILLS = TECHNICAL_SKILLS + SOFT_SKILLS