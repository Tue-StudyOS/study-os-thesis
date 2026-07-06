# Aerospace Propulsion Engineering — Skill Arm (live, edge-case run)

**Date:** 2026-07-03 · **Topic:** Rocket engine / spacecraft propulsion design ·
**Arm:** SKILL · **Role:** Track 4, Task R edge case 1 — niche topic with no real
Tübingen match. Pass condition: the skill says so honestly instead of forcing a
weak match to pad the output.

## Persona (6 dimensions)

- **Interests:** Rocket engine design, spacecraft propulsion systems, combustion
  engineering for launch vehicles
- **Methods:** Hands-on hardware testing (test stands, static fires) + CFD simulation
- **Domain:** Aerospace / space industry
- **Thesis style:** Systems/engineering, experimental — wants to build and test
  hardware, not just model it
- **Skills:** CAD, CFD tooling, thermodynamics, hands-on test-bench work
- **No-gos:** A purely theoretical/desk-based thesis with no hardware component

## Step 3 — Route to relevant faculties

`search-strategy.md` §2's routing table has **no row** for aerospace/propulsion
engineering, and a direct check confirms why: the University of Tübingen has **no
engineering faculty** at all (no Maschinenbau, Elektrotechnik, or Luft- und
Raumfahrttechnik — those exist at TU Berlin, TU Braunschweig, Uni Stuttgart, TUM,
not Tübingen). The only structurally plausible adjacent faculty is Science → FB
Physik (thermodynamics/plasma physics) or FB Chemie (combustion/propellant
chemistry), so both were checked live before concluding no-match, rather than
assuming from the routing table's silence alone.

## Step 4 — Pass 1 backbone crawl (live, this run)

- `physik.uni-tuebingen.de/forschung.html` → reachable; four research themes (Astro
  & Particle Physics, Quantum Science, BioNanoPhysics, Physics in Neuroscience) and
  five institutes. **No propulsion, combustion, or plasma-propulsion group.**
- Chemistry department (`.../fachbereiche/chemie/forschung/`) → reachable; focus is
  sustainable chemistry, molecule/materials design for energy balance. **No
  combustion chemistry, propellant chemistry, or high-temperature-materials group
  for rocket engines.**
- Targeted searches for "Raketenantrieb"/"Antriebstechnik" at Tübingen returned only
  DLR (a different institution) — confirming no chair or Arbeitsbereich anywhere in
  the university works on this topic.

## Steps 5–7 — Enrichment / filters / no-go

Not applicable — the candidate set from Pass 1 is empty. No chair reached Pass 2.

## Step 8 — Output

**No strong Tübingen fit was found for this topic.** Rather than padding the map
with a distant, weakly-justified entry (e.g. a general thermodynamics or materials
chair that merely touches adjacent physics/chemistry, without evidence of actual
propulsion work), the honest output is:

> Rocket-engine and spacecraft-propulsion engineering is not a research area
> represented at the University of Tübingen — the university has no engineering
> faculty (Maschinenbau / Luft- und Raumfahrttechnik), and neither Physics nor
> Chemistry has an active combustion, plasma-propulsion, or propellant-chemistry
> group. If this interest is fixed, look instead at TU Braunschweig, TU Berlin,
> TUM, or Uni Stuttgart, all of which have dedicated aerospace engineering
> departments. If the underlying interest is flexible (e.g. the thermodynamics,
> materials science, or CFD side rather than full-system propulsion), Tübingen's
> Physics and Chemistry departments could be revisited with a narrower, adjacent
> topic — but that would be a different profile, not this one.
>
> This map covers publicly visible chairs as of 2026-07-03. Chairs with a weak web
> presence may still be missing — to be thorough, check the Vorlesungsverzeichnis
> and ask a Fachschaft directly before concluding with certainty.

## Verdict

**PASS.** Following SKILL.md/`search-strategy.md` faithfully on a topic with a
genuine structural no-match produces an honest "no strong fit" statement rather
than a forced, padded list. One gap surfaced by this run: `SKILL.md`'s Output
section (Step 8) does not currently have an explicit instruction for the
zero-candidates case — it only describes what to do when options exist. The
honest behavior held anyway (nothing in the instructions pushes toward padding),
but an explicit line would make this robustness property a spec'd behavior rather
than an emergent one. See the SKILL.md diff in this same commit for the one-line
fix.
