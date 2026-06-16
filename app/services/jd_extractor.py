import json
import os
import re
import logging
from dotenv import load_dotenv
import google.generativeai as genai

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

PROMPT = """
You are an expert recruiter.

Extract information from the Job Description.

Return ONLY valid JSON.
Do not add any extra text, markdown, or explanation.

Schema:
{{
  "role_title": "",
  "required_skills": [],
  "preferred_skills": [],
  "experience_required": ""
}}

Job Description:
{jd_text}
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

def extract_requirements(jd_text: str) -> JDRequirements:
    prompt = PROMPT.format(jd_text=jd_text)

    try:
        response = model.generate_content(prompt)
        data = _parse_json_response(response.text)
        return JDRequirements(**data)
    except Exception as first_error:
        logger.warning("Gemini parse failed once, retrying: %s", first_error)

        retry_prompt = (
            "Return ONLY valid JSON matching the schema. "
            "No extra words, no markdown, no comments.\n\n"
            f"{prompt}"
        )
        response = model.generate_content(retry_prompt)
        data = _parse_json_response(response.text)
        return JDRequirements(**data)