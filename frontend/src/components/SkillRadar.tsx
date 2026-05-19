/**
 * SVG hexagonal radar chart.
 *
 * Fixed 6 axes. Accepts `courses` from the student profile and maps them
 * to axes via keyword heuristics. Falls back to zeros when no data is available.
 *
 * Axes: Programming, Statistics, Databases, Projects, Web, Versioning
 * Scale: 0 (Unaware) → 4 (Expert), derived from German grades (1.0 best → 5.0 fail)
 */

import type { StudentCourse } from "../api/students";

const SIZE = 400;
const CX = SIZE / 2;
const CY = SIZE / 2;
const LEVELS = 4;
const MAX_R = 160;

const AXES = [
  "Programming",
  "Statistics",
  "Databases",
  "Projects",
  "Web",
  "Versioning",
] as const;

const N = AXES.length;

/** Keywords that map a course name to an axis (case-insensitive). */
const AXIS_KEYWORDS: Record<(typeof AXES)[number], string[]> = {
  Programming: [
    // English
    "programm", "algorithm", "software", "coding", "java", "python", "c++",
    "functional", "object", "compiler", "operating system", "computer architecture",
    "data structure", "concurren", "parallel", "embedded", "system",
    // German
    "informatik", "programmier", "algorithmen", "datenstruktur", "betriebssystem",
    "rechnerarchitektur", "compilerbau", "nebenläufig", "parallele", "eingebettete",
    "grundlagen der", "einführung in die", "objektorientiert", "funktional",
    "softwareentwicklung", "systemnahe", "hardwarenahe", "rechnerorganisation",
  ],
  Statistics: [
    // English
    "statistic", "probabilit", "machine learning", "deep learning", "neural",
    "data science", "analysis", "linear algebra", "calculus", "optimization",
    "regression", "inference", "bayesian", "stochastic",
    // German
    "mathematik", "statistik", "wahrscheinlichkeit", "stochastik",
    "maschinelles lernen", "künstliche intelligenz", "ki ", "analysis",
    "lineare algebra", "numerik", "diskrete mathematik", "logik",
    "optimierung", "mustererkennung", "signalverarbeitung", "algebra",
    "differentialrechnung", "integrationsrechnung", "modellierung",
  ],
  Databases: [
    // English
    "database", "sql", "nosql", "storage", "data engineer",
    "information retrieval", "data warehouse", "cloud", "data management",
    "query", "relational",
    // German
    "datenbank", "datenmanagement", "datenhaltung", "informationssystem",
    "informationsretrieval", "wissensrepräsentation", "datenverwaltung",
    "cloud", "big data",
  ],
  Projects: [
    // English
    "project", "lab", "thesis", "research", "engineering", "systems",
    "distributed", "seminar", "workshop", "capstone", "team",
    // German
    "praktikum", "projekt", "seminar", "abschlussarbeit", "forschung",
    "systemtechnik", "verteilte", "teamarbeit", "softwaretechnik",
    "softwareprojekt", "praxisseminar", "teamprojekt", "bachelorarbeit",
    "masterarbeit", "ingenieur", "systementwurf",
  ],
  Web: [
    // English
    "web", "internet", "network", "http", "frontend", "backend",
    "api", "rest", "ui", "ux", "mobile", "app", "fullstack",
    "browser", "html", "css", "javascript", "react", "security",
    // German
    "netzwerk", "rechnernetze", "kommunikation", "protokoll",
    "sicherheit", "kryptograph", "it-sicherheit", "datenschutz",
    "netzwerktechnik", "telekommunikation", "internet der dinge",
  ],
  Versioning: [
    // English
    "git", "version", "devops", "agile", "scrum", "software quality",
    "testing", "ci", "cd", "deployment", "software engineering",
    "software process", "requirements",
    // German
    "softwarequalität", "testen", "qualitätssicherung", "agile",
    "versionierung", "softwareprozess", "anforderungsanalyse",
    "softwareentwurf", "entwurfsmuster", "design pattern",
    "software-engineering", "softwaremanagement",
  ],
};

/** Convert a German grade string (e.g. "1,3") to a 0-4 skill score. */
function gradeToScore(grade: string | null): number {
  if (!grade) return 2; // neutral default
  const normalised = grade.replace(",", ".");
  const val = parseFloat(normalised);
  if (isNaN(val)) return grade.toLowerCase() === "bestanden" ? 2.5 : 1;
  // German grade 1.0 → score 4, 5.0 → score 0
  return Math.max(0, Math.min(4, ((5 - val) / 4) * 4));
}

/** Derive 6-axis scores from a list of student courses. */
export function coursesToRadarData(courses: StudentCourse[]): number[] {
  const axisSums: number[] = Array(N).fill(0);
  const axisCounts: number[] = Array(N).fill(0);

  for (const course of courses) {
    const lower = course.course_name.toLowerCase();
    AXES.forEach((axis, idx) => {
      const matched = AXIS_KEYWORDS[axis].some((kw) => lower.includes(kw));
      if (matched) {
        axisSums[idx] += gradeToScore(course.grade);
        axisCounts[idx] += 1;
      }
    });
  }

  // Compute a global average score across all matched courses as fallback
  // for axes with no keyword matches, so the chart is never completely empty.
  const allScores = courses.map((c) => gradeToScore(c.grade));
  const globalAvg =
    allScores.length > 0
      ? allScores.reduce((a, b) => a + b, 0) / allScores.length
      : 2;
  // Scale down global avg for unmatched axes (student likely has some exposure).
  const fallback = Math.max(0.5, globalAvg * 0.6);

  return AXES.map((_, idx) =>
    axisCounts[idx] > 0 ? axisSums[idx] / axisCounts[idx] : fallback,
  );
}

