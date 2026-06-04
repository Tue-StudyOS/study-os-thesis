/**
 * SVG hexagonal radar chart — data-driven.
 *
 * Accepts computed skill items from GET /api/students/me/skills and renders
 * the top N as radar axes.  The keyword heuristic previously in this file has
 * been replaced by real backend skill computation.
 *
 * Scale: 0 (Unaware) → 4 (Expert), derived from the API score (0.0-1.0).
 */

import type { UserSkillItem } from "../api/skills";

const SIZE = 400;
const CX = SIZE / 2;
const CY = SIZE / 2;
const LEVELS = 4;
const MAX_R = 160;

const LEVEL_LABELS = ["Unaware", "Aware", "Working", "Practitioner", "Expert"];

function polar(angle: number, r: number): [number, number] {
  const rad = (angle - 90) * (Math.PI / 180);
  return [CX + r * Math.cos(rad), CY + r * Math.sin(rad)];
}

function buildPoints(data: number[], n: number): string {
  return data
    .map((v, i) => {
      const angle = (360 / n) * i;
      const r = (v / LEVELS) * MAX_R;
      const [x, y] = polar(angle, r);
      return `${x},${y}`;
    })
    .join(" ");
}

function ringPoints(level: number, n: number): string {
  const r = (level / LEVELS) * MAX_R;
  return Array.from({ length: n }, (_, i) => {
    const [x, y] = polar((360 / n) * i, r);
    return `${x},${y}`;
  }).join(" ");
}

/** Capitalize the first letter of each word for display. */
function toDisplayLabel(skill: string): string {
  return skill
    .split(/[\s_-]+/)
    .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
    .join(" ");
}

interface SkillRadarProps {
  /** Top-N computed skills from the API, sorted by score descending. */
  skills?: UserSkillItem[];
  /** Optional target scores (0.0-1.0) matching the same axes. */
  targetScores?: number[];
  /** How many top skills to show as axes (default 6). */
  topN?: number;
}

export default function SkillRadar({ skills, targetScores, topN = 6 }: SkillRadarProps) {
  const topSkills = (skills ?? []).slice(0, topN);
  const N = topSkills.length;

  // Convert API scores (0.0-1.0) to chart scale (0-4)
  const current = topSkills.map((s) => s.score * LEVELS);
  const target = targetScores
    ? targetScores.slice(0, N).map((s) => s * LEVELS)
    : null;

  const axes = topSkills.map((s) => toDisplayLabel(s.skill));

  if (N === 0) {
    return (
      <div className="flex items-center justify-center h-48 text-on-surface-variant text-body-md">
        Keine Skill-Daten verfügbar. Lade dein Transcript hoch, um dein Kompetenzprofil zu sehen.
      </div>
    );
  }

  return (
    <div className="flex flex-col lg:flex-row gap-8 items-center">
      <div className="w-full lg:w-2/3 aspect-square max-w-[480px] relative">
        <svg viewBox={`0 0 ${SIZE} ${SIZE}`} className="w-full h-full">
          {/* Grid rings */}
          {Array.from({ length: LEVELS }, (_, i) => i + 1).map((level) => (
            <polygon
              key={level}
              points={ringPoints(level, N)}
              fill="none"
              stroke="#e3e2e6"
              strokeWidth="1"
            />
          ))}

          {/* Axis lines */}
          {axes.map((_, i) => {
            const angle = (360 / N) * i;
            const [x, y] = polar(angle, MAX_R);
            return (
              <line key={i} x1={CX} y1={CY} x2={x} y2={y} stroke="#e3e2e6" strokeWidth="1" />
            );
          })}

          {/* Target polygon (blue) — only shown when targetScores provided */}
          {target && (
            <polygon
              points={buildPoints(target, N)}
              fill="rgba(134,160,205,0.15)"
              stroke="#455f88"
              strokeWidth="2"
            />
          )}

          {/* Current polygon (red) */}
          <polygon
            points={buildPoints(current, N)}
            fill="rgba(186,26,26,0.15)"
            stroke="#ba1a1a"
            strokeWidth="2"
          />

          {/* Axis labels */}
          {axes.map((label, i) => {
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
            {target && (
              <div className="flex items-center gap-3">
                <div className="w-4 h-4 rounded bg-primary-container border border-surface-tint shrink-0" />
                <div>
                  <span className="block font-label-md text-on-surface">Zielprofil</span>
                  <span className="text-body-sm text-on-surface-variant">
                    Anforderung für Master-Forschung
                  </span>
                </div>
              </div>
            )}
          </div>
        </div>

        <div className="bg-tertiary-container/10 border border-tertiary-container/20 p-4 rounded-lg flex items-start gap-3">
          <span className="material-symbols-outlined text-tertiary-container mt-0.5">auto_awesome</span>
          <p className="text-body-sm text-on-tertiary-container font-medium">
            Die Skills werden aus deinem Transcript und dem Modulhandbuch berechnet.
          </p>
        </div>
      </div>
    </div>
  );
}
