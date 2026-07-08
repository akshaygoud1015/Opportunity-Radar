"use client";

import { useState } from "react";
import { JobPosting } from "@/lib/api";
import TailorModal from "@/components/TailorModal";

function VisaBadge({ score }: { score: number }) {
  const label = score >= 0.6 ? "Likely" : score >= 0.3 ? "Possible" : "Unclear";
  const color =
    score >= 0.6
      ? "bg-green-50 text-green-800"
      : score >= 0.3
      ? "bg-amber-50 text-amber-800"
      : "bg-gray-100 text-gray-600";
  return <span className={`text-xs px-2 py-1 rounded ${color}`}>{label}</span>;
}

export default function JobTable({ jobs }: { jobs: JobPosting[] }) {
  const [selected, setSelected] = useState<JobPosting | null>(null);

  if (jobs.length === 0) {
    return <p className="text-sm text-gray-500 py-8 text-center">No listings yet -- run a scrape to get started.</p>;
  }

  return (
    <>
      <div className="overflow-x-auto border rounded-lg">
        <table className="w-full text-sm">
          <thead className="bg-gray-100 text-left text-gray-600">
            <tr>
              <th className="px-4 py-2 font-medium">Title</th>
              <th className="px-4 py-2 font-medium">Company</th>
              <th className="px-4 py-2 font-medium">Location</th>
              <th className="px-4 py-2 font-medium">Entry level</th>
              <th className="px-4 py-2 font-medium">Sponsorship</th>
              <th className="px-4 py-2 font-medium"></th>
            </tr>
          </thead>
          <tbody className="divide-y">
            {jobs.map((job) => (
              <tr key={job.id} className="hover:bg-gray-50">
                <td className="px-4 py-2">
                  <a href={job.url} target="_blank" rel="noreferrer" className="text-blue-700 hover:underline">
                    {job.title}
                  </a>
                </td>
                <td className="px-4 py-2">{job.company}</td>
                <td className="px-4 py-2 text-gray-500">{job.location || "--"}</td>
                <td className="px-4 py-2">{job.is_entry_level ? "Yes" : "--"}</td>
                <td className="px-4 py-2">
                  <VisaBadge score={job.visa_score} />
                </td>
                <td className="px-4 py-2">
                  <button
                    onClick={() => setSelected(job)}
                    className="text-navy text-xs font-medium border border-navy px-2 py-1 rounded hover:bg-navy hover:text-white transition"
                  >
                    Tailor resume
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {selected && <TailorModal job={selected} onClose={() => setSelected(null)} />}
    </>
  );
}
