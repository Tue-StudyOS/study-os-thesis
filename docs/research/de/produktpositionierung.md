# Produktpositionierung & Narrativ

**StudyOS Thesis Advisor — Forschungspaket, Bericht 3 von 5**
**Datum:** 11.06.2026

---

## 1. Das Problem, das wir wirklich lösen

**Nicht:** „Professoren wollen einfachere Themenverwaltung."
Das Feedback ist eindeutig — die meisten wollen das nicht (Bericht 1). Butz hat „no problems getting students." Macke „does not see the added value." Luxburg: „profs never update the topics. We've had many attempts in the department already."

**Ja:** „Studierende verschwenden Wochen damit, den richtigen Betreuer zu finden, und Professoren ertrinken in Fehlanfragen."
Belege von den Professoren selbst:

- Menth betreut 20 Abschlussarbeiten, erhielt Anfragen für **50+**, bedauert jede Absage und wünscht sich explizit „ein System, mit dem Studierende leichter an Abschlussarbeiten kommen können."
- Mackes Gruppe erhält „a number of expressions of interest which is way larger than we can supervise."
- Winther: Studierende sahen 4–5 gelistete Themen, gingen davon aus, das sei das gesamte Labor, „and then did not talk to us" — schlechte Information *verschlechterte* das Matching.

Beide Seiten verlieren durch dasselbe Versagen: **Erstkontakt mit schwachem Signal.** Studierende kontaktieren die falschen Lehrstühle mit generischen E-Mails; Lehrstühle verbringen Zeit damit, abzusagen. Die Lösung sind besser vorbereitete Studierende, nicht mehr Listings.

---

## 2. Warum der Plattform-Ansatz schwieriger ist als er scheint

Vier voneinander unabhängige Versagensmodi, jeder durch Feedback bestätigt:

1. **Das Anreizproblem.** Mehr Themen listen → mehr Bewerbungen → mehr Absagen → Professoren bereuen das Listing (Macke, Menth, Hennigs 2022er Präzedenzfall). Hennig: Das Anreizproblem zu lösen „doesn't have much to do with the interface or the frontend … It's all about the internal dynamics of the CS department."
2. **Tool-Müdigkeit.** Lehrstühle jonglieren bereits 8+ Systeme (Mackes Liste). Ein neues Login mit eigenem Rechteverwaltungsoverhead ist ein Kostenfaktor, bevor es Nutzen bringt.
3. **Die Stabilitätsfrage.** Hennig nennt einen konkreten Kadaver: courses.cs.uni-tuebingen.de, von „very engaged" HiWis gebaut, zerfiel in dem Moment, als sie gingen. „The website must be stable for at least a few years (i.e., also after you are long gone)." Wir können diese Garantie derzeit nicht geben.
4. **Die Ko-Kreations-Überzeugung.** Für eine große Gruppe (Berens, Winther, Stephan, Bob, Luxburg) sind vorab gelistete Themen nicht nur unpraktisch — sie sind *pädagogisch falsch*. Bob: „the formulation of the question is actually the most important and difficult part of doing the thesis." Kein UI-Design behebt einen philosophischen Einwand.

---

## 3. Was wir tatsächlich bauen (neu gerahmt)

Drei Ebenen in strikter Prioritätsreihenfolge:

### Ebene 1 — Für Studierende (das Produkt)
Ein Chat-Agent, der einem Studierenden hilft:
- **Formulieren** der eigenen Interessen und Einschränkungen (Transcript-Upload → Kompetenzprofil),
- **Entdecken**, welche Lehrstühle wirklich an relevanten Problemen arbeiten (semantisches Matching über gescrapte öffentliche Daten — Publikationen, Gruppenwebseiten, Forschungsbereichsbeschreibungen),
- **Vorbereiten** eines hochqualitativen Erstkontakts: eine Kontextzusammenfassung, wer man ist, was man kann und warum genau dieser Lehrstuhl passt.

Das ist der bestehende Codebase. Er benötigt **null Professorenbeteiligung**, um Mehrwert zu liefern.

