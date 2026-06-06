export function formatPaperYear(publicationDate: string | null) {
  if (!publicationDate) return "n.d.";
  return new Date(publicationDate).getFullYear().toString();
}

export function formatPublicationDate(iso: string | null): string {
  if (!iso) return "Unknown";
  return new Intl.DateTimeFormat("en", { month: "long", year: "numeric" }).format(new Date(iso));
}

export function formatAuthors(authors: string[], source: string) {
  if (authors.length === 0) return source;
  const shown = authors.slice(0, 3).join(", ");
  const more = authors.length > 3 ? ` +${authors.length - 3}` : "";
  return `${shown}${more}`;
}

export function scoreCount(score: number): number {
  return Math.max(0, Math.min(5, Math.round(score * 5)));
}
