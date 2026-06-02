import { api } from "./client";

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
  { intervalMs = 2000, maxPolls = 150 }: PollJobOptions = {},
): Promise<Job> {
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
