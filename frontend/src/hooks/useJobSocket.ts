/**
 * useJobSocket
 *
 * Provides waitForJob(jobId) which resolves as soon as the backend pushes a
 * terminal WebSocket event for that job, with a transparent REST-poll fallback.
 *
 * The WebSocket connection is managed as a module-level singleton so that
 * React StrictMode's mount→unmount→remount cycle does not repeatedly open and
 * close the socket. The singleton reconnects automatically on close.
 */

import { useRef } from "react";
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

// How long after registering a job listener to start the REST-poll fallback.
const FALLBACK_DELAY_MS = 3000;
const FALLBACK_POLL_MS = 5000;
const FALLBACK_MAX_POLLS = 360;
// Delay before reconnecting after a close (exponential back-off base).
const RECONNECT_BASE_MS = 1000;
const RECONNECT_MAX_MS = 30_000;

// ---------------------------------------------------------------------------
// Module-level singleton — lives for the entire browser session, survives
// React StrictMode remounts.
// ---------------------------------------------------------------------------

let _ws: WebSocket | null = null;
let _reconnectTimer: ReturnType<typeof setTimeout> | null = null;
let _reconnectDelay = RECONNECT_BASE_MS;
const _pending = new Map<string, JobResolver>();

function buildWsUrl(): string | null {
  const token = getToken();
  if (!token) return null;
  const proto = window.location.protocol === "https:" ? "wss" : "ws";
  return `${proto}://${window.location.host}/api/ws?token=${encodeURIComponent(token)}`;
}

function connect(): void {
  if (_ws && (_ws.readyState === WebSocket.CONNECTING || _ws.readyState === WebSocket.OPEN)) {
    return; // already alive
  }

  const url = buildWsUrl();
  if (!url) return;

  let ws: WebSocket;
  try {
    ws = new WebSocket(url);
  } catch {
    scheduleReconnect();
    return;
  }
  _ws = ws;

  ws.onopen = () => {
    _reconnectDelay = RECONNECT_BASE_MS; // reset back-off on successful connect
  };

  ws.onmessage = (ev) => {
    let event: JobEvent;
    try {
      event = JSON.parse(ev.data as string) as JobEvent;
    } catch {
      return;
    }
    const resolver = _pending.get(event.job_id);
    if (!resolver) return;
    if (event.status === "success" || event.status === "failure") {
      _pending.delete(event.job_id);
      resolver(eventToJob(event));
    }
  };

  ws.onerror = () => {};

  ws.onclose = () => {
    _ws = null;
    // Only reconnect if there are pending listeners waiting.
    if (_pending.size > 0) {
      scheduleReconnect();
    }
  };
}

function scheduleReconnect(): void {
  if (_reconnectTimer !== null) return;
  _reconnectTimer = setTimeout(() => {
    _reconnectTimer = null;
    _reconnectDelay = Math.min(_reconnectDelay * 2, RECONNECT_MAX_MS);
    connect();
  }, _reconnectDelay);
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

// ---------------------------------------------------------------------------
// Hook — thin wrapper around the singleton
// ---------------------------------------------------------------------------

export function useJobSocket() {
  // Track whether this hook instance has triggered the initial connect.
  const didConnect = useRef(false);
  if (!didConnect.current) {
    didConnect.current = true;
    connect();
  }

  /**
   * Wait for a terminal job event.
   *
   * Registers a WS resolver immediately (works even if socket is still
   * connecting). Races against a delayed REST-poll fallback. First to deliver
   * a terminal state wins and cancels the other.
   */
  async function waitForJob(jobId: string): Promise<Job> {
    // Ensure we have a live socket before registering the listener.
    connect();

    return new Promise<Job>((resolve) => {
      let settled = false;

      function settle(job: Job) {
        if (settled) return;
        settled = true;
        _pending.delete(jobId);
        resolve(job);
      }

      // 1. Register WS resolver — resolves immediately on the server push.
      _pending.set(jobId, settle);

      // 2. Delayed REST-poll fallback in case the WS never delivers.
      setTimeout(() => {
        if (settled) return;
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
      continue;
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
