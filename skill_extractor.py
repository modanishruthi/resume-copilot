import json
import spacy
from spacy.matcher import PhraseMatcher

with open("skills_db.json", "r") as f:
    skills=json.load(f)
    

all_skills=[]
for key, value in skills.items():
    all_skills.extend(value)

nlp=spacy.load("en_core_web_sm")
matcher= PhraseMatcher(nlp.vocab, attr="LOWER")

patterns=[nlp.make_doc(s) for s in all_skills]
matcher.add("SKILLS",patterns )



def extract_skills(resume_text):
    
    # resume_text=resume_text.lower()
    # extracted_skills=[]
    # for i in all_skills:
    #     if i in resume_text:
    #         extracted_skills.append(i)

    # return list(set(extracted_skills))
    doc=nlp(resume_text)
    matches=matcher(doc)

    extracted=[]
    for match_id, start, end in matches:
        span=doc[start:end]
        extracted.append(span.text.lower())

    return list(set(extracted))


def get_skill_gap(resume_text, target_role):
    your_skills=set(extract_skills(resume_text))
    required_skills=set(skills[target_role])
    missing_skills= required_skills-your_skills
    return list(missing_skills)