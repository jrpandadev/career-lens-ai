from src.extract_text import extract_text
from src.llm_extractor import extract_data

text = extract_text("data/resumes/resume.pdf")

resume = extract_data(text)

print(resume)
print()
print("Candidate:", resume.name)
print("Skills:", resume.skills)
print("Experience:", resume.experience)
print("Projects:", resume.projects)
