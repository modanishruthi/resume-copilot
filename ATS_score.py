def contact_score(resume_text):
    score=0
    if '@' in resume_text:
        score= score+10
    if any (char.isdigit() for char in resume_text):
        score=score+10
    return score

from score import sectionscore, keywordsscore


def check_length(resume_text):
   word_count=len(resume_text.split())
   if word_count<100:
       return 5
   elif word_count<=700:
       return 20
   else:
       return 10
   
def ats_score(target_role, resume_text):
    total=contact_score(resume_text)+sectionscore(resume_text)+keywordsscore(resume_text)+check_length(resume_text)
    return round(total)