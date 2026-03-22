import re

# Predefined skills list
PREDEFINED_SKILLS = [
    "python", "sql", "machine learning", "nlp", "java", "cloud", "aws", 
    "docker", "data analysis", "excel", "communication"
]

def extract_skills(text):
    """
    Extracts predefined skills from text using case-insensitive keyword matching.
    Returns:
        set: A set of unique extracted skill strings.
    """
    if not text:
        return set()
    
    # Normalize text to lowercase for comparison
    text_lower = text.lower()
    
    extracted = set()
    for skill in PREDEFINED_SKILLS:
        # Use regex to find whole words only, ensuring no partial matches (e.g., 'java' in 'javascript')
        # Handle skills with spaces like 'machine learning'
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            extracted.add(skill)
            
    return extracted

def compare_skills(resume_skills, jd_skills):
    """
    Compares resume skills against job description skills.
    Returns:
        tuple: (matched_skills, missing_skills)
    """
    matched_skills = resume_skills.intersection(jd_skills)
    missing_skills = jd_skills.difference(resume_skills)
    
    return sorted(list(matched_skills)), sorted(list(missing_skills))

def skill_match_score(resume_skills, jd_skills):
    """
    Calculates the percentage of JD skills present in the resume.
    Handles division by zero if JD has no predefined skills.
    """
    if not jd_skills:
        return 0
    
    matched_skills = resume_skills.intersection(jd_skills)
    score = (len(matched_skills) / len(jd_skills)) * 100
    return round(score)

def generate_explanation(similarity_score, skill_score, matched_skills, missing_skills):
    """
    Generates a short, rule-based explanation for the ranking.
    """
    # Skill-based segment
    if skill_score > 70:
        skill_eval = "strong alignment in core skills"
    elif skill_score >= 40:
        skill_eval = "moderate alignment in skills"
    else:
        skill_eval = "limited skill match"

    # Semantic-based segment
    if similarity_score < 30:
        sim_eval = "but shows low contextual relevance to the JD"
    else:
        sim_eval = "and solid overall profile relevance"

    explanation = f"This candidate has {skill_eval} {sim_eval}."

    # Highlight specific skills
    if matched_skills:
        # Take top 2 skills for brevity
        explanation += f" They are proficient in {', '.join([s.title() for s in matched_skills[:2]])}."
    
    if missing_skills:
        explanation += f" However, key areas like {', '.join([s.title() for s in missing_skills[:2]])} were not identified in the resume."

    return explanation
