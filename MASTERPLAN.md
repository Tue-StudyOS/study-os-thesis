# Masterplan — StudyOS Thesis-Finder

> **Zweck:** Die herausgezoomte Sicht auf das gesamte Vorhaben. Diese Datei ist ein **Lookup** — sie beschreibt *was* gebaut wird, *in welcher Reihenfolge* und *warum*. Sie ändert sich selten.
>
> **Den aktuellen Fortschritt, offene Schwierigkeiten und Tagesnotizen findest du in [STATUS.md](STATUS.md)** — das ist die einzige Datei, die laufend aktualisiert wird.

---

## 1. Was wir bauen

Einen Satz portabler **Claude Skills**, die einen Studenten von vagen Interessen bis zur vorbereiteten Kontaktaufnahme mit einem passenden Thesis-Betreuer führen — ohne Backend, DB oder UI, allein über kuratierte Markdown-Daten + Live-Recherche.

Der Ablauf der Skills:

```
roher Input ("ich mag Deep Learning + Robotik")
   │
   ▼  build-student-profile        tiefes Interview → strukturiertes Profil (nur in-session)
   ▼  find-university-chairs        passende Lehrstühle aus der Datenbank + Live-Websearch
   ▼  match-thesis-advisors         ranked Betreuer nach Fit + Evidenz
   ▼  find-recent-papers            relevante Paper als Beleg
   ▼  generate-thesis-directions    konkrete Thesis-Richtungen + Proposal-Hooks
   ▼  draft-thesis-contact          erste Kontakt-Mail
```

Plus Wartungs-Skills: `update-openalex-paper-index` (Daten-Refresh) und `design-agent-skill` (Meta).

---

## 2. Die Datenstruktur — der Baum

Das Herzstück ist eine **Baumstruktur** als Markdown-Datenbank:

```
Professor  (Themenbereich + Beschreibung)
   └── PhD  (Themenbereich + Beschreibung)
          └── Paper (mit Zusammenfassung)
```

Jeder Professor hat einen Themenbereich und eine Beschreibung; darunter alle seine PhDs mit eigenem Themenbereich; darunter deren Paper mit Zusammenfassung. Alles als `.md` nach dem Scrapen gespeichert, referenziell verknüpft.

---

## 3. Leitprinzip der Reihenfolge

**Erst die Daten korrekt, dann alles andere.** Downstream-Qualität (Matching, Proposals) ist nicht prüfbar, solange die Datenbasis falsch oder unvollständig ist. Deshalb ist Phase 1 (Datenfundament) ein hartes Gate vor Phase 2 (Optimierung).

**De-Risk-Strategie:** Nicht "alle 47 Profs perfekt" als Gate, sondern **Pilot mit 3 Lehrstühlen → Pipeline + Validierung beweisen → auf 47 skalieren.**

---

## 4. Phase 1 — Datenfundament (aktuelle Phase)

Das Epic "verifizierter Forscher-Baum". Reihenfolge = Abhängigkeit.

| # | Issue | Worum es geht |
|---|---|---|
| 1 | [#45](https://github.com/Tue-StudyOS/study-os-thesis/issues/45) | **Author-IDs für alle 47 Profs** auflösen (Name+URI → OpenAlex-ID, mit Disambiguierung) |
| 2 | [#46](https://github.com/Tue-StudyOS/study-os-thesis/issues/46) | **Ground-Truth-Liste** für 3 Pilot-Lehrstühle (manuelle PhD-Soll-Liste als Messmaßstab) |
| 3 | [#47](https://github.com/Tue-StudyOS/study-os-thesis/issues/47) | **PhD-Discovery pro Lehrstuhl** (Team-Seite + Co-Autor-Graph; keiner vergessen) |
| 4 | [#48](https://github.com/Tue-StudyOS/study-os-thesis/issues/48) | **Baum-Schema** Prof→PhD→Paper + referenzielle Integrität |
| 5 | [#49](https://github.com/Tue-StudyOS/study-os-thesis/issues/49) | **Paper-Scrape + Themenbereich/Beschreibung** pro Person, als Baum-MD |
| 6 | [#50](https://github.com/Tue-StudyOS/study-os-thesis/issues/50) | **Validierungs-Harness** (Anomalie-Checks + Stichproben + Golden Record) |
| 7 | [#51](https://github.com/Tue-StudyOS/study-os-thesis/issues/51) | **Automation** (Cron alle 2 Wochen, PR-Output, Override-Schutz, lautes Scheitern) |

Abhängigkeitsgraph:

```
1 (Prof-IDs) ─┐
2 (Ground Truth) ─→ 3 (PhD-Discovery) ─→ 5 (Paper+Beschreibung) ─→ 6 (Validierung) ─→ 7 (Automation)
4 (Schema) ───────────────────────────────┘
                                                                         ↓
                                                        Gate: erst wenn 6 grün → Phase 2
```

**Gate Phase 1 → Phase 2:** Issue 6 (Validierung) ist grün, Golden Record reproduzierbar, Pilot-Recall ≥ 90 %.

---

## 5. Phase 2 — Skill-Optimierung (nach dem Gate)

Erst sinnvoll, wenn die Daten stimmen.

- **Baseline messen** — aktuelle Eval-Scores einfrieren, bevor irgendetwas geändert wird.
- **Eval-Set erweitern** — pro Kern-Skill mehrere Cases (Happy-Path, flaches Profil, fehlende Infos, Adversarial), statt 1.
- **Few-shot-Beispiele** in die Kern-Skills (`build-student-profile`, `find-university-chairs`, `match-thesis-advisors`).
- **Guardrails vereinheitlichen** (Shallow-Profile-Schutz überall).
- **End-to-End-Flow-Eval** über die ganze Skill-Kette.
- **Judge kalibrieren** gegen menschliches Urteil.

## 6. Phase 3 — Cross-Platform (Stretch)

Inhalt ist portabel, Mechanismus nicht. Reihenfolge: OpenAI Custom GPT (am nächsten am Skill-Erlebnis) → Gemini → generisches RAG. Erst nach Phase 2, da man optimierte Inhalte portiert, keine unfertigen.

---

## 7. Wie dieser Plan benutzt wird

- **MASTERPLAN.md** (diese Datei) = stabiler Lookup. Wird nur angepasst, wenn sich der Plan strukturell ändert.
- **[STATUS.md](STATUS.md)** = lebendes Dokument. Hier landen Fortschritt, Blocker, Entscheidungen, Tagesnotizen. **Immer hier updaten, nicht im Masterplan.**
- **GitHub Issues** = die ausführbaren Einheiten. Jedes Issue oben verlinkt; Details, Akzeptanzkriterien und Diskussion leben im Issue.
