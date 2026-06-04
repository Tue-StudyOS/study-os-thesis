import { api } from "./client";

export interface Paper {
  id: number;
  title: string;
  abstract: string | null;
  summary: string | null;
  authors: string[];
  publication_date: string | null;
  source: string;
  source_url: string;
  arxiv_id: string | null;
  doi: string | null;
  recency_score: number;
  relevance_score: number;
  enriched_at: string | null;
  created_at: string;
  tags: string[];
}

export function listPapers(params: {
  chair_id?: number;
  tag?: string;
  limit?: number;
  offset?: number;
}): Promise<Paper[]> {
  const q = new URLSearchParams();
  if (params.chair_id !== undefined) q.set("chair_id", String(params.chair_id));
  if (params.tag) q.set("tag", params.tag);
  if (params.limit !== undefined) q.set("limit", String(params.limit));
  if (params.offset !== undefined) q.set("offset", String(params.offset));
  return api<Paper[]>(`/api/papers?${q}`);
}
