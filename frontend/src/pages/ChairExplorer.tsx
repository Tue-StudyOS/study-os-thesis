import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import TopBar from "../components/TopBar";
import AiInsightChip from "../components/AiInsightChip";
import { listChairs, getChair, type Chair, type ChairDocument } from "../api/chairs";

// ─── Match circle ─────────────────────────────────────────────────────────────

function MatchCircle({ score, size = "lg" }: { score: number; size?: "sm" | "lg" }) {
  const dim = size === "lg" ? 64 : 44;
  const r = 15.9155;
  const circumference = 2 * Math.PI * r;
  const dash = (score / 100) * circumference;
  const isHigh = score >= 90;
  return (
    <div className="flex flex-col items-end">
      <div
        className="rounded-full border-4 border-surface-container flex items-center justify-center relative bg-surface"
        style={{ width: dim, height: dim }}
      >
        <svg className="absolute inset-0 w-full h-full -rotate-90" viewBox="0 0 36 36">
          <path
            className="text-surface-variant"
            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            fill="none" stroke="currentColor"
            strokeDasharray={`${circumference}, ${circumference}`} strokeWidth="3"
          />
          <path
            style={{ color: isHigh ? "#4cadab" : "#455f88" }}
            d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
            fill="none" stroke="currentColor"
            strokeDasharray={`${dash}, ${circumference}`} strokeWidth="3"
          />
        </svg>
        <span
          className="font-headline-md font-bold"
          style={{ color: isHigh ? "#4cadab" : "#455f88", fontSize: size === "sm" ? 12 : 16 }}
        >
          {score}<span style={{ fontSize: size === "sm" ? 8 : 12 }}>%</span>
        </span>
      </div>
      <span className="font-label-md text-label-md text-on-surface-variant mt-1 text-right">Match</span>
    </div>
  );
}

