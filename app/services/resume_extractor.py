import json
import os
import re
import logging
from dotenv import load_dotenv
import google.generativeai as genai

from app.models.candidate import CandidateProfile

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

PROMPT = """You are an expert resume parser.

Extract candidate information.

Return ONLY JSON.

{{
    "name": "",
    "skills": [],
    "projects": ["Project name: description"],
    "experience": ["Job title at Company(dates):bullet summary"],
    "education": [Degree, School(dates)]
}}

Resume:
{resume_text}
"""

def _parse_json_response(response_text:str) -> dict:
    text = response_text.strip()

    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)

    return json.loads(text)

def extract_candidate_profile(resume_text:str) -> CandidateProfile:
    prompt = PROMPT.format(resume_text=resume_text)

    try:
        response = model.generate_content(prompt)
        data = _parse_json_response(response.text)
        return CandidateProfile(**data)
    except Exception as first_error:
        logger.warning("Gemini parse failed once, retrying: %s", first_error)

        retry_prompt = (
            "Return ONLY valid JSON matching the schema. "
            "No extra words, no markdown, no comments.\n\n"
            f"{prompt}"
        )
        response = model.generate_content(retry_prompt)
        data = _parse_json_response(response.text)
        return CandidateProfile(**data)