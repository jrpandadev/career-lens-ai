from pydantic import BaseModel
class Resume(BaseModel):
    name: str
    skills: list[str]
    experience: int
    projects: list[str]
    education: str