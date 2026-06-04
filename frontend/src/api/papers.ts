import { api } from "./client";
import { pollJob, type Job, type PollJobOptions } from "./jobs";

export interface Paper {
  id: number;
  title: string;
  abstract: string | null;
  summary: string | null;
  authors: string[];
  publication_date: string | null;
  source: string;
  source_url: string;
  arxiv_id: string | null;
  doi: string | null;
  recency_score: number;
  relevance_score: number;
  enriched_at: string | null;
  created_at: string;
  tags: string[];
}

export function listPapers(params: {
  chair_id?: number;
  tag?: string;
  limit?: number;
  offset?: number;
}): Promise<Paper[]> {
  const q = new URLSearchParams();
  if (params.chair_id !== undefined) q.set("chair_id", String(params.chair_id));
  if (params.tag) q.set("tag", params.tag);
  if (params.limit !== undefined) q.set("limit", String(params.limit));
  if (params.offset !== undefined) q.set("offset", String(params.offset));
  return api<Paper[]>(`/api/papers?${q}`);
}

interface DispatchedScrapeJob {
  job_id: string;
}

function dispatchedScrapeJobs(job: Job): DispatchedScrapeJob[] {
  const dispatched = job.result_data?.dispatched;
  if (!Array.isArray(dispatched)) return [];
  return dispatched.filter(
    (item): item is DispatchedScrapeJob =>
      typeof item === "object" &&
      item !== null &&
      "job_id" in item &&
      typeof item.job_id === "string",
  );
}

export async function triggerScrape(
  chairId: number,
  opts: { since_days?: number; max_results?: number } = {},
): Promise<Job> {
  const { job_id } = await api<{ job_id: string }>(`/api/scraper/run/${chairId}`, {
    method: "POST",
    json: { since_days: opts.since_days ?? 365, max_results: opts.max_results ?? 20 },
  });
  const pollOptions: PollJobOptions = { intervalMs: 2000, maxPolls: 300 };
  const parent = await pollJob(job_id, pollOptions);
  if (parent.status !== "success") return parent;

  const childJobs = dispatchedScrapeJobs(parent);
  if (childJobs.length === 0) return parent;

  const children = await Promise.all(childJobs.map((job) => pollJob(job.job_id, pollOptions)));
  const failedChild = children.find((job) => job.status === "failure");
  return failedChild ?? parent;
}
