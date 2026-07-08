"use client";

import { useState } from "react";
import { api, ScrapeRunResult } from "@/lib/api";

export default function ScrapeButton({
  onComplete,
}: {
  onComplete: (result: ScrapeRunResult) => void;
}) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleClick() {
    setLoading(true);
    setError(null);
    try {
      const result = await api.runScrape();
      onComplete(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Scrape failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex items-center gap-3">
      <button
        onClick={handleClick}
        disabled={loading}
        className="bg-navy text-white px-4 py-2 rounded-md text-sm font-medium disabled:opacity-50 hover:opacity-90 transition"
      >
        {loading ? "Scraping..." : "Run scrape"}
      </button>
      {error && <span className="text-sm text-red-600">{error}</span>}
    </div>
  );
}
