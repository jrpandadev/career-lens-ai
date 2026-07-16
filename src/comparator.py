import json
import os

from dotenv import load_dotenv
from groq import Groq

from src.model import JobD, Resume, MatchResult

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found in .env")

client = Groq(api_key=api_key)

MODEL = "llama-3.1-8b-instant"

def normalize_skill(skill: str) -> str:
    """
    Normalize a skill for comparison.
    """
    return skill.strip().lower()

def load_job_description(file_path: str):
    with open(file_path, "r", encoding="utf-8") as file:
        if file_path.endswith(".json"):
            return JobD.model_validate(json.load(file))
        return file.read()

def compare_resume(job: JobD, resume: Resume) -> MatchResult:
    schema = MatchResult.model_json_schema()

    prompt = f"""
You are an expert technical recruiter.

Compare the following candidate with the job description.

Return ONLY valid JSON following this exact structure:
{{
  "score": 0.0,
  "matched_skills": ["string"],
  "missing_skills": ["string"],
  "strengths": ["string"],
  "weaknesses": ["string"],
  "recommendation": "string"
}}

Schema:
{schema}

Job Description:
{job.model_dump_json(indent=2)}

Candidate Resume:
{resume.model_dump_json(indent=2)}

Scoring Guidelines:
- Skills Match (40%)
- Experience Match (30%)
- Projects (20%)
- Education (10%)

Return:
- score (0-100)
- details
"""

    response = client.chat.completions.create(
        model=MODEL,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    data = json.loads(response.choices[0].message.content)

    match_result = MatchResult.model_validate(data)

    # Deterministic skill comparison
    resume_skills = {
        normalize_skill(skill)
        for skill in resume.skills
    }

    matched_skills = []
    missing_skills = []

    for skill in job.required_skills:
        normalized_skill = normalize_skill(skill)
        if normalized_skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    for skill in job.preferred_skills:
        normalized_skill = normalize_skill(skill)
        if normalized_skill in resume_skills:
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    match_result.matched_skills = matched_skills
    match_result.missing_skills = missing_skills

    return match_result
