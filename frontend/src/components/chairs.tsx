import type { Chair } from "../api/chairs";

export type SyncState = "idle" | "running" | "done" | "error";

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

export function professorName(chair: Chair) {
  return (chair.professor_title ? `${chair.professor_title} ` : "") + chair.professor_name;
}

export function ChairListView({
  chairs,
  paperCountsByChair,
  projectCountsByChair,
  onOpenChair,
}: {
  chairs: Chair[];
  paperCountsByChair: Record<number, number>;
  projectCountsByChair: Record<number, number>;
  onOpenChair: (chairId: number) => void;
}) {
  return (
    <>
      {chairs.length === 0 && (
        <div className="rounded-[6px] border border-outline-variant bg-surface-container-lowest p-6 font-body-sm text-on-surface-variant">
          No chairs match your search.
        </div>
      )}

      {chairs.length > 0 && (
        <section className="grid grid-cols-1 gap-4 lg:grid-cols-2 xl:grid-cols-3">
          {chairs.map((chair) => {
            const inferredTopics = inferTopicsFromText(chair.short_description).slice(0, 3);

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
                    <p className="font-title-lg text-[24px] leading-none text-on-surface">
                      {paperCountsByChair[chair.id] ?? 0}
                    </p>
                    <p className="mt-1 font-label-md text-[11px] text-on-surface-variant">Papers</p>
                  </div>
                  <div className="border-l border-outline-variant">
                    <p className="font-title-lg text-[24px] leading-none text-on-surface">
                      {projectCountsByChair[chair.id] ?? 0}
                    </p>
                    <p className="mt-1 font-label-md text-[11px] text-on-surface-variant">Projects</p>
                  </div>
                </div>

                <div className="mt-5 flex flex-wrap gap-2">
                  <button
                    onClick={() => onOpenChair(chair.id)}
                    className="flex flex-1 items-center justify-center gap-2 rounded-[4px] bg-primary px-3 py-2.5 font-label-md text-[12px] text-on-primary hover:bg-primary-container hover:text-on-primary-container"
                  >
                    View Chair
                    <span className="material-symbols-outlined text-[16px]">arrow_forward</span>
                  </button>
                  <button
                    onClick={() => onOpenChair(chair.id)}
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
  );
}

export function ChairDetailHero({
  chair,
  publicationCount,
  activeProjects,
  labCitations,
  teamMembers,
  syncState,
  syncError,
  onBack,
  onSync,
}: {
  chair: Chair;
  publicationCount: number;
  activeProjects: number;
  labCitations: number;
  teamMembers: number;
  syncState: SyncState;
  syncError: string | null;
  onBack: () => void;
  onSync: () => void;
}) {
  return (
    <section className="space-y-4">
      <button
        onClick={onBack}
        className="inline-flex items-center gap-2 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-3 py-1.5 font-label-md text-[12px] text-on-surface hover:bg-surface-container"
      >
        <span className="material-symbols-outlined text-[18px]">arrow_back</span>
        Back to Chairs
      </button>

      <div className="flex flex-col gap-4 lg:flex-row lg:items-start lg:justify-between">
        <h1 className="max-w-[760px] font-serif text-[34px] font-bold leading-[1.02] tracking-normal text-on-surface md:text-[44px] xl:text-[50px]">
          {chair.name}
        </h1>
        <div className="flex shrink-0 flex-col items-start gap-2 lg:items-end">
          <button
            onClick={onSync}
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
            {chair.short_description}
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
  );
}
