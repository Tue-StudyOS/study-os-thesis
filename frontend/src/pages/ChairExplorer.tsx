import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import TopBar from "../components/TopBar";
import { listChairs, getChair, type Chair } from "../api/chairs";
import { listPapers, triggerScrape, type Paper } from "../api/papers";
import { listTheses, type Thesis } from "../api/theses";

type SyncState = "idle" | "running" | "done" | "error";

const latestPublicationLimit = 15;
const tagColors = ["bg-sky-500", "bg-emerald-500", "bg-orange-400", "bg-amber-500", "bg-slate-500"];

const fallbackTopicHints = [
  ["computer vision", ["vision", "scene", "image", "3d", "reconstruction", "segmentation"]],
  ["autonomous systems", ["autonomous", "driving", "robot", "vehicle", "control"]],
  ["generative models", ["generative", "gan", "vae", "diffusion", "synthesis"]],
  ["self-supervised learning", ["self-supervised", "unannotated", "representation"]],
  ["machine learning", ["machine learning", "learning", "model"]],
  ["robotics", ["robotics", "robot", "motion", "perception"]],
  ["synthetic data", ["synthetic", "data generation", "dataset"]],
] as const;

function titleCase(value: string) {
  return value.replace(/\b\w/g, (letter) => letter.toUpperCase());
}

function inferTopicsFromText(text: string) {
  const normalized = text.toLowerCase();
  return fallbackTopicHints
    .filter(([, hints]) => hints.some((hint) => normalized.includes(hint)))
    .map(([topic]) => topic);
}

function formatPaperYear(publicationDate: string | null) {
  if (!publicationDate) return "n.d.";
  return new Date(publicationDate).getFullYear().toString();
}

function formatPublicationDate(iso: string | null): string {
  if (!iso) return "Unknown";
  return new Intl.DateTimeFormat("en", { month: "long", year: "numeric" }).format(new Date(iso));
}

function formatAuthors(authors: string[], source: string) {
  if (authors.length === 0) return source;
  const shown = authors.slice(0, 3).join(", ");
  const more = authors.length > 3 ? ` +${authors.length - 3}` : "";
  return `${shown}${more}`;
}

function scoreCount(score: number): number {
  return Math.max(0, Math.min(5, Math.round(score * 5)));
}

