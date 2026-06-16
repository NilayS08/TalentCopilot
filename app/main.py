from fastapi import FastAPI
from app.api.jd import router as jd_router

app = FastAPI(title="TalentCopilot")

app.include_router(jd_router)