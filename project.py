import streamlit as st
import pdfplumber
from jd_matcher import analyze_resume_vs_jd
from score import section_wise_score
from skill_extractor import get_categorized_skill_gap

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
jd_text = st.text_area(
    "Paste Job Description (optional) - for a more accurate, role-specific match",
    height=150,
    placeholder="Paste the job description here to compare your resume against it..."
)
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

    # gap=get_skill_gap(text, role)
    # st.subheader("❌ Missing Skills:")
    # for skill in gap:
    #     st.badge(skill)
    # st.divider()
    gap=get_skill_gap(text, role)
    critical_missing, nice_to_have_missing=get_categorized_skill_gap(text, role)
    st.subheader("🔴 Critical Missing Skills:")
    if critical_missing:
        for skill in critical_missing:
            st.badge(skill)
    else:
        st.write("No critical skills missing! 🎉")

    st.subheader("🟡 Recommended Skills:")

    if nice_to_have_missing:
        for skill in nice_to_have_missing:
            st.badge(skill)
    else:
        st.write("No nice-to-have skills missing! 🎉")
        
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

    st.subheader("Section-wise Score:")
    section_score=section_wise_score(text,role)
    for section, score in section_score.items():
        col_a, col_b = st.columns([1, 3])
        with col_a:
            st.write(f'{section}')
        with col_b:
            st.progress(score / 100)
            st.write(f"{score}/100")
    st.divider()

    if jd_text.strip():
        st.subheader("🎯 Resume vs Job Description Match")
        with st.spinner("Analyzing match using sentence embeddings.."):
            jd_result=analyze_resume_vs_jd(text, jd_text)
        
        st.progress(jd_result["match_score"]/100)
        st.write(f"**Match Score: {jd_result['match_score']}%**")

        if jd_result["missing_terms"]:
            st.write("Terms in the Job Description that don't appear in your resume")
            for term in jd_result["missing_terms"]:
                st.badge(term)

        else:
            st.write("No major gaps found against this JD. 🎉")

        st.divider()



    projects,roadmap=get_recommendations(gap)
    st.subheader("🔨 Suggested Projects:")
    for project in projects:
        st.write(f"• {project}")
    st.divider()
    st.subheader("📚 Learning Roadmap:")
    for road in roadmap:
        st.write(f"• {road}")
  


