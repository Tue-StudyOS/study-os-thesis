import type { Paper } from "../api/papers";
import { formatAuthors, formatPaperYear, formatPublicationDate, scoreCount } from "../utils/papers";

const tagColors = ["bg-sky-500", "bg-emerald-500", "bg-orange-400", "bg-amber-500", "bg-slate-500"];

export function ScoreMeter({ score }: { score: number }) {
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

export function PaperTags({ tags }: { tags: string[] }) {
  const shown = tags.length > 0 ? tags.slice(0, 3) : ["Causal AI", "Machine Learning"];
  return (
    <div className="flex flex-wrap gap-1">
      {shown.map((tag, index) => (
        <span key={`${tag}-${index}`} className={`${tagColors[index % tagColors.length]} rounded-full px-2 py-0.5 font-label-md text-[10px] text-white`}>
          {tag}
        </span>
      ))}
    </div>
  );
}

export function PaperDetailPanel({ paper, onBack }: { paper: Paper; onBack: () => void }) {
  const abstract = paper.abstract ?? paper.summary ?? "No abstract is available for this paper yet.";
  return (
    <section className="space-y-4">
      <button type="button" onClick={onBack} className="inline-flex items-center gap-2 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-3 py-1.5 font-label-md text-[12px] text-on-surface hover:bg-surface-container">
        <span className="material-symbols-outlined text-[18px]">arrow_back</span>
        Back to Chair
      </button>
      <div className="grid grid-cols-1 gap-4 rounded-[6px] border border-outline-variant bg-surface-container-lowest p-5 shadow-sm md:grid-cols-[1fr_160px]">
        <div>
          <h1 className="max-w-4xl font-headline-lg text-[30px] font-semibold leading-[1.08] text-on-surface md:text-[34px]">{paper.title}</h1>
          <p className="mt-3 font-body-sm text-[13px] text-on-surface">{formatAuthors(paper.authors, paper.source)}</p>
        </div>
        <div>
          <p className="font-label-md text-[12px] text-on-surface">Score</p>
          <div className="mt-2"><ScoreMeter score={paper.relevance_score} /></div>
        </div>
      </div>
      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[minmax(0,1fr)_340px]">
        <section className="rounded-[6px] border border-outline-variant bg-surface-container-lowest p-5 shadow-sm">
          <h2 className="font-title-lg text-[20px] font-semibold text-on-surface">Abstract</h2>
          <div className="mt-3 space-y-4 font-body-sm text-[14px] leading-relaxed text-on-surface">
            {abstract.split(/\n{2,}/).map((paragraph, index) => <p key={index}>{paragraph}</p>)}
          </div>
          <h2 className="mt-6 font-title-lg text-[18px] font-semibold text-on-surface">Keywords</h2>
          <div className="mt-3"><PaperTags tags={paper.tags} /></div>
        </section>
        <aside className="h-fit rounded-[6px] border border-outline-variant bg-surface-container-lowest p-5 shadow-sm">
          <dl className="space-y-4 font-body-sm text-[14px] text-on-surface">
            <div><dt className="font-semibold">Publication Date</dt><dd>{formatPublicationDate(paper.publication_date)}</dd></div>
            <div><dt className="font-semibold">Journal/Conference</dt><dd>{paper.source}</dd></div>
            <div><dt className="font-semibold">Digital Object Identifier (DOI)</dt><dd>{paper.doi ?? "Not available"}</dd></div>
          </dl>
          <a href={paper.source_url || "#"} target="_blank" rel="noreferrer" className="mt-5 flex w-full items-center justify-center rounded-[4px] bg-primary px-4 py-2.5 font-label-md text-[13px] text-on-primary hover:bg-primary-container hover:text-on-primary-container">
            Open Paper
          </a>
        </aside>
      </div>
    </section>
  );
}

type LatestPublicationsTableProps = {
  papers: Paper[];
  total: number;
  search: string;
  page: number;
  pageCount: number;
  pageSize: number;
  onSearchChange: (value: string) => void;
  onPageChange: (value: number) => void;
  onSelectPaper: (paper: Paper) => void;
};

export function LatestPublicationsTable({ papers, total, search, page, pageCount, pageSize, onSearchChange, onPageChange, onSelectPaper }: LatestPublicationsTableProps) {
  const query = search.trim().toLowerCase();
  const filtered = query
    ? papers.filter((paper) => paper.title.toLowerCase().includes(query) || paper.source.toLowerCase().includes(query) || paper.authors.some((author) => author.toLowerCase().includes(query)) || paper.tags.some((tag) => tag.toLowerCase().includes(query)))
    : papers;
  const searchActive = query.length > 0;
  const start = total === 0 ? 0 : (page - 1) * pageSize + 1;
  const end = Math.min(page * pageSize, total);

  return (
    <section>
      <div className="mb-3 flex items-center justify-between gap-4">
        <h2 className="font-headline-md text-[26px] font-semibold text-on-surface">Latest Publications</h2>
      </div>
      {papers.length > 0 && (
        <div className="mb-3 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
          <label className="relative block w-full md:max-w-[420px]">
            <span className="material-symbols-outlined pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-[18px] text-on-surface-variant">search</span>
            <input value={search} onChange={(event) => onSearchChange(event.target.value)} placeholder="Search publications, authors, tags..." className="h-10 w-full rounded-[6px] border border-outline-variant bg-surface-container-lowest pl-10 pr-3 font-body-sm text-[13px] text-on-surface outline-none focus:border-primary" />
          </label>
          <span className="font-body-sm text-[12px] text-on-surface-variant">{searchActive ? `${filtered.length} result${filtered.length === 1 ? "" : "s"} on this page` : `${total} result${total === 1 ? "" : "s"}`}</span>
        </div>
      )}
      <div className="overflow-x-auto">
        {papers.length > 0 && (
          <div className="grid min-w-[900px] grid-cols-[minmax(300px,1fr)_210px_70px_220px_120px] gap-4 px-4 pb-2">
            {["Title", "Authors", "Year", "Tags", "Score"].map((label) => (
              <span key={label} className="font-label-md text-[11px] uppercase tracking-[0.04em] text-on-surface-variant">{label}</span>
            ))}
          </div>
        )}
        {papers.length > 0 && filtered.length > 0 && (
          <div className="min-w-[900px] space-y-1">
            {filtered.map((paper) => (
              <button key={paper.id} onClick={() => onSelectPaper(paper)} className="grid min-h-[78px] w-full grid-cols-[minmax(300px,1fr)_210px_70px_220px_120px] items-center gap-4 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-4 py-2.5 text-left shadow-sm transition hover:shadow-md">
                <div className="min-w-0">
                  <p className="truncate font-body-sm text-[14px] font-semibold text-on-surface">{paper.title}</p>
                  <p className="truncate font-body-sm text-[12px] text-on-surface">{formatAuthors(paper.authors, paper.source)}</p>
                </div>
                <p className="truncate font-body-sm text-[12px] text-on-surface-variant">{paper.authors.slice(0, 2).join(", ") || "-"}</p>
                <p className="font-body-sm text-[14px] text-on-surface">{formatPaperYear(paper.publication_date)}</p>
                <PaperTags tags={paper.tags} />
                <ScoreMeter score={paper.relevance_score} />
              </button>
            ))}
          </div>
        )}
        {papers.length > 0 && filtered.length === 0 && <div className="min-w-[900px] rounded-[4px] border border-outline-variant bg-surface-container-lowest px-4 py-4 font-body-sm text-[13px] text-on-surface-variant">No publications match your search.</div>}
        {papers.length === 0 && <div className="px-4 py-3 font-body-sm text-[13px] text-on-surface-variant">No papers available for this chair yet.</div>}
      </div>
      {papers.length > 0 && (
        <div className="mt-3 flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
          <span className="font-body-sm text-[12px] text-on-surface-variant">{searchActive ? `Showing ${filtered.length} page-local match${filtered.length === 1 ? "" : "es"} from ${start}-${end} of ${total}` : `Showing ${start}-${end} of ${total}`}</span>
          <div className="flex items-center gap-2">
            <button onClick={() => onPageChange(Math.max(1, page - 1))} disabled={page === 1} className="inline-flex items-center gap-1 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-3 py-1.5 font-label-md text-[12px] text-on-surface hover:bg-surface-container disabled:cursor-not-allowed disabled:opacity-45"><span className="material-symbols-outlined text-[16px]">chevron_left</span>Previous</button>
            <span className="min-w-[72px] text-center font-label-md text-[12px] text-on-surface-variant">{page} / {pageCount}</span>
            <button onClick={() => onPageChange(Math.min(pageCount, page + 1))} disabled={page === pageCount} className="inline-flex items-center gap-1 rounded-[4px] border border-outline-variant bg-surface-container-lowest px-3 py-1.5 font-label-md text-[12px] text-on-surface hover:bg-surface-container disabled:cursor-not-allowed disabled:opacity-45">Next<span className="material-symbols-outlined text-[16px]">chevron_right</span></button>
          </div>
        </div>
      )}
    </section>
  );
}
