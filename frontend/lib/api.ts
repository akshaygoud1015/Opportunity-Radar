const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type JobPosting = {
  id: string;
  source: string;
  company: string;
  title: string;
  location: string | null;
  url: string;
  is_entry_level: boolean;
  visa_score: number;
  posted_at: string | null;
  created_at: string;
};

export type ScrapeRunResult = {
  scrape_run: {
    id: string;
    started_at: string;
    finished_at: string | null;
    status: string;
    sources: Record<string, number>;
    job_count: number;
  };
  jobs: JobPosting[];
};

export type SkillMatchResult = {
  matched_skills: string[];
  gap_skills: string[];
};

export type TailorResponse = {
  pdf_url: string;
  matched_skills: string[];
  gap_skills: string[];
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`Request to ${path} failed (${res.status}): ${body}`);
  }
  return res.json();
}

export const api = {
  runScrape: () => request<ScrapeRunResult>("/scrape/run", { method: "POST" }),

  listJobs: (params?: { scrape_run_id?: string; entry_level_only?: boolean; min_visa_score?: number }) => {
    const qs = new URLSearchParams();
    if (params?.scrape_run_id) qs.set("scrape_run_id", params.scrape_run_id);
    if (params?.entry_level_only) qs.set("entry_level_only", "true");
    if (params?.min_visa_score) qs.set("min_visa_score", String(params.min_visa_score));
    const suffix = qs.toString() ? `?${qs.toString()}` : "";
    return request<JobPosting[]>(`/jobs${suffix}`);
  },

  extractSkills: (jobId: string) =>
    request<SkillMatchResult>(`/skills/extract/${jobId}`, { method: "POST" }),

  tailorResume: (jobId: string, docType: "resume" | "cv") =>
    request<TailorResponse>("/resume/tailor", {
      method: "POST",
      body: JSON.stringify({ job_posting_id: jobId, doc_type: docType }),
    }),
};
