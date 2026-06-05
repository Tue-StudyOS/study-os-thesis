import { describe, expect, it } from "vitest";

import { appendIntegerParam, assertInteger, setIntegerBodyField } from "./numeric";

describe("API numeric helpers", () => {
  it("accepts bounded integers", () => {
    expect(assertInteger("limit", 15, { min: 1, max: 30 })).toBe(15);
  });

  it("rejects floats and numeric strings", () => {
    expect(() => assertInteger("limit", 1.5)).toThrow(TypeError);
    expect(() => assertInteger("limit", "1" as unknown as number)).toThrow(TypeError);
  });

  it("rejects values outside explicit bounds", () => {
    expect(() => assertInteger("limit", 0, { min: 1 })).toThrow(RangeError);
    expect(() => assertInteger("limit", 101, { max: 100 })).toThrow(RangeError);
  });

  it("only appends integer URL params", () => {
    const params = new URLSearchParams();

    appendIntegerParam(params, "limit", 15, { min: 1, max: 30 });
    appendIntegerParam(params, "offset", undefined);

    expect(params.toString()).toBe("limit=15");
    expect(() => appendIntegerParam(params, "limit", 15.5)).toThrow(TypeError);
  });

  it("only writes integer body fields", () => {
    const body: { max_results?: number } = {};

    setIntegerBodyField(body, "max_results", 250, { min: 1, max: 500 });

    expect(body).toEqual({ max_results: 250 });
    expect(() => setIntegerBodyField(body, "max_results", "250" as unknown as number)).toThrow(TypeError);
  });
});
