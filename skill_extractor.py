import json

with open("critical_skills.json", "r") as f:
    critical_skills = json.load(f)

with open("skills_db.json", "r") as f:
    skills = json.load(f)

all_skills = []

for key, value in skills.items():
    all_skills.extend(value)

def extract_skills(resume_text):
    resume_text = resume_text.lower()

    extracted = []

    for skill in all_skills:
        if skill.lower() in resume_text:
            extracted.append(skill.lower())

    return list(set(extracted))

def get_skill_gap(resume_text, target_role):
    your_skills = set(extract_skills(resume_text))
    required_skills = set(skills[target_role])

    missing_skills = required_skills - your_skills

    return list(missing_skills)

def get_categorized_skill_gap(resume_text, target_role):
    missing_skills = get_skill_gap(resume_text, target_role)
    critical_for_role = critical_skills[target_role]

    critical_missing = []
    nice_to_have_missing = []

    for skill in missing_skills:
        if skill in critical_for_role:
            critical_missing.append(skill)
        else:
            nice_to_have_missing.append(skill)

    return critical_missing, nice_to_have_missing