// Target profile (fixed — typical master thesis requirements)
const TARGET_DATA = [3.5, 3.5, 3.0, 3.5, 2.5, 3.0];

function polar(angle: number, r: number): [number, number] {
  const rad = (angle - 90) * (Math.PI / 180);
  return [CX + r * Math.cos(rad), CY + r * Math.sin(rad)];
}

function buildPoints(data: number[]): string {
  return data
    .map((v, i) => {
      const angle = (360 / N) * i;
      const r = (v / LEVELS) * MAX_R;
      const [x, y] = polar(angle, r);
      return `${x},${y}`;
    })
    .join(" ");
}

function ringPoints(level: number): string {
  const r = (level / LEVELS) * MAX_R;
  return Array.from({ length: N }, (_, i) => {
    const [x, y] = polar((360 / N) * i, r);
    return `${x},${y}`;
  }).join(" ");
}

const LEVEL_LABELS = ["Unaware", "Aware", "Working", "Practitioner", "Expert"];

interface SkillRadarProps {
  /** Derived from student courses via coursesToRadarData(). Falls back to zeros. */
  currentData?: number[];
}

export default function SkillRadar({ currentData }: SkillRadarProps) {
  const current = currentData ?? Array(N).fill(0);

  return (
    <div className="flex flex-col lg:flex-row gap-8 items-center">
      <div className="w-full lg:w-2/3 aspect-square max-w-[480px] relative">
        <svg viewBox={`0 0 ${SIZE} ${SIZE}`} className="w-full h-full">
          {/* Grid rings */}
          {Array.from({ length: LEVELS }, (_, i) => i + 1).map((level) => (
            <polygon
              key={level}
              points={ringPoints(level)}
              fill="none"
              stroke="#e3e2e6"
              strokeWidth="1"
            />
          ))}

          {/* Axis lines */}
          {AXES.map((_, i) => {
            const angle = (360 / N) * i;
            const [x, y] = polar(angle, MAX_R);
            return (
              <line key={i} x1={CX} y1={CY} x2={x} y2={y} stroke="#e3e2e6" strokeWidth="1" />
            );
          })}

          {/* Target polygon (blue) */}
          <polygon
            points={buildPoints(TARGET_DATA)}
            fill="rgba(134,160,205,0.15)"
            stroke="#455f88"
            strokeWidth="2"
          />

          {/* Current polygon (red) */}
          <polygon
            points={buildPoints(current)}
            fill="rgba(186,26,26,0.15)"
            stroke="#ba1a1a"
            strokeWidth="2"
          />

          {/* Axis labels */}
          {AXES.map((label, i) => {
            const angle = (360 / N) * i;
            const r = MAX_R + 22;
            const [x, y] = polar(angle, r);
            const anchor = Math.abs(x - CX) < 5 ? "middle" : x > CX ? "start" : "end";
            const dy = y < CY ? "-0.3em" : y > CY ? "1em" : "0.4em";
            return (
              <text
                key={label}
                x={x}
                y={y}
                textAnchor={anchor}
                dy={dy}
                fontSize="12"
                fontFamily="Inter, sans-serif"
                fontWeight="600"
                fill="#43474e"
              >
                {label}
              </text>
            );
          })}

          {/* Level labels along top axis */}
          {Array.from({ length: LEVELS + 1 }, (_, i) => {
            const r = (i / LEVELS) * MAX_R;
            const [x, y] = polar(0, r);
            if (i === 0) return null;
            return (
              <text
                key={i}
                x={x + 4}
                y={y}
                fontSize="9"
                fontFamily="Inter, sans-serif"
                fill="#74777f"
                dominantBaseline="middle"
              >
                {LEVEL_LABELS[i]}
              </text>
            );
          })}
        </svg>
      </div>

      {/* Legend */}
      <div className="flex-1 flex flex-col gap-6">
        <div className="flex flex-col gap-4 bg-surface-container-low p-6 rounded-lg">
          <span className="font-title-lg text-primary font-semibold">Legende</span>
          <div className="flex flex-col gap-3">
            <div className="flex items-center gap-3">
              <div className="w-4 h-4 rounded bg-error border border-error shrink-0" />
              <div>
                <span className="block font-label-md text-on-surface">Aktueller Stand</span>
                <span className="text-body-sm text-on-surface-variant">
                  Basierend auf deinem Transcript
                </span>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-4 h-4 rounded bg-primary-container border border-surface-tint shrink-0" />
              <div>
                <span className="block font-label-md text-on-surface">Zielprofil</span>
                <span className="text-body-sm text-on-surface-variant">
                  Anforderung für Master-Forschung
                </span>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-tertiary-container/10 border border-tertiary-container/20 p-4 rounded-lg flex items-start gap-3">
          <span className="material-symbols-outlined text-tertiary-container mt-0.5">info</span>
          <p className="text-body-sm text-on-tertiary-container font-medium">
            Die Achsen werden aus deinen Kursnamen abgeleitet. Lade dein Transcript hoch, um dein
            persönliches Kompetenzprofil zu sehen.
          </p>
        </div>
      </div>
    </div>
  );
}
