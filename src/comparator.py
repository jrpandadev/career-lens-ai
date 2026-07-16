from src.model import JobD, Resume, MatchResult

def compare_resume(job: JobD, resume: Resume) -> MatchResult:
    resume_skills = set(resume.skills)

    matched_required = []
    missing_required = []

    for skill in job.required_skills:
        if skill in resume_skills:
            matched_required.append(skill)
        else:
            missing_required.append(skill)

    matched_preferred = []
    missing_preferred = []

    for skill in job.preferred_skills:
        if skill in resume_skills:
            matched_preferred.append(skill)
        else:
            missing_preferred.append(skill)

    experience_match = (
        resume.total_experience_years is not None
        and job.minimum_experience is not None
        and resume.total_experience_years >= job.minimum_experience
    )

    education_match = len(resume.education) > 0

    return MatchResult(
        matched_required_skills=matched_required,
        missing_required_skills=missing_required,
        matched_preferred_skills=matched_preferred,
        missing_preferred_skills=missing_preferred,
        experience_match=experience_match,
        education_match=education_match
    )
