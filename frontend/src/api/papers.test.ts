import { beforeEach, describe, expect, it, vi } from "vitest";

import { listPapers, triggerScrape } from "./papers";

const { apiMock, waitForJobTreeMock } = vi.hoisted(() => ({
  apiMock: vi.fn(),
  waitForJobTreeMock: vi.fn(),
}));

vi.mock("./client", () => ({
  api: apiMock,
}));

vi.mock("./jobEvents", () => ({
  waitForJobTree: waitForJobTreeMock,
}));

describe("papers API client", () => {
  beforeEach(() => {
    apiMock.mockReset();
    waitForJobTreeMock.mockReset();
    waitForJobTreeMock.mockResolvedValue({ id: "job-1", status: "success" });
  });

  it("serializes only integer paper list params", async () => {
    apiMock.mockResolvedValue({ items: [], total: 0, limit: 15, offset: 30 });

    await listPapers({ chair_id: 6, limit: 15, offset: 30 });

    expect(apiMock).toHaveBeenCalledWith("/api/papers?chair_id=6&limit=15&offset=30");
    expect(() => listPapers({ chair_id: 6.5 })).toThrow(TypeError);
    expect(() => listPapers({ limit: "15" as unknown as number })).toThrow(TypeError);
    expect(() => listPapers({ limit: 201 })).toThrow(RangeError);
  });

  it("sends only integer scraper request body values", async () => {
    apiMock.mockResolvedValue({ job_id: "job-1" });

    await triggerScrape(6, { since_days: 365, max_results: 20 });

    expect(apiMock).toHaveBeenCalledWith("/api/scraper/run/6", {
      method: "POST",
      json: { since_days: 365, max_results: 20 },
    });
    expect(waitForJobTreeMock).toHaveBeenCalledWith("job-1");
  });

  it("rejects non-integer scraper params before making a request", async () => {
    await expect(triggerScrape(6.5)).rejects.toThrow(TypeError);
    await expect(triggerScrape(6, { max_results: "20" as unknown as number })).rejects.toThrow(TypeError);
    await expect(triggerScrape(6, { since_days: 29 })).rejects.toThrow(RangeError);

    expect(apiMock).not.toHaveBeenCalled();
    expect(waitForJobTreeMock).not.toHaveBeenCalled();
  });
});
