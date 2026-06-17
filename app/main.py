from fastapi import FastAPI
from app.api.jd import router as jd_router
from app.api.resume import router as resume_router

app = FastAPI(title="TalentCopilot")

app.include_router(jd_router)
app.include_router(resume_router)