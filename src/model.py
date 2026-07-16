from pydantic import BaseModel, model_validator

class JobD(BaseModel):
    role: str | None = None
    required_skills: list[str] = []
    preferred_skills: list[str] = []
    required_skill_keywords: list[str] = []
    preferred_skill_keywords: list[str] = []
    minimum_experience: float | None = None
    education_requirements: list[str] = [] 
    responsibilities: list[str] = []

    @model_validator(mode='before')
    @classmethod
    def sanitize_nulls(cls, data):
        if isinstance(data, dict):
            for list_field in ['required_skills', 'preferred_skills', 'required_skill_keywords', 'preferred_skill_keywords', 'education_requirements', 'responsibilities']:
                if data.get(list_field) is None:
                    data[list_field] = []
            if data.get('minimum_experience') is None:
                data['minimum_experience'] = 0.0
        return data

class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []

    @model_validator(mode='before')
    @classmethod
    def sanitize_nulls(cls, data):
        if isinstance(data, dict):
            if data.get('skills_used') is None:
                data['skills_used'] = []
        return data

class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    total_experience_years: float | None = None
    skills: list[str] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []
    experiences: list[Experience] = []
    
    @model_validator(mode='before')
    @classmethod
    def sanitize_nulls(cls, data):
        if isinstance(data, dict):
            for list_field in ['skills', 'education', 'projects', 'certifications', 'experiences']:
                if data.get(list_field) is None:
                    data[list_field] = []
            if data.get('total_experience_years') is None:
                data['total_experience_years'] = 0.0
        return data

class MatchResult(BaseModel):
    score: float = 0.0

    matched_required_skills: list[str] = []
    missing_required_skills: list[str] = []

    matched_preferred_skills: list[str] = []
    missing_preferred_skills: list[str] = []

    experience_match: bool = False
    education_match: bool = False

    strengths: list[str] = []
    weaknesses: list[str] = []

    recommendation: str = ""

    @model_validator(mode='before')
    @classmethod
    def sanitize_nulls(cls, data):
        if isinstance(data, dict):
            for list_field in [
                'matched_required_skills', 'missing_required_skills', 
                'matched_preferred_skills', 'missing_preferred_skills', 
                'strengths', 'weaknesses'
            ]:
                if data.get(list_field) is None:
                    data[list_field] = []
            if data.get('score') is None:
                data['score'] = 0.0
            if data.get('experience_match') is None:
                data['experience_match'] = False
            if data.get('education_match') is None:
                data['education_match'] = False
            if data.get('recommendation') is None:
                data['recommendation'] = ""
        return data
   