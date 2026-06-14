import re
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


_model=None

def get_model():
    global _model
    if _model is None:
        _model=SentenceTransformer("all-MiniLM-L6-v2")
    return _model

def clean_text(text):
    text=text.lower()
    text = re.sub(r"[^a-z0-9\s\.\+\#]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def get_match_score(resume_text, jd_text):
    model=get_model()

    resume_clean=clean_text(resume_text)
    jd_clean=clean_text(jd_text)

    embeddings = model.encode([resume_clean, jd_clean])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]

    score = max(0, min(1, sim)) * 100
    return round(float(score), 1)

COMMON_JD_TERMS = [
    "python", "java", "c++", "sql", "javascript", "react", "node",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "github",
    "linux", "rest api", "fastapi", "flask", "django",
    "data structures", "algorithms", "agile", "scrum",
    "ci/cd", "testing", "unit testing", "microservices",
    "html", "css", "tailwind", "mongodb", "postgresql", "mysql",
    "spark", "hadoop", "airflow", "tableau", "power bi", "excel",
    "communication", "leadership", "problem solving"
]

def get_missing_terms(resume_text, jd_text, term_list=None):
    if term_list is None:
        
        term_list=COMMON_JD_TERMS

    resume_clean=clean_text(resume_text)
    jd_clean=clean_text(jd_text)
    missing=[]
    for term in term_list:
        term_clean=clean_text(term)
        in_jd=term_clean in jd_clean
        in_resume =term_clean in resume_clean
        if in_jd and not in_resume:
            missing.append(term)
    return missing


def analyze_resume_vs_jd(resume_text, jd_text):
    score=get_match_score(resume_text, jd_text)
    missing = get_missing_terms(resume_text, jd_text)

    jd_result={"match_score": score,
               "missing_terms": missing
               }
    return jd_result