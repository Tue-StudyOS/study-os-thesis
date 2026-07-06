# Zusammenfassung für Stakeholder — StudyOS Thesis Advisor

**Datum:** 11.06.2026 · **Deadline:** 01.07.2026 · **Vollständige Analyse:** marktanalyse.md, technische_roadmap.md, produktpositionierung.md, detaillierte_analyse.md

---

## Status

Das studentenseitige MVP ist zu ~90 % vollständig: Transcript-Upload, Kompetenzprofil, semantisches Lehrstuhl-Matching und Proposal-Generierung funktionieren alle; i18n ist in Review (PR #38). 5 PRs und 16 Issues sind offen; der kritische Pfad ist das **Landen des Chair-Discovery-Scraping-Agents (PR #35 → #37)**. Wir sind auf Kurs für den 01.07.2026, **wenn** diese Pipeline bis Woche 14 gemergt wird.

## Was uns 27 Professoren sagten

- **~35 %** (Typ B): würden ein Themen-Tool ausprobieren — aber nur wenn ohne Reibung, keine Reminder-E-Mails, jahrelang stabil und auf ihre eigene Webseite exportierbar.
- **~50 %** (Typen A + C): wollen keine zentrale Plattform — entweder bereits mit Anfragen überschwemmt, oder überzeugte Befürworter der Ko-Kreation von Themen im Gespräch.
- **~15 %** (Typ D): für deren Recruiting-Pipeline irrelevant (GTC, Lehrveranstaltungen).

**Kernerkenntnnis:** Eine Listing-Plattform wurde in diesem Fachbereich bereits versucht (~2022) und scheiterte aus Anreizgründen, nicht wegen der Oberfläche (Hennig). **Erst für Studierende bauen; Professoren können optional andocken.** Das am meisten befürwortete Feature ist eines, das wir bereits bauen: Scraping bestehender Lehrstuhl-Webseiten statt Professoren um Dateneingabe zu bitten (Macke: „that would be something I am much more excited about").

## Roadmap

| Phase | Fokus |
|---|---|
| **Jetzt – Woche 14** | Schema-Grundlagen (#35) + Chair-Discovery-Agent (#37) mergen; i18n (#38) mergen |
| **Wochen 15–21** | Eval-Harness (deepeval, #6), RAG-Optimierung (#7), echte Skill-Berechnung (#21/#16), DeepSeek-Dedup (#33) |
| **Wochen 22–28** | Security-Fix (WebSocket-JWT), Trust-Fix (ChairExplorer-Platzhalter-Metriken), Docs-Abgleich, Staging-Deployment |
| **Wochen 29 – 01.07.** | Frühe Nutzung beobachten; quantitative Umfrage (optional) |

## Top 3 Risiken

1. **Chair-Discovery Scope-Creep** — 27 heterogene Lehrstuhl-Webseiten; wenn #37 nach Woche 14 verschiebt, verschiebt sich der gesamte Zeitplan. Mitigation: Timebox auf häufigste Seitenstrukturen, manuelle Fallbacks für den Rest.
2. **WebSocket-JWT im URL** — Tokens werden in Logs/Proxies geleakt; Showstopper für jedes gehostete Deployment. Bekannter Fix, ~3–5 Tage; muss vor Staging landen.
3. **Hardkodierte Metriken im ChairExplorer** — erfundene Team-/Zitationszahlen, die Professoren gezeigt werden, deren Nr.-1-Anliegen Vertrauen ist. Vor *jeder* Demo ausblenden.

## Top 3 Prioritäten, nächste 2 Wochen

1. **#35, dann #37** reviewen und mergen (Chair-Discovery-Pipeline) — CI grün via `gh pr checks`.
2. **Security-Issue anlegen und einplanen** (JWT → kurzlebiges Ticket oder Secure Cookie).
3. **ChairExplorer auf Platzhalter-Daten prüfen**; ausblenden oder als „Daten nicht verfügbar" markieren.
