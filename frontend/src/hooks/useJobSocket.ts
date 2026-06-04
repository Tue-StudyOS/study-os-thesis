/**
 * useJobSocket
 *
 * Opens a single authenticated WebSocket (WS /api/ws?token=<JWT>) for the
 * lifetime of the component. Exposes `waitForJob(jobId)` which returns a
 * Promise that resolves as soon as the server pushes a terminal event
 * (success or failure) for that job.
 *
 * Strategy: register the resolver immediately, then race the WS event against
 * a delayed REST-poll fallback. Whichever finishes first wins; the other is
 * cancelled. This means:
 *   - If the WS is already open: resolves instantly on the server push, zero polls.
 *   - If the WS is still connecting: resolves the moment it delivers the event.
 *   - If the WS never connects: polling starts after FALLBACK_DELAY_MS and
 *     runs at FALLBACK_POLL_MS intervals.
 */

import { useEffect, useRef } from "react";
import { getToken } from "../api/client";
import { getJob, type Job } from "../api/jobs";

interface JobEvent {
  type: string;
  job_id: string;
  user_id: number;
  status: "started" | "success" | "failure" | "retry";
  data: Record<string, unknown>;
  timestamp: string;
}

type JobResolver = (job: Job) => void;

// How long to wait before starting the REST-poll fallback.
// Long enough that a healthy WS has time to connect and deliver; short enough
// that the user isn't left waiting if the WS silently fails.
const FALLBACK_DELAY_MS = 3000;
// Fallback poll cadence and max attempts (5 s × 360 = 30 min).
const FALLBACK_POLL_MS = 5000;
const FALLBACK_MAX_POLLS = 360;

function buildWsUrl(): string | null {
  const token = getToken();
  if (!token) return null;
  const proto = window.location.protocol === "https:" ? "wss" : "ws";
  return `${proto}://${window.location.host}/api/ws?token=${encodeURIComponent(token)}`;
}

function eventToJob(event: JobEvent): Job {
  return {
    id: event.job_id,
    type: event.type,
    status: event.status === "success" ? "success" : "failure",
    user_id: event.user_id,
    celery_task_id: null,
    input_data: null,
    result_data: event.data as Job["result_data"],
    error: event.status === "failure"
      ? ((event.data?.error as string) ?? "Unknown error")
      : null,
    attempts: 0,
    created_at: event.timestamp,
    started_at: null,
    completed_at: event.timestamp,
  };
}

export function useJobSocket() {
  // job_id → resolver waiting for a terminal WS event
  const pendingRef = useRef<Map<string, JobResolver>>(new Map());
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    const url = buildWsUrl();
    if (!url || !("WebSocket" in window)) return;

    let destroyed = false;
    let ws: WebSocket;
    try {
      ws = new WebSocket(url);
    } catch {
      return;
    }
    wsRef.current = ws;

    ws.onopen = () => {
      if (destroyed) { ws.close(); return; }
    };

    ws.onmessage = (ev) => {
      if (destroyed) return;
      let event: JobEvent;
      try {
        event = JSON.parse(ev.data as string) as JobEvent;
      } catch {
        return;
      }
      const resolver = pendingRef.current.get(event.job_id);
      if (!resolver) return;
      if (event.status === "success" || event.status === "failure") {
        pendingRef.current.delete(event.job_id);
        resolver(eventToJob(event));
      }
    };

    ws.onerror = () => {};
    ws.onclose = () => { wsRef.current = null; };

    return () => {
      destroyed = true;
      wsRef.current = null;
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, []);

  /**
   * Wait for a terminal job event.
   *
   * Registers a WS resolver immediately, then races it against a REST-poll
   * fallback that starts after FALLBACK_DELAY_MS. The first to deliver a
   * terminal state wins and cancels the other.
   */
  async function waitForJob(jobId: string): Promise<Job> {
    return new Promise<Job>((resolve) => {
      let settled = false;

      function settle(job: Job) {
        if (settled) return;
        settled = true;
        pendingRef.current.delete(jobId);
        resolve(job);
      }

      // 1. Register WS resolver — fires immediately if the event arrives.
      pendingRef.current.set(jobId, settle);

      // 2. Start delayed REST-poll fallback.
      setTimeout(() => {
        if (settled) return; // WS already won
        void pollUntilDone(jobId, settle);
      }, FALLBACK_DELAY_MS);
    });
  }

  return { waitForJob };
}

async function pollUntilDone(
  jobId: string,
  settle: (job: Job) => void,
): Promise<void> {
  for (let i = 0; i < FALLBACK_MAX_POLLS; i++) {
    await sleep(FALLBACK_POLL_MS);
    let job: Job;
    try {
      job = await getJob(jobId);
    } catch {
      continue; // transient network error — keep polling
    }
    if (job.status === "success" || job.status === "failure") {
      settle(job);
      return;
    }
  }
}

function sleep(ms: number): Promise<void> {
  return new Promise((r) => setTimeout(r, ms));
}