function ScoreMeter({ score }: { score: number }) {
  const count = scoreCount(score);

  return (
    <div className="min-w-[92px]">
      <div className="flex items-end justify-between gap-3">
        <span className="font-label-md text-[14px] font-semibold text-on-surface">{count}</span>
        <span className="font-body-sm text-[12px] text-on-surface-variant">{count}/5</span>
      </div>
      <div className="mt-1 h-1.5 overflow-hidden rounded-full bg-surface-container-high">
        <div className="h-full rounded-full bg-primary" style={{ width: `${(count / 5) * 100}%` }} />
      </div>
    </div>
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

function PaperDetail({ paper, onBack }: { paper: Paper; onBack: () => void }) {
  const abstract = paper.abstract ?? paper.summary ?? "No abstract is available for this paper yet.";

  return (
    <section className="space-y-4">
      <button
        type="button"
        onClick={onBack}
        className="inline-flex items-center gap-2 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-3 py-1.5 font-label-md text-[12px] text-on-surface hover:bg-surface-container"
      >
        <span className="material-symbols-outlined text-[18px]">arrow_back</span>
        Back to Chair
      </button>

      <div className="grid grid-cols-1 gap-4 rounded-[6px] border border-outline-variant bg-surface-container-lowest p-5 shadow-sm md:grid-cols-[1fr_160px]">
        <div>
          <h1 className="max-w-4xl font-headline-lg text-[30px] font-semibold leading-[1.08] text-on-surface md:text-[34px]">
            {paper.title}
          </h1>
          <p className="mt-3 font-body-sm text-[13px] text-on-surface">
            {formatAuthors(paper.authors, paper.source)}
          </p>
        </div>
        <div>
          <p className="font-label-md text-[12px] text-on-surface">Score</p>
          <div className="mt-2">
            <ScoreMeter score={paper.relevance_score} />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[minmax(0,1fr)_340px]">
        <section className="rounded-[6px] border border-outline-variant bg-surface-container-lowest p-5 shadow-sm">
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

        <aside className="h-fit rounded-[6px] border border-outline-variant bg-surface-container-lowest p-5 shadow-sm">
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
              <dd>{paper.doi ?? "Not available"}</dd>
            </div>
          </dl>
          <a
            href={paper.source_url || "#"}
            target="_blank"
            rel="noreferrer"
            className="mt-5 flex w-full items-center justify-center rounded-[4px] bg-primary px-4 py-2.5 font-label-md text-[13px] text-on-primary hover:bg-primary-container hover:text-on-primary-container"
          >
            Open Paper
          </a>
        </aside>
      </div>
    </section>
  );
}

function professorName(chair: Chair) {
  return (chair.professor_title ? `${chair.professor_title} ` : "") + chair.professor_name;
}

function ChairDetailPanel({
  chairId,
  onClose,
  onProposals,
  onPapers,
}: {
  chairId: number;
  onClose: () => void;
  onProposals: (id: number) => void;
  onPapers: (id: number) => void;
}) {
  const [chair, setChair] = useState<Chair | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    getChair(chairId)
      .then(setChair)
      .catch((e) => setError(e instanceof Error ? e.message : "Fehler"))
      .finally(() => setLoading(false));
  }, [chairId]);

  return (
    <>
      <div className="fixed inset-0 z-40 bg-black/35 backdrop-blur-[3px]" onClick={onClose} />
      <aside className="fixed right-0 top-0 z-50 flex h-full w-full max-w-[560px] flex-col overflow-hidden bg-surface shadow-2xl">
        <div className="flex h-[86px] items-center justify-between border-b border-outline-variant px-7">
          <h2 className="truncate pr-5 font-headline-md text-[28px] font-semibold text-on-surface">
            {loading ? "Lädt..." : chair?.name ?? "Lehrstuhl"}
          </h2>
          <button
            onClick={onClose}
            className="shrink-0 rounded-full p-2 text-on-surface hover:bg-surface-container-high"
            aria-label="Close details"
          >
            <span className="material-symbols-outlined text-[28px]">close</span>
          </button>
        </div>

        {loading && (
          <div className="flex flex-1 items-center justify-center">
            <div className="h-8 w-8 rounded-full border-2 border-outline-variant border-t-primary animate-spin" />
          </div>
        )}

        {error && (
          <div className="flex flex-1 items-center justify-center p-7">
            <p className="font-body-md text-error">{error}</p>
          </div>
        )}

        {chair && !loading && (
          <div className="flex-1 overflow-y-auto px-7 py-8">
            <div className="space-y-7">
              <div className="flex items-center gap-3 text-on-surface-variant">
                <span className="material-symbols-outlined text-[22px]">person</span>
                <span className="font-body-md text-[18px]">{professorName(chair)}</span>
              </div>

              {chair.website_url && (
                <a
                  href={chair.website_url}
                  target="_blank"
                  rel="noreferrer"
                  className="grid grid-cols-[26px_1fr] gap-4 break-words font-body-md text-[18px] leading-snug text-primary hover:underline"
                >
                  <span className="material-symbols-outlined text-[24px]">open_in_new</span>
                  <span>{chair.website_url}</span>
                </a>
              )}

              <section>
                <h3 className="font-title-lg text-[20px] font-semibold text-on-surface">Beschreibung</h3>
                <p className="mt-3 font-body-md text-[18px] leading-relaxed text-on-surface-variant">
                  {chair.short_description}
                </p>
              </section>
            </div>
          </div>
        )}

        {chair && (
          <div className="border-t border-outline-variant p-7">
            <div className="flex flex-col gap-3">
              <button
                onClick={() => onPapers(chair.id)}
                className="flex w-full items-center justify-center gap-3 rounded-[4px] bg-secondary-container px-4 py-4 font-label-md text-[14px] text-on-secondary-container hover:opacity-90"
              >
                <span className="material-symbols-outlined text-[22px]">article</span>
                Alle Papers ansehen
              </button>
              <button
                onClick={() => onProposals(chair.id)}
                className="flex w-full items-center justify-center gap-3 rounded-[4px] bg-primary px-4 py-4 font-label-md text-[14px] text-on-primary hover:bg-primary-container hover:text-on-primary-container"
              >
                <span className="material-symbols-outlined text-[22px]">description</span>
                Proposals für diesen Lehrstuhl ansehen
              </button>
            </div>
          </div>
        )}
      </aside>
    </>
  );
}

