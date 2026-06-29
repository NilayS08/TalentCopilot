from unittest.mock import MagicMock, patch

from app.models.candidate import CandidateProfile
from app.models.evaluation import CandidateEvaluation
from app.models.jd import JDRequirements
from app.services.insight_generator import generate_insight, _parse_json_response


class TestParseJsonResponse:
    def test_plain_json(self):
        result = _parse_json_response('{"summary": "test"}')
        assert result == {"summary": "test"}

    def test_markdown_fence(self):
        result = _parse_json_response('```json\n{"summary": "test"}\n```')
        assert result == {"summary": "test"}

    def test_extra_text(self):
        result = _parse_json_response('Some text\n{"summary": "hello"}\nmore text')
        assert result == {"summary": "hello"}


@patch("app.services.insight_generator.model")
class TestGenerateInsight:
    def test_returns_insight(self, mock_model):
        mock_response = MagicMock()
        mock_response.text = '{"summary": "Strong Python skills align well with the role. Recommended for interview."}'
        mock_model.generate_content.return_value = mock_response

        jd = JDRequirements(
            role_title="Backend Engineer",
            required_skills=["Python"],
            preferred_skills=[],
            experience_required="3 years",
        )
        candidate = CandidateProfile(
            name="Alice",
            skills=["Python"],
            projects=[],
            experience=["Engineer at Co(3 years):Built APIs"],
        )
        evaluation = CandidateEvaluation(
            skill_score=100.0,
            experience_score=100.0,
            matched_skills=["Python"],
            missing_skills=[],
        )

        insight = generate_insight(jd, candidate, evaluation)

        assert (
            insight.summary
            == "Strong Python skills align well with the role. Recommended for interview."
        )
        mock_model.generate_content.assert_called_once()

    def test_retry_on_failure(self, mock_model):
        mock_model.generate_content.side_effect = [
            Exception("First parse failed"),
            MagicMock(text='{"summary": "Retry succeeded."}'),
        ]

        jd = JDRequirements(
            role_title="Dev",
            required_skills=[],
            preferred_skills=[],
            experience_required="",
        )
        candidate = CandidateProfile(name="Bob", skills=[], projects=[], experience=[])
        evaluation = CandidateEvaluation(
            skill_score=0.0,
            experience_score=0.0,
            matched_skills=[],
            missing_skills=[],
        )

        insight = generate_insight(jd, candidate, evaluation)

        assert insight.summary == "Retry succeeded."
        assert mock_model.generate_content.call_count == 2
