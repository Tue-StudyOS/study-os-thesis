# Gesamtplan 2026-07-02 — Codebase-Review, Ideen-Diskussion, Weg zur 1.0

**Branch:** `plan/gesamtplan-2026-07-02` (von `feat/no-db-universal-skill`)
**Grundlage:** Voll-Review der Skills, Referenzen, Eval-Artefakte und Docs + kritische
Diskussion von `Ideen_Domi_02_07.md`.

---

## 1. Executive Summary

Das Tool ist in einem guten, ehrlichen Zustand: Der No-DB-Zwei-Pass-Ansatz funktioniert
nachweislich live (+65 pp über plain-Claude, alle 4 Fakultäten ≥70 % primary recall nach
I-Fix). Die Skill-Architektur ist sauber, die Selbstkritik in den Findings ist vorbildlich.
**Kernrisiko für die Note:** Die Evaluation ist der schwächste Baustein — manuell, n=1,
selbst gescored, Firmen-GT zirkulär, Live-Harness auf Codex gebaut (nicht verfügbar).
**Kernchance:** Domis SML-Intuition (Punkt 6) ist nicht nur richtig, sie ist *die These*.
Empfehlung: Scope hart auf **Tübingen + BW** fixieren, andere Unis **nur als
Kontrollbedingung im Experiment** nutzen, und die verbleibende Zeit fast vollständig in
ein sauberes, wiederholbares Eval-Design stecken. Kein neues Feature bringt mehr
Notenpunkte als ein verteidigbares Experiment.

---

## 2. Codebase-Reifegrad

| Achse | Reifegrad | Beleg | Konsequenz |
|---|---|---|---|
| **Kernfunktion** (No-DB-Live-Discovery) | 🟢 | `skills/find-university-chairs/SKILL.md:51-125` (Pass 1 Backbone-Crawl inkl. MPI-IS/ELLIS als first-class Quellen, 2e-Personen-Verifikation, 2f-Existenz-Check); Live-Ergebnis `findings/no_db_universal_skill/2026-06-28-I-fix-revalidation.md` (alle 4 Fakultäten ≥70 %) | Kern hält, was er verspricht. Restrisiko: alles hängt an Prompt-Compliance des ausführenden Modells — es gibt keinen Mechanismus, der die 8 Workflow-Schritte erzwingt. Als bekannte Limitation in die Thesis, nicht "fixen". |
| **Evaluation** | 🔴/🟡 | Fixture-Eval ist zugegebenermaßen zirkulär (`STATUS.md:181-190`: Skill-Arm handgeschrieben mit GT-Namen, Baseline ein Strawman mit 0 %). Live-Eval (Task I) ist ehrlich und gut dokumentiert (`2026-06-28-live-eval-results.md:16-26`: primary vs. strict recall), aber **manuell, n=1, selbst gescored**. Live-Runner des Harness verlangen Codex (`scripts/run_codex_multiturn_eval.py:32`: `VALID_RUNNERS = ("fixture", "codex-local", "codex-chair")`) — nicht verfügbar. Firmen-GT aus demselben Backbone wie der Skill (`Design-Entscheidungen.md` §10.2). | Größter Notenhebel. Ein Gutachter greift genau hier an: Stichprobengröße, Selbst-Scoring, Zirkularität, fehlende Varianzschätzung. Siehe Umsetzungsplan T2–T4. |
| **Backbone Uni** | 🟢 | `tuebingen-faculty-backbone.md`: alle 7 Fakultäten + ZITh, je ≥1 offizielle Listing-URL, Drill-down-Muster, Caveats zu URL-Drift. MPI-IS/ELLIS-Leg nach CS-Miss nachgerüstet (Zeile 65-66). | Solide. Lücke: außeruniversitäre Institute sind nur für CS/Neuro als Pflicht-Quellen verdrahtet — nicht für Psych (IWM), Bio (MPI f. Biologie, FML), Medtech (NMI). Siehe Idee 4. |
| **Backbone Firmen** | 🟡 | `bw-company-backbone.md`: 107 Einträge, 7 Sektoren, 14 URLs spot-geprüft. MINT-lastig; Psych/UX, EdTech, Umwelt, Life-Science-Spinouts fehlen weitgehend (`Design-Entscheidungen.md` §10.1 benennt das selbst). | "Für alle Fachbereiche" ist derzeit ein Uni-Versprechen, kein Firmen-Versprechen. Kleine kuratierte Ergänzung (T7), keine Vollabdeckung. |
| **Skill-Architektur** | 🟢 | `thesis-finder/SKILL.md`: dünner Orchestrator mit Session-Persistenz (`~/.claude/thesis-finder/session.md`), klare New/Returning-Flows, Dead-End-Exclusions. Harte Profil-Gates in beiden Discovery-Skills. | Zwei konkrete Defekte: (1) **Dimensions-Inkonsistenz** — `thesis-finder/SKILL.md:27` verlangt *Interests, Methods, Domain, Thesis style, Skills, No-gos*; `build-student-profile/SKILL.md:15` definiert stattdessen *interests, liked/disliked courses, skills, experience, thesis style, no-gos* (Methods/Domain fehlen dort als Pflicht). Der Standalone-Pfad kann also ein "vollständiges" Profil liefern, das die Discovery-Gates nicht erfüllt. (2) Session-Pfad `~/.claude/` ist Claude-spezifisch; README verspricht Portabilität (Codex, Gemini CLI). Beides billig zu fixen (T6). |
| **Wissenschaftliche Substanz** | 🟡 | Echte Messung existiert (+65 pp primary, `2026-06-28-live-eval-results.md:40`), Profil-Steering nachgewiesen (ebd. L108-115), Ehrlichkeit hoch (strict-recall-Linse selbst eingeführt). Aber: die *These* ist nirgends als falsifizierbare Behauptung formuliert; die Scope-Frage ist offen; keine unabhängige Validation. | Die Thesis hat derzeit ein gutes Tool und gute Ingenieurspraxis, aber noch kein Experiment-Design, das eine Behauptung beweist. T1–T3 schließen genau das. |