### Ebene 2 — Für Lehrstühle (optional, später)
Kein Management-Dashboard. Drei leichte Touchpoints, jeder einer expliziten Anfrage aus dem Feedback entsprechend:
- **Schlüsselworte / Forschungsbereiche, keine Projektinventare** (Häufle, Bob, Niels, Mario) — Daten, die „would not need revision very often."
- **Von bestehenden Webseiten ziehen** statt Input abzufragen (Mackes Gegenvorschlag; Ostermanns ps.cs.uni-tuebingen.de hat die Daten bereits). Das ist PR #37.
- **Exportierbar** — Listings portierbar zu Gruppenwebseiten (Husons Bedingung).
- **Eiserne Regel: keine Reminder-E-Mails als Standard.** (Macke; Wichmann will Frequenz „under user control" — Standard null.)

### Ebene 3 — Für den Fachbereich (nur lesend)
Eine aggregierte, durchsuchbare Übersicht aller Forschungsbereiche aller Lehrstühle — aus Ebene-2-Daten und Scraping gebaut, für Studierende browsbar. Kein Lehrstuhl-Workflow dahinter. Jede Lehrstuhlseite trägt Bobs vorgeschlagenen Standardhinweis, sinngemäß: *„Dies sind nur Ausgangspunkte. Ein wesentlicher Teil einer Abschlussarbeit ist die Formulierung und Präzisierung der Frage selbst."*

---

## 4. Wie das die Feedback-Punkte beantwortet

| Professoren sagten | Wir bieten nun |
|---|---|
| „Baut kein System, das wir nutzen müssen" (Macke, Stephan) | Ein Studierenden-Tool; Lehrstühle sind standardmäßig passive Datenquellen |
| „Lest unsere bestehende Webseite stattdessen" (Macke, Ostermann) | Scraping-Agent (#37) ist der Kern-Ingestion-Pfad |
| „Themen werden ko-kreiert, nicht gebrowst" (Winther, Berens, Bob) | Wir zeigen *Forschungsbereiche + Personen* und coachen Studierende Richtung Gespräch, nicht Themen-Shopping |
| „Zu viele Fehlanfragen" (Menth, Macke, Butz) | Besser gematchte, besser vorbereitete Studierende → weniger kalte Low-Signal-Mails |
| „Wird das in 3 Jahren noch existieren?" (Hennig, Zell) | Ebene 1 braucht keine Professoreneinlage; Abandon kostet Lehrstühle nichts, ihre Webseiten bleiben die Datenquelle |
| „Spam- / Scoop-Risiko" (Carsten, Georg) | Wir aggregieren nur bereits öffentliche Daten; von Lehrstühlen eingegebene Inhalte können auf Uni-Tübingen-Zugang beschränkt werden |

Die Alignment-Story in einem Satz: **Studierende erhalten bessere Discovery, Professoren erhalten weniger, aber bessere Anfragen, der Fachbereich erhält Sichtbarkeit — und niemand wird gezwungen, etwas zu pflegen.**

---

## 5. Erfolgskennzahlen (nach MVP)

- **Studierende:** „Ich habe den richtigen Lehrstuhl beim ersten Versuch kontaktiert" — messbar über die geplante Umfrage (Plan.docx Wochen 29–01.07): Zeit bis zum ersten bedeutsamen Kontakt, Anzahl kontaktierter Lehrstühle vor einem Match.
- **Professoren:** „Die Anfragen, die ich erhalte, sind besser informiert" — qualitativ; mit den 2–3 freundlichen Typ-B-Lehrstühlen abfragen (Wichmann, Huson, Kerstin zeigten Goodwill).
- **Fachbereich:** Mehr erfolgreiche Matches, weniger Irrwege.
- **Explizit keine Kennzahl: Professorenakzeptanz der Plattform.** Das war das alte Narrativ; das Feedback hat es beendet. Lehrstuhl-Opt-in (Ebene 2) ist ein Bonus-Signal, kein Erfolgskriterium.

Der MVP-Maßstab bleibt wie in Plan.docx formuliert: *Nach weniger als einer Stunde mit dem Tool hat ein Studierender eine viel bessere Idee, welchen Lehrstuhl er kontaktieren soll.* Alles oben Genannte dient diesem Satz.
