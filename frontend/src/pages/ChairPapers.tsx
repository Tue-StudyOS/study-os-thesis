import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import TopBar from "../components/TopBar";
import { useAuth } from "../auth/AuthContext";
import { getChair, type Chair } from "../api/chairs";
import { listPapers, triggerScrape, type Paper } from "../api/papers";

// ─── Helpers ──────────────────────────────────────────────────────────────────

function formatDate(iso: string | null): string {
  if (!iso) return "—";
  return new Date(iso).getFullYear().toString();
}

function scoreBar(score: number) {
  const pct = Math.round(score * 100);
  const color = pct >= 70 ? "#4cadab" : pct >= 40 ? "#455f88" : "#8a8fa8";
  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1.5 rounded-full bg-surface-container-high overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${pct}%`, background: color }} />
      </div>
      <span className="font-label-md text-[11px] text-on-surface-variant w-7 text-right">{pct}</span>
    </div>
  );
}

// ─── Sort state ───────────────────────────────────────────────────────────────

type SortKey = "publication_date" | "relevance_score" | "title";
type SortDir = "asc" | "desc";

function SortIcon({ active, dir }: { active: boolean; dir: SortDir }) {
  return (
    <span
      className="material-symbols-outlined text-[14px] transition-opacity"
      style={{ opacity: active ? 1 : 0.3 }}
    >
      {active && dir === "asc" ? "arrow_upward" : "arrow_downward"}
    </span>
  );
}

// ─── Row expanded detail ──────────────────────────────────────────────────────

function ExpandedRow({ paper }: { paper: Paper }) {
  return (
    <tr>
      <td colSpan={5} className="px-4 pb-4 pt-0 bg-surface-container-low/60">
        <div className="rounded-lg border border-outline-variant bg-surface-container-lowest p-4 space-y-3">
          {paper.summary && (
            <div>
              <p className="font-label-md text-[11px] uppercase tracking-wider text-on-surface-variant mb-1">
                AI Summary
              </p>
              <p className="font-body-sm text-body-sm text-on-surface leading-relaxed">{paper.summary}</p>
            </div>
          )}
          {paper.abstract && !paper.summary && (
            <div>
              <p className="font-label-md text-[11px] uppercase tracking-wider text-on-surface-variant mb-1">
                Abstract
              </p>
              <p className="font-body-sm text-body-sm text-on-surface-variant leading-relaxed line-clamp-5">
                {paper.abstract}
              </p>
            </div>
          )}
          <div className="flex flex-wrap gap-4 text-[11px] text-on-surface-variant font-label-md pt-1">
            {paper.authors.length > 0 && (
              <span className="flex items-center gap-1">
                <span className="material-symbols-outlined text-[13px]">group</span>
                {paper.authors.slice(0, 5).join(", ")}
                {paper.authors.length > 5 && ` +${paper.authors.length - 5} more`}
              </span>
            )}
            <span className="flex items-center gap-1">
              <span className="material-symbols-outlined text-[13px]">database</span>
              {paper.source}
            </span>
            {paper.arxiv_id && (
              <a
                href={`https://arxiv.org/abs/${paper.arxiv_id}`}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-1 text-primary hover:underline"
                onClick={(e) => e.stopPropagation()}
              >
                <span className="material-symbols-outlined text-[13px]">open_in_new</span>
                arXiv:{paper.arxiv_id}
              </a>
            )}
          </div>
        </div>
      </td>
    </tr>
  );
}

// ─── Main page ────────────────────────────────────────────────────────────────

