export type IntegerBounds = {
  min?: number;
  max?: number;
};

export function assertInteger(name: string, value: number, bounds: IntegerBounds = {}): number {
  if (!Number.isInteger(value)) {
    throw new TypeError(`${name} must be an integer`);
  }
  if (bounds.min !== undefined && value < bounds.min) {
    throw new RangeError(`${name} must be >= ${bounds.min}`);
  }
  if (bounds.max !== undefined && value > bounds.max) {
    throw new RangeError(`${name} must be <= ${bounds.max}`);
  }
  return value;
}

export function appendIntegerParam(
  params: URLSearchParams,
  name: string,
  value: number | undefined,
  bounds: IntegerBounds = {},
): void {
  if (value === undefined) return;
  params.set(name, String(assertInteger(name, value, bounds)));
}

export function setIntegerBodyField<TName extends string>(
  body: Partial<Record<TName, number>>,
  name: TName,
  value: number | undefined,
  bounds: IntegerBounds = {},
): void {
  if (value === undefined) return;
  body[name] = assertInteger(name, value, bounds);
}
