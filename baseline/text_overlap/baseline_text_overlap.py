from skipwords import skipWords

def read_file(file_name):
    try:
        with open(file_name, 'r') as f:
            return f.read()
    except FileNotFoundError as e:
        return {"error": str(e)}
    
def preprocess_words(text: str):
    # lowercase and strip punctuation, return list of tokens
    tokens = text.split()
    cleaned = [t.lower().strip(".,:\n()[]{}!?;\"'") for t in tokens]
    return cleaned

def get_matching_words(resume_tokens, jd_tokens):
    matching = []

    jd_set = set(jd_tokens)  # faster lookup

    for item in resume_tokens:
        if item in jd_set and item not in skipWords:
            matching.append(item)
    
    return matching

def get_missing_words(resume_tokens, jd_tokens):
    missing = []

    jd_set = set(jd_tokens)

    for item in jd_set:
        if item not in resume_tokens and item not in skipWords:
            missing.append(item)

    return missing

def baseline_similarity_score(resume_tokens, jd_tokens):
    # similarity = (# of matching words) / (min(len(resume_tokens), len(jd_tokens)))
    matches = get_matching_words(resume_tokens, jd_tokens)
    denom = min(len(resume_tokens), len(jd_tokens))
    return len(matches) / denom if denom > 0 else 0.0


def overlap_analysis(resume_text: str, jd_text: str):
    # return keyword overlap + baseline score
    resume_tokens = preprocess_words(resume_text)
    jd_tokens = preprocess_words(jd_text)

    matching = get_matching_words(resume_tokens, jd_tokens)
    missing = get_missing_words(resume_tokens, jd_tokens)
    score = round(baseline_similarity_score(resume_tokens, jd_tokens), 2)

    return {
        "similarityScore": score,
        "strengths": matching,
        "weaknesses": missing
    }

if __name__ == "__main__":
    job_description = """
    Software Engineer Position

    We're looking for a backend engineer to join our team.

    Requirements:
    - 2+ years experience with Python
    - Strong knowledge of Django or Flask
    - Experience with PostgreSQL or MySQL
    - Familiarity with Docker and Kubernetes
    - Understanding of REST API design
    - Experience with AWS or Azure cloud platforms
    - Git version control

    Nice to have:
    - React or Vue.js experience
    - Redis caching
    - CI/CD pipeline setup 
    - C++
    """

    user_resume = """
        Sarah Chen
        Software Engineer
        sarah.chen@email.com

        EXPERIENCE
        Backend Engineer at DataFlow Inc (2022-2024)
        - Built REST APIs using Python and Django
        - Worked with PostgreSQL and Redis for data storage
        - Implemented  pipelines with Jenkins and Docker
        - Collaborated with frontend team on React integration

        SKILLS
        Python, JavaScript, Django, Flask, PostgreSQL, Docker, Git, AWS
        """
    
    results = overlap_analysis(user_resume, job_description)
    print(f"Score: {results['similarityScore']}")
    print(f"Strengths: {results['strengths']}")
    print(f"Weaknesses: {results['weaknesses']}")