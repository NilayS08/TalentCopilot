import { useState, useCallback } from "react";
import Sidebar from "./components/Sidebar";
import UploadSection from "./components/UploadSection";
import CandidateRanking from "./components/CandidateRanking";
import CandidateDetails from "./components/CandidateDetails";
import InfoPanel from "./components/InfoPanel";
import UserFlow from "./components/UserFlow";
import { uploadJD, uploadResume, rankCandidates, generateInsight } from "./api";

export default function App() {
  const [jd, setJd] = useState(null);
  const [candidates, setCandidates] = useState([]);
  const [jdFiles, setJdFiles] = useState(0);
  const [resumeCount, setResumeCount] = useState(0);
  const [ranked, setRanked] = useState([]);
  const [evaluating, setEvaluating] = useState(false);
  const [error, setError] = useState(null);
  const [selectedRanked, setSelectedRanked] = useState(null);
  const [selectedInsight, setSelectedInsight] = useState(null);

  const handleJDUpload = useCallback(async (file) => {
    setError(null);
    const result = await uploadJD(file);
    setJd(result);
    setJdFiles((c) => c + 1);
  }, []);

  const handleResumeUpload = useCallback(async (files) => {
    setError(null);
    const profiles = await Promise.all(files.map((f) => uploadResume(f)));
    setCandidates((prev) => [...prev, ...profiles]);
    setResumeCount((c) => c + files.length);
  }, []);

  const handleEvaluate = useCallback(async () => {
    if (!jd || candidates.length === 0) return;
    setEvaluating(true);
    setError(null);
    setRanked([]);
    setSelectedRanked(null);
    setSelectedInsight(null);
    try {
      const result = await rankCandidates(jd, candidates);
      setRanked(result);
    } catch (e) {
      setError(e.message || "Evaluation failed");
    } finally {
      setEvaluating(false);
    }
  }, [jd, candidates]);

  const handleViewDetails = useCallback(async (rankedCandidate) => {
    setSelectedRanked(rankedCandidate);
    setSelectedInsight(null);
    try {
      const result = await generateInsight(
        jd,
        rankedCandidate.candidate,
        rankedCandidate.evaluation,
      );
      setSelectedInsight(result.summary);
    } catch (e) {
      setSelectedInsight("Unable to generate insight at this time.");
    }
  }, [jd]);

  const showResults = ranked.length > 0;

  return (
    <div className="flex h-screen bg-[#F8FAFC]">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <div className="flex">
          <div className="flex-1 p-8 pb-0">
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-sm text-gray-500 mt-1 mb-8">
              Upload a Job Description and candidate resumes to find the best matching candidates.
            </p>

            <UploadSection
              onJDUpload={handleJDUpload}
              onResumeUpload={handleResumeUpload}
              onEvaluate={handleEvaluate}
              jdUploaded={jdFiles > 0}
              resumeCount={resumeCount}
              evaluating={evaluating}
            />

            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl text-sm text-red-700">
                {error}
              </div>
            )}

            {evaluating && (
              <div className="flex items-center justify-center py-12 text-gray-500 text-sm">
                <svg className="animate-spin h-5 w-5 mr-3 text-blue-600" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
                Evaluating candidates...
              </div>
            )}

            {showResults && (
              <>
                <CandidateRanking candidates={ranked} onSelect={handleViewDetails} />
                {selectedRanked && (
                  <CandidateDetails
                    rankedCandidate={selectedRanked}
                    insight={selectedInsight}
                    onClose={() => { setSelectedRanked(null); setSelectedInsight(null); }}
                  />
                )}
                <UserFlow />
              </>
            )}
          </div>
          {showResults && (
            <div className="pt-8 pr-8 pb-8">
              <InfoPanel />
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
