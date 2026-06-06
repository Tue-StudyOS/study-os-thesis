import { describe, expect, it } from "vitest";

import { chairIdFromRouteParam } from "./chairRoutes";

describe("chair route parsing", () => {
  it("accepts only the explicit chairID route shape with a positive integer", () => {
    expect(chairIdFromRouteParam("chairID=6")).toBe(6);
  });

  it("rejects malformed or non-integer route values", () => {
    expect(chairIdFromRouteParam(undefined)).toBeNull();
    expect(chairIdFromRouteParam("6")).toBeNull();
    expect(chairIdFromRouteParam("chairID=001")).toBeNull();
    expect(chairIdFromRouteParam("chairID=0")).toBeNull();
    expect(chairIdFromRouteParam("chairID=-6")).toBeNull();
    expect(chairIdFromRouteParam("chairID=6.5")).toBeNull();
    expect(chairIdFromRouteParam("chairID=6abc")).toBeNull();
    expect(chairIdFromRouteParam("chairID=")).toBeNull();
    expect(chairIdFromRouteParam("chairID=9007199254740992")).toBeNull();
  });
});
