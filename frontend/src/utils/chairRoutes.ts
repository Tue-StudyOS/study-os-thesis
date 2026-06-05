const CHAIR_ROUTE_PATTERN = /^chairID=([1-9]\d*)$/;

export function chairIdFromRouteParam(chairParam: string | undefined): number | null {
  if (chairParam === undefined) return null;

  const match = CHAIR_ROUTE_PATTERN.exec(chairParam);
  if (match === null) return null;

  const chairId = Number(match[1]);
  return Number.isSafeInteger(chairId) ? chairId : null;
}
