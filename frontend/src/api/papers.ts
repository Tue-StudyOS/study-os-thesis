import { api } from "./client";
import {
  PAPER_LIST_MAX_LIMIT,
  PAPER_LIST_MIN_LIMIT,
  PAPER_LIST_MIN_OFFSET,
  SCRAPE_MAX_RESULTS_MAX,
  SCRAPE_MAX_RESULTS_MIN,
  SCRAPE_SINCE_DAYS_MAX,
  SCRAPE_SINCE_DAYS_MIN,
} from "./constants";
import { waitForJobTree } from "./jobEvents";
import type { Job } from "./jobs";
import { appendIntegerParam, assertInteger, setIntegerBodyField } from "./numeric";

export interface Paper {
  id: number;
  title: string;
  abstract: string | null;
  summary: string | null;
  authors: string[];
  publication_date: string | null;
  source: string;
  source_url: string;
  doi: string | null;
  recency_score: number;
  relevance_score: number;
  enriched_at: string | null;
  created_at: string;
  tags: string[];
}

export interface PaginatedPapers {
  items: Paper[];
  total: number;
  limit: number;
  offset: number;
}

export function listPapers(params: {
  chair_id?: number;
  tag?: string;
  limit?: number;
  offset?: number;
}): Promise<PaginatedPapers> {
  const q = new URLSearchParams();
  appendIntegerParam(q, "chair_id", params.chair_id, { min: 1 });
  if (params.tag) q.set("tag", params.tag);
  appendIntegerParam(q, "limit", params.limit, { min: PAPER_LIST_MIN_LIMIT, max: PAPER_LIST_MAX_LIMIT });
  appendIntegerParam(q, "offset", params.offset, { min: PAPER_LIST_MIN_OFFSET });
  return api<PaginatedPapers>(`/api/papers?${q}`);
}

export async function triggerScrape(
  chairId: number,
  opts: { since_days?: number; max_results?: number } = {},
): Promise<Job> {
  assertInteger("chairId", chairId, { min: 1 });
  const body: { since_days?: number; max_results?: number } = {};
  setIntegerBodyField(body, "since_days", opts.since_days, { min: SCRAPE_SINCE_DAYS_MIN, max: SCRAPE_SINCE_DAYS_MAX });
  setIntegerBodyField(body, "max_results", opts.max_results, { min: SCRAPE_MAX_RESULTS_MIN, max: SCRAPE_MAX_RESULTS_MAX });

  const { job_id } = await api<{ job_id: string }>(`/api/scraper/run/${chairId}`, {
    method: "POST",
    json: body,
  });
  return waitForJobTree(job_id);
}
