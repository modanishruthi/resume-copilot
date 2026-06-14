from skill_extractor import extract_skills, get_skill_gap
from skill_extractor import skills

sections_list=["education","projects","skills","experience","certifications","hobbies","achievements","summary"]

def sectionscore(resume_text):
    sections_list=["education","projects","skills","experience","certifications","hobbies","achievements","summary"]
    section_have=0
    total_sections=8
    Total_section_score =30
    for i in sections_list:
        if i in resume_text.lower():
            section_have=section_have+1
    final_score=(section_have/total_sections)*Total_section_score
    return final_score


def skillscore(resume_text, target_role):
    missing_skills=get_skill_gap(resume_text, target_role)
    total_required=len(skills[target_role])
    skills_have=total_required-len(missing_skills)
    final_skills_score=(skills_have/total_required)*50

    return final_skills_score

keywords_list=["developed","built","implemented","designed","created","managed"]

def keywordsscore(resume_text):
    keywords_list=["developed","built","implemented","designed","created","managed"]
    keywords_have=0
    total_keywords=6
    for i in keywords_list:
        if i in resume_text.lower():
            keywords_have=keywords_have+1
    final_keywords_score=(keywords_have/total_keywords)*20
    return final_keywords_score


def experience_score(resume_text):
    import re
    text=resume_text.lower()
    score=0

    action_verbs = ["developed", "built", "implemented", "designed", 
                    "created", "managed", "led", "improved", "optimized",
                    "deployed", "achieved", "increased", "reduced"]
    
    verbs_found=0
    for verb in action_verbs:
        if verb in text:
            verbs_found=verbs_found+1
    score=score+(verbs_found/len(action_verbs))*40
    if re.search(r'\d+\s*(year|month|yr)', text):
        score = score + 30
 
    if re.search(r'\d+%|\d+x|increased by \d+|reduced by \d+', text):
        score = score + 30
    
    return round(score)

def projects_score(resume_text):
    import re
    text=resume_text.lower()
    score=0

    project_keywords = ["project", "built", "developed", "github",
                        "deployed", "created", "application", "system"]
    
    keywords_found=0
    for word in project_keywords:
        if word in text:
            keywords_found=keywords_found+1
    score=score+(keywords_found/len(project_keywords))*40
    tech_keywords = ["python", "javascript", "react", "sql", "api",
                     "machine learning", "tensorflow", "flask", "docker"]
    
    
    tech_found = 0
    for tech in tech_keywords:
        if tech in text:
            tech_found = tech_found + 1

    score = score + (tech_found / len(tech_keywords)) * 30
    
    if re.search(r'\d+%|\d+x|accuracy|f1|precision|recall', text):
        score = score + 30

    return round(score)


def education_score(resume_text):
    import re
    text=resume_text.lower()
    score=0

    degrees=["bachelor", "master", "b.tech", "m.tech", "b.e",
               "m.e", "phd", "bsc", "msc", "degree"]
    degree_found=False
    for degree in degrees:
        if degree in text:
            degree_found=True
    if degree_found:
        score = score + 40

   
    university_keywords = ["university", "college", "institute", "school"]
    uni_found=False
    for uni in university_keywords:
        if uni in text:
            uni_found=True
    if uni_found:
        score=score+30

    if re.search(r'gpa|cgpa|\d+\.\d+%|\d{2}%', text):
        score = score + 30

    return round(score)

def achievements_score(resume_text):
    text = resume_text.lower()
    score = 0

    # Certifications (40 points)
    cert_keywords = ["certified", "certification", "certificate",
                     "coursera", "udemy", "aws certified", "google"]
    
    cert_found = 0
    for cert in cert_keywords:
        if cert in text:
            cert_found = cert_found + 1

    score = score + (cert_found / len(cert_keywords)) * 40

    
    award_keywords = ["award", "winner", "first place", "hackathon",
                      "competition", "scholarship", "honor"]
    
    award_found = False
    for award in award_keywords:
        if award in text:
            award_found = True

    if award_found:
        score = score + 30

   
    research_keywords = ["published", "research", "paper", "journal"]
    
    research_found = False
    for word in research_keywords:
        if word in text:
            research_found = True

    if research_found:
        score = score + 30

    return round(score)

def section_wise_score(resume_text, target_role):
    scores = {
        "Skills":       round((skillscore(resume_text, target_role) / 50) * 100),
        "Experience":   experience_score(resume_text),
        "Projects":     projects_score(resume_text),
        "Education":    education_score(resume_text),
        "Achievements": achievements_score(resume_text)
    }
    return scores













def resume_score(target_role, resume_text):
    total=sectionscore(resume_text)+skillscore(resume_text, target_role)+keywordsscore(resume_text)
    return round(total)

