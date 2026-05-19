import { api } from "./client";

export interface Thesis {
  id: number;
  title: string;
  abstract: string;
  chair_id: number | null;
  supervisor_id: number | null;
  submitter_id: number;
  source: "professor" | "student" | "openalex";
  created_at: string;
}

export interface ThesisCreate {
  title: string;
  abstract: string;
  chair_id?: number | null;
  supervisor_id?: number | null;
}

export function listTheses(limit = 50, offset = 0): Promise<Thesis[]> {
  return api<Thesis[]>(`/api/theses?limit=${limit}&offset=${offset}`);
}

export function getThesis(id: number): Promise<Thesis> {
  return api<Thesis>(`/api/theses/${id}`);
}

export function createThesis(body: ThesisCreate): Promise<Thesis> {
  return api<Thesis>("/api/theses", { method: "POST", json: body });
}
