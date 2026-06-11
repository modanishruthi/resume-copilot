import streamlit as st
import pdfplumber

from skill_extractor import extract_skills, get_skill_gap
from score import resume_score
from recommender import get_recommendations
from ATS_score import ats_score

def extract_file(pdf_file):
    text=""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text=text+page.extract_text() or ""
    return text

st.title("AI Resume Copilot")
st.subheader("upload your resume and get instant insights")
st.sidebar.title("About")
st.sidebar.write("AI Resume Copilot helps you optimize your resume for your target role.")
st.sidebar.write("Built with Python + Streamlit + NLP")

role= st.selectbox("Select Target Role:", ["ml_engineer", "data_analyst", "software_engineer", 
     "web_developer", "data_engineer"])

uploaded_file= st.file_uploader("Upload Resume (PDF only)", type=["pdf"])


if uploaded_file is not None:
    text=extract_file(uploaded_file)
    
    st.success("Resume uploaded successfully")
    st.divider()
   
    skills = extract_skills(text)
    st.subheader("✅ Skills Found:")
    for skill in skills:
        st.badge(skill)
    st.divider()
    gap=get_skill_gap(text, role)
    st.subheader("❌ Missing Skills:")
    for skill in gap:
        st.badge(skill)
    st.divider()
    score=resume_score(role, text)
    Atsscore=ats_score(role, text)
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Resume Score:")
        st.progress(score/100)
        st.write(f"{score}/100")
    with col2:
        st.subheader("🤖 ATS Score:")
        st.progress(Atsscore/100)
        st.write(f"{Atsscore}/100")
    st.divider()

    projects,roadmap=get_recommendations(gap)
    st.subheader("🔨 Suggested Projects:")
    for project in projects:
        st.write(f"• {project}")
    st.divider()
    st.subheader("📚 Learning Roadmap:")
    for road in roadmap:
        st.write(f"• {roadmap}")
  

    