// ─── Chair detail slide-over ──────────────────────────────────────────────────

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

  const papers = chair?.documents.filter((d) => d.kind === "paper") ?? [];

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/30 z-40 backdrop-blur-sm"
        onClick={onClose}
      />
      {/* Panel */}
      <aside className="fixed right-0 top-0 h-full w-full max-w-lg bg-surface z-50 shadow-2xl flex flex-col overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-outline-variant">
          <h2 className="font-headline-md text-headline-md text-on-surface truncate pr-4">
            {loading ? "Lädt…" : chair?.name ?? "Lehrstuhl"}
          </h2>
          <button
            onClick={onClose}
            className="shrink-0 p-2 rounded-full hover:bg-surface-container-high transition-colors"
          >
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>

        {loading && (
          <div className="flex-1 flex items-center justify-center">
            <div className="w-8 h-8 border-2 border-outline-variant border-t-primary rounded-full animate-spin" />
          </div>
        )}

        {error && (
          <div className="flex-1 flex items-center justify-center p-6">
            <p className="text-error font-body-md">{error}</p>
          </div>
        )}

        {chair && !loading && (
          <div className="flex-1 overflow-y-auto p-6 space-y-6">
            {/* Meta */}
            <div className="flex items-center gap-2 text-on-surface-variant">
              <span className="material-symbols-outlined text-[18px]">person</span>
              <span className="font-body-md text-body-md">
                {(chair.professor_title ? `${chair.professor_title} ` : "") + chair.professor_name}
              </span>
            </div>
            {chair.website_url && (
              <a
                href={chair.website_url}
                target="_blank"
                rel="noreferrer"
                className="flex items-center gap-2 text-primary font-body-sm hover:underline"
              >
                <span className="material-symbols-outlined text-[16px]">open_in_new</span>
                {chair.website_url}
              </a>
            )}

            {/* Description */}
            <div>
              <h3 className="font-title-md text-on-surface font-semibold mb-2">Beschreibung</h3>
              <p className="font-body-md text-body-md text-on-surface-variant leading-relaxed">
                {chair.short_description}
              </p>
            </div>

            {/* Papers */}
            {papers.length > 0 && (
              <div>
                <h3 className="font-title-md text-on-surface font-semibold mb-3 flex items-center gap-2">
                  <span className="material-symbols-outlined text-[18px]">article</span>
                  Publikationen ({papers.length})
                </h3>
                <div className="space-y-3">
                  {papers.map((doc) => (
                    <PaperRow key={doc.id} doc={doc} />
                  ))}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Footer */}
        {chair && (
          <div className="p-6 border-t border-outline-variant flex flex-col gap-2">
            <button
              onClick={() => onPapers(chair.id)}
              className="w-full bg-secondary-container text-on-secondary-container py-3 rounded-lg font-label-md text-label-md flex items-center justify-center gap-2 hover:opacity-90 transition-opacity"
            >
              <span className="material-symbols-outlined text-sm">article</span>
              Alle Papers ansehen
            </button>
            <button
              onClick={() => onProposals(chair.id)}
              className="w-full bg-primary text-on-primary py-3 rounded-lg font-label-md text-label-md flex items-center justify-center gap-2 hover:bg-primary-container hover:text-on-primary-container transition-colors"
            >
              <span className="material-symbols-outlined text-sm">description</span>
              Proposals für diesen Lehrstuhl ansehen
            </button>
          </div>
        )}
      </aside>
    </>
  );
}

function PaperRow({ doc }: { doc: ChairDocument }) {
  return (
    <div className="bg-surface-container-low rounded-lg p-4 border border-outline-variant">
      <div className="flex items-start justify-between gap-2">
        <p className="font-body-sm text-body-sm text-on-surface font-medium line-clamp-2">
          {doc.title ?? "Kein Titel"}
        </p>
        {doc.published_year && (
          <span className="shrink-0 font-label-md text-label-md text-on-surface-variant">
            {doc.published_year}
          </span>
        )}
      </div>
      {doc.arxiv_id && (
        <a
          href={`https://arxiv.org/abs/${doc.arxiv_id}`}
          target="_blank"
          rel="noreferrer"
          className="mt-1 inline-flex items-center gap-1 text-primary font-label-md text-[11px] hover:underline"
          onClick={(e) => e.stopPropagation()}
        >
          <span className="material-symbols-outlined text-[12px]">open_in_new</span>
          arXiv:{doc.arxiv_id}
        </a>
      )}
      <p className="mt-2 font-body-sm text-[11px] text-on-surface-variant line-clamp-3">
        {doc.content}
      </p>
    </div>
  );
}

// ─── Main page ────────────────────────────────────────────────────────────────

export default function ChairExplorer() {
  const [chairs, setChairs] = useState<Chair[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");
  const [selectedChairId, setSelectedChairId] = useState<number | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    listChairs()
      .then(setChairs)
      .catch((e) => setError(e instanceof Error ? e.message : "Fehler beim Laden der Lehrstühle"))
      .finally(() => setLoading(false));
  }, []);

  const filtered = chairs.filter(
    (c) =>
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      ((c.professor_title ? `${c.professor_title} ` : "") + c.professor_name).toLowerCase().includes(search.toLowerCase()) ||
      c.short_description.toLowerCase().includes(search.toLowerCase()),
  );

  const [featured, ...rest] = filtered;

  function goToProposals(chairId?: number) {
    navigate(chairId ? `/proposals?chair_id=${chairId}` : "/proposals");
  }

  return (
    <div className="flex flex-col min-h-screen bg-surface-bright">
      <TopBar title="Lehrstuhl-Explorer" showSearch={false} />

      {selectedChairId !== null && (
        <ChairDetailPanel
          chairId={selectedChairId}
          onClose={() => setSelectedChairId(null)}
          onProposals={(id) => { setSelectedChairId(null); goToProposals(id); }}
          onPapers={(id) => { setSelectedChairId(null); navigate(`/chairs/${id}/papers`); }}
        />
      )}

      <main className="flex-1 overflow-y-auto p-4 md:p-margin-desktop">
        <div className="max-w-container-max mx-auto space-y-stack-lg">
          {/* Header */}
          <section className="flex flex-col md:flex-row justify-between items-start md:items-end gap-4">
            <div>
              <h2 className="font-display-lg text-display-lg text-on-surface mb-2">
                Find Your Academic Match
              </h2>
              <p className="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">
                Entdecke Forschungsgruppen, die zu deinem akademischen Profil passen.
              </p>
            </div>
            <div className="relative">
              <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant text-sm">
                search
              </span>
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Lehrstuhl oder Professor suchen…"
                className="pl-10 pr-4 py-2 rounded-full border border-outline-variant bg-surface-container-lowest font-label-md text-label-md text-on-surface outline-none focus:border-primary w-72 transition-all"
              />
            </div>
          </section>

          {/* Loading */}
          {loading && (
            <div className="flex justify-center py-24">
              <div className="w-10 h-10 border-2 border-outline-variant border-t-primary rounded-full animate-spin" />
            </div>
          )}

          {/* Error */}
          {error && (
            <div className="bg-error-container text-on-error-container rounded-xl p-6 font-body-md">
              {error}
            </div>
          )}

          {/* Empty */}
          {!loading && !error && chairs.length === 0 && (
            <div className="flex flex-col items-center justify-center py-24 gap-4 text-on-surface-variant">
              <span className="material-symbols-outlined text-[48px]">school</span>
              <p className="font-body-lg">Noch keine Lehrstühle erfasst.</p>
              <p className="font-body-sm">Admins können Lehrstühle über die Admin-Seite anlegen.</p>
            </div>
          )}

          {/* Grid */}
          {!loading && !error && filtered.length > 0 && (
            <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-gutter">
              {/* Featured card */}
              {featured && (
                <article
                  className="col-span-1 lg:col-span-2 xl:col-span-2 bg-surface-container-lowest rounded-xl border border-outline-variant p-6 hover-lift flex flex-col relative overflow-hidden group cursor-pointer"
                  onClick={() => setSelectedChairId(featured.id)}
                >
                  <div className="absolute top-0 right-0 w-64 h-64 bg-tertiary-fixed opacity-10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2 group-hover:opacity-20 transition-opacity" />

                  <div className="relative z-10 flex flex-col md:flex-row justify-between items-start gap-4 mb-6">
                    <div>
                      <div className="flex items-center gap-2 mb-2">
                        <AiInsightChip label="Featured" />
                        {featured.documents.filter((d) => d.kind === "paper").length > 0 && (
                          <button
                            onClick={(e) => { e.stopPropagation(); navigate(`/chairs/${featured.id}/papers`); }}
                            className="px-2 py-0.5 rounded-md bg-secondary-container text-on-secondary-fixed-variant font-label-md text-[10px] uppercase tracking-wider hover:opacity-80 transition-opacity"
                          >
                            {featured.documents.filter((d) => d.kind === "paper").length} Papers
                          </button>
                        )}
                      </div>
                      <h3 className="font-headline-md text-headline-md text-on-surface mb-1">
                        {featured.name}
                      </h3>
                      <p className="font-body-md text-body-md text-on-surface-variant flex items-center gap-2">
                        <span className="material-symbols-outlined text-sm">person</span>
                        {(featured.professor_title ? `${featured.professor_title} ` : "") + featured.professor_name}
                      </p>
                    </div>
                    <MatchCircle score={Math.min(99, featured.documents.length * 10 + 60)} />
                  </div>

                  <div className="relative z-10 space-y-4">
                    <p className="font-body-md text-body-md text-on-surface-variant line-clamp-3">
                      {featured.short_description}
                    </p>
                    <div className="flex items-center justify-between border-t border-outline-variant pt-4">
                      <span className="font-body-sm text-body-sm text-on-surface-variant flex items-center gap-1">
                        <span className="material-symbols-outlined text-sm">article</span>
                        {featured.documents.filter((d) => d.kind === "paper").length} Publikationen
                      </span>
                      <button
                        onClick={(e) => { e.stopPropagation(); goToProposals(featured.id); }}
                        className="bg-primary text-on-primary px-5 py-2 rounded-lg font-label-md text-label-md flex items-center gap-2 hover:bg-primary-container transition-colors shadow-sm"
                      >
                        <span className="material-symbols-outlined text-sm">description</span>
                        Proposals
                      </button>
                    </div>
                  </div>
                </article>
              )}

              {/* Standard cards */}
              {rest.map((chair) => (
                <article
                  key={chair.id}
                  className="bg-surface-container-lowest rounded-xl border border-outline-variant p-6 hover-lift flex flex-col cursor-pointer"
                  onClick={() => setSelectedChairId(chair.id)}
                >
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex-1 min-w-0 pr-4">
                      <h3 className="font-title-lg text-title-lg text-on-surface mb-1 leading-tight">
                        {chair.name}
                      </h3>
                      <p className="font-body-sm text-body-sm text-on-surface-variant flex items-center gap-1">
                        <span className="material-symbols-outlined text-xs">person</span>
                        {(chair.professor_title ? `${chair.professor_title} ` : "") + chair.professor_name}
                      </p>
                    </div>
                    <button
                      onClick={(e) => { e.stopPropagation(); navigate(`/chairs/${chair.id}/papers`); }}
                      className="flex items-center gap-1 bg-surface-container px-2 py-1 rounded-md shrink-0 hover:bg-surface-container-high transition-colors"
                    >
                      <span className="material-symbols-outlined text-primary text-sm">article</span>
                      <span className="font-label-md text-label-md text-on-surface">
                        {chair.documents.filter((d) => d.kind === "paper").length}
                      </span>
                    </button>
                  </div>

                  <p className="font-body-sm text-body-sm text-on-surface-variant mb-4 line-clamp-3 flex-1">
                    {chair.short_description}
                  </p>

                  <div className="border-t border-outline-variant pt-4 mt-auto">
                    <button
                      onClick={(e) => { e.stopPropagation(); goToProposals(chair.id); }}
                      className="w-full bg-transparent border border-primary text-primary px-4 py-2 rounded-lg font-label-md text-label-md flex items-center justify-center gap-2 hover:bg-surface-container transition-colors"
                    >
                      <span className="material-symbols-outlined text-sm">description</span>
                      Proposals ansehen
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
