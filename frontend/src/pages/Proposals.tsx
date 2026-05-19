import { useEffect, useState } from "react";
import { useSearchParams } from "react-router-dom";
import TopBar from "../components/TopBar";
import AiInsightChip from "../components/AiInsightChip";
import { listTheses, type Thesis } from "../api/theses";
import { listChairs, type Chair } from "../api/chairs";

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString("de-DE", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function ProposalCard({ thesis, chairName }: { thesis: Thesis; chairName?: string }) {
  return (
    <article className="bg-surface rounded-xl border border-outline-variant p-stack-md hover:shadow-[0px_4px_20px_rgba(26,54,93,0.08)] transition-shadow duration-300 flex flex-col h-full">
      <div className="flex justify-between items-start mb-stack-sm">
        <div className="flex gap-2 items-center flex-wrap">
          {thesis.source === "openalex" ? (
            <AiInsightChip label="OpenAlex" />
          ) : thesis.source === "professor" ? (
            <span className="inline-flex items-center px-2 py-1 rounded-full bg-primary-fixed/20 text-primary font-label-md text-[10px]">
              Professor
            </span>
          ) : (
            <span className="inline-flex items-center px-2 py-1 rounded-full bg-surface-container-high text-on-surface-variant font-label-md text-[10px]">
              Student
            </span>
          )}
          <span className="font-label-md text-label-md text-on-surface-variant">
            {formatDate(thesis.created_at)}
          </span>
        </div>
      </div>

      <h3 className="font-title-lg text-title-lg text-on-background mb-2 line-clamp-2">
        {thesis.title}
      </h3>

      {chairName && (
        <div className="flex items-center gap-2 mb-stack-md">
          <span className="material-symbols-outlined text-on-surface-variant text-[16px]">
            account_balance
          </span>
          <span className="font-label-md text-label-md text-on-surface-variant truncate">
            {chairName}
          </span>
        </div>
      )}

      <p className="font-body-sm text-body-sm text-on-surface-variant mb-stack-md flex-1 line-clamp-4">
        {thesis.abstract}
      </p>

      <div className="flex gap-3 mt-auto pt-stack-sm border-t border-outline-variant/50">
        <button className="flex-1 py-2 px-4 rounded-lg bg-primary text-on-primary font-label-md text-label-md hover:bg-primary-container hover:text-on-primary-container transition-colors text-center">
          Details
        </button>
      </div>
    </article>
  );
}

export default function Proposals() {
  const [searchParams] = useSearchParams();
  const filterChairId = searchParams.get("chair_id")
    ? Number(searchParams.get("chair_id"))
    : null;

  const [theses, setTheses] = useState<Thesis[]>([]);
  const [chairs, setChairs] = useState<Chair[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [search, setSearch] = useState("");

  useEffect(() => {
    setLoading(true);
    Promise.all([listTheses(), listChairs()])
      .then(([t, c]) => { setTheses(t); setChairs(c); })
      .catch((e) => setError(e instanceof Error ? e.message : "Fehler beim Laden"))
      .finally(() => setLoading(false));
  }, []);

  const chairMap = Object.fromEntries(chairs.map((c) => [c.id, c.name]));

  const filtered = theses.filter((t) => {
    const matchesChair = filterChairId == null || t.chair_id === filterChairId;
    const lower = search.toLowerCase();
    const matchesSearch =
      !lower ||
      t.title.toLowerCase().includes(lower) ||
      t.abstract.toLowerCase().includes(lower) ||
      (t.chair_id && chairMap[t.chair_id]?.toLowerCase().includes(lower));
    return matchesChair && matchesSearch;
  });

  const [featured, ...rest] = filtered;

  const activeChairName = filterChairId ? chairMap[filterChairId] : null;

  return (
    <div className="flex flex-col min-h-screen bg-background">
      <TopBar showSearch={false} />

      <main className="flex-1 px-4 md:px-margin-desktop py-stack-lg max-w-container-max mx-auto w-full">
        {/* Header */}
        <div className="mb-stack-lg flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div>
            <h2 className="font-headline-lg text-headline-lg-mobile md:text-headline-lg text-on-background mb-2">
              Forschungsvorschläge
            </h2>
            <p className="font-body-md text-body-md text-on-surface-variant">
              {activeChairName
                ? `Gefiltert nach: ${activeChairName}`
                : "Alle verfügbaren Themenvorschläge"}
            </p>
          </div>
          <div className="flex gap-3">
            <div className="relative">
              <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant">
                search
              </span>
              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Vorschläge durchsuchen…"
                className="pl-10 pr-4 py-2 rounded-lg border border-outline-variant bg-surface focus:border-primary font-body-sm text-body-sm text-on-surface w-full md:w-64 transition-all outline-none"
              />
            </div>
          </div>
        </div>

        {/* Loading */}
        {loading && (
          <div className="flex justify-center py-24">
            <div className="w-10 h-10 border-2 border-outline-variant border-t-primary rounded-full animate-spin" />
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="bg-error-container text-on-error-container rounded-xl p-6 font-body-md mb-6">
            {error}
          </div>
        )}

        {/* Empty */}
        {!loading && !error && theses.length === 0 && (
          <div className="flex flex-col items-center justify-center py-24 gap-4 text-on-surface-variant">
            <span className="material-symbols-outlined text-[48px]">description</span>
            <p className="font-body-lg">Noch keine Vorschläge verfügbar.</p>
            <p className="font-body-sm">Professoren können Themen über die Admin-Seite einreichen.</p>
          </div>
        )}

        {/* No results for filter */}
        {!loading && !error && theses.length > 0 && filtered.length === 0 && (
          <div className="flex flex-col items-center justify-center py-24 gap-4 text-on-surface-variant">
            <span className="material-symbols-outlined text-[48px]">search_off</span>
            <p className="font-body-lg">Keine Vorschläge gefunden.</p>
          </div>
        )}

        {/* Grid */}
        {!loading && !error && filtered.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-gutter">
            {/* Featured */}
            {featured && (
              <article className="bg-surface rounded-xl border border-outline-variant p-stack-md hover:shadow-[0px_4px_20px_rgba(26,54,93,0.08)] transition-shadow duration-300 flex flex-col h-full lg:col-span-2 relative overflow-hidden">
                <div className="absolute top-0 right-0 w-32 h-32 bg-primary-container opacity-10 rounded-bl-full -z-10" />

                <div className="flex justify-between items-start mb-stack-sm">
                  <div className="flex gap-2 items-center flex-wrap">
                    {featured.source === "professor" && (
                      <AiInsightChip label="Professor" />
                    )}
                    <span className="font-label-md text-label-md text-on-surface-variant">
                      {formatDate(featured.created_at)}
                    </span>
                  </div>
                </div>

                <h3 className="font-title-lg text-title-lg text-on-background mb-2">
                  {featured.title}
                </h3>

                {featured.chair_id && chairMap[featured.chair_id] && (
                  <div className="flex items-center gap-2 mb-stack-md">
                    <span className="material-symbols-outlined text-on-surface-variant text-[16px]">
                      account_balance
                    </span>
                    <span className="font-label-md text-label-md text-on-surface-variant">
                      {chairMap[featured.chair_id]}
                    </span>
                  </div>
                )}

                <p className="font-body-sm text-body-sm text-on-surface-variant mb-stack-md flex-1 line-clamp-4">
                  {featured.abstract}
                </p>

                <div className="flex gap-3 mt-auto pt-stack-sm border-t border-outline-variant/50">
                  <button className="flex-1 py-2 px-4 rounded-lg bg-primary text-on-primary font-label-md text-label-md hover:bg-primary-container hover:text-on-primary-container transition-colors text-center">
                    Details ansehen
                  </button>
                </div>
              </article>
            )}

            {rest.map((thesis) => (
              <ProposalCard
                key={thesis.id}
                thesis={thesis}
                chairName={thesis.chair_id ? chairMap[thesis.chair_id] : undefined}
              />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
