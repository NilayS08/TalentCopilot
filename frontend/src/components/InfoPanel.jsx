import { BsUpload, BsSearch, BsBarChart, BsCheckCircle, BsFileText, BsPeople } from "react-icons/bs";

export default function InfoPanel() {
  return (
    <div className="w-72 shrink-0 space-y-5">
      <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
        <h4 className="text-sm font-semibold text-gray-800 mb-4">Dashboard Overview</h4>
        <div className="space-y-4">
          {[
            { icon: BsUpload, label: "Upload JD", color: "text-blue-600 bg-blue-100" },
            { icon: BsPeople, label: "Upload Resumes", color: "text-purple-600 bg-purple-100" },
            { icon: BsBarChart, label: "Evaluate", color: "text-orange-600 bg-orange-100" },
            { icon: BsCheckCircle, label: "View Ranked Candidates", color: "text-green-600 bg-green-100" },
          ].map((step, i) => (
            <div key={step.label} className="flex items-center gap-3">
              <div className={`w-8 h-8 rounded-lg flex items-center justify-center text-sm ${step.color}`}>
                <step.icon />
              </div>
              <div>
                <p className="text-sm text-gray-700">{step.label}</p>
                {i < 3 && (
                  <div className="ml-0.5 mt-0.5">
                    <svg width="10" height="16" viewBox="0 0 10 16" fill="none" className="text-gray-300">
                      <path d="M5 0L5 16" stroke="currentColor" strokeWidth="2" strokeDasharray="2 2" />
                    </svg>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-5">
        <h4 className="text-sm font-semibold text-gray-800 mb-4">Match Score Guide</h4>
        <div className="space-y-3">
          {[
            { range: "85–100%", label: "Strong Match", dot: "bg-green-500", bg: "bg-green-100 text-green-800" },
            { range: "65–84%", label: "Potential Match", dot: "bg-yellow-500", bg: "bg-yellow-100 text-yellow-800" },
            { range: "0–64%", label: "Low Match", dot: "bg-red-500", bg: "bg-red-100 text-red-800" },
          ].map((g) => (
            <div key={g.label} className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                <span className={`w-2 h-2 rounded-full ${g.dot}`} />
                <span className="text-sm text-gray-600">{g.range}</span>
              </div>
              <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${g.bg}`}>{g.label}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
