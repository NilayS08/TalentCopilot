from pydantic import BaseModel

class JDRequirements(BaseModel):
    role_title:str
    required_skills:list[str]
    preferred_skills:list[str]
    experience_required:str
# enforces structure of the data for JD requirements, ensuring consistency and validation when processing job descriptions
