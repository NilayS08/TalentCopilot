from unittest.mock import patch

from app.models.candidate import CandidateProfile
from app.models.jd import JDRequirements
from app.services.candidate_ranker import _compute_overall_score, rank_candidates


class TestOverallScore:
    def test_average_of_scores(self):
        evaluation = _build_evaluation(skill=80.0, exp=60.0)
        assert _compute_overall_score(evaluation) == 70.0

    def test_perfect_scores(self):
        evaluation = _build_evaluation(skill=100.0, exp=100.0)
        assert _compute_overall_score(evaluation) == 100.0

    def test_zero_scores(self):
        evaluation = _build_evaluation(skill=0.0, exp=0.0)
        assert _compute_overall_score(evaluation) == 0.0

    def test_rounding(self):
        evaluation = _build_evaluation(skill=83.33, exp=66.67)
        assert _compute_overall_score(evaluation) == 75.0


@patch("app.services.candidate_ranker.evaluate_candidate")
class TestRankCandidates:
    def test_sorts_by_score_descending(self, mock_evaluate):
        mock_evaluate.side_effect = [
            _build_evaluation(skill=60.0, exp=60.0),
            _build_evaluation(skill=90.0, exp=90.0),
            _build_evaluation(skill=80.0, exp=80.0),
        ]

        jd = JDRequirements(
            role_title="Engineer",
            required_skills=[],
            preferred_skills=[],
            experience_required="",
        )
        candidates = [
            CandidateProfile(name="C", skills=[], projects=[], experience=[]),
            CandidateProfile(name="A", skills=[], projects=[], experience=[]),
            CandidateProfile(name="B", skills=[], projects=[], experience=[]),
        ]

        ranked = rank_candidates(jd, candidates)

        assert len(ranked) == 3
        assert ranked[0].candidate.name == "A"
        assert ranked[1].candidate.name == "B"
        assert ranked[2].candidate.name == "C"
        assert ranked[0].rank == 1
        assert ranked[1].rank == 2
        assert ranked[2].rank == 3
        assert ranked[0].overall_score == 90.0
        assert ranked[1].overall_score == 80.0
        assert ranked[2].overall_score == 60.0

    def test_single_candidate(self, mock_evaluate):
        mock_evaluate.return_value = _build_evaluation(skill=75.0, exp=75.0)

        jd = JDRequirements(
            role_title="Dev",
            required_skills=[],
            preferred_skills=[],
            experience_required="",
        )
        candidates = [
            CandidateProfile(name="Solo", skills=[], projects=[], experience=[])
        ]

        ranked = rank_candidates(jd, candidates)
        assert len(ranked) == 1
        assert ranked[0].rank == 1
        assert ranked[0].candidate.name == "Solo"
        assert ranked[0].overall_score == 75.0

    def test_empty_candidates(self, mock_evaluate):
        jd = JDRequirements(
            role_title="Dev",
            required_skills=[],
            preferred_skills=[],
            experience_required="",
        )
        ranked = rank_candidates(jd, [])
        assert ranked == []

    def test_tie_same_score(self, mock_evaluate):
        mock_evaluate.return_value = _build_evaluation(skill=50.0, exp=50.0)

        jd = JDRequirements(
            role_title="Dev",
            required_skills=[],
            preferred_skills=[],
            experience_required="",
        )
        candidates = [
            CandidateProfile(name="X", skills=[], projects=[], experience=[]),
            CandidateProfile(name="Y", skills=[], projects=[], experience=[]),
        ]

        ranked = rank_candidates(jd, candidates)
        assert len(ranked) == 2
        assert ranked[0].overall_score == ranked[1].overall_score
        assert ranked[0].rank == 1
        assert ranked[1].rank == 2


def _build_evaluation(skill: float, exp: float):
    from app.models.evaluation import CandidateEvaluation

    return CandidateEvaluation(
        skill_score=skill,
        experience_score=exp,
        matched_skills=[],
        missing_skills=[],
    )
