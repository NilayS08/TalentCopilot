from fastapi import APIRouter
from pydantic import BaseModel

from app.models.candidate import CandidateProfile
from app.models.evaluation import CandidateEvaluation, RankedCandidate
from app.models.jd import JDRequirements
from app.services.candidate_evaluator import evaluate_candidate
from app.services.candidate_ranker import rank_candidates

router = APIRouter(
    prefix="/evaluation",
    tags=["Candidate Evaluation"],
)


class EvaluateRequest(BaseModel):
    jd: JDRequirements
    candidate: CandidateProfile


class RankRequest(BaseModel):
    jd: JDRequirements
    candidates: list[CandidateProfile]


@router.post("/evaluate", response_model=CandidateEvaluation)
async def evaluate_candidate_endpoint(request: EvaluateRequest):
    return evaluate_candidate(request.jd, request.candidate)


@router.post("/rank", response_model=list[RankedCandidate])
async def rank_candidates_endpoint(request: RankRequest):
    return rank_candidates(request.jd, request.candidates)
