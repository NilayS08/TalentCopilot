from pydantic import BaseModel

class CandidateProfile(BaseModel):
    name:str
    skills:list[str]
    projects:list[str]
    experience:list[str]
    education:list[str]
