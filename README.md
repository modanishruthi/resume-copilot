# AI Resume Copilot

AI Resume Copilot is an NLP-powered resume analysis platform that helps users evaluate and improve their resumes for specific job roles. The application provides ATS scoring, skill gap analysis, resume-to-job-description matching, personalized project recommendations, and learning roadmaps.

## Features

### Resume Analysis
- Upload resumes in PDF format
- Extract and process resume content automatically
- Generate an overall Resume Score
- Generate an ATS Compatibility Score
- Section-wise evaluation of:
  - Skills
  - Education
  - Projects
  - Experience
  - Achievements

### Skill Gap Analysis
- Extract technical skills from resumes
- Compare skills against role-specific requirements
- Identify critical missing skills
- Suggest additional recommended skills

### Job Description Matching
- Compare resumes against job descriptions
- Semantic similarity analysis using Sentence Transformers
- Generate Resume-JD Match Score
- Highlight missing keywords and technologies

### Personalized Recommendations
- Recommend projects based on skill gaps
- Generate learning roadmaps for target roles
- Provide actionable improvement suggestions

### Analysis History
- Store previous resume analyses
- Track resume improvements over time using SQLite

## Supported Roles

- Machine Learning Engineer
- Data Analyst
- Software Engineer
- Web Developer
- Data Engineer

## Tech Stack

### Frontend
- Streamlit

### Backend
- Python
- SQLite

### Machine Learning & NLP
- Sentence Transformers
- Scikit-learn
- Cosine Similarity

### Data Processing
- Pandas
- NumPy
- PDFPlumber

### Visualization
- Plotly

## Project Structure

```text
resume-copilot/
│
├── project.py
├── ATS_score.py
├── database.py
├── jd_matcher.py
├── recommender.py
├── score.py
├── skill_extractor.py
├── skills_db.json
├── critical_skills.json
├── resume_history.db
├── requirements.txt
└── runtime.txt
```

## Installation

Clone the repository:

```bash
git clone https://github.com/modanishruthi/resume-copilot.git
cd resume-copilot
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run project.py
```

## Workflow

1. Upload a resume in PDF format.
2. Select the target job role.
3. Optionally provide a job description.
4. Analyze the resume.
5. Review:
   - Resume Score
   - ATS Score
   - Section-wise Analysis
   - Skill Gaps
   - JD Match Score
   - Project Recommendations
   - Learning Roadmap
   - Analysis History

## Future Enhancements

- Resume Role Classification
- Cover Letter Generation
- Interview Question Generator
- Resume Version Tracking
- Resume Improvement Assistant
- Advanced ATS Optimization Suggestions

## Author

Shruthi Modani

GitHub: https://github.com/modanishruthi

LeetCode: https://leetcode.com/u/shruthi_modani/

 Live Demo: https://resume-copilot-3fp8ny4ovwmbmrd7tdnbin.streamlit.app/
