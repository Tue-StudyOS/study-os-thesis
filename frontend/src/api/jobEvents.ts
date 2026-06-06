import { getToken } from "./client";
import {
  JOB_TREE_CHILD_POLL_INTERVAL_MS,
  JOB_TREE_PARENT_POLL_INTERVAL_MS,
  JOB_TREE_TIMEOUT_MS,
} from "./constants";
import { getJob, type Job, type JobStatus } from "./jobs";
import { assertInteger } from "./numeric";

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
  parentPollIntervalMs?: number;
  childPollIntervalMs?: number;
  timeoutMs?: number;
};

const TERMINAL = new Set<JobStatus>(["success", "failure"]);
const JOB_STATUSES = new Set<JobStatus>(["pending", "started", "success", "failure", "retry"]);

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

function optionalString(value: unknown): string | undefined {
  return typeof value === "string" ? value : undefined;
}

function optionalRecord(value: unknown): Record<string, unknown> | undefined {
  return typeof value === "object" && value !== null && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : undefined;
}

export function parseJobEventMessage(data: string): JobEvent {
  const event = JSON.parse(data) as unknown;
  if (typeof event !== "object" || event === null) {
    throw new Error("Malformed job event");
  }

  const candidate = event as Partial<JobEvent>;
  if (typeof candidate.job_id !== "string" || !JOB_STATUSES.has(candidate.status as JobStatus)) {
    throw new Error("Malformed job event");
  }

  const parsed: JobEvent = {
    type: typeof candidate.type === "string" ? candidate.type : "job_status",
    job_id: candidate.job_id,
    status: candidate.status as JobStatus,
  };
  const dataRecord = optionalRecord(candidate.data);
  const error = optionalString(candidate.error);
  const timestamp = optionalString(candidate.timestamp);
  if (dataRecord !== undefined) parsed.data = dataRecord;
  if (error !== undefined) parsed.error = error;
  if (timestamp !== undefined) parsed.timestamp = timestamp;
  return parsed;
}

function wsUrl(token: string): string {
  const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
  return `${protocol}//${window.location.host}/api/ws?token=${encodeURIComponent(token)}`;
}

function openJobSocket(onEvent: (event: JobEvent) => void, onError: (error: Error) => void): WebSocket | null {
  const token = getToken();
  if (!token) return null;

  const socket = new WebSocket(wsUrl(token));
  socket.onmessage = (message) => {
    try {
      onEvent(parseJobEventMessage(message.data));
    } catch (error) {
      onError(error instanceof Error ? error : new Error("Malformed job event"));
      socket.close();
    }
  };
  return socket;
}

async function waitForTerminalJob(
  jobId: string,
  pollIntervalMs: number,
  deadline: number,
  events: Map<string, JobEvent>,
  getSocketError: () => Error | null,
): Promise<Job> {
  let lastJob: Job | null = null;

  while (Date.now() < deadline) {
    const socketError = getSocketError();
    if (socketError !== null) throw socketError;

    const event = events.get(jobId);
    if (event && isTerminal(event.status)) {
      const job = await getJob(jobId);
      return job.status === event.status ? job : { ...job, status: event.status, error: event.error ?? job.error };
    }

    lastJob = await getJob(jobId);
    if (isTerminal(lastJob.status)) return lastJob;

    await sleep(pollIntervalMs);
  }

  return lastJob ?? getJob(jobId);
}

export async function waitForJobTree(
  parentJobId: string,
  {
    parentPollIntervalMs = JOB_TREE_PARENT_POLL_INTERVAL_MS,
    childPollIntervalMs = JOB_TREE_CHILD_POLL_INTERVAL_MS,
    timeoutMs = JOB_TREE_TIMEOUT_MS,
  }: WaitForJobTreeOptions = {},
): Promise<Job> {
  assertInteger("parentPollIntervalMs", parentPollIntervalMs, { min: 1 });
  assertInteger("childPollIntervalMs", childPollIntervalMs, { min: 1 });
  assertInteger("timeoutMs", timeoutMs, { min: 1 });
  const events = new Map<string, JobEvent>();
  let socketError: Error | null = null;
  const socket = openJobSocket(
    (event) => events.set(event.job_id, event),
    (error) => {
      socketError = error;
    },
  );
  const deadline = Date.now() + timeoutMs;

  try {
    const parent = await waitForTerminalJob(parentJobId, parentPollIntervalMs, deadline, events, () => socketError);
    if (parent.status !== "success") return parent;

    const parentEvent = events.get(parentJobId);
    const childJobs = [
      ...dispatchedJobsFromData(parent.result_data),
      ...dispatchedJobsFromData(parentEvent?.data),
    ];
    const childIds = [...new Set(childJobs.map((job) => job.job_id))];
    if (childIds.length === 0) return parent;

    const children = await Promise.all(
      childIds.map((jobId) => waitForTerminalJob(jobId, childPollIntervalMs, deadline, events, () => socketError)),
    );
    const failedChild = children.find((job) => job.status === "failure");
    return failedChild ?? parent;
  } finally {
    socket?.close();
  }
}
