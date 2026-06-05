import { describe, expect, it } from "vitest";

import type { Job } from "../api/jobs";
import {
  chairIdFromScrapeJob,
  getChairSyncStatus,
  idleChairSync,
  runningSyncMapFromJobs,
  setChairSyncStatus,
  type ChairSyncMap,
} from "./chairSync";

function makeJob(inputData: Record<string, unknown> | null): Job {
  return {
    id: crypto.randomUUID(),
    type: "scrape_chair",
    status: "started",
    user_id: 1,
    celery_task_id: null,
    input_data: inputData,
    result_data: null,
    error: null,
    attempts: 0,
    created_at: "2026-06-05T00:00:00Z",
    started_at: "2026-06-05T00:00:01Z",
    completed_at: null,
  };
}

describe("chair sync state helpers", () => {
  it("returns idle state for unknown or missing chairs", () => {
    const syncByChairId: ChairSyncMap = {
      6: { state: "running", error: null },
    };

    expect(getChairSyncStatus(syncByChairId, 5)).toEqual(idleChairSync);
    expect(getChairSyncStatus(syncByChairId, null)).toEqual(idleChairSync);
  });

  it("keeps spinner state scoped to the chair that started syncing", () => {
    const syncByChairId = setChairSyncStatus({}, 6, { state: "running", error: null });

    expect(getChairSyncStatus(syncByChairId, 6)).toEqual({ state: "running", error: null });
    expect(getChairSyncStatus(syncByChairId, 5)).toEqual({ state: "idle", error: null });
  });

  it("allows multiple chairs to sync independently", () => {
    const chairSixRunning = setChairSyncStatus({}, 6, { state: "running", error: null });
    const bothRunning = setChairSyncStatus(chairSixRunning, 5, { state: "running", error: null });
    const chairSixDone = setChairSyncStatus(bothRunning, 6, { state: "done", error: null });

    expect(getChairSyncStatus(chairSixDone, 6)).toEqual({ state: "done", error: null });
    expect(getChairSyncStatus(chairSixDone, 5)).toEqual({ state: "running", error: null });
  });

  it("does not mutate prior sync maps", () => {
    const original = setChairSyncStatus({}, 6, { state: "running", error: null });
    const updated = setChairSyncStatus(original, 6, { state: "error", error: "boom" });

    expect(original[6]).toEqual({ state: "running", error: null });
    expect(updated[6]).toEqual({ state: "error", error: "boom" });
  });

  it("extracts chair ids from scrape job input data", () => {
    expect(chairIdFromScrapeJob(makeJob({ chair_id: 6 }))).toBe(6);
    expect(chairIdFromScrapeJob(makeJob({ chair_id: "6" }))).toBeNull();
    expect(chairIdFromScrapeJob(makeJob({ chair_id: 6.5 }))).toBeNull();
    expect(chairIdFromScrapeJob(makeJob({ chair_id: 0 }))).toBeNull();
    expect(chairIdFromScrapeJob(makeJob({ chair_id: "-6" }))).toBeNull();
    expect(chairIdFromScrapeJob(makeJob(null))).toBeNull();
  });

  it("rehydrates running sync state from active scrape jobs", () => {
    const syncByChairId = runningSyncMapFromJobs([
      makeJob({ chair_id: 6 }),
      makeJob({ chair_id: 5 }),
      makeJob({ chair_id: "not-a-number" }),
    ]);

    expect(getChairSyncStatus(syncByChairId, 6)).toEqual({ state: "running", error: null });
    expect(getChairSyncStatus(syncByChairId, 5)).toEqual({ state: "running", error: null });
    expect(getChairSyncStatus(syncByChairId, 4)).toEqual({ state: "idle", error: null });
  });
});
