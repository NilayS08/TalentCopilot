from app.models.candidate import CandidateProfile
from app.models.evaluation import CandidateEvaluation, RankedCandidate
from app.models.jd import JDRequirements
from app.services.candidate_evaluator import evaluate_candidate


def _compute_overall_score(evaluation: CandidateEvaluation) -> float:
    return (evaluation.skill_score + evaluation.experience_score) / 2.0


def rank_candidates(
    jd: JDRequirements,
    candidates: list[CandidateProfile],
) -> list[RankedCandidate]:
    results: list[tuple[float, CandidateEvaluation, CandidateProfile]] = []

    for candidate in candidates:
        evaluation = evaluate_candidate(jd, candidate)
        overall = _compute_overall_score(evaluation)
        results.append((overall, evaluation, candidate))

    results.sort(key=lambda x: x[0], reverse=True)

    return [
        RankedCandidate(
            rank=i + 1,
            candidate=candidate,
            evaluation=evaluation,
            overall_score=round(overall, 2),
        )
        for i, (overall, evaluation, candidate) in enumerate(results)
    ]
