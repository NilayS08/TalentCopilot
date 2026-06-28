import re

from app.models.candidate import CandidateProfile
from app.models.evaluation import CandidateEvaluation
from app.models.jd import JDRequirements
from app.services.skill_matcher import semantic_skill_score


def _parse_experience_years(text: str) -> float:
    years = 0.0
    year_match = re.search(r"(\d+)\s*(?:year|yr)s?", text, re.IGNORECASE)
    month_match = re.search(r"(\d+)\s*(?:month|mo)s?", text, re.IGNORECASE)
    if year_match:
        years += int(year_match.group(1))
    if month_match:
        years += int(month_match.group(1)) / 12.0
    return years


def _parse_required_experience(text: str) -> float:
    numbers = re.findall(r"\d+", text)
    return float(numbers[0]) if numbers else 0.0


def _compute_experience_score(
    candidate_experience: list[str], jd_required: str
) -> float:
    total_years = sum(_parse_experience_years(exp) for exp in candidate_experience)
    required_years = _parse_required_experience(jd_required)
    if required_years <= 0:
        return 100.0
    return min(total_years / required_years, 1.0) * 100.0


def evaluate_candidate(
    jd: JDRequirements,
    candidate: CandidateProfile,
) -> CandidateEvaluation:
    result = semantic_skill_score(jd.required_skills, candidate.skills)

    return CandidateEvaluation(
        skill_score=result["score"],
        experience_score=_compute_experience_score(
            candidate.experience, jd.experience_required
        ),
        matched_skills=result["matched_skills"],
        missing_skills=result["missing_skills"],
    )
