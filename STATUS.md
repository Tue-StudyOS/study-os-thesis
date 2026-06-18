# Status — StudyOS Thesis-Finder

> **Dies ist die einzige laufend aktualisierte Datei.** Hier sammeln wir Fortschritt, Blocker, Schwierigkeiten und Entscheidungen. Der stabile Gesamtplan steht in [MASTERPLAN.md](MASTERPLAN.md).
>
> **Konvention:** Beim Arbeiten an einem Schritt hier den Status ändern, Schwierigkeiten notieren und unten im Log eine datierte Zeile ergänzen. Nicht den Masterplan editieren.

**Letztes Update:** 2026-06-18

---

## Aktuelle Phase

**Phase 1 — Datenfundament.** Ziel: verifizierter Forscher-Baum (Prof → PhD → Paper) für die Pilot-Lehrstühle, dann skaliert auf 47 Profs.

---

## Step-Status

Legende: ⬜ offen · 🟨 in Arbeit · ✅ fertig · ⛔ blockiert

| # | Step | Status | Owner | Notizen / Schwierigkeiten |
|---|---|---|---|---|
| 1 | [#45](https://github.com/Tue-StudyOS/study-os-thesis/issues/45) Author-IDs für alle 47 Profs | ⬜ | – | Aktuell nur 7/47 in `researchers/INDEX.md`. Disambiguierung ist die Hürde. |
| 2 | [#46](https://github.com/Tue-StudyOS/study-os-thesis/issues/46) Ground-Truth für 3 Pilot-Lehrstühle | ⬜ | – | Maßstab, um "keiner vergessen" messbar zu machen. |
| 3 | [#47](https://github.com/Tue-StudyOS/study-os-thesis/issues/47) PhD-Discovery pro Lehrstuhl | ⬜ | – | Schwerster Teil: OpenAlex hat keine Betreuer→PhD-Kante. |
| 4 | [#48](https://github.com/Tue-StudyOS/study-os-thesis/issues/48) Baum-Schema + Integrität | ⬜ | – | PhD-Ebene fehlt im aktuellen Schema. |
| 5 | [#49](https://github.com/Tue-StudyOS/study-os-thesis/issues/49) Paper-Scrape + Beschreibung pro Person | ⬜ | – | Beschreibung/Zusammenfassung = LLM-Schritt; Entscheidung Abstract vs. LLM offen. |
| 6 | [#50](https://github.com/Tue-StudyOS/study-os-thesis/issues/50) Validierungs-Harness | ⬜ | – | Anomalie-Checks statt Vollprüfung; Golden Record als Anker. |
| 7 | [#51](https://github.com/Tue-StudyOS/study-os-thesis/issues/51) Automation (Cron + PR + Overrides) | ⬜ | – | Override-Schutz, damit Re-Scrape manuelle Fixes nicht zerstört. |

**Gate Phase 1 → 2:** Step 6 grün · Golden Record reproduzierbar · Pilot-Recall ≥ 90 %.

---

## Offene Entscheidungen

- **Datenquelle zur Laufzeit:** Scraper-DB zuerst oder Live-Websearch zuerst? → später optimieren, blockiert Phase 1 nicht.
- **Beschreibung/Zusammenfassung:** Abstract übernehmen (gratis, deterministisch) vs. LLM-Summary (schöner, teurer)?
- **Scrape-Kadenz:** alle 2 Wochen vs. monatlich?

---

## Bekannte Schwierigkeiten / Risiken

- **PhD-Discovery-Recall** — 47 heterogene Team-Seiten; ohne Ground Truth nicht messbar (siehe Step 2 → 3).
- **Name→ID-Disambiguierung** — häufige Namen, PhDs mit wenigen Papern.
- **Manuelle Korrekturen** — dürfen beim Re-Scrape nicht überschrieben werden (Step 7).
- **30-MB-Upload-Limit** der Skills-API im Blick behalten, wenn der Baum wächst.
- **Personendaten (DSGVO)** — PhD-Namen + Forschung werden gebündelt; öffentliche akademische Daten, aber bewusst dokumentieren.

---

## Log

- **2026-06-18** — Masterplan + Status + Workflow angelegt. Phase 1 definiert, 7 Issues erstellt. Ausgangslage: 8 Skills funktionsfähig, Daten erst 7/47 Profs, 0 PhDs.
