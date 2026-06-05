import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import { api, setToken } from "./client";

describe("api client", () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    const storage = new Map<string, string>();
    vi.stubGlobal("localStorage", {
      getItem: vi.fn((key: string) => storage.get(key) ?? null),
      removeItem: vi.fn((key: string) => {
        storage.delete(key);
      }),
      setItem: vi.fn((key: string, value: string) => {
        storage.set(key, value);
      }),
    });
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("omits an undefined request body", async () => {
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    await api("/api/test");

    const init = fetchMock.mock.calls[0]?.[1];
    expect(init).toBeDefined();
    expect(init).not.toHaveProperty("body");
  });

  it("adds bearer authorization when a token exists", async () => {
    setToken("token-123");
    const fetchMock = vi.spyOn(globalThis, "fetch").mockResolvedValue(
      new Response(JSON.stringify({ ok: true }), {
        status: 200,
        headers: { "Content-Type": "application/json" },
      }),
    );

    await api("/api/test");

    expect(fetchMock.mock.calls[0]?.[1]?.headers).toMatchObject({
      Authorization: "Bearer token-123",
    });
  });
});
