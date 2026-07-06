#!/usr/bin/env python3
"""Generate three meaningful SVGs into evals/ from real file and fixture data.

SVGs produced:
  evals/skill-architecture.svg  — product flow: which skills call which, ref files
  evals/quality-matrix.svg      — per-skill property checks from actual file contents
  evals/behavior-comparison.svg — skill vs baseline behavioral differences (fixture-based)

No API key required. All data comes from the repo itself.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
FIXTURES_DIR = SKILLS_DIR / "tests" / "simulations" / "fixtures"
EVALS_DIR = REPO_ROOT / "evals"

FONT = "system-ui, -apple-system, 'Segoe UI', sans-serif"
TEXT      = "#111827"
TEXT_MID  = "#6B7280"
TEXT_LIGHT = "#9CA3AF"
BORDER    = "#E5E7EB"
BG_ALT    = "#F9FAFB"
GREEN     = "#10B981"
BLUE      = "#3B82F6"
PURPLE    = "#8B5CF6"
ORANGE    = "#F59E0B"
RED       = "#EF4444"


# ── SVG primitives ────────────────────────────────────────────────────────

def _rect(x, y, w, h, fill, stroke=None, sw=1, rx=0, opacity=1):
    s = f'x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}"'
    if rx: s += f' rx="{rx}"'
    if stroke: s += f' stroke="{stroke}" stroke-width="{sw}"'
    if opacity != 1: s += f' opacity="{opacity:.2f}"'
    return f"<rect {s}/>"


def _text(x, y, content, anchor="middle", size=12, fill=TEXT, weight="normal"):
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" font-size="{size}" '
        f'fill="{fill}" font-weight="{weight}" font-family="{FONT}">{content}</text>'
    )


def _line(x1, y1, x2, y2, stroke=BORDER, sw=1, dashed=False):
    s = f'x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"'
    if dashed: s += ' stroke-dasharray="4,3"'
    return f"<line {s}/>"


def _path(d, fill="none", stroke=TEXT_MID, sw=1.5, dashed=False, marker="url(#ah)"):
    s = f'd="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"'
    if dashed: s += ' stroke-dasharray="5,3"'
    if marker: s += f' marker-end="{marker}"'
    return f'<path {s}/>'


def _pill(x, y, w, h, bg, border, label, text_fill, size=9):
    return (
        _rect(x, y, w, h, bg, stroke=border, sw=1, rx=h // 2)
        + _text(x + w / 2, y + h / 2 + size // 2 - 1, label, size=size, fill=text_fill)
    )


def _svg(w, h, body, defs=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
        + (f"<defs>{defs}</defs>\n" if defs else "")
        + '<rect width="' + str(w) + '" height="' + str(h) + '" fill="white"/>\n'
        + "\n".join(body) + "\n</svg>\n"
    )


ARROW_MARKER = (
    '<marker id="ah" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">'
    '<path d="M0,0 L0,6 L7,3 z" fill="#9CA3AF"/>'
    '</marker>'
)


# ── Data collection ──────────────────────────────────────────────────────

SKILL_ORDER = [
    "build-student-profile",
    "thesis-finder",
    "find-university-chairs",
    "find-company-thesis-options",
    "generate-thesis-directions",
    "draft-thesis-contact",
    "find-recent-papers",
    "design-agent-skill",
]

# Skills that intentionally skip the no-DB and evidence checks (meta/router)
NO_DB_EXEMPT   = {"design-agent-skill", "thesis-finder"}
EVIDENCE_EXEMPT = {"design-agent-skill", "thesis-finder", "build-student-profile"}

REF_PATTERN = re.compile(r"`(references/[^`]+)`")


def collect_quality_data() -> list[dict]:
    rows = []
    for name in SKILL_ORDER:
        skill_dir = SKILLS_DIR / name
        skill_md  = skill_dir / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")

        # frontmatter
        fm_match = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
        fm_keys = set()
        if fm_match:
            for line in fm_match.group(1).splitlines():
                k, sep, _ = line.partition(":")
                if sep:
                    fm_keys.add(k.strip())
        fm_valid = fm_keys == {"name", "description"}

        # description checks
        desc = ""
        if fm_match:
            for line in fm_match.group(1).splitlines():
                k, sep, v = line.partition(":")
                if sep and k.strip() == "description":
                    desc = v.strip()
        use_when = "Use when" in desc
        desc_len_ok = len(desc) <= 1024

        # reference files
        ref_dir = skill_dir / "references"
        ref_files = list(ref_dir.rglob("*.md")) if ref_dir.is_dir() else []
        has_refs = len(ref_files) > 0

        # broken reference links
        linked = REF_PATTERN.findall(text)
        broken = [r for r in linked if not (skill_dir / r).exists()]
        links_ok = len(broken) == 0

        # no-db disclaimer
        no_db_phrases = [
            "Do not depend on the old UI",
            "the only authoritative source during discovery.",
            "No runtime company database",
        ]
        no_db = any(p in text for p in no_db_phrases)
        no_db_result = "exempt" if name in NO_DB_EXEMPT else ("pass" if no_db else "fail")

        # evidence rules
        evidence_phrases = ["Do not fabricate", "Do not invent", "Never invent", "Never fabricate"]
        evidence = any(p in text for p in evidence_phrases)
        evidence_result = "exempt" if name in EVIDENCE_EXEMPT else ("pass" if evidence else "fail")

        rows.append({
            "name":            name,
            "fm_valid":        fm_valid,
            "use_when":        use_when,
            "desc_len_ok":     desc_len_ok,
            "has_refs":        has_refs,
            "ref_count":       len(ref_files),
            "links_ok":        links_ok,
            "no_db":           no_db_result,
            "evidence":        evidence_result,
        })
    return rows


FACULTY_FIXTURES = [
    ("cs",         "cs-student-skill",    "cs-student-baseline",    "Informatik / AI"),
    ("medicine",   "neuro-student-skill", "neuro-student-baseline", "Medizin"),
    ("psychology", "psych-student-skill", "psych-student-baseline", "Psychologie"),
    ("wiso",       "wiso-student-skill",  "wiso-student-baseline",  "WiSo"),
]

FACULTY_GROUND_TRUTH = {
    "cs":        ["Martius", "Hennig", "Hein", "Luxburg", "Schölkopf", "Brendel", "Bethge"],
    "medicine":  ["Gasser", "Jucker", "Lerche", "Ziemann", "Siegel", "Tabatabai"],
    "psychology":["Bartels", "Nürk", "Friedrich", "Huff", "Svaldi", "Gawrilow"],
    "wiso":      ["Diez", "Abels", "Schlumberger", "Hasenclever", "Bieling", "Müller", "Baten"],
}


def collect_fixture_data() -> list[dict]:
    rows = []
    for fac_key, skill_fix, base_fix, label in FACULTY_FIXTURES:
        gt = FACULTY_GROUND_TRUTH[fac_key]
        for arm, fix_name in [("skill", skill_fix), ("baseline", base_fix)]:
            d = json.loads((FIXTURES_DIR / f"{fix_name}.json").read_text(encoding="utf-8"))
            turns = d["turns"]
            asst_turns = [t for t in turns if t["role"] == "assistant"]
            asst_text  = " ".join(t["content"] for t in asst_turns).lower()
            user_turns = [t for t in turns if t["role"] == "user"]

            map_out   = "**[" in " ".join(t["content"] for t in asst_turns)
            gate      = "if any dimension is missing" in asst_text or "stop here" in asst_text
            chairs    = sum(1 for name in gt if name.lower() in asst_text)

            rows.append({
                "faculty":    label,
                "fac_key":    fac_key,
                "arm":        arm,
                "turns":      len(turns),
                "user_turns": len(user_turns),
                "asst_turns": len(asst_turns),
                "map_out":    map_out,
                "gate":       gate,
                "chairs":     chairs,
                "gt_total":   len(gt),
            })
    return rows


# ── SVG 1: Skill Architecture ─────────────────────────────────────────────

def render_architecture() -> str:
    W, H = 820, 390
    els = []

    # title
    els.append(_text(W / 2, 26, "Skill Architecture — Student Thesis Journey", size=15, weight="600"))
    els.append(_text(W / 2, 44, "Skill invocation graph · reference files · data sources",
                     size=11, fill=TEXT_MID))

    # ── boxes (x, y, w, h, bg, border, label_lines, step_label, badge) ──
    boxes = {
        "build-student-profile": {
            "x": 12, "y": 170, "w": 152, "h": 52,
            "bg": "#EFF6FF", "border": BLUE,
            "lines": ["build-student-", "profile"],
            "step": "① PROFILE",
        },
        "thesis-finder": {
            "x": 205, "y": 170, "w": 118, "h": 52,
            "bg": "#F5F3FF", "border": PURPLE,
            "lines": ["thesis-finder"],
            "step": "② ROUTE",
        },
        "find-university-chairs": {
            "x": 378, "y": 82, "w": 166, "h": 52,
            "bg": "#F0FDF4", "border": GREEN,
            "lines": ["find-university-", "chairs"],
            "step": "③ DISCOVER",
            "badge": "live web",
        },
        "find-company-thesis-options": {
            "x": 378, "y": 262, "w": 178, "h": 52,
            "bg": "#F0FDF4", "border": GREEN,
            "lines": ["find-company-", "thesis-options"],
            "step": "③ DISCOVER",
            "badge": "live web",
        },
        "draft-thesis-contact": {
            "x": 605, "y": 170, "w": 150, "h": 52,
            "bg": "#FFF7ED", "border": ORANGE,
            "lines": ["draft-thesis-", "contact"],
            "step": "④ DRAFT",
        },
    }

    # ref tag specs: [(label, w)]
    ref_tags = {
        "build-student-profile": [
            ("profile-schema.md", 112),
        ],
        "find-university-chairs": [
            ("faculty-backbone.md", 118),
            ("search-strategy.md", 108),
        ],
        "find-company-thesis-options": [
            ("bw-company-backbone.md", 130),
            ("company-search-strategy.md", 155),
        ],
    }

    # draw step labels above boxes
    step_drawn = set()
    for bname, b in boxes.items():
        step = b["step"]
        bx = b["x"] + b["w"] / 2
        els.append(_text(bx, b["y"] - 8, step, size=9, fill=TEXT_MID, weight="600"))

    # draw arrows (before boxes so boxes render on top)
    # 1. build-student-profile → thesis-finder (horizontal)
    els.append(_path(f'M {164:.0f},{196:.0f} L {205:.0f},{196:.0f}'))
    # 2. thesis-finder → find-university-chairs (diagonal up)
    els.append(_path(f'M 315,182 C 348,182 348,108 378,108'))
    # 3. thesis-finder → find-company-thesis-options (diagonal down)
    els.append(_path(f'M 315,208 C 348,208 348,288 378,288'))
    # 4. find-university-chairs → draft-thesis-contact
    els.append(_path(f'M 544,108 C 576,108 576,190 605,190'))
    # 5. find-company-thesis-options → draft-thesis-contact
    els.append(_path(f'M 556,288 C 582,288 582,210 605,210'))

    # draw boxes
    for bname, b in boxes.items():
        x, y, w, h = b["x"], b["y"], b["w"], b["h"]
        els.append(_rect(x, y, w, h, b["bg"], stroke=b["border"], sw=1.5, rx=8))

        # text lines
        lines = b["lines"]
        if len(lines) == 1:
            els.append(_text(x + w / 2, y + h / 2 + 5, lines[0], size=11, fill=TEXT, weight="600"))
        else:
            els.append(_text(x + w / 2, y + h / 2 - 3, lines[0], size=11, fill=TEXT, weight="600"))
            els.append(_text(x + w / 2, y + h / 2 + 13, lines[1], size=11, fill=TEXT, weight="600"))

        # live web badge
        if b.get("badge"):
            bw2, bh2 = 58, 18
            bx2 = x + w - bw2 - 4
            by2 = y + h - bh2 - 4
            els.append(_rect(bx2, by2, bw2, bh2, "#D1FAE5", stroke="#6EE7B7", sw=1, rx=9))
            els.append(_text(bx2 + bw2 / 2, by2 + 12, "⚡ live web", size=8, fill="#065F46"))

    # draw reference file tags
    tag_h = 20
    for bname, tags in ref_tags.items():
        b = boxes[bname]
        bx, by, bw, bh = b["x"], b["y"], b["w"], b["h"]
        tag_y = by + bh + 6
        gap = 5
        total_w = sum(w for _, w in tags) + gap * (len(tags) - 1)
        start_x = bx + (bw - total_w) / 2
        cx = start_x
        for label, tw in tags:
            els.append(_pill(cx, tag_y, tw, tag_h, "#EFF6FF", "#BFDBFE", label, "#1D4ED8", size=9))
            cx += tw + gap

    # supporting / optional skills note
    els.append(_line(12, 352, 590, 352, stroke=BORDER, sw=1, dashed=True))
    els.append(_text(12, 368, "Also available: find-recent-papers (background papers) · generate-thesis-directions (proposal sketches) · design-agent-skill (meta)",
                     anchor="start", size=9, fill=TEXT_LIGHT))

    return _svg(W, H, els, defs=ARROW_MARKER)


# ── SVG 2: Quality Matrix ─────────────────────────────────────────────────

PROPS = [
    ("Frontmatter", "fm_valid"),
    ("Use-when", "use_when"),
    ("Desc ≤1024", "desc_len_ok"),
    ("Ref files", "has_refs"),
    ("No broken links", "links_ok"),
    ("No-DB rule", "no_db"),
    ("Evidence rules", "evidence"),
]

PROP_LABELS  = [p[0] for p in PROPS]
PROP_KEYS    = [p[1] for p in PROPS]


def _cell_color(value):
    if value is True or value == "pass":
        return "#D1FAE5", "#10B981", "✓", "#065F46"
    if value == "exempt":
        return "#F3F4F6", "#D1D5DB", "—", TEXT_LIGHT
    if value is False or value == "fail":
        return "#FEE2E2", "#EF4444", "✗", "#991B1B"
    # False for has_refs means no refs
    return "#F3F4F6", "#D1D5DB", "—", TEXT_LIGHT


def render_quality_matrix(rows: list[dict]) -> str:
    W     = 780
    left  = 20
    row_h = 32
    col_w = 86
    name_w = 192
    header_h = 48
    top   = 65
    n_props = len(PROPS)
    n_skills = len(rows)

    H = top + header_h + n_skills * row_h + 48

    els = []

    els.append(_text(W / 2, 26, "Skill Quality Properties", size=15, weight="600"))
    els.append(_text(W / 2, 44, "Checked directly from SKILL.md file contents — no API call required",
                     size=11, fill=TEXT_MID))

    # header background
    els.append(_rect(left, top, name_w + n_props * col_w, header_h, BG_ALT, stroke=BORDER, sw=1, rx=6))

    # column headers (diagonal-ish: just tilted labels at 45°)
    # SVG doesn't easily do rotated text in a portable way, so I'll do two-line headers
    for ci, label in enumerate(PROP_LABELS):
        cx = left + name_w + ci * col_w + col_w / 2
        words = label.split()
        if len(words) == 1:
            els.append(_text(cx, top + 22, words[0], size=10, fill=TEXT_MID, weight="600"))
        else:
            els.append(_text(cx, top + 14, words[0], size=10, fill=TEXT_MID, weight="600"))
            els.append(_text(cx, top + 28, " ".join(words[1:]), size=10, fill=TEXT_MID, weight="600"))

    # skill name column header
    els.append(_text(left + name_w / 2, top + 22, "Skill", size=10, fill=TEXT_MID, weight="600"))

    # data rows
    for ri, row in enumerate(rows):
        ry = top + header_h + ri * row_h
        if ri % 2 == 1:
            els.append(_rect(left, ry, name_w + n_props * col_w, row_h, BG_ALT, rx=0))
        els.append(_line(left, ry, left + name_w + n_props * col_w, ry, stroke=BORDER))

        # skill name
        els.append(_text(left + 8, ry + row_h / 2 + 4, row["name"], anchor="start", size=11, fill=TEXT))

        # property cells
        for ci, key in enumerate(PROP_KEYS):
            cx = left + name_w + ci * col_w + col_w / 2
            cy = ry + row_h / 2
            raw = row[key]
            bg, border, symbol, sym_fill = _cell_color(raw)
            cell_w, cell_h = 32, 20
            els.append(_rect(cx - cell_w / 2, cy - cell_h / 2, cell_w, cell_h, bg,
                             stroke=border, sw=1, rx=4))
            els.append(_text(cx, cy + 5, symbol, size=12, fill=sym_fill, weight="700"))

    # bottom border
    bottom_y = top + header_h + n_skills * row_h
    els.append(_line(left, bottom_y, left + name_w + n_props * col_w, bottom_y, stroke=BORDER))

    # legend
    ly = H - 22
    for sym, label, bg, bd, sf in [
        ("✓", "property verified", "#D1FAE5", "#10B981", "#065F46"),
        ("—", "not applicable (meta/router skill)", "#F3F4F6", "#D1D5DB", TEXT_LIGHT),
    ]:
        lx = left + 8 if sym == "✓" else left + 200
        els.append(_rect(lx, ly - 12, 22, 16, bg, stroke=bd, sw=1, rx=4))
        els.append(_text(lx + 11, ly, sym, size=11, fill=sf, weight="700"))
        els.append(_text(lx + 28, ly, label, anchor="start", size=10, fill=TEXT_MID))

    return _svg(W, H, els)


# ── SVG 3: Behavior Comparison ────────────────────────────────────────────

def render_behavior_comparison(fixture_rows: list[dict]) -> str:
    W    = 760
    left = 20
    H    = 400

    # group by faculty
    faculties = []
    seen = []
    for r in fixture_rows:
        if r["faculty"] not in seen:
            seen.append(r["faculty"])
    fac_order = seen

    els = []

    els.append(_text(W / 2, 26, "Skill vs. Baseline — Fixture Conversation Comparison",
                     size=15, weight="600"))
    els.append(_text(W / 2, 44,
                     "Pre-written fixture transcripts · shows intended behavioral contract, not a live measurement",
                     size=11, fill=TEXT_MID))

    # column layout: label | turns chart | MAP ✓ | Chairs named
    fac_col_w  = 112
    chart_w    = 340    # stacked bar area for 4 faculty × 2 arms
    badge_col  = 90
    chairs_col = 90
    total_cols = fac_col_w + chart_w + badge_col + chairs_col

    header_y = 62
    row_h    = 66
    bar_max  = 8       # max turns in fixtures

    # header
    header_bg_w = total_cols + 8
    els.append(_rect(left, header_y, header_bg_w, 24, BG_ALT, stroke=BORDER, sw=1, rx=4))
    els.append(_text(left + fac_col_w / 2, header_y + 16, "Faculty", size=10, fill=TEXT_MID, weight="600"))
    els.append(_text(left + fac_col_w + chart_w / 2, header_y + 16, "Conversation turns  (user + assistant)", size=10, fill=TEXT_MID, weight="600"))
    els.append(_text(left + fac_col_w + chart_w + badge_col / 2, header_y + 16, "MAP output", size=10, fill=TEXT_MID, weight="600"))
    els.append(_text(left + fac_col_w + chart_w + badge_col + chairs_col / 2, header_y + 16, "Chairs named", size=10, fill=TEXT_MID, weight="600"))

    bar_area_x  = left + fac_col_w + 10
    bar_unit    = (chart_w - 60) / bar_max   # px per turn
    bar_h_skill = 18
    bar_h_base  = 14
    arm_gap     = 6

    for fi, fac in enumerate(fac_order):
        ry = header_y + 24 + fi * row_h
        if fi % 2 == 1:
            els.append(_rect(left, ry, header_bg_w, row_h, BG_ALT, rx=0))
        els.append(_line(left, ry, left + header_bg_w, ry, stroke=BORDER))

        fac_rows = {r["arm"]: r for r in fixture_rows if r["faculty"] == fac}
        sk = fac_rows.get("skill", {})
        bs = fac_rows.get("baseline", {})

        # faculty label
        els.append(_text(left + 8, ry + row_h / 2 - 5, fac, anchor="start", size=11, fill=TEXT, weight="600"))
        els.append(_text(left + 8, ry + row_h / 2 + 10, f"{sk.get('gt_total', '?')} ground-truth chairs",
                         anchor="start", size=9, fill=TEXT_LIGHT))

        # turn bars
        bar_y_skill = ry + 12
        bar_y_base  = ry + 12 + bar_h_skill + arm_gap

        for arm_data, bar_y, bar_h, arm_color, arm_label in [
            (sk, bar_y_skill, bar_h_skill, BLUE, "skill"),
            (bs, bar_y_base,  bar_h_base,  BORDER, "baseline"),
        ]:
            turns = arm_data.get("turns", 0)
            bw_total = turns * bar_unit

            # user turns (lighter shade)
            user_t = arm_data.get("user_turns", 0)
            asst_t = arm_data.get("asst_turns", 0)
            user_w = user_t * bar_unit
            asst_w = asst_t * bar_unit

            # background track
            els.append(_rect(bar_area_x, bar_y, bar_max * bar_unit, bar_h, "#F3F4F6", rx=3))
            # user turns
            els.append(_rect(bar_area_x, bar_y, user_w, bar_h,
                             "#93C5FD" if arm_label == "skill" else "#E5E7EB", rx=3))
            # asst turns layered on right half
            els.append(_rect(bar_area_x + user_w, bar_y, asst_w, bar_h,
                             arm_color, rx=3))

            # count label
            els.append(_text(bar_area_x + bw_total + 6, bar_y + bar_h / 2 + 4,
                             f"{turns} turns", anchor="start", size=9,
                             fill=BLUE if arm_label == "skill" else TEXT_MID))

            # arm label on left
            els.append(_text(bar_area_x - 4, bar_y + bar_h / 2 + 4,
                             arm_label, anchor="end", size=9,
                             fill=BLUE if arm_label == "skill" else TEXT_MID))

        # MAP badge
        map_cx = left + fac_col_w + chart_w + badge_col / 2
        sk_map = sk.get("map_out", False)
        bs_map = bs.get("map_out", False)
        for badge_val, by_off in [(sk_map, bar_y_skill), (bs_map, bar_y_base)]:
            bw, bh = 44, bar_h_skill if by_off == bar_y_skill else bar_h_base
            els.append(_rect(map_cx - bw / 2, by_off, bw, bh,
                             "#D1FAE5" if badge_val else "#FEE2E2",
                             stroke="#10B981" if badge_val else "#EF4444", sw=1, rx=bh // 2))
            els.append(_text(map_cx, by_off + bh / 2 + 4,
                             "✓ yes" if badge_val else "✗ no",
                             size=9, fill="#065F46" if badge_val else "#991B1B", weight="600"))

        # Chairs named
        chairs_cx = left + fac_col_w + chart_w + badge_col + chairs_col / 2
        for arm_data, by_off, bar_h in [
            (sk, bar_y_skill, bar_h_skill),
            (bs, bar_y_base, bar_h_base),
        ]:
            named  = arm_data.get("chairs", 0)
            total  = arm_data.get("gt_total", 1)
            label  = f"{named} / {total}"
            color  = BLUE if arm_data.get("arm") == "skill" else TEXT_MID
            els.append(_text(chairs_cx, by_off + bar_h / 2 + 4, label, size=10, fill=color, weight="600"))

    # bottom border + legend
    bottom_y = header_y + 24 + len(fac_order) * row_h
    els.append(_line(left, bottom_y, left + header_bg_w, bottom_y, stroke=BORDER))

    ly = bottom_y + 20
    els.append(_rect(left, ly - 10, 12, 12, "#93C5FD", rx=2))
    els.append(_text(left + 16, ly, "user turns", anchor="start", size=10, fill=TEXT_MID))
    els.append(_rect(left + 90, ly - 10, 12, 12, BLUE, rx=2))
    els.append(_text(left + 106, ly, "assistant turns (skill)", anchor="start", size=10, fill=TEXT_MID))
    els.append(_rect(left + 260, ly - 10, 12, 12, BORDER, rx=2))
    els.append(_text(left + 276, ly, "baseline turns (combined)", anchor="start", size=10, fill=TEXT_MID))
    els.append(_text(left, ly + 18,
                     "Chairs named = ground-truth last-name matches in assistant output · fixture = pre-written transcript, not a live run",
                     anchor="start", size=9, fill=TEXT_LIGHT))

    return _svg(W, H, els)


# ── main ──────────────────────────────────────────────────────────────────

def main() -> None:
    EVALS_DIR.mkdir(parents=True, exist_ok=True)

    quality_rows  = collect_quality_data()
    fixture_rows  = collect_fixture_data()

    charts = [
        ("skill-architecture.svg",   render_architecture()),
        ("quality-matrix.svg",        render_quality_matrix(quality_rows)),
        ("behavior-comparison.svg",   render_behavior_comparison(fixture_rows)),
    ]

    for name, svg in charts:
        path = EVALS_DIR / name
        path.write_text(svg, encoding="utf-8")
        print(f"  {path.relative_to(REPO_ROOT)}")

    # also write a small JSON summary of the quality data for reference
    summary_path = EVALS_DIR / "quality-summary.json"
    summary_path.write_text(
        json.dumps({"skills": quality_rows}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"  {summary_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
