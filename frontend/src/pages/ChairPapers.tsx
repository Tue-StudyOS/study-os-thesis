import { Fragment, useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import TopBar from "../components/TopBar";
import { useAuth } from "../auth/AuthContext";
import { getChair, type Chair, type ChairDocument } from "../api/chairs";
import { listPapers, triggerScrape, type Paper } from "../api/papers";

type SortKey = "publication_date" | "relevance_score" | "title";
type SortDir = "asc" | "desc";
type SyncState = "idle" | "running" | "done" | "error";

const tagColors = ["bg-sky-500", "bg-emerald-500", "bg-orange-400", "bg-amber-500", "bg-slate-500"];

function formatYear(iso: string | null): string {
  if (!iso) return "-";
  return new Date(iso).getFullYear().toString();
}

function formatPublicationDate(iso: string | null): string {
  if (!iso) return "Unknown";
  return new Intl.DateTimeFormat("en", { month: "long", year: "numeric" }).format(new Date(iso));
}

function scoreCount(score: number): number {
  return Math.max(0, Math.min(5, Math.round(score * 5)));
}

function scorePercent(score: number): number {
  return Math.max(0, Math.min(100, Math.round(score * 100)));
}

function ScoreMeter({ score, showPercent = false }: { score: number; showPercent?: boolean }) {
  const count = scoreCount(score);
  const width = showPercent ? scorePercent(score) : (count / 5) * 100;

  return (
    <div className="min-w-[92px]">
      <div className="flex items-end justify-between gap-3">
        <span className="font-label-md text-[14px] font-semibold text-on-surface">
          {showPercent ? `${scorePercent(score)}%` : count}
        </span>
        <span className="font-body-sm text-[12px] text-on-surface-variant">{count}/5</span>
      </div>
      <div className="mt-1 h-1.5 rounded-full bg-surface-container-high overflow-hidden">
        <div className="h-full rounded-full bg-primary" style={{ width: `${width}%` }} />
      </div>
    </div>
  );
}

function SortHeader({
  label,
  active,
  dir,
  onClick,
  className = "",
}: {
  label: string;
  active?: boolean;
  dir?: SortDir;
  onClick?: () => void;
  className?: string;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={`flex items-center gap-1 text-left font-label-md text-[11px] uppercase tracking-[0.04em] text-on-surface-variant ${className}`}
    >
      {label}
      {active && (
        <span className="material-symbols-outlined text-[14px]">
          {dir === "asc" ? "arrow_upward" : "arrow_downward"}
        </span>
      )}
    </button>
  );
}

function PaperTags({ tags }: { tags: string[] }) {
  const shown = tags.length > 0 ? tags.slice(0, 3) : ["Causal AI", "Machine Learning"];

  return (
    <div className="flex flex-wrap gap-1">
      {shown.map((tag, index) => (
        <span
          key={`${tag}-${index}`}
          className={`${tagColors[index % tagColors.length]} rounded-full px-2 py-0.5 font-label-md text-[10px] text-white`}
        >
          {tag}
        </span>
      ))}
    </div>
  );
}

function truncateAuthors(authors: string[], source: string) {
  if (authors.length === 0) return source;
  const base = authors.slice(0, 3).join(", ");
  const more = authors.length > 3 ? ` +${authors.length - 3}` : "";
  return `${base}${source ? ` - ${source}` : ""}${more}`;
}

function DocumentPaperRow({ doc }: { doc: ChairDocument }) {
  return (
    <a
      href={doc.arxiv_id ? `https://arxiv.org/abs/${doc.arxiv_id}` : undefined}
      target={doc.arxiv_id ? "_blank" : undefined}
      rel={doc.arxiv_id ? "noreferrer" : undefined}
      className="grid w-full grid-cols-[minmax(300px,1fr)_170px_70px_190px_100px] items-center gap-4 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-4 py-2.5 text-left shadow-sm transition hover:shadow-md"
    >
      <div className="min-w-0">
        <p className="truncate font-body-sm text-[14px] font-semibold text-on-surface">
          {doc.title ?? "Untitled paper"}
        </p>
        <p className="truncate font-body-sm text-[12px] text-on-surface">
          {doc.arxiv_id ? `arXiv:${doc.arxiv_id}` : "Chair document"}
        </p>
      </div>
      <p className="font-body-sm text-[12px] text-on-surface-variant">-</p>
      <p className="font-body-sm text-[14px] text-on-surface">{doc.published_year ?? "-"}</p>
      <PaperTags tags={[]} />
      <ScoreMeter score={0} />
    </a>
  );
}

function SyncButton({
  state,
  onClick,
}: {
  state: SyncState;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      disabled={state === "running"}
      className="flex min-w-[92px] items-center justify-center gap-2 rounded-[4px] bg-primary px-4 py-2 font-label-md text-[12px] text-on-primary shadow-sm disabled:opacity-70"
    >
      {state === "running" ? (
        <span className="h-4 w-4 shrink-0 rounded-full border-2 border-on-primary/30 border-t-on-primary animate-spin" />
      ) : (
        <span className="material-symbols-outlined text-[16px]">check_circle</span>
      )}
      {state === "running" ? "Syncing" : "Synced"}
    </button>
  );
}

function PaperDetail({ paper, onBack }: { paper: Paper; onBack: () => void }) {
  const abstract = paper.abstract ?? paper.summary ?? "No abstract is available for this paper yet.";

  return (
    <div className="space-y-3">
      <button
        type="button"
        onClick={onBack}
        className="mb-1 inline-flex items-center gap-1 font-label-md text-[12px] text-on-surface-variant hover:text-on-surface"
      >
        <span className="material-symbols-outlined text-[18px]">arrow_back</span>
        Back to papers
      </button>

      <section className="grid grid-cols-1 gap-4 rounded-[4px] border border-outline-variant bg-surface-container-lowest p-5 shadow-sm md:grid-cols-[1fr_150px]">
        <div>
          <h1 className="max-w-4xl font-headline-lg text-[30px] leading-[1.08] text-on-surface md:text-[34px]">
            {paper.title}
          </h1>
          <p className="mt-3 font-body-sm text-[13px] text-on-surface">
            {truncateAuthors(paper.authors, paper.source)}
          </p>
        </div>
        <div>
          <p className="font-label-md text-[12px] text-on-surface">Score</p>
          <div className="mt-2">
            <ScoreMeter score={paper.relevance_score} showPercent />
          </div>
        </div>
      </section>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[minmax(0,1fr)_350px]">
        <section className="rounded-[4px] border border-outline-variant bg-surface-container-lowest p-5 shadow-sm">
          <h2 className="font-title-lg text-[20px] font-semibold text-on-surface">Abstract</h2>
          <div className="mt-3 space-y-4 font-body-sm text-[14px] leading-relaxed text-on-surface">
            {abstract.split(/\n{2,}/).map((paragraph, index) => (
              <p key={index}>{paragraph}</p>
            ))}
          </div>

          <h2 className="mt-6 font-title-lg text-[18px] font-semibold text-on-surface">Keywords</h2>
          <div className="mt-3">
            <PaperTags tags={paper.tags} />
          </div>
        </section>

        <aside className="h-fit rounded-[4px] border border-outline-variant bg-surface-container-lowest p-5 shadow-sm">
          <dl className="space-y-4 font-body-sm text-[14px] text-on-surface">
            <div>
              <dt className="font-semibold">Publication Date</dt>
              <dd>{formatPublicationDate(paper.publication_date)}</dd>
            </div>
            <div>
              <dt className="font-semibold">Journal/Conference</dt>
              <dd>{paper.source}</dd>
            </div>
            <div>
              <dt className="font-semibold">Digital Object Identifier (DOI)</dt>
              <dd>{paper.doi ?? paper.arxiv_id ?? "Not available"}</dd>
            </div>
          </dl>
          <a
            href={paper.source_url || (paper.arxiv_id ? `https://arxiv.org/pdf/${paper.arxiv_id}` : "#")}
            target="_blank"
            rel="noreferrer"
            className="mt-5 flex w-full items-center justify-center rounded-[4px] bg-primary px-4 py-2.5 font-label-md text-[13px] text-on-primary hover:bg-primary-container hover:text-on-primary-container"
          >
            Download PDF
          </a>
        </aside>
      </div>
    </div>
  );
}

export default function ChairPapers() {
  const { id } = useParams<{ id: string }>();
  const chairId = Number(id);
  const { user } = useAuth();

  const [chair, setChair] = useState<Chair | null>(null);
  const [papers, setPapers] = useState<Paper[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [syncState, setSyncState] = useState<SyncState>("idle");
  const [syncError, setSyncError] = useState<string | null>(null);
  const [sortKey, setSortKey] = useState<SortKey>("relevance_score");
  const [sortDir, setSortDir] = useState<SortDir>("desc");
  const [search, setSearch] = useState("");
  const [selectedPaper, setSelectedPaper] = useState<Paper | null>(null);
  const documentPapers = useMemo(
    () => (chair?.documents ?? []).filter((doc) => doc.kind === "paper"),
    [chair],
  );

  useEffect(() => {
    if (!chairId) return;
    setLoading(true);
    Promise.all([getChair(chairId), listPapers({ chair_id: chairId, limit: 200 })])
      .then(([nextChair, nextPapers]) => {
        setChair(nextChair);
        setPapers(nextPapers);
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

  const filtered = useMemo(() => {
    let rows = papers;
    if (search) {
      const q = search.toLowerCase();
      rows = rows.filter(
        (paper) =>
          paper.title.toLowerCase().includes(q) ||
          paper.authors.some((author) => author.toLowerCase().includes(q)) ||
          paper.tags.some((tag) => tag.toLowerCase().includes(q)),
      );
    }
    return [...rows].sort((a, b) => {
      let av: number | string;
      let bv: number | string;
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
  }, [papers, search, sortKey, sortDir]);

  function toggleSort(key: SortKey) {
    if (sortKey === key) {
      setSortDir((current) => (current === "asc" ? "desc" : "asc"));
      return;
    }
    setSortKey(key);
    setSortDir("desc");
  }

  return (
    <div className="flex min-h-screen flex-col bg-surface-bright">
      <TopBar
        title={chair?.name ?? "Lehrstuhl für Distributed Intelligence"}
        showSearch
        searchValue={search}
        onSearchChange={setSearch}
        searchPlaceholder="Search papers, authors, topics..."
      />

      <main className="flex-1 overflow-y-auto px-4 py-5 md:px-8 lg:px-14">
        <div className="mx-auto max-w-[1120px] space-y-5">
          {user && (
            <div className="flex justify-end">
              <SyncButton state={syncState} onClick={handleSync} />
            </div>
          )}

          {syncState === "error" && syncError && (
            <div className="rounded-[4px] bg-error-container px-4 py-3 font-body-sm text-[13px] text-on-error-container">
              {syncError}
            </div>
          )}

          {loading && (
            <div className="flex justify-center py-24">
              <div className="h-8 w-8 rounded-full border-2 border-outline-variant border-t-primary animate-spin" />
            </div>
          )}

          {error && (
            <div className="rounded-[4px] bg-error-container p-6 font-body-md text-on-error-container">
              {error}
            </div>
          )}

          {!loading && !error && selectedPaper && (
            <PaperDetail paper={selectedPaper} onBack={() => setSelectedPaper(null)} />
          )}

          {!loading && !error && !selectedPaper && (
            <>
              {papers.length === 0 && documentPapers.length === 0 && (
                <div className="flex flex-col items-center justify-center gap-3 py-24 text-on-surface-variant">
                  <span className="material-symbols-outlined text-[48px]">article</span>
                  <p className="font-body-lg">No papers yet.</p>
                </div>
              )}

              {(papers.length > 0 || documentPapers.length > 0) && (
                <div className="overflow-x-auto">
                  <div className="grid min-w-[900px] grid-cols-[minmax(300px,1fr)_170px_70px_190px_100px] gap-4 px-4 pb-2">
                    <SortHeader
                      label="Title"
                      active={sortKey === "title"}
                      dir={sortDir}
                      onClick={() => toggleSort("title")}
                    />
                    <span className="font-label-md text-[11px] uppercase tracking-[0.04em] text-on-surface-variant">
                      Authors
                    </span>
                    <SortHeader
                      label="Year"
                      active={sortKey === "publication_date"}
                      dir={sortDir}
                      onClick={() => toggleSort("publication_date")}
                    />
                    <span className="font-label-md text-[11px] uppercase tracking-[0.04em] text-on-surface-variant">
                      Tags
                    </span>
                    <SortHeader
                      label="Score"
                      active={sortKey === "relevance_score"}
                      dir={sortDir}
                      onClick={() => toggleSort("relevance_score")}
                    />
                  </div>

                  <div className="min-w-[900px] space-y-1">
                    {papers.length > 0
                      ? filtered.map((paper) => (
                          <Fragment key={paper.id}>
                            <button
                              type="button"
                              onClick={() => setSelectedPaper(paper)}
                              className="grid w-full grid-cols-[minmax(300px,1fr)_170px_70px_190px_100px] items-center gap-4 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-4 py-2.5 text-left shadow-sm transition hover:shadow-md"
                            >
                              <div className="min-w-0">
                                <p className="truncate font-body-sm text-[14px] font-semibold text-on-surface">
                                  {paper.title}
                                </p>
                                <p className="truncate font-body-sm text-[12px] text-on-surface">
                                  {truncateAuthors(paper.authors, paper.source)}
                                </p>
                              </div>
                              <p className="truncate font-body-sm text-[12px] text-on-surface-variant">
                                {paper.authors.slice(0, 2).join(", ") || "-"}
                              </p>
                              <p className="font-body-sm text-[14px] text-on-surface">
                                {formatYear(paper.publication_date)}
                              </p>
                              <PaperTags tags={paper.tags} />
                              <ScoreMeter score={paper.relevance_score} />
                            </button>
                          </Fragment>
                        ))
                      : documentPapers.map((doc) => <DocumentPaperRow key={doc.id} doc={doc} />)}
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </main>
    </div>
  );
}
