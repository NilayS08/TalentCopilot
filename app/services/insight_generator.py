import json
import os
import re
import logging
from dotenv import load_dotenv
import google.generativeai as genai

from app.models.candidate import CandidateProfile
from app.models.evaluation import CandidateEvaluation, RecruiterInsight
from app.models.jd import JDRequirements

logger = logging.getLogger(__name__)

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    generation_config={
        "response_mime_type": "application/json",
        "temperature": 0,
    },
)

PROMPT = """You are an expert technical recruiter.

Given a Job Description, a Candidate Profile, and their evaluation scores, provide a concise 2-3 sentence recruiter insight about this candidate.

Focus on:
- Why the candidate is or isn't a good fit
- Key strengths relevant to the role
- Notable missing skills
- Interview recommendation

Be direct and specific. Avoid generic statements.

Return ONLY JSON:
{{
    "summary": ""
}}

Job Description:
Role: {role_title}
Required Skills: {required_skills}
Preferred Skills: {preferred_skills}
Experience Required: {experience_required}

Candidate: {candidate_name}
Skills: {candidate_skills}
Experience: {candidate_experience}
Projects: {candidate_projects}

Evaluation:
Skill Score: {skill_score}/100
Experience Score: {experience_score}/100
Matched Skills: {matched_skills}
Missing Skills: {missing_skills}
"""


def _parse_json_response(response_text: str) -> dict:
    text = response_text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)

    return json.loads(text)


def generate_insight(
    jd: JDRequirements,
    candidate: CandidateProfile,
    evaluation: CandidateEvaluation,
) -> RecruiterInsight:
    prompt = PROMPT.format(
        role_title=jd.role_title,
        required_skills=", ".join(jd.required_skills),
        preferred_skills=", ".join(jd.preferred_skills),
        experience_required=jd.experience_required,
        candidate_name=candidate.name,
        candidate_skills=", ".join(candidate.skills),
        candidate_experience=" | ".join(candidate.experience),
        candidate_projects=" | ".join(candidate.projects),
        skill_score=evaluation.skill_score,
        experience_score=evaluation.experience_score,
        matched_skills=", ".join(evaluation.matched_skills),
        missing_skills=", ".join(evaluation.missing_skills),
    )

    try:
        response = model.generate_content(prompt)
        data = _parse_json_response(response.text)
        return RecruiterInsight(**data)
    except Exception as first_error:
        logger.warning("Gemini insight failed once, retrying: %s", first_error)

        retry_prompt = (
            "Return ONLY valid JSON matching the schema. "
            "No extra words, no markdown, no comments.\n\n"
            f"{prompt}"
        )
        response = model.generate_content(retry_prompt)
        data = _parse_json_response(response.text)
        return RecruiterInsight(**data)
