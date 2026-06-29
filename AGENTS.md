# TalentCopilot – Project Context & Development Roadmap

> Reference document for AI agents and contributors working on this project.
> Read this before making changes to understand architecture, philosophy, and current progress.

---

## Project Overview

TalentCopilot is an AI-powered candidate screening platform designed to help recruiters quickly evaluate large numbers of resumes against a given Job Description (JD).

Unlike a traditional ATS that relies primarily on keyword matching, TalentCopilot combines structured information extraction, semantic matching, and LLM-generated recruiter insights.

**Primary design goals:**

- Support uploading **one or many resumes**
- Minimize LLM usage to reduce cost
- Produce explainable rankings
- Be modular and easy to extend
- Build a working MVP first, then progressively improve it

---

## Overall MVP Architecture

```
Upload JD
      ↓
Extract JD Text
      ↓
Extract JD Requirements (LLM)
      ↓
Upload Resume(s)
      ↓
Extract Resume Text
      ↓
Extract Candidate Profile (LLM)
      ↓
Skill Matching
      ↓
Candidate Ranking
      ↓
Top Candidates
      ↓
LLM Explanation Generation
```

---

## Guiding Principle

The project follows three development stages:

### Phase 1 — Make it Work

Focus only on getting every module functional.

- Do not optimize.
- Do not over-engineer.

### Phase 2 — Make it Better

- Improve extraction quality
- Improve prompts
- Improve schemas
- Improve scoring

### Phase 3 — Production Ready

- Optimize speed
- Improve robustness
- Handle edge cases
- Add authentication, persistence, deployment, etc.

---

## Modules Completed

### 1. Upload JD

**Status:** Implemented

**Functionality:**

- Upload JD PDF
- Save file locally
- Extract text using PyMuPDF

### 2. JD Requirement Extraction

**Status:** Implemented

**Uses:**

- Gemini
- Temperature = 0
- JSON response
- Pydantic validation

**Output:**

```json
{
    "role_title": "",
    "required_skills": [],
    "preferred_skills": [],
    "experience_required": ""
}
```

**Implemented improvements:**

- `response_mime_type="application/json"`
- JSON response cleaning
- Markdown stripping
- Regex JSON extraction

### 3. Resume Upload

**Status:** Implemented

- Resume PDF upload
- PDF text extraction

### 4. Resume Profile Extraction

**Status:** Implemented

**Uses Gemini to extract structured candidate information.**

**Output:**

```json
{
    "name": "",
    "skills": [],
    "projects": [],
    "experience": [],
    "education": []
}
```

**Experience format:**

Each entry uses `"Job title at Company(X years Y months):bullet summary"`. Duration is extracted in a deterministic format from dates or estimated if needed.

### 5. Exact Skill Matching

**Status:** Implemented

**Current functionality:**

- Lowercase normalization
- Set intersection
- Match percentage
- Missing skills
- Matched skills

**Current scoring:**

```
Exact Score = Matched Skills / Required Skills
```

### 6. Semantic Skill Matching

**Status:** Implemented

**Uses:**

- SentenceTransformers (`all-MiniLM-L6-v2`)
- Cosine similarity with threshold (default 0.6)
- Exact match fast path before embedding lookup

**Function:** `semantic_skill_score()` in `app/services/skill_matcher.py`

**Output:**

```json
{
    "score": 75.0,
    "matched_skills": ["Python", "FastAPI", "RAG"],
    "missing_skills": ["LangChain"],
    "skill_matches": [
        {
            "jd_skill": "RAG",
            "candidate_skill": "Retrieval-Augmented Generation",
            "similarity": 0.72,
            "match_type": "semantic"
        }
    ]
}
```

---

## Current Project Structure

```
TalentCopilot/

app/
    api/
        jd.py
        resume.py

    models/
        jd.py
        candidate.py
        evaluation.py

    services/
        pdf_parser.py
        jd_extractor.py
        resume_extractor.py
        skill_matcher.py
        candidate_evaluator.py
        candidate_ranker.py
        insight_generator.py

    main.py

data/
    jds/
    resumes/

requirement.txt
README.md
setup.md

frontend/
    src/
        App.jsx
        main.jsx
        index.css
        components/
            Sidebar.jsx
            UploadSection.jsx
            CandidateRanking.jsx
            CandidateDetails.jsx
            InfoPanel.jsx
            UserFlow.jsx
    vite.config.js
    package.json
```

---

## MVP Philosophy

For the MVP, **do NOT use the LLM for every candidate.**

The LLM should only be used for:

1. JD extraction
2. Resume extraction
3. Final explanation generation

Everything else should be **deterministic**.

---

## Remaining MVP Development Plan

### 7. Candidate Evaluation

