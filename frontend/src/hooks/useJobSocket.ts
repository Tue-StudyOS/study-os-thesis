/**
 * useJobSocket
 *
 * Opens a single authenticated WebSocket (WS /api/ws?token=<JWT>) for the
 * lifetime of the component. Exposes `waitForJob(jobId)` which returns a
 * Promise that resolves as soon as the server pushes a terminal event
 * (success or failure) for that job.
 *
 * Fallback: if the WebSocket cannot connect within WS_CONNECT_TIMEOUT_MS
 * the promise transparently falls back to polling GET /api/jobs/{id} every
 * 5 s — silent from the caller's perspective.
 */

import { useEffect, useRef } from "react";
import { getToken } from "../api/client";
import { pollJob, type Job } from "../api/jobs";

interface JobEvent {
  type: string;
  job_id: string;
  user_id: number;
  status: "started" | "success" | "failure" | "retry";
  data: Record<string, unknown>;
  timestamp: string;
}

type JobResolver = (event: JobEvent) => void;

// Give the WS this long to open before falling back to polling.
const WS_CONNECT_TIMEOUT_MS = 4000;
// Fallback poll cadence and max attempts (5 s × 360 = 30 min).
const FALLBACK_POLL_MS = 5000;
const FALLBACK_MAX_POLLS = 360;

function buildWsUrl(): string | null {
  const token = getToken();
  if (!token) return null;
  const proto = window.location.protocol === "https:" ? "wss" : "ws";
  return `${proto}://${window.location.host}/api/ws?token=${encodeURIComponent(token)}`;
}

export function useJobSocket() {
  const pendingRef = useRef<Map<string, JobResolver>>(new Map());
  const wsRef = useRef<WebSocket | null>(null);
  const connectedRef = useRef<boolean>(false);

  useEffect(() => {
    const url = buildWsUrl();
    if (!url || !("WebSocket" in window)) return;

    // Guard against React StrictMode's double-invoke: if this cleanup runs
    // before the socket opens, we mark it destroyed and skip all callbacks.
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
      connectedRef.current = true;
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
        resolver(event);
      }
    };

    ws.onerror = () => { connectedRef.current = false; };
    ws.onclose = () => { connectedRef.current = false; wsRef.current = null; };

    return () => {
      destroyed = true;
      connectedRef.current = false;
      wsRef.current = null;
      // Only close OPEN sockets. Closing a CONNECTING socket triggers a
      // browser console error ("WebSocket closed before connection established")
      // which is harmless but noisy — let onopen handle the close instead.
      if (ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, []);

  /** Wait up to WS_CONNECT_TIMEOUT_MS for the socket to open. */
  function awaitConnection(): Promise<void> {
    return new Promise<void>((resolve) => {
      if (connectedRef.current) { resolve(); return; }
      let elapsed = 0;
      const interval = setInterval(() => {
        elapsed += 50;
        if (connectedRef.current || elapsed >= WS_CONNECT_TIMEOUT_MS) {
          clearInterval(interval);
          resolve();
        }
      }, 50);
    });
  }

  /**
   * Wait for a terminal job event via WebSocket, falling back to REST polling
   * if the socket is unavailable. Returns a Job-shaped object in both paths.
   */
  async function waitForJob(jobId: string): Promise<Job> {
    await awaitConnection();

    if (connectedRef.current && wsRef.current?.readyState === WebSocket.OPEN) {
      return new Promise<Job>((resolve) => {
        pendingRef.current.set(jobId, (event) => {
          resolve({
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
          });
        });
      });
    }

    // WebSocket unavailable — fall back to REST polling.
    return pollJob(jobId, { intervalMs: FALLBACK_POLL_MS, maxPolls: FALLBACK_MAX_POLLS });
  }

  return { waitForJob };
}
