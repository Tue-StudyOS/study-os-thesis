import { api } from "./client";

export interface ChairDocument {
  id: number;
  kind: "description";
  title: string | null;
  content: string;
  published_year: number | null;
  created_at: string;
}

export interface Chair {
  id: number;
  name: string;
  short_description: string;
  professor_title: string | null;
  professor_name: string;
  professor_user_id: number | null;
  website_url: string | null;
  created_at: string;
  documents: ChairDocument[];
}

export interface ChairCreate {
  name: string;
  short_description: string;
  professor_title?: string | null;
  professor_name: string;
  professor_user_id?: number | null;
  website_url?: string | null;
}

export interface ChairPatch {
  name?: string;
  short_description?: string;
  professor_title?: string | null;
  professor_name?: string;
  professor_user_id?: number | null;
  website_url?: string | null;
}

export function listChairs(): Promise<Chair[]> {
  return api<Chair[]>("/api/chairs");
}

export function getChair(id: number): Promise<Chair> {
  return api<Chair>(`/api/chairs/${id}`);
}

export function createChair(body: ChairCreate): Promise<Chair> {
  return api<Chair>("/api/chairs", { method: "POST", json: body });
}

export function updateChair(id: number, body: ChairPatch): Promise<Chair> {
  return api<Chair>(`/api/chairs/${id}`, { method: "PATCH", json: body });
}

export function deleteChair(id: number): Promise<void> {
  return api<void>(`/api/chairs/${id}`, { method: "DELETE" });
}
