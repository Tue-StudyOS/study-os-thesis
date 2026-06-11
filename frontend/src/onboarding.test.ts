import { describe, expect, it } from "vitest";
import { inferNameFromEmail, isLikelyInTuebingen, isUniversityEmail } from "./onboarding";

describe("onboarding helpers", () => {
  it("accepts Tuebingen university email domains", () => {
    expect(isUniversityEmail("max@student.uni-tuebingen.de")).toBe(true);
    expect(isUniversityEmail("max@uni-tuebingen.de")).toBe(true);
    expect(isUniversityEmail("max@example.com")).toBe(false);
  });

  it("infers a readable name from the login email", () => {
    expect(inferNameFromEmail("max.mustermann@student.uni-tuebingen.de")).toBe("Max Mustermann");
    expect(inferNameFromEmail("alex-muster@uni-tuebingen.de")).toBe("Alex Muster");
  });

  it("detects coordinates near Tuebingen", () => {
    expect(isLikelyInTuebingen(48.5216, 9.0576)).toBe(true);
    expect(isLikelyInTuebingen(48.7758, 9.1829)).toBe(false);
  });
});