export default function ChairExplorer() {
  const { chairParam } = useParams<{ chairParam: string }>();
  const [chairs, setChairs] = useState<Chair[]>([]);
  const [papers, setPapers] = useState<Paper[]>([]);
  const [paperTotal, setPaperTotal] = useState(0);
  const [paperCountsByChair, setPaperCountsByChair] = useState<Record<number, number>>({});
  const [theses, setTheses] = useState<Thesis[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [syncState, setSyncState] = useState<SyncState>("idle");
  const [syncError, setSyncError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [latestSearch, setLatestSearch] = useState("");
  const [latestPage, setLatestPage] = useState(1);
  const [selectedPaper, setSelectedPaper] = useState<Paper | null>(null);
  const [selectedChairId, setSelectedChairId] = useState<number | null>(null);
  const navigate = useNavigate();
  const routeChairId = chairParam?.startsWith("chairID=")
    ? Number(chairParam.replace("chairID=", ""))
    : null;

  useEffect(() => {
    Promise.all([listChairs(), listTheses(100)])
      .then(([nextChairs, nextTheses]) => {
        setChairs(nextChairs);
        setTheses(nextTheses);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Fehler beim Laden der Lehrstühle"))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    if (chairs.length === 0) {
      setPaperCountsByChair({});
      return;
    }

    Promise.all(
      chairs.map((chair) =>
        listPapers({ chair_id: chair.id, limit: 1 })
          .then((chairPapers) => [chair.id, chairPapers.total] as const)
          .catch(() => [chair.id, 0] as const),
      ),
    ).then((counts) => {
      setPaperCountsByChair(Object.fromEntries(counts));
    });
  }, [chairs]);

  const filtered = useMemo(
    () =>
      chairs.filter(
        (chair) =>
          chair.name.toLowerCase().includes(search.toLowerCase()) ||
          professorName(chair).toLowerCase().includes(search.toLowerCase()) ||
          chair.short_description.toLowerCase().includes(search.toLowerCase()),
      ),
    [chairs, search],
  );

  const featured = routeChairId ? chairs.find((chair) => chair.id === routeChairId) ?? null : null;
  const visiblePapers = papers.length > 0 ? papers : [];
  const publicationCount = paperTotal;
  const activeProjects = featured ? theses.filter((thesis) => thesis.chair_id === featured.id).length : 0;
  // TODO: Replace this hard-coded fallback when chair team-member scraping lands.
  const teamMembers = 25;
  // TODO: Add citation_count to the paper API once a citation source is available.
  const labCitations = papers.reduce((total) => total + (0 satisfies number), 0);

  useEffect(() => {
    if (!featured) {
      setPapers([]);
      setPaperTotal(0);
      return;
    }
    setLatestSearch("");
    setLatestPage(1);
    setSelectedPaper(null);
  }, [featured]);

  useEffect(() => {
    if (!featured) return;
    listPapers({
      chair_id: featured.id,
      limit: latestPublicationLimit,
      offset: (latestPage - 1) * latestPublicationLimit,
    })
      .then((result) => {
        setPapers(result.items);
        setPaperTotal(result.total);
      })
      .catch((e) => setError(e instanceof Error ? e.message : "Fehler beim Laden der Papers"));
  }, [featured, latestPage]);

  const newestPapers = useMemo(
    () =>
      visiblePapers
        .slice()
        .sort(
          (a, b) =>
            (b.publication_date ?? "").localeCompare(a.publication_date ?? "") ||
            b.id - a.id,
        ),
    [visiblePapers],
  );

  const filteredLatestPapers = useMemo(() => {
    const query = latestSearch.trim().toLowerCase();
    if (!query) return newestPapers;
    return newestPapers.filter(
      (paper) =>
        paper.title.toLowerCase().includes(query) ||
        paper.source.toLowerCase().includes(query) ||
        paper.authors.some((author) => author.toLowerCase().includes(query)) ||
        paper.tags.some((tag) => tag.toLowerCase().includes(query)),
    );
  }, [latestSearch, newestPapers]);
  const latestPageCount = Math.max(1, Math.ceil(paperTotal / latestPublicationLimit));
  const safeLatestPage = Math.min(latestPage, latestPageCount);
  const visibleLatestPapers = filteredLatestPapers;
  const latestSearchActive = latestSearch.trim().length > 0;
  const currentPageStart = paperTotal === 0 ? 0 : (safeLatestPage - 1) * latestPublicationLimit + 1;
  const currentPageEnd = Math.min(safeLatestPage * latestPublicationLimit, paperTotal);

  useEffect(() => {
    setLatestPage(1);
  }, [latestSearch]);

  function goToProposals(chairId?: number) {
    navigate(chairId ? `/proposals?chair_id=${chairId}` : "/proposals");
  }

  async function handleSyncPapers() {
    if (!featured || syncState === "running") return;
    setSyncState("running");
    setSyncError(null);
    try {
      const job = await triggerScrape(featured.id);
      if (job.status === "success") {
        const fresh = await listPapers({
          chair_id: featured.id,
          limit: latestPublicationLimit,
          offset: (safeLatestPage - 1) * latestPublicationLimit,
        });
        setPapers(fresh.items);
        setPaperTotal(fresh.total);
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

  return (
    <div className="flex min-h-screen flex-col bg-surface-bright">
      <TopBar
        title={featured?.name ?? "Lehrstuhl-Explorer"}
        showSearch
        searchValue={search}
        onSearchChange={setSearch}
        searchPlaceholder={featured ? "Search research, projects, topics..." : "Search chairs, professors, topics..."}
      />

      {selectedChairId !== null && (
        <ChairDetailPanel
          chairId={selectedChairId}
          onClose={() => setSelectedChairId(null)}
          onProposals={(id) => {
            setSelectedChairId(null);
            goToProposals(id);
          }}
          onPapers={(id) => {
            setSelectedChairId(null);
            navigate(`/chairs/chairID=${id}`);
          }}
        />
      )}

      <main className="flex-1 overflow-y-auto px-4 py-6 md:px-8 lg:px-10 xl:px-14">
        <div className="mx-auto max-w-[1440px] space-y-8">
          {loading && (
            <div className="flex justify-center py-24">
              <div className="h-10 w-10 rounded-full border-2 border-outline-variant border-t-primary animate-spin" />
            </div>
          )}

          {error && (
            <div className="rounded-[4px] bg-error-container p-6 font-body-md text-on-error-container">
              {error}
            </div>
          )}

          {!loading && !error && chairs.length === 0 && (
            <div className="flex flex-col items-center justify-center gap-3 py-24 text-on-surface-variant">
              <span className="material-symbols-outlined text-[48px]">school</span>
              <p className="font-body-lg">Noch keine Lehrstühle erfasst.</p>
              <p className="font-body-sm">Admins können Lehrstühle über die Admin-Seite anlegen.</p>
            </div>
          )}

          {!loading && !error && !routeChairId && chairs.length > 0 && (
            <>
              <section className="flex flex-col gap-3 md:flex-row md:items-end md:justify-between">
                <div>
                  <h1 className="font-serif text-[48px] font-bold leading-none text-on-surface md:text-[64px]">
                    Lehrstuhl-Explorer
                  </h1>
                  <p className="mt-2 max-w-2xl font-body-md text-[16px] text-on-surface-variant">
                    Browse all research chairs and open a focused repository dashboard for each chair.
                  </p>
                </div>
                <span className="font-label-md text-[13px] text-on-surface-variant">
                  {filtered.length} chair{filtered.length === 1 ? "" : "s"}
                </span>
              </section>

              {filtered.length === 0 && (
                <div className="rounded-[6px] border border-outline-variant bg-surface-container-lowest p-6 font-body-sm text-on-surface-variant">
                  No chairs match your search.
                </div>
              )}

              {filtered.length > 0 && (
                <section className="grid grid-cols-1 gap-4 lg:grid-cols-2 xl:grid-cols-3">
                  {filtered.map((chair) => {
                    const paperCount = paperCountsByChair[chair.id] ?? 0;
                    const chairProjects = theses.filter((thesis) => thesis.chair_id === chair.id).length;
                    const inferredTopics = inferTopicsFromText(
                      chair.short_description,
                    ).slice(0, 3);

                    return (
                      <article
                        key={chair.id}
                        className="flex min-h-[260px] flex-col rounded-[6px] border border-outline-variant bg-surface-container-lowest p-5 shadow-sm transition hover:shadow-md"
                      >
                        <div className="flex-1">
                          <h2 className="font-title-lg text-[22px] font-semibold leading-tight text-on-surface">
                            {chair.name}
                          </h2>
                          <p className="mt-2 flex items-center gap-2 font-body-sm text-[14px] text-on-surface-variant">
                            <span className="material-symbols-outlined text-[18px]">person</span>
                            {professorName(chair)}
                          </p>
                          <p className="mt-4 line-clamp-4 font-body-sm text-[14px] leading-relaxed text-on-surface">
                            {chair.short_description}
                          </p>

                          {inferredTopics.length > 0 && (
                            <div className="mt-4 flex flex-wrap gap-1.5">
                              {inferredTopics.map((topic) => (
                                <span
                                  key={topic}
                                  className="rounded-[4px] bg-surface-container-high px-2 py-0.5 font-label-md text-[10px] text-on-surface"
                                >
                                  #{titleCase(topic).replace(/\s+/g, "")}
                                </span>
                              ))}
                            </div>
                          )}
                        </div>

                        <div className="mt-5 grid grid-cols-2 gap-2 border-t border-outline-variant pt-4 text-center">
                          <div>
                            <p className="font-title-lg text-[24px] leading-none text-on-surface">{paperCount}</p>
                            <p className="mt-1 font-label-md text-[11px] text-on-surface-variant">Papers</p>
                          </div>
                          <div className="border-l border-outline-variant">
                            <p className="font-title-lg text-[24px] leading-none text-on-surface">{chairProjects}</p>
                            <p className="mt-1 font-label-md text-[11px] text-on-surface-variant">Projects</p>
                          </div>
                        </div>

                        <div className="mt-5 flex flex-wrap gap-2">
                          <button
                            onClick={() => navigate(`/chairs/chairID=${chair.id}`)}
                            className="flex flex-1 items-center justify-center gap-2 rounded-[4px] bg-primary px-3 py-2.5 font-label-md text-[12px] text-on-primary hover:bg-primary-container hover:text-on-primary-container"
                          >
                            View Chair
                            <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
                          </button>
                          <button
                            onClick={() => navigate(`/chairs/chairID=${chair.id}`)}
                            className="flex flex-1 items-center justify-center gap-2 rounded-[4px] border border-outline-variant px-3 py-2.5 font-label-md text-[12px] text-on-surface hover:bg-surface-container"
                          >
                            Papers
                            <span className="material-symbols-outlined text-[16px]">article</span>
                          </button>
                        </div>
                      </article>
                    );
                  })}
                </section>
              )}
            </>
          )}

          {!loading && !error && routeChairId && !featured && (
            <div className="rounded-[6px] border border-outline-variant bg-surface-container-lowest p-6 font-body-md text-on-surface-variant">
              Chair not found.
            </div>
          )}

          {!loading && !error && featured && (
            <>
              {selectedPaper ? (
                <PaperDetail paper={selectedPaper} onBack={() => setSelectedPaper(null)} />
              ) : (
                <>
              <section className="space-y-4">
                <button
                  onClick={() => navigate("/chairs")}
                  className="inline-flex items-center gap-2 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-3 py-1.5 font-label-md text-[12px] text-on-surface hover:bg-surface-container"
                >
                  <span className="material-symbols-outlined text-[18px]">arrow_back</span>
                  Back to Chairs
                </button>

                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                  <h1 className="max-w-[760px] font-serif text-[34px] font-bold leading-[1.02] tracking-normal text-on-surface md:text-[44px] xl:text-[50px]">
                    {featured.name}
                  </h1>
                  <div className="flex shrink-0 flex-col items-start gap-2 lg:items-end">
                    <button
                      onClick={handleSyncPapers}
                      disabled={syncState === "running"}
                      className="flex min-w-[112px] items-center justify-center gap-2 rounded-[4px] bg-primary px-4 py-2.5 font-label-md text-[12px] text-on-primary shadow-sm disabled:opacity-70"
                    >
                      {syncState === "running" ? (
                        <span className="h-4 w-4 shrink-0 rounded-full border-2 border-on-primary/30 border-t-on-primary animate-spin" />
                      ) : (
                        <span className="material-symbols-outlined text-[16px]">check_circle</span>
                      )}
                      {syncState === "running" ? "Syncing" : "Synced"}
                    </button>
                    {syncState === "error" && syncError && (
                      <p className="max-w-[240px] text-left font-label-md text-[11px] text-error lg:text-right">
                        {syncError}
                      </p>
                    )}
                  </div>
                </div>

                <div className="grid gap-6 xl:grid-cols-[minmax(0,1.55fr)_minmax(380px,0.85fr)] xl:items-stretch">
                  <div className="max-w-none">
                    <h2 className="font-title-lg text-[16px] font-semibold text-on-surface">About</h2>
                    <p className="mt-1 max-w-[860px] font-body-md text-[15px] font-semibold leading-snug text-on-surface">
                      {featured.short_description}
                    </p>
                  </div>

                  <div className="grid grid-cols-2 overflow-hidden rounded-[6px] border border-outline-variant bg-surface-container-lowest shadow-sm">
                    {[
                      [publicationCount.toLocaleString(), "Publications"],
                      [activeProjects.toLocaleString(), "Active Projects"],
                      [labCitations.toLocaleString(), "Lab Citations"],
                      [teamMembers.toLocaleString(), "Team Members"],
                    ].map(([value, label], index) => (
                      <div
                        key={label}
                        className={[
                          "flex min-h-[94px] flex-col items-center justify-center px-5 py-3",
                          index % 2 === 1 ? "border-l border-outline-variant" : "",
                          index > 1 ? "border-t border-outline-variant" : "",
                        ].join(" ")}
                      >
                        <p className="font-title-lg text-[30px] leading-none text-on-surface">{value}</p>
                        <p className="mt-2 font-label-md text-[12px] text-on-surface-variant">{label}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </section>

              <section>
                <div className="mb-3 flex items-center justify-between gap-4">
                  <h2 className="font-headline-md text-[26px] font-semibold text-on-surface">
                    Latest Publications
                  </h2>
                </div>

                {newestPapers.length > 0 && (
                  <div className="mb-3 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                    <label className="relative block w-full md:max-w-[420px]">
                      <span className="material-symbols-outlined pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-[18px] text-on-surface-variant">
                        search
                      </span>
                      <input
                        value={latestSearch}
                        onChange={(event) => setLatestSearch(event.target.value)}
                        placeholder="Search publications, authors, tags..."
                        className="h-10 w-full rounded-[6px] border border-outline-variant bg-surface-container-lowest pl-10 pr-3 font-body-sm text-[13px] text-on-surface outline-none focus:border-primary"
                      />
                    </label>
                    <span className="font-body-sm text-[12px] text-on-surface-variant">
                      {latestSearchActive
                        ? `${filteredLatestPapers.length} result${filteredLatestPapers.length === 1 ? "" : "s"} on this page`
                        : `${paperTotal} result${paperTotal === 1 ? "" : "s"}`}
                    </span>
                  </div>
                )}

                <div className="overflow-x-auto">
                  {newestPapers.length > 0 && (
                    <div className="grid min-w-[900px] grid-cols-[minmax(300px,1fr)_210px_70px_220px_120px] gap-4 px-4 pb-2">
                      <span className="font-label-md text-[11px] uppercase tracking-[0.04em] text-on-surface-variant">
                        Title
                      </span>
                      <span className="font-label-md text-[11px] uppercase tracking-[0.04em] text-on-surface-variant">
                        Authors
                      </span>
                      <span className="font-label-md text-[11px] uppercase tracking-[0.04em] text-on-surface-variant">
                        Year
                      </span>
                      <span className="font-label-md text-[11px] uppercase tracking-[0.04em] text-on-surface-variant">
                        Tags
                      </span>
                      <span className="flex items-center gap-1 font-label-md text-[11px] uppercase tracking-[0.04em] text-on-surface-variant">
                        Score
                        <span className="material-symbols-outlined text-[18px]">arrow_downward</span>
                      </span>
                    </div>
                  )}

                  {newestPapers.length > 0 && filteredLatestPapers.length > 0 && (
                    <div className="min-w-[900px] space-y-1">
                      {visibleLatestPapers.map((paper) => (
                        <button
                          key={paper.id}
                          onClick={() => setSelectedPaper(paper)}
                          className="grid min-h-[78px] w-full grid-cols-[minmax(300px,1fr)_210px_70px_220px_120px] items-center gap-4 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-4 py-2.5 text-left shadow-sm transition hover:shadow-md"
                        >
                          <div className="min-w-0">
                            <p className="truncate font-body-sm text-[14px] font-semibold text-on-surface">
                              {paper.title}
                            </p>
                            <p className="truncate font-body-sm text-[12px] text-on-surface">
                              {formatAuthors(paper.authors, paper.source)}
                            </p>
                          </div>
                          <p className="truncate font-body-sm text-[12px] text-on-surface-variant">
                            {paper.authors.slice(0, 2).join(", ") || "-"}
                          </p>
                          <p className="font-body-sm text-[14px] text-on-surface">
                            {formatPaperYear(paper.publication_date)}
                          </p>
                          <PaperTags tags={paper.tags} />
                          <ScoreMeter score={paper.relevance_score} />
                        </button>
                      ))}
                    </div>
                  )}

                  {newestPapers.length > 0 && filteredLatestPapers.length === 0 && (
                    <div className="min-w-[900px] rounded-[4px] border border-outline-variant bg-surface-container-lowest px-4 py-4 font-body-sm text-[13px] text-on-surface-variant">
                      No publications match your search.
                    </div>
                  )}

                  {newestPapers.length === 0 && (
                    <div className="px-4 py-3 font-body-sm text-[13px] text-on-surface-variant">
                      No papers available for this chair yet.
                    </div>
                  )}
                </div>

                {newestPapers.length > 0 && (
                  <div className="mt-3 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
                    <span className="font-body-sm text-[12px] text-on-surface-variant">
                      {latestSearchActive
                        ? `Showing ${filteredLatestPapers.length} page-local match${filteredLatestPapers.length === 1 ? "" : "es"} from ${currentPageStart}-${currentPageEnd} of ${paperTotal}`
                        : `Showing ${currentPageStart}-${currentPageEnd} of ${paperTotal}`}
                    </span>
                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => setLatestPage((page) => Math.max(1, page - 1))}
                        disabled={safeLatestPage === 1}
                        className="inline-flex items-center gap-1 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-3 py-1.5 font-label-md text-[12px] text-on-surface hover:bg-surface-container disabled:cursor-not-allowed disabled:opacity-45"
                      >
                        <span className="material-symbols-outlined text-[16px]">chevron_left</span>
                        Previous
                      </button>
                      <span className="min-w-[72px] text-center font-label-md text-[12px] text-on-surface-variant">
                        {safeLatestPage} / {latestPageCount}
                      </span>
                      <button
                        onClick={() => setLatestPage((page) => Math.min(latestPageCount, page + 1))}
                        disabled={safeLatestPage === latestPageCount}
                        className="inline-flex items-center gap-1 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-3 py-1.5 font-label-md text-[12px] text-on-surface hover:bg-surface-container disabled:cursor-not-allowed disabled:opacity-45"
                      >
                        Next
                        <span className="material-symbols-outlined text-[16px]">chevron_right</span>
                      </button>
                    </div>
                  </div>
                )}
              </section>

                </>
              )}

            </>
          )}
        </div>
      </main>
    </div>
  );
}
