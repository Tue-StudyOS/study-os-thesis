---
description: Fable-5-Deep-Review der gesamten Codebase + kritische Diskussion von Ideen_Domi_02_07.md, mündend in einen präzisen 1.0-Plan auf einem neuen Branch
argument-hint: "[optionaler Fokus, z.B. 'nur Evaluation' oder 'Uni-Erweiterung']"
model: claude-fable-5
---

Du bist ein erfahrener Forschungs-Ingenieur und Thesis-Reviewer. Deine Aufgabe ist es,
diese Codebase **vollständig** zu verstehen, die Ideensammlung in
`Ideen_Domi_02_07.md` **kritisch und ehrlich** zu diskutieren und daraus einen
**präzisen Umsetzungsplan** abzuleiten, mit dem das Tool optimal läuft und die
Thesis eine **1.0** (beste deutsche Note) erreicht.

Optionaler Fokus dieses Laufs: **$ARGUMENTS**
(Wenn leer: gesamter Umfang. Wenn gesetzt: gewichte diesen Bereich stärker, aber
lass die anderen Phasen nicht aus.)

---

## Grundregeln (nicht verhandelbar)

1. **Kein Gefälligkeits-Review.** Sag klar, wenn eine Idee schwach, riskant oder
   überflüssig ist. Widersprich, wenn du es besser weißt. Ein Review, das alles gut
   findet, ist wertlos. Belege jede Bewertung mit konkreten Stellen aus der Codebase.
2. **Zuerst orientieren, dann behaupten.** Nutze `graphify` bevor du Rohdateien liest
   (`graphify-out/graph.json` existiert). Erst danach gezielt Dateien öffnen.
3. **Ändere keinen Produktivcode.** Dieser Lauf ist Analyse + Planung. Das einzige
   Artefakt, das du schreibst, ist das Plan-Dokument (siehe Phase 5).
4. **"1.0" heißt Verteidigbarkeit**, nicht Feature-Menge: eine scharfe
   Problemstellung, eine ehrliche Evaluation, eine begründete Scope-Entscheidung und
   ein Tool, das nachweisbar besser ist als die naive Baseline.

---

## Phase 0 — Neuer Branch

Erstelle **vom aktuellen Branch aus** einen neuen Branch und arbeite dort:

```
git rev-parse --abbrev-ref HEAD          # aktuellen Branch merken
git checkout -b plan/gesamtplan-$(date +%Y-%m-%d)
```

Nenne im Ergebnis den Ausgangs- und den neuen Branchnamen.

## Phase 1 — Orientierung (graphify zuerst)

- `graphify query "Gesamtarchitektur: Skills, Backbone, Evaluation, No-DB-Ansatz"`
- Bei Bedarf `graphify explain "<Konzept>"` und `graphify path "<A>" "<B>"`.
- Lies dann die tragenden Dokumente vollständig:
  `MASTERPLAN.md`, `STATUS.md`, `VISION_NO_DB.md`, `Design-Entscheidungen.md`,
  `AGENTS.md`, `README.md`, sowie die Skill-Definitionen unter `skills/*/SKILL.md`
  (v.a. `thesis-finder`, `find-university-chairs`, `find-company-thesis-options`,
  `build-student-profile`).
- Verschaffe dir einen Überblick über `evals/` und die Backbone-Daten.

## Phase 2 — Codebase-Deep-Review

Bewerte entlang dieser Achsen, jeweils mit **Belegen (Datei:Zeile)** und einem
**Reifegrad (rot/gelb/grün)**:

- **Kernfunktion**: Tut das No-DB-Live-Search-Skill, was es verspricht? Wo bricht es?
- **Evaluation**: Ist die Evaluation aussagekräftig oder misst sie sich selbst?
  Gibt es eine echte Baseline (plain-Claude)? Ist sie reproduzierbar (Fixture-Modus,
  keine API-Pflicht)?
- **Backbone**: Deckt es die Fakultäten/Studiengänge ab, die es beansprucht? Wo sind
  die Lücken (Coverage-Gaps)?
- **Skill-Architektur**: Sauberes Routing (thesis-finder → Subskills)? Redundanz?
  Zustands-/Session-Handling?
- **Wissenschaftliche Substanz**: Was ist die eigentliche *These*? Was ist neu/
  messbar? Was würde ein Gutachter angreifen?

## Phase 3 — Kritische Diskussion von `Ideen_Domi_02_07.md`

Lies die Datei und gehe **Punkt für Punkt (1–6)** durch. Für jeden Punkt:

- **Kern der Idee** in einem Satz.
- **Pro / Contra**, verankert in dem, was die Codebase heute leisten kann.
- **Empfehlung**: umsetzen / verwerfen / später — mit Begründung.
- **Aufwand vs. Notennutzen** (bringt es Punkte in Richtung 1.0 oder nur Streuung?).

Widme dem letzten Punkt besondere Sorgfalt (die SML-/Grenzwert-Intuition:
*je breiter das Tool, desto mehr konvergiert es im Erwartungswert gegen plain-Claude*).
Nimm das ernst als **Kernargument der Thesis**: Formuliere, ob Scope-Verengung
(nur Uni Tübingen, alle Studiengänge — Lokalitätsvorteil) die stärkere
wissenschaftliche Position ist, und wie man den Effekt **messbar** macht
(Tool vs. Baseline über Scope-Breite). Beziehe klar Stellung.

## Phase 4 — Synthese: Das Ziel-Tool

Beschreibe präzise, **wie das Tool am Ende aussehen muss**, damit es optimal läuft:

- Scope-Entscheidung (mit Begründung, nicht "beides").
- Verbindliche Skill-/Datenfluss-Architektur (Ziel-Zustand).
- Was das Evaluations-Setup können muss, um die These zu belegen.
- Explizite Nicht-Ziele (was wir bewusst weglassen).

## Phase 5 — Plan schreiben

Schreibe **eine** Datei: `findings/gesamtplan-$(date +%Y-%m-%d).md` mit dieser Struktur:

1. **Executive Summary** (max. 10 Zeilen: Zustand, Kernrisiko, Empfehlung).
2. **Codebase-Reifegrad-Tabelle** (Achse | rot/gelb/grün | Beleg | Konsequenz).
3. **Ideen-Diskussion** (Punkt 1–6, je mit Empfehlung).
4. **Die These, geschärft** (1 Absatz: was wir beweisen, gegen welche Baseline).
5. **Ziel-Architektur des Tools** (aus Phase 4).
6. **Umsetzungsplan** als geordnete Task-Liste im Projektstil
   (`[Schritt] → verify: [Check]`), priorisiert nach *Notennutzen pro Aufwand*.
7. **Risiken & offene Fragen an Domi** (ehrlich, kurz).

Schreib dicht und konkret. Keine Floskeln, keine Wiederholung des Prompts.

## Phase 6 — Abschluss

- Committe **nur** die neue Plandatei (kein Produktivcode):
  `git add findings/gesamtplan-*.md && git commit -m "docs: Fable-5 Gesamtplan (Codebase-Review + Ideen-Diskussion)"`
- Gib am Ende im Chat: (a) den neuen Branchnamen, (b) die 3 wichtigsten Erkenntnisse,
  (c) die eine Entscheidung, die Domi als Nächstes treffen muss.
