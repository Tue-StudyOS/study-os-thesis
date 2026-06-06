import { api } from "./client";
import {
  THESIS_LIST_DEFAULT_LIMIT,
  THESIS_LIST_MAX_LIMIT,
  THESIS_LIST_MIN_LIMIT,
  THESIS_LIST_MIN_OFFSET,
} from "./constants";
import { appendIntegerParam, assertInteger } from "./numeric";

export type ThesisDifficulty = "bachelor" | "master" | "phd";

export interface SkillsRequired {
  programming: string[];
  math: string[];
  theory: string[];
  domain: string[];
  other: string[];
}

export interface Thesis {
  id: number;
  title: string;
  abstract: string;
  chair_id: number | null;
  supervisor_id: number | null;
  submitter_id: number;
  source: "professor" | "student" | "openalex";
  difficulty: ThesisDifficulty | null;
  skills_required: SkillsRequired | null;
  generated_for_user_id: number | null;
  chat_session_id: number | null;
  created_at: string;
}

export interface ThesisCreate {
  title: string;
  abstract: string;
  chair_id?: number | null;
  supervisor_id?: number | null;
}

export function listTheses(limit = THESIS_LIST_DEFAULT_LIMIT, offset = 0): Promise<Thesis[]> {
  const q = new URLSearchParams();
  appendIntegerParam(q, "limit", limit, { min: THESIS_LIST_MIN_LIMIT, max: THESIS_LIST_MAX_LIMIT });
  appendIntegerParam(q, "offset", offset, { min: THESIS_LIST_MIN_OFFSET });
  return api<Thesis[]>(`/api/theses?${q}`);
}

export function getThesis(id: number): Promise<Thesis> {
  assertInteger("id", id, { min: 1 });
  return api<Thesis>(`/api/theses/${id}`);
}

export function createThesis(body: ThesisCreate): Promise<Thesis> {
  return api<Thesis>("/api/theses", { method: "POST", json: body });
}

export function listMyProposals(): Promise<Thesis[]> {
  return api<Thesis[]>("/api/proposals/mine");
}
