import streamlit as st
import pdfplumber
from jd_matcher import analyze_resume_vs_jd
from score import section_wise_score,sectionscore
from skill_extractor import get_categorized_skill_gap
from skill_extractor import extract_skills, get_skill_gap
from score import resume_score
from recommender import get_recommendations
from ATS_score import ats_score
import plotly.graph_objects as go
from database import init_db, save_analysis, get_all_history

init_db()





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
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "🛠️ Skills", "🎯 JD Match", "📚 Roadmap", "📜 History"])
   
    skills = extract_skills(text)
    with tab2:
        st.subheader("✅ Skills Found:")
        for skill in skills:
            st.badge(skill)
   

    section_score=section_wise_score(text, role)
    critical_missing = get_skill_gap(text,role)
    # gap=get_skill_gap(text, role)
    # st.subheader("❌ Missing Skills:")
    # for skill in gap:
    #     st.badge(skill)
    # st.divider()
    gap=get_skill_gap(text, role)
    critical_missing, nice_to_have_missing=get_categorized_skill_gap(text, role)
    with tab2:
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
            
        with tab2:
            st.subheader("📈 Skill Coverage Chart")
            chart = go.Figure(go.Bar(
                x=["Skills You Have", "Critical Missing", "Nice-to-Have Missing"],
                y=[len(skills), len(critical_missing), len(nice_to_have_missing)],
                marker_color=["#2ecc71", "#e74c3c", "#f1c40f"]
                ))
            chart.update_layout(
                yaxis_title="Number of Skills",
                height=350
                )
            st.plotly_chart(chart, use_container_width=True)
            
    score=resume_score(role, text)
    Atsscore=ats_score(role, text)
    save_analysis(role, score, Atsscore, section_score)
    
    with tab1:
        col1, col2=st.columns(2)
        with col1:
            st.subheader("📊 Resume Score:")
            st.progress(score/100)
            st.write(f"{score}/100")
        with col2:
            st.subheader("🤖 ATS Score:")
            st.progress(Atsscore/100)
            st.write(f"{Atsscore}/100")
            
    with tab1:
        st.subheader("Section-wise Score:")
        # section_score=section_wise_score(text,role)
        for section, score in section_score.items():
            col_a, col_b = st.columns([1, 3])
            with col_a:
                st.write(f'{section}')
            with col_b:
                st.progress(score / 100)
                st.write(f"{score}/100")
                
    with tab3:
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
                
    projects,roadmap=get_recommendations(gap)
    with tab4:
        st.subheader("🔨 Suggested Projects:")
        for project in projects:
            st.write(f"• {project}")
            
        st.divider()
        st.subheader("📚 Learning Roadmap:")
        for road in roadmap:
            st.write(f"• {road}")
        
        
    with tab1:
        st.subheader("💡 Why is your score this?")
        strong_points = []
        improve_points = []
        # Education
        if section_score["Education"] >= 70:
            strong_points.append(
                f"Education section is well presented ({section_score['Education']}/100)"
            )
        else:
            improve_points.append(
                f"Education score is only {section_score['Education']}/100. Include degree name, university, graduation year, and CGPA."
            )
        # Experience
        if section_score["Experience"] >= 50:
            strong_points.append(
                f"Experience section is strong ({section_score['Experience']}/100) with action-oriented content."
            )
        else:
            improve_points.append(
                f"Experience score is {section_score['Experience']}/100. Add action verbs and measurable achievements such as 'improved accuracy by 20%' or 'reduced processing time by 30%'."
            )
         # Projects
        if section_score["Projects"] >= 50:
            strong_points.append(
                f"Projects section looks strong ({section_score['Projects']}/100)."
            )
        else:
            improve_points.append(
                f"Projects score is {section_score['Projects']}/100. Add GitHub links, tech stack details, deployment links, and impact metrics."
            )
         # Achievements
        if section_score["Achievements"] >= 40:
            strong_points.append(
                f"Achievements section adds value ({section_score['Achievements']}/100)."
            )
            
        else:
            improve_points.append(
                f"Achievements score is {section_score['Achievements']}/100. Consider adding certifications, hackathons, awards, research work, or publications."
            )
        # Skills
        if not critical_missing:
            strong_points.append("All critical skills required for the selected role are present.")
        else:
            improve_points.append(
                f"Missing critical skills: {', '.join(critical_missing)}"
            )
    # Resume strength
    with tab1:
        if score >= 90:
            level = "🚀 Excellent"
        elif score >= 75:
            level = "✅ Strong"
        elif score >= 60:
            level = "👍 Good"
        elif score >= 40:
            level = "⚠️ Needs Improvement"
        else:
            level = "❌ Weak"
            
        st.info(f"Overall Resume Strength: {level} ({score}/100)")
        # Section Score Breakdown
        with st.expander("📊 Section Score Breakdown"):
            for section, value in section_score.items():
                st.write(f"**{section}:** {value}/100")
        if strong_points:
            st.success("Strong Points")
            for point in strong_points:
                st.write(f"• {point}")
        # Areas to Improve
        if improve_points:
            st.warning("Areas to Improve")
            for point in improve_points:
                st.write(f"• {point}")
        else:
            st.success("Excellent! No major weaknesses detected.")
            
    with tab5:
        st.subheader("📜 Your Resume Analysis History")
        history = get_all_history()

        if history:
            for row in history:
                st.write(f"**{row[1]}** | Role: {row[2]} | Resume Score: {row[3]}/100 | ATS Score: {row[4]}/100")
        else:
            st.write("No history yet. Upload a resume to start tracking!")
