"use client";

import { useEffect, useState } from "react";
import { api, JobPosting } from "@/lib/api";

export default function TailorModal({
  job,
  onClose,
}: {
  job: JobPosting;
  onClose: () => void;
}) {
  const [stage, setStage] = useState<"extracting" | "ready" | "generating" | "done" | "error">(
    "extracting"
  );
  const [matched, setMatched] = useState<string[]>([]);
  const [gaps, setGaps] = useState<string[]>([]);
  const [pdfUrl, setPdfUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .extractSkills(job.id)
      .then((res) => {
        setMatched(res.matched_skills);
        setGaps(res.gap_skills);
        setStage("ready");
      })
      .catch((err) => {
        setError(err instanceof Error ? err.message : "Skill extraction failed");
        setStage("error");
      });
  }, [job.id]);

  async function handleGenerate(docType: "resume" | "cv") {
    setStage("generating");
    try {
      const res = await api.tailorResume(job.id, docType);
      setPdfUrl(res.pdf_url);
      setStage("done");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Generation failed");
      setStage("error");
    }
  }

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-lg w-full p-6 space-y-4">
        <div className="flex justify-between items-start">
          <div>
            <h2 className="text-lg font-medium">{job.title}</h2>
            <p className="text-sm text-gray-500">{job.company}</p>
          </div>
          <button onClick={onClose} className="text-gray-400 hover:text-gray-600">
            ✕
          </button>
        </div>

        {stage === "extracting" && <p className="text-sm text-gray-600">Reading job description...</p>}

        {(stage === "ready" || stage === "generating" || stage === "done") && (
          <>
            <div>
              <p className="text-sm font-medium mb-1">Your skills this job wants</p>
              <div className="flex flex-wrap gap-1.5">
                {matched.map((s) => (
                  <span key={s} className="text-xs bg-green-50 text-green-800 px-2 py-1 rounded">
                    {s}
                  </span>
                ))}
              </div>
            </div>

            {gaps.length > 0 && (
              <div>
                <p className="text-sm font-medium mb-1">Skills this job wants that you don&apos;t have yet</p>
                <div className="flex flex-wrap gap-1.5">
                  {gaps.map((s) => (
                    <span key={s} className="text-xs bg-amber-50 text-amber-800 px-2 py-1 rounded">
                      {s}
                    </span>
                  ))}
                </div>
                <p className="text-xs text-gray-400 mt-1">
                  These are never added to your resume automatically -- worth learning if you see them often.
                </p>
              </div>
            )}

            <div className="flex gap-2 pt-2">
              <button
                onClick={() => handleGenerate("resume")}
                disabled={stage === "generating"}
                className="bg-navy text-white text-sm px-3 py-2 rounded-md disabled:opacity-50"
              >
                Generate resume
              </button>
              <button
                onClick={() => handleGenerate("cv")}
                disabled={stage === "generating"}
                className="border border-navy text-navy text-sm px-3 py-2 rounded-md disabled:opacity-50"
              >
                Generate CV
              </button>
            </div>
          </>
        )}

        {stage === "done" && pdfUrl && (
          <a
            href={pdfUrl}
            target="_blank"
            rel="noreferrer"
            className="block text-sm text-blue-700 underline"
          >
            Download PDF
          </a>
        )}

        {stage === "error" && <p className="text-sm text-red-600">{error}</p>}
      </div>
    </div>
  );
}
