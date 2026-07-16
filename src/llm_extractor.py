import json
import os
import time

from dotenv import load_dotenv
from groq import Groq
from src.model import Resume, JobD
from src.skills_dict import extract_skills_from_text

load_dotenv()

my_api_key=os.getenv("GROQ_API_KEY")
if not my_api_key:
    raise ValueError("GROQ_API_KEY not found in .env file")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"

def call_groq_with_retry(messages, retries=3, delay=2.0):
    for attempt in range(retries):
        try:
            return client.chat.completions.create(
                model=model,
                messages=messages,
                response_format={"type": "json_object"}
            )
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(delay * (2 ** attempt))

def sanitize(obj):
    if isinstance(obj, dict):
        return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [
            sanitize(item)
            for item in obj
            if item is not None
            and str(item).strip().lower() != "null"
        ]
    if isinstance(obj, str):
        if obj.strip().lower() in {"null", "none", "n/a"}:
            return None
    return obj

def clean_skill_list(skills: list[str]) -> list[str]:
    seen = set()
    cleaned = []

    for skill in skills:
        skill = skill.strip()

        if not skill:
            continue

        normalized = skill.lower()

        if normalized not in seen:
            seen.add(normalized)
            cleaned.append(skill)

    return cleaned

def extract_data(extract_text: str, extra_skills: set[str] = None) -> Resume:
    """
    Extract structured data from resume text using Groq LLM.
    """
    # Adding sleep to prevent hitting rate limits when processing multiple resumes
    time.sleep(5)
    
    schema=Resume.model_json_schema()
    prompt=f"""
You are an expert HR assistant. Extract the following information from the resume.

Return ONLY a valid JSON object.
Do not include:
- Markdown
- Code fences
- Explanations
- Notes
- Additional text

Make sure your response is exactly valid JSON, and all fields in the schema are extracted.
If a field cannot be extracted, return empty string for string fields, empty list for list fields and null for numeric fields.
CRITICAL: 
- `education`, `projects`, and `certifications` MUST be lists of strings, NOT lists of objects.
- Each object in the `experiences` list MUST be a dictionary matching the Experience schema, and MUST include a `skills_used` field which is a list of strings (or empty list if none).
- Ensure the candidate's `name` is properly formatted in Title Case and remove any unnatural spacing (e.g., "A s h i s h" should be "Ashish").
- CRITICAL: Never use single quotes for JSON keys or values. Use standard double quotes for all JSON strings, keys, and array items. Do not output raw newlines or unescaped control characters inside JSON strings.

{schema}

Resume Text:
{extract_text}
"""
    
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    response = call_groq_with_retry(messages)
    result = response.choices[0].message.content
    data = json.loads(result)

    data = sanitize(data)

    resume = Resume.model_validate(data)
    resume.skills = extract_skills_from_text(extract_text, extra_skills)
    return resume

def extract_job(job_text: str) -> JobD:
    schema = JobD.model_json_schema()

    prompt = f"""
You are an ATS Job Description Parser.

Your task is ONLY to convert the job description into structured JSON.

STRICT RULES:

1. Extract information ONLY from the job description.
2. NEVER invent information.
3. NEVER summarize.
4. NEVER rewrite skill names.
5. NEVER split one bullet into multiple skills.
6. NEVER merge multiple bullets.
7. Preserve wording exactly as written.

For example:

If the job description says:

"Experience with at least one general-purpose programming language such as Java, Python, C++, C#, Go, Rust, or TypeScript"

then required_skills should contain EXACTLY ONE ITEM:

[
"Experience with at least one general-purpose programming language such as Java, Python, C++, C#, Go, Rust, or TypeScript"
]

NOT

[
"Java",
"Python",
"C++"
]

Likewise,

If the JD says:

"Database systems (SQL and NoSQL)"

keep it exactly as:

"Database systems (SQL and NoSQL)"

Do NOT split it.

8. In addition to preserving the exact bullets in required_skills and preferred_skills, you MUST ALSO extract a clean list of short, 1-3 word hard technical skill keywords (e.g. "Python", "Apache Kafka", "System Design") into the required_skill_keywords and preferred_skill_keywords fields.
WARNING: ONLY extract HARD technical tools, languages, and frameworks. DO NOT extract soft skills (e.g. "communication", "problem-solving", "adaptability"). DO NOT extract education degrees or fields (e.g. "Computer Science", "STEM", "Information Systems").

Return ONLY valid JSON.

Schema:

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

    response = call_groq_with_retry(messages)

    result = response.choices[0].message.content

    data = json.loads(result)

    data = sanitize(data)

    job = JobD.model_validate(data)
    
    job_specific_skills = set(job.required_skill_keywords + job.preferred_skill_keywords)
    
    job.required_skills = extract_skills_from_text(" ".join(job.required_skills), job_specific_skills)
    job.preferred_skills = extract_skills_from_text(" ".join(job.preferred_skills), job_specific_skills)

    return job
