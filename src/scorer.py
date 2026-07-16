from src.model import MatchResult, JobD, Resume

def calculate_score(result: MatchResult, job: JobD, resume: Resume) -> MatchResult:
    # Score calculation
    req_score = 0.0
    if job.required_skills:
        req_score = (len(result.matched_required_skills) / len(job.required_skills)) * 50.0
    else:
        req_score = 50.0

    pref_score = 0.0
    if job.preferred_skills:
        pref_score = (len(result.matched_preferred_skills) / len(job.preferred_skills)) * 15.0
    else:
        pref_score = 15.0

    exp_score = 25.0 if result.experience_match else 0.0
    edu_score = 10.0 if result.education_match else 0.0
    
    total_score = req_score + pref_score + exp_score + edu_score
    result.score = round(total_score, 2)

    # Generate Strengths
    strengths = []
    if len(result.matched_required_skills) >= 5:
        strengths.append("Strong required skill match")
    if result.experience_match:
        strengths.append("Meets experience requirement")
    
    result.strengths = strengths

    # Generate Weaknesses
    weaknesses = []
    if result.missing_required_skills:
        weaknesses.append(f"Missing {len(result.missing_required_skills)} required skills")
    if not result.experience_match:
        weaknesses.append("Does not meet experience requirement")
        
    result.weaknesses = weaknesses

    # Recommendation
    if result.score >= 85:
        recommendation = "Strong Hire"
    elif result.score >= 70:
        recommendation = "Interview"
    elif result.score >= 50:
        recommendation = "Manual Review"
    else:
        recommendation = "Reject"
        
    result.recommendation = recommendation

    return result
