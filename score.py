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


def resume_score(target_role, resume_text):
    total=sectionscore(resume_text)+skillscore(resume_text, target_role)+keywordsscore(resume_text)
    return round(total)