import re
from functools import lru_cache

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

MODEL_NAME = "all-MiniLM-L6-v2"
SIMILARITY_THRESHOLD = 0.6


@lru_cache(maxsize=1)
def _get_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def _normalize_for_embedding(skill: str) -> str:
    return re.sub(r"[\-_/]+", " ", skill.strip()).lower()


def _words(text: str) -> list[str]:
    return [word for word in re.split(r"[\s\-_/]+", text.strip()) if word]


def _is_acronym(acronym: str, phrase: str) -> bool:
    letters = re.sub(r"[^a-zA-Z0-9]", "", acronym).upper()
    words = _words(phrase)

    if len(letters) < 2 or len(letters) != len(words):
        return False

    return all(letter == word[0].upper() for letter, word in zip(letters, words))


def _parenthetical_acronyms(text: str) -> list[str]:
    return [
        match.upper()
        for match in re.findall(r"\(([A-Za-z]{2,})\)", text)
    ]


def _acronym_match(skill_a: str, skill_b: str) -> bool:
    a = skill_a.strip()
    b = skill_b.strip()

    if _is_acronym(a, b) or _is_acronym(b, a):
        return True

    a_compact = re.sub(r"[^a-zA-Z0-9]", "", a).upper()
    b_compact = re.sub(r"[^a-zA-Z0-9]", "", b).upper()

    for acronym in _parenthetical_acronyms(a):
        if acronym == b_compact:
            return True

    for acronym in _parenthetical_acronyms(b):
        if acronym == a_compact:
            return True

    return False


def _find_acronym_match(jd_skill: str, candidate_skills: list[str]) -> str | None:
    for candidate_skill in candidate_skills:
        if _acronym_match(jd_skill, candidate_skill):
            return candidate_skill
    return None


def exact_skill_score(
    jd_skills: list[str],
    candidate_skills: list[str],
) -> dict:
    jd_set = {skill.lower().strip() for skill in jd_skills if skill.strip()}
    candidate_set = {skill.lower().strip() for skill in candidate_skills if skill.strip()}

    if not jd_set:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
        }

    matched = jd_set.intersection(candidate_set)
    missing = jd_set - matched
    score = (len(matched) / len(jd_set)) * 100

    return {
        "score": round(score, 2),
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
    }


def semantic_skill_score(
    jd_skills: list[str],
    candidate_skills: list[str],
    threshold: float = SIMILARITY_THRESHOLD,
) -> dict:
    jd_skills = [skill.strip() for skill in jd_skills if skill.strip()]
    candidate_skills = [skill.strip() for skill in candidate_skills if skill.strip()]

    if not jd_skills:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": [],
            "skill_matches": [],
        }

    if not candidate_skills:
        return {
            "score": 0,
            "matched_skills": [],
            "missing_skills": jd_skills,
            "skill_matches": [],
        }

    candidate_lower = {skill.lower(): skill for skill in candidate_skills}
    model = _get_model()

    jd_normalized = [_normalize_for_embedding(skill) for skill in jd_skills]
    candidate_normalized = [_normalize_for_embedding(skill) for skill in candidate_skills]

    jd_embeddings = model.encode(jd_normalized, normalize_embeddings=True)
    candidate_embeddings = model.encode(candidate_normalized, normalize_embeddings=True)
    similarities = cosine_similarity(jd_embeddings, candidate_embeddings)

    matched_skills: list[str] = []
    missing_skills: list[str] = []
    skill_matches: list[dict] = []

    for i, jd_skill in enumerate(jd_skills):
        exact_match = candidate_lower.get(jd_skill.lower())
        if exact_match:
            matched_skills.append(jd_skill)
            skill_matches.append(
                {
                    "jd_skill": jd_skill,
                    "candidate_skill": exact_match,
                    "similarity": 1.0,
                    "match_type": "exact",
                }
            )
            continue

        acronym_match = _find_acronym_match(jd_skill, candidate_skills)
        if acronym_match:
            matched_skills.append(jd_skill)
            skill_matches.append(
                {
                    "jd_skill": jd_skill,
                    "candidate_skill": acronym_match,
                    "similarity": 1.0,
                    "match_type": "acronym",
                }
            )
            continue

        best_idx = int(np.argmax(similarities[i]))
        best_similarity = float(similarities[i][best_idx])

        if best_similarity >= threshold:
            matched_skills.append(jd_skill)
            skill_matches.append(
                {
                    "jd_skill": jd_skill,
                    "candidate_skill": candidate_skills[best_idx],
                    "similarity": round(best_similarity, 4),
                    "match_type": "semantic",
                }
            )
        else:
            missing_skills.append(jd_skill)

    score = (len(matched_skills) / len(jd_skills)) * 100

    return {
        "score": round(score, 2),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "skill_matches": skill_matches,
    }
