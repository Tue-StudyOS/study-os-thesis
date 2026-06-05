import type { SyncState } from "../components/chairs";
import type { Job } from "../api/jobs";

export type ChairSyncStatus = {
  state: SyncState;
  error: string | null;
};

export type ChairSyncMap = Record<number, ChairSyncStatus>;

export const idleChairSync: ChairSyncStatus = { state: "idle", error: null };

export function getChairSyncStatus(syncByChairId: ChairSyncMap, chairId: number | null | undefined): ChairSyncStatus {
  if (chairId == null) return idleChairSync;
  return syncByChairId[chairId] ?? idleChairSync;
}

export function setChairSyncStatus(
  syncByChairId: ChairSyncMap,
  chairId: number,
  status: ChairSyncStatus,
): ChairSyncMap {
  return {
    ...syncByChairId,
    [chairId]: status,
  };
}

export function chairIdFromScrapeJob(job: Job): number | null {
  const chairId = job.input_data?.chair_id;
  return typeof chairId === "number" && Number.isInteger(chairId) ? chairId : null;
}

export function runningSyncMapFromJobs(jobs: Job[]): ChairSyncMap {
  return jobs.reduce<ChairSyncMap>((syncByChairId, job) => {
    const chairId = chairIdFromScrapeJob(job);
    if (chairId == null) return syncByChairId;
    return setChairSyncStatus(syncByChairId, chairId, { state: "running", error: null });
  }, {});
}
