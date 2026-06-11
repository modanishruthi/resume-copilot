import json
with open("skills_db.json", "r") as f:
    skills=json.load(f)
    

all_skills=[]
for key, value in skills.items():
    all_skills.extend(value)


def extract_skills(resume_text):
    resume_text=resume_text.lower()
    extracted_skills=[]
    for i in all_skills:
        if i in resume_text:
            extracted_skills.append(i)

    return list(set(extracted_skills))


def get_skill_gap(resume_text, target_role):
    your_skills=set(extract_skills(resume_text))
    required_skills=set(skills[target_role])
    missing_skills= required_skills-your_skills
    return list(missing_skills)