**Status:** Implemented

**Function:** `evaluate_candidate()` in `app/services/candidate_evaluator.py`

**Input:**

- `JDRequirements`
- `CandidateProfile`

**Output (`CandidateEvaluation`):**

```json
{
    "skill_score": 82.0,
    "experience_score": 100.0,
    "matched_skills": [],
    "missing_skills": []
}
```

**Scoring:**

- **Skill score** — Uses semantic skill matching on `required_skills` vs candidate `skills`.
- **Experience score** — Parses duration (X years Y months) from each `experience` entry, sums total years, compares to `jd.experience_required`, capped at 100%.

**Helpers in `candidate_evaluator.py`:**
- `_parse_experience_years()` — extracts years/months from a single experience entry
- `_parse_required_experience()` — parses the first numeric value from `jd.experience_required`
- `_compute_experience_score()` — deterministic ratio-based scoring

Later this service will include:

- Project relevance score

### Phase 8 — Candidate Ranking

**Status:** Implemented

**Function:** `rank_candidates()` in `app/services/candidate_ranker.py`

Takes a `JDRequirements` and `list[CandidateProfile]`, evaluates each via `evaluate_candidate()`, computes an overall score (average of skill + experience), sorts descending, and returns `list[RankedCandidate]`.

**Output (`RankedCandidate`):**

```json
{
    "rank": 1,
    "candidate": { ... },
    "evaluation": {
        "skill_score": 90.0,
        "experience_score": 80.0,
        "matched_skills": [],
        "missing_skills": []
    },
    "overall_score": 85.0
}
```

**API:** `POST /evaluation/rank` — accepts `JDRequirements` + list of `CandidateProfile`s, returns ranked list.

### Phase 9 — LLM Recruiter Insights

**Status:** Implemented

**Function:** `generate_insight()` in `app/services/insight_generator.py`

Takes a `JDRequirements`, `CandidateProfile`, and `CandidateEvaluation`, and returns a concise 1-2 sentence recruiter insight via Gemini.

**Output (`RecruiterInsight`):**

```json
{
    "summary": "Strong Python and FastAPI skills align well with the Backend Engineer role. Has 5.5 years of relevant experience, recommend interview."
}
```

**Usage:** Only call for **Top K** candidates after ranking to keep LLM costs low.

**API:** `POST /evaluation/insight` — accepts `JDRequirements` + `CandidateProfile` + `CandidateEvaluation`, returns insight.

### Phase 10 — Recruiter Dashboard

**Status:** Implemented

Built with React + Vite + Tailwind CSS.

**Components:**
- `Sidebar.jsx` — Dark navy sidebar (logo, nav, AI credits, recruiter profile)
- `UploadSection.jsx` — Two drag-and-drop cards for JD and multiple resumes
- `CandidateRanking.jsx` — Ranked table with name, experience, match score, status badge, view button
- `CandidateDetails.jsx` — Expandable panel with circular progress, matched/missing skills, AI recommendation
- `InfoPanel.jsx` — Workflow overview and match score guide
- `UserFlow.jsx` — Visual 5-step flow at the bottom

**Design system:**
- Clean white background (#F8FAFC), dark sidebar (#0F172A), blue accent (#2563EB)
- Tailwind CSS, React Icons, rounded cards (16px), subtle shadows
- Responsive layout

---

## Future Improvements (After MVP)

These are intentionally postponed until the MVP is complete:

- Better Pydantic schemas
- Project relevance scoring
- Education scoring
- Embedding caching
- Hybrid scoring algorithm
- Resume chunking
- Vector database integration
- Persistent database
- Authentication
- Export reports
- Interview question generation
- Candidate comparison
- Recruiter chat assistant

---

## Core Design Principle

1. Every module should be **independently testable**.
2. Each module should produce **structured output** that becomes the input for the next module.
3. The project should **always remain functional** after completing each phase.
4. Avoid unnecessary optimization until the entire MVP pipeline is complete.

---

## Agent Instructions

When working on this project:

- **Stay in Phase 1** until the full MVP pipeline (Phases 6–10) is complete. Do not prematurely optimize or add production features.
- **Preserve modularity.** New logic belongs in `app/services/`. API routes in `app/api/` should stay thin.
- **Minimize LLM calls.** Only use Gemini for JD extraction, resume extraction, and top-K recruiter insights.
- **Use deterministic scoring** for matching, evaluation, and ranking.
- **Match existing conventions:** FastAPI, Pydantic models in `app/models/`, Gemini with temperature 0 and JSON output for extraction.
- **Keep changes scoped.** Complete one phase at a time; ensure the pipeline still works after each change.
- **Do not over-engineer schemas or scoring** until Phase 2 unless required for the current MVP phase.
