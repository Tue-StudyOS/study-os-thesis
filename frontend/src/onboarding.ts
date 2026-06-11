import type { User } from "./auth/AuthContext";

const STORAGE_PREFIX = "scholarai:onboarding:";
const UNIVERSITY_EMAIL_DOMAINS = ["uni-tuebingen.de", "student.uni-tuebingen.de"];

export type TuebingenResidence = "yes" | "no" | "unknown";

export type OnboardingProfile = {
  displayName: string;
  degree: string;
  semester: string;
  livesInTuebingen: TuebingenResidence;
  locationSource: "manual" | "browser" | null;
  completedAt: string;
};

function keyForUser(userId: number): string {
  return `${STORAGE_PREFIX}${userId}`;
}

export function isUniversityEmail(email: string): boolean {
  const domain = email.trim().toLowerCase().split("@").at(-1);
  return !!domain && UNIVERSITY_EMAIL_DOMAINS.includes(domain);
}

export function inferNameFromEmail(email: string): string {
  const localPart = email.split("@")[0]?.replace(/[._-]+/g, " ").trim();
  if (!localPart) return "";
  return localPart
    .split(" ")
    .filter(Boolean)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(" ");
}

export function isLikelyInTuebingen(latitude: number, longitude: number): boolean {
  return latitude >= 48.45 && latitude <= 48.58 && longitude >= 8.95 && longitude <= 9.15;
}

export function getOnboardingProfile(user: User | null): OnboardingProfile | null {
  if (!user) return null;
  const raw = window.localStorage.getItem(keyForUser(user.id));
  if (!raw) return null;

  try {
    return JSON.parse(raw) as OnboardingProfile;
  } catch {
    window.localStorage.removeItem(keyForUser(user.id));
    return null;
  }
}

export function hasCompletedOnboarding(user: User | null): boolean {
  return !!getOnboardingProfile(user);
}

export function saveOnboardingProfile(user: User, profile: OnboardingProfile): void {
  window.localStorage.setItem(keyForUser(user.id), JSON.stringify(profile));
}
