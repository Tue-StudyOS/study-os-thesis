import { useEffect, useMemo, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import TopBar from "../components/TopBar";
import { listChairs, getChair, type Chair } from "../api/chairs";
import { listPapers, triggerScrape, type Paper } from "../api/papers";
import { listTheses, type Thesis } from "../api/theses";

type SyncState = "idle" | "running" | "done" | "error";

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

function topicDescription(topic: string) {
  if (topic.includes("vision")) return "Visual perception, reconstruction, and scene understanding.";
  if (topic.includes("autonomous")) return "Methods for autonomous perception and control.";
  if (topic.includes("generative")) return "Generative modelling and synthetic data methods.";
  if (topic.includes("self-supervised")) return "Learning from limited or unannotated data.";
  if (topic.includes("robot")) return "Robotic perception, planning, and interaction.";
  if (topic.includes("data")) return "Datasets, data generation, and benchmarks.";
  return "Chair-specific research area inferred from papers.";
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
  const [paperCountsByChair, setPaperCountsByChair] = useState<Record<number, number>>({});
  const [theses, setTheses] = useState<Thesis[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [syncState, setSyncState] = useState<SyncState>("idle");
  const [syncError, setSyncError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
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
        listPapers({ chair_id: chair.id, limit: 200 })
          .then((chairPapers) => [chair.id, chairPapers.length] as const)
          .catch(() => [chair.id, chair.documents.filter((doc) => doc.kind === "paper").length] as const),
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
  const chairDocumentPapers = useMemo(
    () => (featured?.documents ?? []).filter((doc) => doc.kind === "paper"),
    [featured],
  );
  const visiblePapers = papers.length > 0 ? papers : [];
  const publicationCount = Math.max(visiblePapers.length, chairDocumentPapers.length);
  const activeProjects = featured ? theses.filter((thesis) => thesis.chair_id === featured.id).length : 0;
  // TODO: Replace this hard-coded fallback when chair team-member scraping lands.
  const teamMembers = 25;
  // TODO: Add citation_count to the paper API once a citation source is available.
  const labCitations = papers.reduce((total) => total + (0 satisfies number), 0);

  useEffect(() => {
    if (!featured) {
      setPapers([]);
      return;
    }
    listPapers({ chair_id: featured.id, limit: 200 })
      .then(setPapers)
      .catch((e) => setError(e instanceof Error ? e.message : "Fehler beim Laden der Papers"));
  }, [featured]);

  const topicCards = useMemo(
    () => {
      const counts = new Map<string, number>();

      visiblePapers.forEach((paper) => {
        paper.tags.forEach((tag) => {
          counts.set(tag, (counts.get(tag) ?? 0) + 1);
        });
      });

      chairDocumentPapers.forEach((doc) => {
        const inferred = inferTopicsFromText(`${doc.title ?? ""} ${doc.content}`);
        inferred.forEach((topic) => {
          counts.set(topic, Math.max(counts.get(topic) ?? 0, 1));
        });
      });

      if (counts.size === 0 && featured) {
        inferTopicsFromText(featured.short_description).forEach((topic) => {
          counts.set(topic, 0);
        });
      }

      return Array.from(counts.entries())
        .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
        .slice(0, 5)
        .map(([topic, count]) => ({
          title: titleCase(topic),
          description: topicDescription(topic),
          tags: [`#${titleCase(topic).replace(/\s+/g, "")}`],
          papers: count,
        }));
    },
    [chairDocumentPapers, featured, visiblePapers],
  );

  const newestPapers = useMemo(
    () =>
      visiblePapers
        .slice()
        .sort((a, b) => (b.publication_date ?? "").localeCompare(a.publication_date ?? ""))
        .slice(0, 10),
    [visiblePapers],
  );

  const newestDocumentPapers = useMemo(
    () =>
      chairDocumentPapers
        .slice()
        .sort((a, b) => (b.published_year ?? 0) - (a.published_year ?? 0))
        .slice(0, 10),
    [chairDocumentPapers],
  );

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
        const fresh = await listPapers({ chair_id: featured.id, limit: 200 });
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
            navigate(`/chairs/${id}/papers`);
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
                    const chairPapers = chair.documents.filter((doc) => doc.kind === "paper");
                    const paperCount = Math.max(paperCountsByChair[chair.id] ?? 0, chairPapers.length);
                    const chairProjects = theses.filter((thesis) => thesis.chair_id === chair.id).length;
                    const inferredTopics = inferTopicsFromText(
                      `${chair.short_description} ${chairPapers.map((doc) => `${doc.title ?? ""} ${doc.content}`).join(" ")}`,
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
                            onClick={() => navigate(`/chairs/${chair.id}/papers`)}
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
              <section className="space-y-6">
                <button
                  onClick={() => navigate("/chairs")}
                  className="inline-flex items-center gap-2 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-3 py-2 font-label-md text-[12px] text-on-surface hover:bg-surface-container"
                >
                  <span className="material-symbols-outlined text-[18px]">arrow_back</span>
                  Back to Chairs
                </button>

                <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
                  <h1 className="max-w-[920px] font-serif text-[40px] font-bold leading-[1] tracking-normal text-on-surface md:text-[52px] xl:text-[60px]">
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

                <div className="grid gap-8 xl:grid-cols-[minmax(0,1.7fr)_minmax(430px,0.9fr)] xl:items-stretch">
                  <div className="max-w-none">
                    <h2 className="font-title-lg text-[18px] font-semibold text-on-surface">About</h2>
                    <p className="mt-1 max-w-[920px] font-body-md text-[17px] font-semibold leading-snug text-on-surface">
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
                          "flex min-h-[118px] flex-col items-center justify-center px-5 py-4",
                          index % 2 === 1 ? "border-l border-outline-variant" : "",
                          index > 1 ? "border-t border-outline-variant" : "",
                        ].join(" ")}
                      >
                        <p className="font-title-lg text-[36px] leading-none text-on-surface">{value}</p>
                        <p className="mt-2 font-label-md text-[13px] text-on-surface-variant">{label}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </section>

              <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-5">
                {topicCards.map((topic) => (
                  <article
                    key={topic.title}
                    className="flex min-h-[178px] flex-col rounded-[6px] border border-outline-variant bg-surface-container-lowest p-5 shadow-sm"
                  >
                    <h3 className="font-title-lg text-[18px] font-semibold leading-tight text-on-surface">
                      {topic.title}
                    </h3>
                    <p className="mt-2 flex-1 font-body-sm text-[14px] font-semibold leading-snug text-on-surface">
                      {topic.description}
                    </p>
                    <div className="mt-3 flex flex-wrap gap-1">
                      {topic.tags.map((tag) => (
                        <span
                          key={tag}
                          className="rounded-[4px] bg-surface-container-high px-1.5 py-0.5 font-label-md text-[10px] text-on-surface"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                    <div className="mt-3 flex items-center justify-between gap-2">
                      <span className="font-body-sm text-[12px] text-on-surface-variant">
                        {topic.papers} Papers
                      </span>
                      <button
                        onClick={() => navigate(`/chairs/${featured.id}/papers`)}
                        className="rounded-[4px] border border-outline-variant px-2 py-1 font-label-md text-[11px] text-on-surface hover:bg-surface-container"
                      >
                        View Repository
                        <span className="material-symbols-outlined ml-1 text-[12px]">arrow_forward</span>
                      </button>
                    </div>
                  </article>
                ))}
              </section>

              <section>
                <div className="mb-3 flex items-center justify-between gap-4">
                  <h2 className="font-headline-md text-[26px] font-semibold text-on-surface">
                    Latest Publications
                  </h2>
                  <button
                    onClick={() => navigate(`/chairs/${featured.id}/papers`)}
                    className="rounded-[4px] border border-outline-variant px-3 py-1.5 font-label-md text-[12px] text-on-surface hover:bg-surface-container"
                  >
                    View Repository
                    <span className="material-symbols-outlined ml-1 text-[14px]">arrow_forward</span>
                  </button>
                </div>

                <div className="overflow-hidden rounded-[6px] border border-outline-variant bg-surface-container-lowest shadow-sm">
                  {newestPapers.length > 0 && newestPapers.map((paper) => (
                    <button
                      key={paper.id}
                      onClick={() => navigate(`/chairs/${featured.id}/papers`)}
                      className="grid w-full gap-2 border-b border-outline-variant px-4 py-3 text-left last:border-b-0 md:grid-cols-[minmax(0,1fr)_80px_150px]"
                    >
                      <div className="min-w-0">
                        <p className="truncate font-body-sm text-[14px] font-semibold text-on-surface">
                          {paper.title}
                        </p>
                        <p className="truncate font-body-sm text-[12px] text-on-surface-variant">
                          {paper.authors.slice(0, 3).join(", ") || paper.source}
                        </p>
                      </div>
                      <p className="font-body-sm text-[13px] text-on-surface">{formatPaperYear(paper.publication_date)}</p>
                      <p className="font-body-sm text-[12px] text-on-surface-variant md:text-right">
                        {paper.source}
                      </p>
                    </button>
                  ))}

                  {newestPapers.length === 0 && newestDocumentPapers.map((doc) => (
                    <button
                      key={doc.id}
                      onClick={() => navigate(`/chairs/${featured.id}/papers`)}
                      className="grid w-full gap-2 border-b border-outline-variant px-4 py-3 text-left last:border-b-0 md:grid-cols-[minmax(0,1fr)_80px_150px]"
                    >
                      <div className="min-w-0">
                        <p className="truncate font-body-sm text-[14px] font-semibold text-on-surface">
                          {doc.title ?? "Untitled paper"}
                        </p>
                        <p className="truncate font-body-sm text-[12px] text-on-surface-variant">
                          {doc.arxiv_id ? `arXiv:${doc.arxiv_id}` : "Chair document"}
                        </p>
                      </div>
                      <p className="font-body-sm text-[13px] text-on-surface">{doc.published_year ?? "n.d."}</p>
                      <p className="font-body-sm text-[12px] text-on-surface-variant md:text-right">
                        arXiv
                      </p>
                    </button>
                  ))}

                  {newestPapers.length === 0 && newestDocumentPapers.length === 0 && (
                    <div className="px-4 py-3 font-body-sm text-[13px] text-on-surface-variant">
                      No papers available for this chair yet.
                    </div>
                  )}
                </div>
              </section>

            </>
          )}
        </div>
      </main>
    </div>
  );
}
