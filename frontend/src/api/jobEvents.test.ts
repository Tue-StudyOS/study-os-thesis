import { describe, expect, it } from "vitest";

import { parseJobEventMessage } from "./jobEvents";

describe("job event parsing", () => {
  it("accepts a well-formed job status event", () => {
    expect(
      parseJobEventMessage(
        JSON.stringify({
          type: "job_status",
          job_id: "job-1",
          status: "success",
          data: { dispatched: [] },
          error: "ignored for success",
          timestamp: "2026-06-06T00:00:00Z",
        }),
      ),
    ).toEqual({
      type: "job_status",
      job_id: "job-1",
      status: "success",
      data: { dispatched: [] },
      error: "ignored for success",
      timestamp: "2026-06-06T00:00:00Z",
    });
  });

  it("rejects malformed job events", () => {
    expect(() => parseJobEventMessage("null")).toThrow("Malformed job event");
    expect(() => parseJobEventMessage(JSON.stringify({ job_id: "job-1", status: "done" }))).toThrow(
      "Malformed job event",
    );
    expect(() => parseJobEventMessage(JSON.stringify({ job_id: 1, status: "success" }))).toThrow(
      "Malformed job event",
    );
  });

  it("drops invalid optional fields instead of coercing them", () => {
    expect(
      parseJobEventMessage(
        JSON.stringify({
          job_id: "job-1",
          status: "failure",
          data: [],
          error: 500,
          timestamp: false,
        }),
      ),
    ).toEqual({
      type: "job_status",
      job_id: "job-1",
      status: "failure",
    });
  });

  it("defaults missing event type while preserving valid payload data", () => {
    expect(
      parseJobEventMessage(
        JSON.stringify({
          job_id: "job-2",
          status: "retry",
          data: { error: "temporary" },
        }),
      ),
    ).toEqual({
      type: "job_status",
      job_id: "job-2",
      status: "retry",
      data: { error: "temporary" },
    });
  });

  it("rejects non-object JSON payloads and missing statuses", () => {
    expect(() => parseJobEventMessage(JSON.stringify(["job-1", "success"]))).toThrow("Malformed job event");
    expect(() => parseJobEventMessage(JSON.stringify({ job_id: "job-1" }))).toThrow("Malformed job event");
  });
});
