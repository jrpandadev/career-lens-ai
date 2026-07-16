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

MODEL = "llama-3.3-70b-versatile"

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

Return ONLY valid JSON following this schema.

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

    return MatchResult.model_validate(data)
