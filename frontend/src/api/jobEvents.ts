import { getToken } from "./client";
import { getJob, type Job, type JobStatus } from "./jobs";

export type JobEvent = {
  type: string;
  job_id: string;
  status: JobStatus;
  data?: Record<string, unknown>;
  error?: string;
  timestamp?: string;
};

type DispatchedJob = {
  job_id: string;
};

type WaitForJobTreeOptions = {
  parentFallbackMs?: number;
  childFallbackMs?: number;
  timeoutMs?: number;
};

const TERMINAL = new Set<JobStatus>(["success", "failure"]);

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function isTerminal(status: JobStatus): boolean {
  return TERMINAL.has(status);
}

function dispatchedJobsFromData(data: Record<string, unknown> | null | undefined): DispatchedJob[] {
  const dispatched = data?.dispatched;
  if (!Array.isArray(dispatched)) return [];
  return dispatched.filter(
    (item): item is DispatchedJob =>
      typeof item === "object" &&
      item !== null &&
      "job_id" in item &&
      typeof item.job_id === "string",
  );
}

function wsUrl(token: string): string {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}/api/ws?token=${encodeURIComponent(token)}`;
}

function openJobSocket(onEvent: (event: JobEvent) => void): WebSocket | null {
  const token = getToken();
  if (!token) return null;

  const socket = new WebSocket(wsUrl(token));
  socket.onmessage = (message) => {
    try {
      const event = JSON.parse(message.data) as JobEvent;
      if (typeof event.job_id === "string" && typeof event.status === "string") {
        onEvent(event);
      }
    } catch {
      // Ignore malformed socket messages; REST fallback will recover state.
    }
  };
  return socket;
}

async function waitForTerminalJob(
  jobId: string,
  fallbackMs: number,
  deadline: number,
  events: Map<string, JobEvent>,
): Promise<Job> {
  let lastJob: Job | null = null;

  while (Date.now() < deadline) {
    const event = events.get(jobId);
    if (event && isTerminal(event.status)) {
      const job = await getJob(jobId);
      return job.status === event.status ? job : { ...job, status: event.status, error: event.error ?? job.error };
    }

    lastJob = await getJob(jobId);
    if (isTerminal(lastJob.status)) return lastJob;

    await sleep(fallbackMs);
  }

  return lastJob ?? getJob(jobId);
}

export async function waitForJobTree(
  parentJobId: string,
  {
    parentFallbackMs = 5000,
    childFallbackMs = 10000,
    timeoutMs = 10 * 60 * 1000,
  }: WaitForJobTreeOptions = {},
): Promise<Job> {
  const events = new Map<string, JobEvent>();
  const socket = openJobSocket((event) => events.set(event.job_id, event));
  const deadline = Date.now() + timeoutMs;

  try {
    const parent = await waitForTerminalJob(parentJobId, parentFallbackMs, deadline, events);
    if (parent.status !== "success") return parent;

    const parentEvent = events.get(parentJobId);
    const childJobs = [
      ...dispatchedJobsFromData(parent.result_data),
      ...dispatchedJobsFromData(parentEvent?.data),
    ];
    const childIds = [...new Set(childJobs.map((job) => job.job_id))];
    if (childIds.length === 0) return parent;

    const children = await Promise.all(
      childIds.map((jobId) => waitForTerminalJob(jobId, childFallbackMs, deadline, events)),
    );
    const failedChild = children.find((job) => job.status === "failure");
    return failedChild ?? parent;
  } finally {
    socket?.close();
  }
}
