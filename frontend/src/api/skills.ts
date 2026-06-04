import { api } from "./client";

export interface SkillEvidence {
  course_name: string;
  credits: number | null;
  grade: string | null;
  handbook_module: string | null;
  match_method: string;
  match_confidence: number;
  contribution: number;
}

export interface UserSkillItem {
  skill: string;
  category: string | null;
  score: number; // 0.0-1.0
  evidence: SkillEvidence[];
}

export interface UserSkillProfile {
  user_id: number;
  computation_run_id: string | null;
  computed_at: string | null;
  skills: UserSkillItem[];
  unmatched_courses: string[];
  warnings: string[];
}

export function getUserSkills(): Promise<UserSkillProfile> {
  return api<UserSkillProfile>("/api/students/me/skills");
}

export function recomputeSkills(): Promise<{ job_id: string }> {
  return api<{ job_id: string }>("/api/students/me/skills/recompute", {
    method: "POST",
  });
}
