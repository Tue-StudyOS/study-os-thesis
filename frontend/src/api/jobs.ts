import { api } from "./client";
import {
  JOB_POLL_DEFAULT_INTERVAL_MS,
  JOB_POLL_DEFAULT_MAX_POLLS,
  JOB_POLL_MIN_INTERVAL_MS,
  JOB_POLL_MIN_MAX_POLLS,
} from "./constants";
import { assertInteger } from "./numeric";

export type JobStatus = "pending" | "started" | "success" | "failure" | "retry";

export interface Job {
  id: string;
  type: string;
  status: JobStatus;
  user_id: number;
  celery_task_id: string | null;
  input_data: Record<string, unknown> | null;
  result_data: Record<string, unknown> | null;
  error: string | null;
  attempts: number;
  created_at: string;
  started_at: string | null;
  completed_at: string | null;
}

export function getJob(jobId: string): Promise<Job> {
  return api<Job>(`/api/jobs/${jobId}`);
}

export function listJobs(params: {
  type?: string;
  status?: JobStatus;
} = {}): Promise<Job[]> {
  const q = new URLSearchParams();
  if (params.type) q.set("type", params.type);
  if (params.status) q.set("status", params.status);
  const suffix = q.toString() ? `?${q}` : "";
  return api<Job[]>(`/api/jobs${suffix}`);
}

export interface PollJobOptions {
  /** Delay between polls in milliseconds. */
  intervalMs?: number;
  /** Maximum number of polls before giving up. */
  maxPolls?: number;
}

/**
 * Poll a background job until it reaches a terminal state (`success` or
 * `failure`) or `maxPolls` is exhausted. Returns the last fetched job, so
 * callers should inspect `job.status` to distinguish completion from a timeout.
 *
 * Defaults (2s × 150 ≈ 5 min) mirror the worker's 300s soft time limit; local
 * LLMs can be slow, especially under memory pressure.
 */
export async function pollJob(
  jobId: string,
  { intervalMs = JOB_POLL_DEFAULT_INTERVAL_MS, maxPolls = JOB_POLL_DEFAULT_MAX_POLLS }: PollJobOptions = {},
): Promise<Job> {
  assertInteger("intervalMs", intervalMs, { min: JOB_POLL_MIN_INTERVAL_MS });
  assertInteger("maxPolls", maxPolls, { min: JOB_POLL_MIN_MAX_POLLS });
  let job = await getJob(jobId);
  for (
    let i = 0;
    i < maxPolls && job.status !== "success" && job.status !== "failure";
    i++
  ) {
    await new Promise((r) => setTimeout(r, intervalMs));
    job = await getJob(jobId);
  }
  return job;
}
