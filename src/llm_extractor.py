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
model="llama-3.3-70b-versatile"
role="user"

def extract_data(extract_text:str) -> Resume:
    schema=Resume.model_json_schema()
    response_format={
    "type": "json_object"
    }
    prompt=f"""
You are an expert HR assistant.Extract the following information from the resume.Return ONLY valid JSON. Make sure your response is exactly valid JSON, without any explanations or surrounding text and all fields in the schema are extracted.If a field cannot be extracted, return empty string for string fields, empty list for list fields and 0 for numeric fields.
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
    data=json.loads(result)
    resume=Resume.model_validate(data)
    return resume

def extract_job(job_text: str) -> JobD:
    schema = JobD.model_json_schema()
    response_format = {
        "type": "json_object"
    }
    prompt = f"""
You are an expert HR assistant. Extract the following information from the job description. Return ONLY valid JSON. Make sure your response is exactly valid JSON, without any explanations or surrounding text and all fields in the schema are extracted. If a field cannot be extracted, return empty string for string fields, empty list for list fields and 0 for numeric fields.
{schema} 
Job Description Text:
{job_text}
"""
    
    messages = [{
        "role" : "user",
        "content" : prompt
    }]

    response = client.chat.completions.create(model=model, messages=messages, response_format=response_format)
    result = response.choices[0].message.content
    data = json.loads(result)
    job = JobD.model_validate(data)
    return job
