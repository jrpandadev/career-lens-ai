from src.extract_text import extract_text
from src.llm_extractor import extract_data
from src.comparator import (
    load_hr_requirements,
    compare_resume,
)
from src.scorer import calculate_score

text = extract_text("data/resumes/resume.pdf")

resume = extract_data(text)

hr = load_hr_requirements("data/hr_requirements.json")

comparison = compare_resume(resume, hr)

score = calculate_score(comparison, hr)

print("Match Score:", score, "%")