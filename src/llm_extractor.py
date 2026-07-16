from pyexpat.errors import messages
import json
import os

from dotenv import load_dotenv
from groq import Groq
from src.model import Resume, JobD

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client=Groq(api_key=my_api_key)
model="llama-3.1-8b-instant"
role="user"

def clean_skill_list(skills: list[str]) -> list[str]:
    """
    Remove duplicate skills while preserving order.
    """

    seen = set()
    cleaned = []

    for skill in skills:

        normalized = skill.strip().lower()

        if normalized not in seen:
            seen.add(normalized)
            cleaned.append(skill.strip())

    return cleaned

def extract_data(extract_text:str) -> Resume:
    schema=Resume.model_json_schema()
    response_format={
    "type": "json_object"
    }
    prompt=f"""
You are an expert HR assistant.Extract the following information from the resume.Return ONLY valid JSON. Make sure your response is exactly valid JSON, without any explanations or surrounding text and all fields in the schema are extracted.If a field cannot be extracted, return empty string for string fields, empty list for list fields and 0 for numeric fields.
CRITICAL: 
- `education`, `projects`, and `certifications` MUST be lists of strings, NOT lists of objects.
- Each object in the `experiences` list MUST be a dictionary matching the Experience schema, and MUST include a `skills_used` field which is a list of strings (or empty list if none).
{schema} 
Resume Text:
{extract_text}
"""
    
    messages=[{
    "role" : "user",
    "content" : prompt
    }]

    response=client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    result=response.choices[0].message.content
    data = json.loads(result)
    resume = Resume.model_validate(data)
    resume.skills = clean_skill_list(resume.skills)
    return resume

def extract_job(job_text: str) -> JobD:
    schema = JobD.model_json_schema()

    response_format = {
        "type": "json_object"
    }

    prompt = f"""
You are an expert HR assistant.

Extract the following information from the Job Description.

Return ONLY valid JSON.

If any field is missing:
- use an empty list for list fields
- use null for numeric fields
- use an empty string for string fields

JSON Schema:
{schema}

Job Description:

{job_text}
"""

    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        response_format=response_format
    )

    result = response.choices[0].message.content

    data = json.loads(result)

    job = JobD.model_validate(data)
    job.required_skills = clean_skill_list(job.required_skills)
    job.preferred_skills = clean_skill_list(job.preferred_skills)

    return job
