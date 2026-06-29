import { BsEye } from "react-icons/bs";

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

const badgeClass = (score) => {
  if (score >= 85) return "bg-green-100 text-green-800";
  if (score >= 65) return "bg-yellow-100 text-yellow-800";
  return "bg-red-100 text-red-800";
};

const badgeLabel = (score) => {
  if (score >= 85) return "Strong Match";
  if (score >= 65) return "Potential Match";
  return "Low Match";
};

const dotColor = (score) => {
  if (score >= 85) return "bg-green-500";
  if (score >= 65) return "bg-yellow-500";
  return "bg-red-500";
};

export default function CandidateRanking({ candidates, onSelect }) {
  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-8">
      <h3 className="text-base font-semibold text-gray-800 mb-5">Top Candidates</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-500 border-b border-gray-100">
              <th className="pb-3 pr-4 font-medium">Rank</th>
              <th className="pb-3 pr-4 font-medium">Candidate Name</th>
              <th className="pb-3 pr-4 font-medium">Experience</th>
              <th className="pb-3 pr-4 font-medium">Match Score</th>
              <th className="pb-3 pr-4 font-medium">Status</th>
              <th className="pb-3 pr-4 font-medium">Action</th>
            </tr>
          </thead>
          <tbody>
            {candidates.map((c) => {
              const expYears = totalExperienceYears(c.candidate.experience);
              return (
                <tr key={c.rank} className="border-b border-gray-50 hover:bg-gray-50/50 transition-colors">
                  <td className="py-3.5 pr-4 text-gray-400 font-medium">{c.rank}</td>
                  <td className="py-3.5 pr-4 font-medium text-gray-800">{c.candidate.name}</td>
                  <td className="py-3.5 pr-4 text-gray-600">{expYears} Year{expYears !== 1 ? "s" : ""}</td>
                  <td className="py-3.5 pr-4 font-semibold text-gray-800">{Math.round(c.overall_score)}%</td>
                  <td className="py-3.5 pr-4">
                    <span className={`inline-flex items-center gap-1.5 text-xs font-medium px-3 py-1 rounded-full ${badgeClass(c.overall_score)}`}>
                      <span className={`w-1.5 h-1.5 rounded-full ${dotColor(c.overall_score)}`} />
                      {badgeLabel(c.overall_score)}
                    </span>
                  </td>
                  <td className="py-3.5">
                    <button
                      onClick={() => onSelect(c)}
                      className="inline-flex items-center gap-1.5 text-blue-600 hover:text-blue-800 text-xs font-medium transition-colors"
                    >
                      <BsEye /> View Details
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
