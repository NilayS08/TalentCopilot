from unittest.mock import patch

import pytest

from app.models.candidate import CandidateProfile
from app.models.jd import JDRequirements
from app.services.candidate_evaluator import (
    _compute_experience_score,
    _parse_experience_years,
    _parse_required_experience,
    evaluate_candidate,
)


class TestParseExperienceYears:
    def test_years_and_months(self):
        assert _parse_experience_years(
            "Software Engineer at Google(2 years 3 months):Built APIs"
        ) == pytest.approx(2.25)

    def test_years_only(self):
        assert _parse_experience_years("Senior Dev at Meta(5 years):Led team") == 5.0

    def test_months_only(self):
        assert _parse_experience_years(
            "Intern at Acme(6 months):Helped"
        ) == pytest.approx(0.5)

    def test_year_abbreviation(self):
        assert _parse_experience_years("Engineer at Co(1 yr):desc") == 1.0
        assert _parse_experience_years("Engineer at Co(2 yrs):desc") == 2.0

    def test_month_abbreviation(self):
        assert _parse_experience_years("Dev at Co(3 mo):desc") == pytest.approx(0.25)

    def test_no_duration(self):
        assert _parse_experience_years("Some role at Some Co:desc") == 0.0

    def test_multiple_experiences(self):
        entries = [
            "Engineer at A(2 years):desc",
            "Senior at B(3 years 6 months):desc",
            "Lead at C(1 year):desc",
        ]
        total = sum(_parse_experience_years(e) for e in entries)
        assert total == pytest.approx(6.5)


class TestParseRequiredExperience:
    def test_simple_years(self):
        assert _parse_required_experience("3 years") == 3.0

    def test_plus_years(self):
        assert _parse_required_experience("5+ years") == 5.0

    def test_range(self):
        assert _parse_required_experience("2-3 years") == 2.0

    def test_with_description(self):
        assert (
            _parse_required_experience(
                "At least 7 years of experience in software development"
            )
            == 7.0
        )

    def test_no_number(self):
        assert _parse_required_experience("Not specified") == 0.0


class TestComputeExperienceScore:
    def test_exact_match(self):
        exp = ["Engineer at A(2 years):desc", "Senior at B(3 years):desc"]
        assert _compute_experience_score(exp, "5 years") == 100.0

    def test_under_required(self):
        exp = ["Engineer at A(2 years):desc", "Senior at B(3 years):desc"]
        assert _compute_experience_score(exp, "10 years") == 50.0

    def test_over_required(self):
        exp = ["Engineer at A(5 years):desc", "Senior at B(4 years):desc"]
        assert _compute_experience_score(exp, "3 years") == 100.0

    def test_no_required_specified(self):
        exp = ["Engineer at A(2 years):desc"]
        assert _compute_experience_score(exp, "") == 100.0

    def test_no_experience(self):
        assert _compute_experience_score([], "5 years") == 0.0

    def test_partial_months(self):
        exp = ["Engineer at A(1 year 6 months):desc"]
        assert _compute_experience_score(exp, "3 years") == 50.0


@patch("app.services.candidate_evaluator.semantic_skill_score")
class TestEvaluateCandidate:
    def test_full_evaluation(self, mock_semantic):
        mock_semantic.return_value = {
            "score": 80.0,
            "matched_skills": ["Python", "FastAPI"],
            "missing_skills": ["Docker"],
        }

        jd = JDRequirements(
            role_title="Backend Engineer",
            required_skills=["Python", "FastAPI", "Docker"],
            preferred_skills=["AWS"],
            experience_required="5 years",
        )
        candidate = CandidateProfile(
            name="Alice",
            skills=["Python", "FastAPI"],
            projects=[],
            experience=[
                "Backend Dev at Corp(3 years):Built APIs",
                "Senior at Startup(2 years 6 months):Led team",
            ],
        )

        result = evaluate_candidate(jd, candidate)

        assert result.skill_score == 80.0
        assert result.experience_score == 100.0  # 5.5 / 5 capped
        assert result.matched_skills == ["Python", "FastAPI"]
        assert result.missing_skills == ["Docker"]

    def test_skill_only_experience_zero(self, mock_semantic):
        mock_semantic.return_value = {
            "score": 100.0,
            "matched_skills": ["Python"],
            "missing_skills": [],
        }

        jd = JDRequirements(
            role_title="Dev",
            required_skills=["Python"],
            preferred_skills=[],
            experience_required="5 years",
        )
        candidate = CandidateProfile(
            name="Bob",
            skills=["Python"],
            projects=[],
            experience=[],
        )

        result = evaluate_candidate(jd, candidate)

        assert result.skill_score == 100.0
        assert result.experience_score == 0.0
