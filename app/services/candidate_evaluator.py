from app.models.candidate import CandidateProfile
from app.models.evaluation import CandidateEvaluation
from app.models.jd import JDRequirements
from app.services.skill_matcher import semantic_skill_score


def evaluate_candidate(
    jd: JDRequirements,
    candidate: CandidateProfile,
) -> CandidateEvaluation:
    result = semantic_skill_score(jd.required_skills, candidate.skills)

    return CandidateEvaluation(
        skill_score=result["score"],
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
    )