---

## 3. Diskussion `Ideen_Domi_02_07.md` (Punkt für Punkt)

### Idee 1 — Suche auf andere Unis ausweiten (KIT, TUM als 3. Track)

- **Kern:** Neben Tübingen-intern und BW-Firmen ein dritter Track "andere Unis", weil es dort (zentrale Seiten!) interessante Stellen gibt.
- **Pro:** Realer Nutzerbedarf (Domi hat es selbst gebraucht). Zentrale Thesis-Portale sind leicht zu crawlen.
- **Contra:** Genau *weil* KIT/TUM zentrale Seiten haben, ist plain-Claude dort schon gut — das Tool-Delta wäre klein. Vor allem: es gibt dort **kein Backbone**, also entfällt der Anti-SEO-Anker, der laut Live-Eval den Mehrwert trägt. Ein dritter Track ohne Backbone verwässert das Kernargument und vergrößert die Testfläche, ohne dass wir ihn je validieren könnten.
- **Empfehlung: als Feature verwerfen — als Experiment-Arm umsetzen.** Eine fremde Uni (KIT *oder* TUM, gleiche Skill-Mechanik, ohne Backbone) ist die perfekte **Kontrollbedingung**, um den Backbone-Effekt zu isolieren (siehe §4/T3). Der Nachfrage-Teil der Idee ("wo willst du hin, sonst lokal suchen") ist dagegen ein billiger, sinnvoller UX-Fix: `thesis-finder` soll den Scope (Tübingen + BW) explizit nennen und bei Auswärts-Wunsch ehrlich sagen, dass das Tool dort nicht optimiert ist (T9).
- **Aufwand vs. Notennutzen:** Als Feature: mittel/negativ. Als Experiment-Arm: mittel/**sehr hoch**.

### Idee 2 — Evaluation testbar und aussagekräftig machen

- **Kern:** Die Evaluation soll wirklich messen, ob das Ding funktioniert.
- **Pro:** Trifft exakt die rote Achse aus §2. Ohne das ist jede weitere Arbeit Streuung.
- **Contra:** Keines. Nur die Versuchung, "Testbarkeit" als mehr Fixtures misszuverstehen — die Fixtures testen den Verhaltensvertrag, nie die Live-Qualität (das dokumentiert `evals/README.md:116` selbst).
- **Empfehlung: umsetzen, höchste Priorität.** Konkret: (a) **strict recall + Attributions-Präzision** als Hauptmetriken (primary recall ist durch das Org-Chart-Echo geschönt — die GT wurde aus denselben Seiten gebaut, die Pass 1 crawlt); (b) standardisiertes wiederholbares Live-Protokoll mit **n≥3 Läufen pro Zelle** (LLM-Varianz!), festen Personas, No-Peeking, Scoring-Blatt; (c) Runner-Realität anerkennen: Codex ist nicht verfügbar (nur Claude Pro) — Protokoll auf manuell-aber-standardisiert oder Claude-CLI-Runner umstellen; (d) unabhängige Firmen-GT (fremdkuratiert, nicht aus dem Backbone) gegen die Zirkularität.
- **Aufwand vs. Notennutzen:** hoch/**maximal**. Das ist der Unterschied zwischen 1.7 und 1.0.

### Idee 3 — Firmen-Backbone für alle Studiengänge/Fakultäten

- **Kern:** Das BW-Backbone soll Firmen für alle Fachbereiche abbilden, nicht nur MINT.
- **Pro:** Direkt am "alle Fachbereiche"-Anspruch (§10.1 der Design-Entscheidungen). Ohne minimale Nicht-MINT-Abdeckung ist Track (b) für eine Psychologin faktisch leer.
- **Contra:** Vollabdeckung zerstört genau die Eigenschaft, die das Backbone wertvoll macht (klein, kuratiert, wartbar — `Design-Entscheidungen.md` §1). Und Domi selbst erwartet (Idee 6), dass primär technische Studiengänge das Tool nutzen — der Grenznutzen breiter Firmen-Abdeckung ist also begrenzt.
- **Empfehlung: klein umsetzen.** Je 3–5 kuratierte Einträge für die vier benannten Lücken (Psych/Human-Factors/UX, EdTech, Umwelt, Life-Science) — deckungsgleich mit TODO 3 der Design-Entscheidungen. Nicht mehr.
- **Aufwand vs. Notennutzen:** klein/mittel.

### Idee 4 — Zusatzinfos (MPI/ELLIS-Äquivalente) für alle Studiengänge

- **Kern:** Was der MPI-IS/ELLIS-Fix für CS war, für jede Fakultät: die außeruniversitären/interfakultären Institute als Pflicht-Pass-1-Quellen.
- **Pro:** Das ist empirisch die wirksamste bekannte Intervention im Projekt: Der CS-Recall sprang durch genau diesen Fix von 60 % auf 100 % (`STATUS.md`, Task I-fix). Tübingen hat offensichtliche Kandidaten: IWM (Leibniz-Institut für Wissensmedien — Psych/EdTech), MPI für biologische Kybernetik, MPI für Biologie + FML, NMI Reutlingen (Medtech), DZNE/HIH (schon teils drin), CIN. Genau dieses kuratierte Lokalwissen ist es, was plain-Claude *nicht* hat — es stärkt die These direkt.
- **Contra:** Pflegeaufwand pro Eintrag; Gefahr, das Uni-Backbone aufzublähen. Beherrschbar: eine Tabelle "außeruniversitäre Pflicht-Quellen je Fachbereich" mit ~10–15 Zeilen reicht.
- **Empfehlung: umsetzen.** Bester Feature-Kandidat des ganzen Ideenzettels. Bonus: liefert die Daten für ein Dose-Response-Argument (Fakultäten mit dichter Kuratierung sollten größeres Delta zeigen).
- **Aufwand vs. Notennutzen:** klein-mittel/**hoch**.

### Idee 5 — Für alle Unis abstrahieren (Entry-Point per Websearch je Uni)?

- **Kern:** Ein generischer Mechanismus, der für beliebige Unis den Fakultäts-Entry-Point per Websearch findet — mit Domis eigenem Einwand: mehr Varianz, nicht für alle optimierbar, deshalb vielleicht doch nur Tübingen (Lokalitätsvorteil).
- **Pro:** Größere potenzielle Reichweite; intellektuell reizvoll.
- **Contra (entscheidend):** Ein Skill, dessen erster Schritt "google den Entry-Point" ist, *ist* im Wesentlichen plain-Claude mit Manieren. Der gemessene Mehrwert kommt aus dem kuratierten Backbone + Lokalwissen (MPI-Leg, Host-Besonderheiten wie `medizin.uni-tuebingen.de`, Drill-down-Muster) — nichts davon ist per Websearch zur Laufzeit herstellbar, sonst hätte die Baseline es auch. Abstraktion auf alle Unis konvergiert per Konstruktion gegen die Baseline (das ist Punkt 6, angewandt). Zudem: unvalidierbar — wir können nicht für 100 Unis Ground Truth bauen.
- **Empfehlung: verwerfen.** Domis Einwand gewinnt. Stattdessen: die **Generalisierung als Rezept dokumentieren** (AGENTS.md-Abschnitt: "So baust du ein Backbone für Uni X in ~2 Tagen" — Schritte, Qualitätskriterien, Prüfliste). Das zeigt dem Gutachter Generalisierbarkeit als *Methode*, ohne den Scope zu sprengen, und macht das Projekt für Nachnutzer andockbar.
- **Aufwand vs. Notennutzen:** hoch/negativ (als Feature); das Rezept: klein/mittel.

### Idee 6 — Sichtbarkeit + die SML-/Grenzwert-Intuition

- **Kern (a) Sichtbarkeit:** Website, E-Mail-Umfrage, Ersti-Heft, Menth — primär für Informatiker/technische Studiengänge.
- **Kern (b) SML-Intuition:** *Je breiter das Tool, desto mehr konvergiert es im Erwartungswert gegen plain-Claude.*

**Zu (b) — das ist das Kernargument der Thesis, und es verdient, ernst genommen zu werden.**
Formalisiert: Der Mehrwert ist Δ = E[Q(Tool) − Q(Baseline)] über die Anfrageverteilung.
Das Tool = Baseline + kuratierter Kontext (Backbone, Suchstrategie, Prozessdisziplin).
Die Kuratierungskapazität ist fix (eine Person, begrenzte Pflegezeit). Verbreitert man
den Scope, sinkt die **Kuratierungsdichte pro Anfrage**, und Δ → 0: Das Tool degeneriert
zum Erwartungswert der Baseline plus Rauschen. Umgekehrt maximiert Scope-Verengung
(Tübingen, alle Studiengänge) die Dichte — der **Lokalitätsvorteil**. Die eigenen Daten
stützen das bereits in zwei Richtungen: Der MPI-IS-Fix (mehr Lokalwissen → CS 60→100 %)
und der schwache C1-Firmen-Delta (+17 pp, weil die Baseline Bosch/ZF/Mercedes ohnehin
kennt — wo die Welt schon SEO-sichtbar ist, schrumpft Δ).

**Klare Stellungnahme: Ja, Scope-Verengung ist die stärkere wissenschaftliche Position.**
Nicht als Verlegenheitslösung, sondern als *Behauptung mit Vorhersagekraft*:

> **These:** Der Mehrwert eines LLM-Discovery-Agents über seine ungestützte Baseline ist
> proportional zur Dichte des kuratierten Lokalwissens im Anfrage-Scope. Ein bewusst
> scope-verengtes Tool (eine Universität, alle Fachbereiche) schlägt die Baseline
> deutlich; dieselbe Mechanik ohne Lokalwissen (fremde Universität) tut es nicht.

**Messbar machen (2×2-Design):** Arme = {Tool, Baseline} × {in-scope: Tübingen, out-of-scope: KIT oder TUM}. Für die fremde Uni eine kleine GT (1–2 Fakultäten, ~6 Chairs, fremdkuratiert oder von einer zweiten Person) bauen; das Tool läuft dort mit identischer Mechanik, aber ohne Backbone-Datei. Vorhersage: Δ_Tübingen ≫ Δ_fremd ≈ 0. Ergänzend Dose-Response innerhalb Tübingens: Δ pro Fakultät gegen Kuratierungsdichte (CS mit MPI-Leg vs. Fakultäten mit nur offiziellen Listen). Wenn beide Muster sichtbar sind, ist die Scope-Entscheidung **empirisch begründet** statt behauptet — das ist der Unterschied zwischen "wir haben ein Tool gebaut" und einer verteidigbaren These.

**Zu (a):** Umsetzen, aber als **Nutzerstudie framen**, nicht als Marketing: 5–10 echte Studierende (bewusst auch Nicht-Informatiker), echtes Profil, kurzer Fragebogen (Nützlichkeit, gefundene vs. selbst bekannte Optionen, Vertrauen). Das erledigt zugleich TODO 1 der Design-Entscheidungen (unabhängige Validation) und liefert das qualitative Evaluations-Kapitel. Ersti-Heft/Menth/Website sind Post-Thesis-Distribution — für die Note nachrangig.

- **Aufwand vs. Notennutzen:** (b) mittel/**maximal** — das ist die Thesis. (a) als Studie: mittel/hoch; als reine Distribution: klein/niedrig.

---

## 4. Die These, geschärft

Wir beweisen: **Kuratiertes, scope-verengtes Lokalwissen — nicht die LLM-Fähigkeit —
ist der begrenzende Faktor für verlässliche Thesis-Discovery.** Konkret: Ein
datenbankloser Agent-Skill, der ein diszipliniertes Profil-Interview mit einem
kuratierten Struktur-Backbone (offizielle Fakultätsstruktur + außeruniversitäre
Institute + BW-Firmenliste) und einer Zwei-Pass-Live-Suche kombiniert, erreicht an der
Universität Tübingen signifikant höheren, korrekt attribuierten Recall als plain-Claude
mit Websearch (Baseline) — und dieser Vorsprung verschwindet, wenn dieselbe Mechanik
ohne Lokalwissen auf eine fremde Universität angewandt wird. Gemessen wird gegen eine
**ernstzunehmende Baseline** (plain-Claude *mit* Websearch, gleiches Profil als Input),
mit strict recall + Attributions-Präzision, n≥3 Wiederholungen pro Zelle, fremdkuratierter
Ground Truth für Firmen und fremde Uni, und einer kleinen Realnutzer-Studie als externe
Validität. Die bewusste Nicht-Generalisierung auf andere Unis ist damit kein Mangel,
sondern das zentrale, empirisch belegte Designergebnis.

---

## 5. Ziel-Architektur des Tools

**Scope-Entscheidung:** Universität Tübingen (alle Fakultäten) + BW-Firmen. Punkt.
Andere Unis erscheinen ausschließlich (a) als Experiment-Kontrollarm und (b) als
dokumentiertes Generalisierungs-Rezept in AGENTS.md. Begründung: §3 Idee 5/6.

**Skill-/Datenfluss (Ziel-Zustand — weitgehend heutiger Zustand, plus Deltas):**

```
thesis-finder (Entry, Session-Persistenz, Scope-Ansage "Tübingen + BW")
   ├─ Profil: EINE kanonische 6D-Definition (Interests, Methods, Domain,
   │  Thesis-Stil, Skills, No-Gos) — identisch in thesis-finder,
   │  build-student-profile und beiden Discovery-Gates          [Delta: T6]
   ├─ find-university-chairs
   │    Pass 1: Fakultäts-Backbone + NEU: Pflicht-Tabelle außeruniversitärer
   │            Institute je Fachbereich (IWM, MPI-Kybernetik, NMI, …)  [Delta: T5]
   │    Pass 2: Live-Enrichment mit 2e/2f (unverändert)
   └─ find-company-thesis-options
        Pass 1: BW-Backbone (+ minimale Nicht-MINT-Ergänzung)   [Delta: T7]
        Pass 2: Live-Enrichment, doppelte URL-Verifikation (unverändert)
```

**Evaluations-Setup (was es können muss, um die These zu belegen):**

1. **Vier Zellen:** {Tool, Baseline} × {Tübingen, fremde Uni}; Baseline = plain-Claude
   *mit* Websearch und demselben Profil (kein Strawman).
2. **Metriken:** strict recall (empfohlen + korrekt attribuiert) als Hauptmetrik;
   Attributions-Fehler als eigene Fehlerklasse (ein falscher Prof ist schlimmer als ein
   fehlender); primary recall nur nachrichtlich.
3. **Wiederholung:** n≥3 Läufe pro Zelle, Mittelwert + Spannweite berichtet.
4. **Unabhängige GT:** Firmen-GT und Fremd-Uni-GT nicht aus den eigenen Backbones;
   idealerweise von einer zweiten Person kuratiert.
5. **Reproduzierbarkeit ohne Codex:** standardisiertes manuelles Protokoll
   (Checkliste + Scoring-Blatt, Artefakte versioniert wie `dist/live-validation/`)
   oder Claude-basierter Runner; der Codex-Runner-Pfad wird als optional dokumentiert.
6. **Extern:** 5–10-Personen-Nutzerstudie mit Kurzfragebogen.

**Explizite Nicht-Ziele:** kein Multi-Uni-Produkt; kein Stellen-Scraping; keine
Datenbank/Backend; keine Vollabdeckung des Firmen-Backbones; keine Website mit
Login/Speicherung; kein Umbau des CI/Release-Systems (funktioniert).

---

## 6. Umsetzungsplan (priorisiert nach Notennutzen pro Aufwand)

1. **These + Scope fixieren** — MASTERPLAN/VISION um den These-Absatz (§4) und die
   Scope-Entscheidung ergänzen; Ideen 1/5 als "bewusst verworfen, weil…" dokumentieren.
   → verify: These steht wörtlich in MASTERPLAN.md; STATUS-Logzeile; Domi-Review.
2. **Eval-Protokoll v2 schreiben** — standardisiertes Live-Protokoll (Personas, No-Peeking,
   Scoring-Blatt, strict recall + Attributions-Präzision, n≥3, Artefakt-Ablage) als
   `findings/…-eval-protocol-v2.md`; Codex-Abhängigkeit als optional deklarieren.
   → verify: 1 Pilotlauf (Tübingen, 1 Fakultät, Tool-Arm) nach Protokoll durchgeführt
   und gescored, Artefakte committed.
3. **Scope-Experiment (Kern)** — Fremd-Uni-GT bauen (KIT *oder* TUM, 1–2 Fakultäten,
   ~6 Chairs, fremd-/zweitpersonen-kuratiert); 4 Zellen × n≥3 laufen; Dose-Response-Tabelle
   (Δ je Tübinger Fakultät vs. Kuratierungsdichte) mitführen.
   → verify: Ergebnis-Doc mit 4-Zellen-Tabelle; Vorhersage Δ_in ≫ Δ_out geprüft
   (auch ein Negativergebnis ist berichtbar — dann diskutieren, ehrlich).
4. **Unabhängige Firmen-GT + Re-Eval** — 2–3 Profile gegen fremdkuratierte Firmenliste
   (nicht aus `bw-company-backbone.md`) messen; Zirkularitäts-Caveat damit schließen
   oder quantifizieren.
   → verify: Recall gegen fremde GT dokumentiert; Design-Entscheidungen §10.2 aktualisiert.
5. **Außeruniversitäre Pflicht-Quellen je Fachbereich** (Idee 4) — Tabelle mit ~10–15
   Instituten (IWM, MPI-Kybernetik, MPI Biologie/FML, NMI, DZNE, CIN, …) in
   `tuebingen-faculty-backbone.md` + Verdrahtung in SKILL.md Step 4.
   → verify: Psychologie-Live-Lauf strict recall verbessert sich gegenüber Task-I-fix-Stand;
   Referenz-Validator/pytest grün.
6. **Profil-Dimensionen vereinheitlichen** — `build-student-profile/SKILL.md:15` auf die
   kanonischen 6D (inkl. Methods, Domain) bringen; Kurs-/Erfahrungsfragen bleiben als
   Erhebungsweg, nicht als Dimension.
   → verify: identische 6D-Liste in allen 4 betroffenen SKILL.md; `pytest -q` grün.
7. **Firmen-Backbone Nicht-MINT-Minimum** (Idee 3) — je 3–5 kuratierte Einträge für
   Psych/UX, EdTech, Umwelt, Life-Science; URLs live spot-checken.
   → verify: 4 neue Unterabschnitte mit Last-verified-Datum; Spot-check-Log ergänzt.
8. **Scope-Ansage im thesis-finder** (Idee 1b) — Ein Satz im New-User-Flow: Scope ist
   Tübingen + BW; bei explizitem Auswärts-Wunsch ehrlicher Hinweis statt stiller
   Degradierung.
   → verify: SKILL.md-Diff + Smoke-Trace; Tests grün.
9. **Nutzerstudie** (Idee 6a / TODO 1) — 5–10 Studierende, mind. 3 Nicht-Informatik;
   Kurzfragebogen; Ergebnisse als findings-Doc.
   → verify: ausgefüllte Bögen (anonymisiert) + Auswertungs-Doc committed.
10. **Generalisierungs-Rezept** (aus Idee 5) — AGENTS.md-Abschnitt "Backbone für eine
    neue Universität bauen" (Schritte, Qualitätskriterien, Aufwandsschätzung).
    → verify: Abschnitt existiert; von T3-Erfahrung (Fremd-Uni-GT) informiert.

Reihenfolge-Logik: T1–T3 sind die Notenbringer und voneinander abhängig (These → Protokoll
→ Experiment). T5 vor T3 abschließen, damit das Experiment den End-Zustand des Tools misst.
T4/T9 parallelisierbar. T6–T8 sind kleine Hygiene-Fixes für zwischendurch. T10 zuletzt.

---

## 7. Risiken & offene Fragen an Domi

- **Risiko: Das Scope-Experiment könnte die These nicht bestätigen** (Δ_fremd unerwartet
  groß, weil KIT/TUM-Zentralportale dem Tool *und* der Baseline helfen). Das wäre kein
  Beinbruch — dann lautet das Ergebnis "der Backbone-Vorteil hängt von der
  Web-Struktur der Ziel-Uni ab", ebenfalls verteidigbar. Aber einplanen, dass die
  Diskussion beide Ausgänge tragen muss.
- **Risiko Selbst-Scoring:** Auch Protokoll v2 wird von dir gescored. Minimal-Fix: eine
  zweite Person scored eine Stichprobe nach (Inter-Rater-Check auf ~20 % der Items).
- **Risiko Zeit:** T3 + T4 + T9 sind zusammen mehrere volle Tage. Wenn gekürzt werden
  muss: T9 (Nutzerstudie) zuerst verkleinern (5 statt 10), niemals T3.
- **Frage 1 (die Entscheidung):** Fremd-Uni für den Kontrollarm — **KIT oder TUM?**
  (KIT näher/BW, TUM hat das prominenteste Zentralportal und ist damit der härtere,
  ehrlichere Vergleich. Empfehlung: TUM.)
- **Frage 2:** Wer ist die zweite Person für fremdkuratierte GT + Inter-Rater-Check
  (Kommilitone, Fachschaft, Max)?
- **Frage 3:** Gibt es eine Deadline/Abgabetermin, gegen die T3/T9 geplant werden müssen?
