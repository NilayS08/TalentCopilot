import { BsRobot, BsGrid, BsPeople, BsFileText, BsBarChart, BsGear } from "react-icons/bs";
import { HiOutlineCreditCard } from "react-icons/hi";

const navItems = [
  { label: "Dashboard", icon: BsGrid, active: true },
  { label: "Candidates", icon: BsPeople, active: false },
  { label: "Job Descriptions", icon: BsFileText, active: false },
  { label: "Evaluations", icon: BsBarChart, active: false },
  { label: "Settings", icon: BsGear, active: false },
];

const progress = 1250 / 2000;

export default function Sidebar() {
  return (
    <aside className="w-[18vw] min-w-[220px] h-screen bg-[#0F172A] flex flex-col text-white shrink-0">
      <div className="flex items-center gap-2.5 px-6 pt-7 pb-9">
        <BsRobot className="text-2xl text-blue-400" />
        <span className="text-lg font-semibold tracking-tight">Nexalogic ATS</span>
      </div>

      <nav className="flex flex-col gap-1 px-3 flex-1">
        {navItems.map((item) => (
          <a
            key={item.label}
            href="#"
            className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
              item.active
                ? "bg-blue-600 text-white"
                : "text-gray-400 hover:text-white hover:bg-white/5"
            }`}
          >
            <item.icon className="text-lg" />
            {item.label}
          </a>
        ))}
      </nav>

      <div className="px-5 pb-4">
        <div className="bg-white/5 rounded-xl p-4 mb-3">
          <div className="flex items-center gap-2 text-xs text-gray-400 mb-2.5">
            <HiOutlineCreditCard className="text-sm" />
            <span>AI Credits</span>
          </div>
          <div className="flex items-baseline gap-1 mb-2">
            <span className="text-lg font-semibold">1250</span>
            <span className="text-xs text-gray-400">/ 2000</span>
          </div>
          <div className="h-1.5 bg-white/10 rounded-full overflow-hidden">
            <div
              className="h-full bg-blue-500 rounded-full transition-all"
              style={{ width: `${progress * 100}%` }}
            />
          </div>
        </div>

        <div className="flex items-center gap-3 pt-2 border-t border-white/10">
          <div className="w-9 h-9 rounded-full bg-gray-600 flex items-center justify-center text-xs font-medium text-white">
            JD
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-medium truncate">Jane Doe</p>
            <p className="text-xs text-gray-400 truncate">jane@nexalogic.com</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
