# Frontend Setup — Recruiter Dashboard

## Prerequisites

- Node.js 18+ and npm
- Backend running at `http://localhost:8000`

## Step 1: Create React App with Vite

```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install
```

## Step 2: Install Dependencies

```bash
npm install tailwindcss @tailwindcss/vite
```

## Step 3: Configure Tailwind

Open `frontend/vite.config.js` and add Tailwind:

```js
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

Replace `frontend/src/index.css` with:

```css
@import "tailwindcss";
```

## Step 4: Configure API Proxy

Open `frontend/vite.config.js` and add the proxy under `defineConfig`:

```js
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
```

## Step 5: Verify Setup

```bash
cd frontend
npm run dev
```

Visit `http://localhost:5173`. You should see the default Vite + React page.

## Project Structure (After Building)

```
frontend/
  src/
    App.jsx          — main layout with tabs/steps
    App.css
    main.jsx         — entry point
    index.css        — tailwind import
    components/
      JDUpload.jsx       — JD PDF upload + extract requirements
      ResumeUpload.jsx   — multiple resume upload + extract profiles
      RankingTable.jsx   — ranked candidate list
      CandidateCard.jsx  — expandable candidate details
      InsightPanel.jsx   — LLM recruiter insight per candidate
  vite.config.js
  package.json
```

## Backend API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/jd/upload` | Upload JD PDF, returns text |
| POST | `/jd/extract-requirements` | Upload JD PDF, returns structured JDRequirements |
| POST | `/resume/upload` | Upload resume PDF, returns text |
| POST | `/resume/extract-profile` | Upload resume PDF, returns CandidateProfile |
| POST | `/evaluation/evaluate` | Single candidate evaluation |
| POST | `/evaluation/rank` | Rank multiple candidates |
| POST | `/evaluation/insight` | LLM insight for a candidate |

## Running Locally

Terminal 1 — Backend:
```bash
cd TalentCopilot
./venv/bin/uvicorn app.main:app --reload
```

Terminal 2 — Frontend:
```bash
cd frontend
npm run dev
```
