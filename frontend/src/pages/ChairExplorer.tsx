import { useEffect, useMemo, useRef, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import TopBar from "../components/TopBar";
import { ChairDetailHero, ChairListView, professorName } from "../components/chairs";
import { LatestPublicationsTable, PaperDetailPanel } from "../components/publications";
import { listChairs, getChair, type Chair } from "../api/chairs";
import { listJobs, type Job } from "../api/jobs";
import { waitForJobTree } from "../api/jobEvents";
import { listPapers, triggerScrape, type Paper } from "../api/papers";
import { listTheses, type Thesis } from "../api/theses";
import {
  chairIdFromScrapeJob,
  getChairSyncStatus,
  runningSyncMapFromJobs,
  setChairSyncStatus,
  type ChairSyncMap,
} from "../utils/chairSync";

const latestPublicationLimit = 15;

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
  const [syncByChairId, setSyncByChairId] = useState<ChairSyncMap>({});
  const [search, setSearch] = useState("");
  const [latestSearch, setLatestSearch] = useState("");
  const [latestPage, setLatestPage] = useState(1);
  const [selectedPaper, setSelectedPaper] = useState<Paper | null>(null);
  const [selectedChairId, setSelectedChairId] = useState<number | null>(null);
  const visibleChairIdRef = useRef<number | null>(null);
  const latestPageRef = useRef(1);
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
  const projectCountsByChair = useMemo(() => {
    const counts: Record<number, number> = {};
    for (const thesis of theses) {
      if (thesis.chair_id == null) continue;
      counts[thesis.chair_id] = (counts[thesis.chair_id] ?? 0) + 1;
    }
    return counts;
  }, [theses]);

  const featured = routeChairId ? chairs.find((chair) => chair.id === routeChairId) ?? null : null;
  const featuredSync = getChairSyncStatus(syncByChairId, featured?.id);
  const visiblePapers = papers.length > 0 ? papers : [];
  const publicationCount = paperTotal;
  const activeProjects = featured ? theses.filter((thesis) => thesis.chair_id === featured.id).length : 0;
  // TODO: Replace this hard-coded fallback when chair team-member scraping lands.
  const teamMembers = 25;
  // TODO: Add citation_count to the paper API once a citation source is available.
  const labCitations = papers.reduce((total) => total + (0 satisfies number), 0);

  useEffect(() => {
    visibleChairIdRef.current = featured?.id ?? null;
  }, [featured]);

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

  const latestPageCount = Math.max(1, Math.ceil(paperTotal / latestPublicationLimit));
  const safeLatestPage = Math.min(latestPage, latestPageCount);

  useEffect(() => {
    latestPageRef.current = safeLatestPage;
  }, [safeLatestPage]);

  useEffect(() => {
    setLatestPage(1);
  }, [latestSearch]);

  function goToProposals(chairId?: number) {
    navigate(chairId ? `/proposals?chair_id=${chairId}` : "/proposals");
  }

  async function refreshSyncedChair(chairId: number) {
    const countResult = await listPapers({ chair_id: chairId, limit: 1 });
    setPaperCountsByChair((current) => ({
      ...current,
      [chairId]: countResult.total,
    }));
    if (visibleChairIdRef.current !== chairId) return;

    const fresh = await listPapers({
      chair_id: chairId,
      limit: latestPublicationLimit,
      offset: (latestPageRef.current - 1) * latestPublicationLimit,
    });
    if (visibleChairIdRef.current === chairId) {
      setPapers(fresh.items);
      setPaperTotal(fresh.total);
    }
  }

  async function settleSyncJob(chairId: number, job: Job) {
    if (job.status === "success") {
      await refreshSyncedChair(chairId);
      setSyncByChairId((current) => setChairSyncStatus(current, chairId, { state: "done", error: null }));
      return;
    }

    setSyncByChairId((current) =>
      setChairSyncStatus(current, chairId, { state: "error", error: job.error ?? "Scrape job failed" }),
    );
  }

  useEffect(() => {
    let cancelled = false;

    async function restoreActiveScrapes() {
      try {
        const [pending, started] = await Promise.all([
          listJobs({ type: "scrape_chair", status: "pending" }),
          listJobs({ type: "scrape_chair", status: "started" }),
        ]);
        if (cancelled) return;

        const activeJobs = [...pending, ...started];
        setSyncByChairId((current) => ({
          ...current,
          ...runningSyncMapFromJobs(activeJobs),
        }));

        for (const activeJob of activeJobs) {
          const chairId = chairIdFromScrapeJob(activeJob);
          if (chairId == null) continue;
          void waitForJobTree(activeJob.id).then((job) => {
            if (!cancelled) void settleSyncJob(chairId, job);
          });
        }
      } catch {
        // Active job rehydration is best-effort; normal page loading still works without it.
      }
    }

    void restoreActiveScrapes();

    return () => {
      cancelled = true;
    };
  }, []);

  async function handleSyncPapers(chairId: number) {
    if (syncByChairId[chairId]?.state === "running") return;
    setSyncByChairId((current) => setChairSyncStatus(current, chairId, { state: "running", error: null }));
    try {
      const job = await triggerScrape(chairId);
      await settleSyncJob(chairId, job);
    } catch (e) {
      setSyncByChairId((current) =>
        setChairSyncStatus(current, chairId, {
          state: "error",
          error: e instanceof Error ? e.message : "Unknown error",
        }),
      );
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

              <ChairListView
                chairs={filtered}
                paperCountsByChair={paperCountsByChair}
                projectCountsByChair={projectCountsByChair}
                onOpenChair={(chairId) => navigate(`/chairs/chairID=${chairId}`)}
              />
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
                <PaperDetailPanel paper={selectedPaper} onBack={() => setSelectedPaper(null)} />
              ) : (
                <>
              <ChairDetailHero
                chair={featured}
                publicationCount={publicationCount}
                activeProjects={activeProjects}
                labCitations={labCitations}
                teamMembers={teamMembers}
                syncState={featuredSync.state}
                syncError={featuredSync.error}
                onBack={() => navigate("/chairs")}
                onSync={() => handleSyncPapers(featured.id)}
              />

              <LatestPublicationsTable
                papers={newestPapers}
                total={paperTotal}
                search={latestSearch}
                page={safeLatestPage}
                pageCount={latestPageCount}
                pageSize={latestPublicationLimit}
                onSearchChange={setLatestSearch}
                onPageChange={setLatestPage}
                onSelectPaper={setSelectedPaper}
              />

                </>
              )}

            </>
          )}
        </div>
      </main>
    </div>
  );
}
