from pydantic import BaseModel


class CandidateEvaluation(BaseModel):
    skill_score: float
    matched_skills: list[str]
    missing_skills: list[str]
