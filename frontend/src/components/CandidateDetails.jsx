import { BsX, BsCheckCircle, BsXCircle, BsRobot } from "react-icons/bs";

function CircularProgress({ value }) {
  const r = 40;
  const circumference = 2 * Math.PI * r;
  const offset = circumference - (value / 100) * circumference;
  const color = value >= 85 ? "#22c55e" : value >= 65 ? "#eab308" : "#ef4444";

  return (
    <div className="relative w-[100px] h-[100px] flex items-center justify-center">
      <svg className="w-full h-full -rotate-90" viewBox="0 0 100 100">
        <circle cx="50" cy="50" r={r} fill="none" stroke="#e5e7eb" strokeWidth="8" />
        <circle cx="50" cy="50" r={r} fill="none" stroke={color} strokeWidth="8" strokeDasharray={circumference} strokeDashoffset={offset} strokeLinecap="round" />
      </svg>
      <span className="absolute text-xl font-bold text-gray-800">{Math.round(value)}%</span>
    </div>
  );
}

function totalExperienceYears(experience) {
  let total = 0;
  for (const exp of experience) {
    const y = exp.match(/(\d+)\s*(?:year|yr)s?/i);
    const m = exp.match(/(\d+)\s*(?:month|mo)s?/i);
    if (y) total += parseInt(y[1]);
    if (m) total += parseInt(m[1]) / 12;
  }
  return Math.round(total);
}

export default function CandidateDetails({ rankedCandidate, insight, onClose }) {
  if (!rankedCandidate) return null;

  const { candidate, evaluation } = rankedCandidate;
  const expYears = totalExperienceYears(candidate.experience);
  const initials = candidate.name.split(" ").map((n) => n[0]).join("");

  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-8">
      <div className="flex items-start justify-between mb-6">
        <div className="flex items-center gap-5">
          <div className="w-14 h-14 rounded-full bg-blue-100 flex items-center justify-center text-xl font-bold text-blue-700">
            {initials}
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-800">{candidate.name}</h3>
            <p className="text-sm text-gray-500">{expYears} Year{expYears !== 1 ? "s" : ""} of experience</p>
          </div>
        </div>
        <div className="flex items-center gap-6">
          <CircularProgress value={rankedCandidate.overall_score} />
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            <BsX className="text-xl" />
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div>
          <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Matched Skills</h4>
          <div className="flex flex-wrap gap-2">
            {evaluation.matched_skills.map((s) => (
              <span key={s} className="inline-flex items-center gap-1 text-xs font-medium px-3 py-1.5 rounded-full bg-green-100 text-green-800">
                <BsCheckCircle className="text-green-600" /> {s}
              </span>
            ))}
            {evaluation.matched_skills.length === 0 && (
              <p className="text-sm text-gray-400">None</p>
            )}
          </div>
        </div>

        <div>
          <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">Missing Skills</h4>
          <div className="flex flex-wrap gap-2">
            {evaluation.missing_skills.map((s) => (
              <span key={s} className="inline-flex items-center gap-1 text-xs font-medium px-3 py-1.5 rounded-full bg-red-100 text-red-800">
                <BsXCircle className="text-red-500" /> {s}
              </span>
            ))}
            {evaluation.missing_skills.length === 0 && (
              <p className="text-sm text-gray-400">None</p>
            )}
          </div>
        </div>

        <div>
          <h4 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-3">AI Recommendation</h4>
          {insight ? (
            <div className="bg-green-50 border border-green-200 rounded-xl p-4 flex items-start gap-2.5">
              <BsRobot className="text-green-600 text-lg mt-0.5 shrink-0" />
              <p className="text-sm text-green-900 leading-relaxed">{insight}</p>
            </div>
          ) : (
            <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 flex items-center justify-center">
              <p className="text-sm text-gray-400">Generating insight...</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