export default function ChairPapers() {
  const { id } = useParams<{ id: string }>();
  const chairId = Number(id);
  const navigate = useNavigate();
  const { user } = useAuth();

  const [chair, setChair] = useState<Chair | null>(null);
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Sync button state
  type SyncState = "idle" | "running" | "done" | "error";
  const [syncState, setSyncState] = useState<SyncState>("idle");
  const [syncError, setSyncError] = useState<string | null>(null);

  const [sortKey, setSortKey] = useState<SortKey>("relevance_score");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [tagFilter, setTagFilter] = useState<string>("");
  const [search, setSearch] = useState("");
  const [expandedId, setExpandedId] = useState<number | null>(null);

  useEffect(() => {
    if (!chairId) return;
    setLoading(true);
    Promise.all([getChair(chairId), listPapers({ chair_id: chairId, limit: 200 })])
      .then(([c, p]) => {
        setChair(c);
        setPapers(p);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Error loading papers"))
      .finally(() => setLoading(false));
  }, [chairId]);

  async function handleSync() {
    if (!chairId || syncState === "running") return;
    setSyncState("running");
    setSyncError(null);
    try {
      const job = await triggerScrape(chairId);
      if (job.status === "success") {
        // Reload papers after successful scrape
        const fresh = await listPapers({ chair_id: chairId, limit: 200 });
        setPapers(fresh);
        setSyncState("done");
      } else {
        setSyncError(job.error ?? "Scrape job failed");
        setSyncState("error");
      }
    } catch (e) {
      setSyncError(e instanceof Error ? e.message : "Unknown error");
      setSyncState("error");
    }
  }

  // Collect all unique tags from loaded papers
  const allTags = useMemo(() => {
    const s = new Set<string>();
    papers.forEach((p) => p.tags.forEach((t) => s.add(t)));
    return Array.from(s).sort();
  }, [papers]);

  const filtered = useMemo(() => {
    let rows = papers;
    if (tagFilter) rows = rows.filter((p) => p.tags.includes(tagFilter));
    if (search) {
      const q = search.toLowerCase();
      rows = rows.filter(
        (p) =>
          p.title.toLowerCase().includes(q) ||
          p.authors.some((a) => a.toLowerCase().includes(q)) ||
          (p.summary ?? "").toLowerCase().includes(q),
      );
    }
    return [...rows].sort((a, b) => {
      let av: number | string, bv: number | string;
      if (sortKey === "publication_date") {
        av = a.publication_date ?? "";
        bv = b.publication_date ?? "";
      } else if (sortKey === "relevance_score") {
        av = a.relevance_score;
        bv = b.relevance_score;
      } else {
        av = a.title.toLowerCase();
        bv = b.title.toLowerCase();
      }
      if (av < bv) return sortDir === "asc" ? -1 : 1;
      if (av > bv) return sortDir === "asc" ? 1 : -1;
      return 0;
    });
  }, [papers, tagFilter, search, sortKey, sortDir]);

  function toggleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir((d) => (d === "asc" ? "desc" : "asc"));
    } else {
      setSortKey(key);
      setSortDir("desc");
    }
  }

  function toggleRow(id: number) {
    setExpandedId((prev) => (prev === id ? null : id));
  }

  const colHeader = (key: SortKey, label: string, extraClass = "") => (
    <th
      className={`px-4 py-3 text-left font-label-md text-[11px] uppercase tracking-wider text-on-surface-variant cursor-pointer select-none hover:text-on-surface transition-colors whitespace-nowrap ${extraClass}`}
      onClick={() => toggleSort(key)}
    >
      <span className="inline-flex items-center gap-1">
        {label}
        <SortIcon active={sortKey === key} dir={sortDir} />
      </span>
    </th>
  );

  return (
    <div className="flex flex-col min-h-screen bg-surface-bright">
      <TopBar title={chair ? `${chair.name} — Papers` : "Papers"} showSearch={false} />

      <main className="flex-1 overflow-y-auto p-4 md:p-margin-desktop">
        <div className="max-w-container-max mx-auto space-y-stack-md">

          {/* Back + header */}
          <div className="flex items-center justify-between gap-3">
            <div className="flex items-center gap-3">
              <button
                onClick={() => navigate("/chairs")}
                className="p-2 rounded-full hover:bg-surface-container transition-colors text-on-surface-variant"
              >
                <span className="material-symbols-outlined">arrow_back</span>
              </button>
              <div>
                <h2 className="font-headline-md text-headline-md text-on-surface">
                  {chair?.name ?? "Lehrstuhl"}
                </h2>
                {chair && (
                  <p className="font-body-sm text-body-sm text-on-surface-variant flex items-center gap-1 mt-0.5">
                    <span className="material-symbols-outlined text-[14px]">person</span>
                    {chair.professor_name}
                  </p>
                )}
              </div>
            </div>

            {/* Sync button */}
            {user && (
              <div className="flex flex-col items-end gap-1">
                <button
                  onClick={handleSync}
                  disabled={syncState === "running"}
                  className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-on-primary font-label-md text-label-md hover:bg-primary-container hover:text-on-primary-container transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
                >
                  <span
                    className={`material-symbols-outlined text-[18px] ${syncState === "running" ? "animate-spin" : ""}`}
                  >
                    {syncState === "done" ? "check_circle" : "sync"}
                  </span>
                  {syncState === "running" ? "Syncing…" : syncState === "done" ? "Synced" : "Sync papers"}
                </button>
                {syncState === "error" && syncError && (
                  <p className="font-label-md text-[11px] text-error max-w-xs text-right">{syncError}</p>
                )}
              </div>
            )}
          </div>

          {/* Loading */}
          {loading && (
            <div className="flex justify-center py-24">
              <div className="w-8 h-8 border-2 border-outline-variant border-t-primary rounded-full animate-spin" />
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="bg-error-container text-on-error-container rounded-xl p-6 font-body-md">
              {error}
            </div>
          )}

          {!loading && !error && (
            <>
              {/* Toolbar: search + tag filter + count */}
              <div className="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between">
                <div className="flex items-center gap-3 flex-wrap">
                  {/* Search */}
                  <div className="relative">
                    <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-sm">
                      search
                    </span>
                    <input
                      value={search}
                      onChange={(e) => setSearch(e.target.value)}
                      placeholder="Title, author, summary…"
                      className="pl-9 pr-4 py-1.5 rounded-full border border-outline-variant bg-surface-container-lowest font-label-md text-label-md text-on-surface outline-none focus:border-primary w-56 transition-all"
                    />
                  </div>

                  {/* Tag filter */}
                  {allTags.length > 0 && (
                    <select
                      value={tagFilter}
                      onChange={(e) => setTagFilter(e.target.value)}
                      className="px-3 py-1.5 rounded-full border border-outline-variant bg-surface-container-lowest font-label-md text-label-md text-on-surface outline-none focus:border-primary cursor-pointer"
                    >
                      <option value="">All topics</option>
                      {allTags.map((t) => (
                        <option key={t} value={t}>
                          {t}
                        </option>
                      ))}
                    </select>
                  )}
                </div>

                <span className="font-label-md text-label-md text-on-surface-variant shrink-0">
                  {filtered.length} paper{filtered.length !== 1 ? "s" : ""}
                </span>
              </div>

              {/* Empty state */}
              {papers.length === 0 && (
                <div className="flex flex-col items-center justify-center py-24 gap-4 text-on-surface-variant">
                  <span className="material-symbols-outlined text-[48px]">article</span>
                  <p className="font-body-lg">No papers yet.</p>
                  <p className="font-body-sm text-center max-w-sm">
                    Trigger a scrape from the Admin page or ingest individual papers via
                    the API to populate this view.
                  </p>
                </div>
              )}

              {/* Table */}
              {papers.length > 0 && (
                <div className="rounded-xl border border-outline-variant overflow-hidden bg-surface-container-lowest">
                  <table className="w-full border-collapse">
                    <thead className="bg-surface-container border-b border-outline-variant">
                      <tr>
                        {colHeader("title", "Title", "w-full min-w-[200px]")}
                        {colHeader("publication_date", "Year", "w-16")}
                        <th className="px-4 py-3 text-left font-label-md text-[11px] uppercase tracking-wider text-on-surface-variant whitespace-nowrap">
                          Tags
                        </th>
                        {colHeader("relevance_score", "Score", "w-28")}
                        <th className="w-10" />
                      </tr>
                    </thead>
                    <tbody>
                      {filtered.map((paper) => (
                        <>
                          <tr
                            key={paper.id}
                            className="border-b border-outline-variant/50 hover:bg-surface-container/60 cursor-pointer transition-colors"
                            onClick={() => toggleRow(paper.id)}
                          >
                            {/* Title + authors */}
                            <td className="px-4 py-3">
                              <p className="font-body-sm text-body-sm text-on-surface font-medium line-clamp-2 leading-snug">
                                {paper.title}
                              </p>
                              {paper.authors.length > 0 && (
                                <p className="font-label-md text-[11px] text-on-surface-variant mt-0.5 line-clamp-1">
                                  {paper.authors.slice(0, 3).join(", ")}
                                  {paper.authors.length > 3 && ` +${paper.authors.length - 3}`}
                                </p>
                              )}
                            </td>

                            {/* Year */}
                            <td className="px-4 py-3 text-on-surface-variant font-body-sm text-body-sm whitespace-nowrap">
                              {formatDate(paper.publication_date)}
                            </td>

                            {/* Tags */}
                            <td className="px-4 py-3">
                              <div className="flex flex-wrap gap-1">
                                {paper.tags.slice(0, 3).map((t) => (
                                  <span
                                    key={t}
                                    className="px-1.5 py-0.5 rounded bg-secondary-container text-on-secondary-fixed-variant font-label-md text-[10px] whitespace-nowrap"
                                  >
                                    {t}
                                  </span>
                                ))}
                                {paper.tags.length > 3 && (
                                  <span className="font-label-md text-[10px] text-on-surface-variant">
                                    +{paper.tags.length - 3}
                                  </span>
                                )}
                              </div>
                            </td>

                            {/* Relevance score bar */}
                            <td className="px-4 py-3 min-w-[100px]">
                              {scoreBar(paper.relevance_score)}
                            </td>

                            {/* Expand chevron */}
                            <td className="px-3 py-3 text-on-surface-variant">
                              <span
                                className="material-symbols-outlined text-[18px] transition-transform"
                                style={{
                                  transform:
                                    expandedId === paper.id ? "rotate(180deg)" : "rotate(0deg)",
                                }}
                              >
                                expand_more
                              </span>
                            </td>
                          </tr>

                          {expandedId === paper.id && (
                            <ExpandedRow key={`${paper.id}-exp`} paper={paper} />
                          )}
                        </>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}
