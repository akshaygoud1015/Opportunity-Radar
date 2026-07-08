"use client";

import { useEffect, useState } from "react";
import { api, JobPosting, ScrapeRunResult } from "@/lib/api";
import ScrapeButton from "@/components/ScrapeButton";
import JobTable from "@/components/JobTable";

export default function Home() {
  const [jobs, setJobs] = useState<JobPosting[]>([]);
  const [lastRun, setLastRun] = useState<ScrapeRunResult["scrape_run"] | null>(null);
  const [loadingInitial, setLoadingInitial] = useState(true);

  useEffect(() => {
    api
      .listJobs()
      .then(setJobs)
      .catch(() => {
        /* backend may not be up yet on first load -- surfaced via empty table */
      })
      .finally(() => setLoadingInitial(false));
  }, []);

  function handleScrapeComplete(result: ScrapeRunResult) {
    setLastRun(result.scrape_run);
    setJobs(result.jobs);
  }

  return (
    <main className="max-w-5xl mx-auto px-6 py-10 space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-medium text-navy">OpportunityRadar</h1>
          <p className="text-sm text-gray-500">
            Entry-level, visa-friendly listings -- pulled when you ask, not on a schedule.
          </p>
        </div>
        <ScrapeButton onComplete={handleScrapeComplete} />
      </div>

      {lastRun && (
        <div className="text-sm text-gray-600 bg-white border rounded-md px-4 py-2">
          Last run pulled {lastRun.job_count} new listings ({Object.entries(lastRun.sources)
            .map(([src, count]) => `${src}: ${count}`)
            .join(", ")})
        </div>
      )}

      {loadingInitial ? (
        <p className="text-sm text-gray-500">Loading...</p>
      ) : (
        <JobTable jobs={jobs} />
      )}
    </main>
  );
}
