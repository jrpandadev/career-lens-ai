from pydantic import BaseModel, Field
from typing import List, Optional

class ExtractedDetails(BaseModel):
    name: Optional[str] = Field(None, description="Candidate's full name")
    email: Optional[str] = Field(None, description="Candidate's email address")
    phone: Optional[str] = Field(None, description="Candidate's phone number")
    skills: List[str] = Field(default_factory=list, description="Key skills extracted from the resume")
    experience_years: Optional[float] = Field(None, description="Total years of experience")
    education: List[str] = Field(default_factory=list, description="Education details (degrees, universities)")

class MatchResult(BaseModel):
    candidate_name: str
    match_score: int = Field(..., description="Score from 0 to 100")
    matching_skills: List[str]
    missing_skills: List[str]
    justification: str = Field(..., description="Brief explanation for the score")
