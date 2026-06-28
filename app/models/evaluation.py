from pydantic import BaseModel

from app.models.candidate import CandidateProfile

class CandidateEvaluation(BaseModel):
    skill_score: float
    experience_score: float
    matched_skills: list[str]
    missing_skills: list[str]

class RankedCandidate(BaseModel):
    rank: int
    candidate: CandidateProfile
    evaluation: CandidateEvaluation
    overall_score: float
