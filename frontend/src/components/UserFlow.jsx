import { BsUpload, BsPeople, BsBarChart, BsCheckCircle, BsStars } from "react-icons/bs";

const steps = [
  { icon: BsUpload, label: "Upload JD" },
  { icon: BsPeople, label: "Upload Resumes" },
  { icon: BsBarChart, label: "Evaluate" },
  { icon: BsCheckCircle, label: "View Results" },
  { icon: BsStars, label: "Hire Best Candidate" },
];

export default function UserFlow() {
  return (
    <div className="bg-white rounded-2xl border border-gray-200 shadow-sm p-6 mb-8">
      <h3 className="text-base font-semibold text-gray-800 mb-6">User Flow</h3>
      <div className="flex items-center justify-center gap-0 flex-wrap">
        {steps.map((step, i) => (
          <div key={step.label} className="flex items-center">
            <div className="flex flex-col items-center gap-2.5">
              <div className="w-12 h-12 rounded-xl bg-blue-50 border border-blue-200 flex items-center justify-center text-blue-600">
                <step.icon className="text-lg" />
              </div>
              <span className="text-xs font-medium text-gray-600 text-center leading-tight max-w-20">{step.label}</span>
            </div>
            {i < steps.length - 1 && (
              <div className="flex items-center mx-3 mt-[-28px]">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" className="text-gray-300">
                  <path d="M9 18L15 12L9 6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
