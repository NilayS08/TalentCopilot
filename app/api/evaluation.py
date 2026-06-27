from fastapi import APIRouter
from pydantic import BaseModel

from app.models.candidate import CandidateProfile
from app.models.evaluation import CandidateEvaluation
from app.models.jd import JDRequirements
from app.services.candidate_evaluator import evaluate_candidate

router = APIRouter(
    prefix="/evaluation",
    tags=["Candidate Evaluation"],
)


class EvaluateRequest(BaseModel):
    jd: JDRequirements
    candidate: CandidateProfile


@router.post("/evaluate", response_model=CandidateEvaluation)
async def evaluate_candidate_endpoint(request: EvaluateRequest):
    return evaluate_candidate(request.jd, request.candidate)
