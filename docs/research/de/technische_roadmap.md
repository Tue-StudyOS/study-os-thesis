# Technischer Status & Roadmap

**StudyOS Thesis Advisor — Forschungspaket, Bericht 2 von 5**
**Datum:** 11.06.2026 · **Deadline:** 01.07.2026 · **Verifiziert gegen Live-Repo:** 5 offene PRs, 16 offene Issues (Stand: 11.06.2026)

---

## 1. Architektur-Bewertung

| Komponente | Zustand | Anmerkungen |
|---|---|---|
| FastAPI + async SQLAlchemy | Ausgereift | Externer Review (StudyOS Bot) bestätigt „real MVP, not demo" |
| Datenbank-Migrationen | Stabil | Alembic-Kette 0001–0014; Parent-Refs und Down-Revisions in den letzten 5 Commits korrigiert |
| Frontend (React/Vite) | Feature-komplett für MVP | i18n fast fertig (PR #38, aktueller Branch) |
| LLM-Integration (Ollama / gemma4) | Funktioniert | Local-First; DeepSeek-Pfad hat bekannten Duplikate-Bug (#33) |
| Celery/Redis Job-Queue | Funktioniert | WebSocket-Job-Events laufen; aber siehe Sicherheitspunkt unten |
| PostgreSQL + pgvector | Ausgereift | Keine Änderungen erforderlich |

Zwei nicht-funktionale Punkte aus dem externen Review sind als **Deployment-Blocker** einzustufen:

- **Sicherheit:** WebSocket-JWT im URL-Query-String (`frontend/src/api/jobEvents.ts`, `backend/app/ws/controller.py`). URLs landen in Server-Logs, Proxies und Browser-History. Muss auf ein kurzlebiges Ticket oder ein Secure Cookie umgestellt werden, bevor irgendeine gehostete Instanz läuft.
- **Vertrauen:** `ChairExplorer.tsx` enthält hardkodierte Metriken (Team-Größen, Zitationszahlen). Erfundene Zahlen gegenüber den Professoren zu zeigen, die uns sagten, Vertrauen sei ihr Hauptkritikum (Bericht 1, §3.4), wäre selbstverschuldeter Schaden. Ausblenden oder als „nicht verfügbar" markieren, bis echte Scraping-Daten vorliegen.

---

## 2. Feature-Checkliste vs. MVP-Ziel

MVP-Ziel (Plan.docx): *„Nach <1 Stunde haben Nutzer eine viel bessere Idee, welchen Lehrstuhl sie kontaktieren sollen + Infrastruktur für einfache Lehrstuhl-Updates."*

| Feature | Status |
|---|---|
| Transcript (Notenausdruck)-Upload | ✅ Funktioniert |
| Kompetenzprofil | ✅ Funktioniert (Berechnung noch Dummy — #16/PR #21) |
| Semantisches Lehrstuhl-Matching | ✅ Funktioniert |
| Proposal-Generierung | ✅ Funktioniert |
| Einstellungen + i18n (DE/EN) | 🔄 PR #38 (aktueller Branch), schließt #23/#29 |
| Auto-Discovery von Lehrstuhl-Infos | 🔄 PR #35 + #37 (schließt #22/#36) |

**Bewertung: Student-seitiges MVP ist zu ~90 % vollständig.** Die „Infrastruktur für einfache Lehrstuhl-Updates" liegt vollständig in der #35→#37-Pipeline — das ist der kritische Pfad.

---

## 3. Priorisierung offener PRs

| PR | Titel | Priorität | Begründung |
|---|---|---|---|
| #35 | Chair & University-Employee Schema | **P0 — zuerst mergen** | Voraussetzung für #37; alles Nachgelagerte basiert auf diesem Schema |
| #37 | Chair-Discovery Scraping Agent | **P0 — kritischer Pfad** | Das feedback-validierte Kernfeature (Macke: „reads the relevant section in our website … much more excited about"). Schließt #36/#22 |
| #38 | i18n-Übersetzung aller Seiten | **P1 — vor Deployment mergen** | Fertige Arbeit, geringes Risiko; Merge räumt Backlog auf |
| #21 | Skill-Berechnung | **P2** | Ersetzt Dummy-Kompetenzberechnung (#16); für Profil-Genauigkeit in der RAG-Phase wichtig, nicht jetzt |
| #34 | Dedup DOI-lose Re-Scrapes | **P2** | Datenqualitäts-Polish; wird wichtiger, sobald #37 im Produktionsbetrieb scrapt |

Empfohlene Merge-Reihenfolge: **#35 → #37 → #38 → #34 → #21** (#38 kann jederzeit gemergt werden, solange kein Konflikt besteht).

---

## 4. Priorisierung offener Issues nach Timeline

### Wochen 8–14 (JETZT — Auto-Discovery-Phase)
- **#36 / #22** — Chair-Discovery-Agent: PRs #35 + #37 landen. Das Gate für alles weitere.
- **#18** — Startup-Loading-Icon-Bug: klein, opportunistisch beheben.
- **#15** — UI-Formatierungsfehler: ebenso.

### Wochen 15–21 (RAG-Phase)
- **#7** — RAG-Fähigkeiten optimieren (das erklärte Ziel dieser Phase).
- **#16** — Dummy-Skill-Berechnung ersetzen (PR #21 hier landen).
- **#33** — DeepSeek-Duplikate (vor jeder Präsentation beheben — doppelte Daten sind ein Vertrauensproblem).
- **#6** — deepeval hinzufügen: früh in dieser Phase; „RAG verbessert" ist eine unbelegbare Behauptung ohne Eval-Harness.
- **#32** — Paper-Tags: unterstützt besseres Retrieval.

### Wochen 22–28 (Deployment-Phase)
- **Sicherheits-Audit:** WebSocket-JWT → kurzlebiges Ticket/Secure Cookie (noch kein Issue — **Issue anlegen**).
- **Vertrauens-Audit:** ChairExplorer-Hardcoded-Metriken (noch kein Issue — **Issue anlegen**).
- **Docs-Abgleich:** README sagt „no cloud accounts needed", Config unterstützt Azure/DeepSeek — vor externen Augen bereinigen.
- **#25** — Markdown-Rendering (sichtbarer Polish für erste Nutzer).
- **#29** — Hilfe/Einstellungsseite (soweit von #38 noch nicht abgedeckt).

### Wochen 29–01.07 (Umfrage/Puffer)
- Quantitative Umfrage (Google Forms, per Plan.docx „nice-to-have").
- Bug-Reports von frühen Nutzern.
- **Zurückgestellt:** #14 (Startprompt), #4 (OCR-Engine), #5 (Port-Adapter-Pattern), #13 (DeepSeek-Tests). #5 ist ein Architektur-Refactoring ohne MVP-Nutzen.

---

## 5. Kritischer Pfad bis 01.07.

```
Woche 8–10   #35 mergen, #37 stabilisieren (Review, CI grün, Rebase-Kette)
Woche 11–14  Chair-Discovery-Agent läuft gegen echte Lehrstuhl-Seiten;
             #38, #34 mergen; #18/#15 opportunistisch fixen
Woche 15–16  deepeval-Harness (#6) + Baseline RAG-Metriken
Woche 17–19  RAG-Optimierung (#7), Skill-Berechnung (#21/#16), #33
Woche 20–21  Vollständiger RAG-Retest gegen Baseline
Woche 22–24  Security-Fix (JWT), Trust-Fix (ChairExplorer), Docs
Woche 25–26  Staging-Deployment, Smoke-Tests
Woche 27–28  Abschließende Bugfixes, Polish (#25)
Woche 29–1.7 Frühe Nutzung beobachten; Umfrage wenn Zeit
```

Gemäß CLAUDE.md §4: Jedes Phasen-Gate ist „CI grün via `gh pr checks`" — keine Phase startet auf einem roten Main.

---

## 6. Risiko-Bewertung

| Risiko | Wahrscheinlichkeit | Auswirkung | Mitigation |
|---|---|---|---|
| Chair-Discovery (#37) Scope-Creep — 27+ Lehrstühle mit heterogenen Webseiten (Typo3, Custom, PDF-Listen, Google Docs) | **Hoch** | Terminverzug kaskadiert | Timebox: zunächst 5–8 häufigste Seitenstrukturen; manuelle Fallback-Einträge für den Rest. „Funktioniert für 20 von 27 Lehrstühlen" ist ein valides MVP |
| JWT-in-URL bei Demo/Hosting entdeckt | Mittel | Showstopper für Vertrauen | Fix in Woche 22 spätestens; ca. 3–5 Tage Aufwand; explizit einplanen |
| Hardkodierte Metriken im ChairExplorer einem Professor gezeigt | Mittel | Glaubwürdigkeitsverlust bei der Kernzielgruppe | Vor *jeder* Demo ausblenden/markieren |
| RAG-Phase frisst Deployment-Puffer | Mittel | Wochen 22–28 verdichten sich | RAG-Verbesserungen blockieren MVP nicht — Scope kürzen, bevor Deployment-Aufgaben weichen |
| Team-Kapazität (Valentin Mo/Mi) | Bekannte Einschränkung | Durchsatz-Deckel | Scope oben berücksichtigt das; die zurückgestellte Issue-Liste ist das Druckventil |
| Technische Schulden | Niedrig | — | Kein MVP-blockierendes Problem identifiziert |

**Fazit: Eng, aber machbar.** Der Zeitplan hält, wenn #35+#37 bis Woche 14 landen. Alles in Wochen 15–21 kann schrumpfen; die Sicherheits- und Vertrauens-Fixes in Wochen 22–24 nicht.
