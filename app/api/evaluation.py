from fastapi import APIRouter
from pydantic import BaseModel

from app.models.candidate import CandidateProfile
from app.models.evaluation import CandidateEvaluation, RankedCandidate, RecruiterInsight
from app.models.jd import JDRequirements
from app.services.candidate_evaluator import evaluate_candidate
from app.services.candidate_ranker import rank_candidates
from app.services.insight_generator import generate_insight

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


class InsightRequest(BaseModel):
    jd: JDRequirements
    candidate: CandidateProfile
    evaluation: CandidateEvaluation


@router.post("/evaluate", response_model=CandidateEvaluation)
async def evaluate_candidate_endpoint(request: EvaluateRequest):
    return evaluate_candidate(request.jd, request.candidate)


@router.post("/rank", response_model=list[RankedCandidate])
async def rank_candidates_endpoint(request: RankRequest):
    return rank_candidates(request.jd, request.candidates)


@router.post("/insight", response_model=RecruiterInsight)
async def insight_endpoint(request: InsightRequest):
    return generate_insight(request.jd, request.candidate, request.evaluation)
