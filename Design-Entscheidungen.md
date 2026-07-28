# Design-Entscheidungen — Thesis-Finder

> Dieses Dokument erklärt **warum** der Thesis-Finder so gebaut ist, wie er gebaut ist.
> Es ist so geschrieben, dass es auch jemand versteht, der noch nie mit dem Projekt
> gearbeitet hat. Roter Faden von oben nach unten: erst das Ziel, dann das Grundprinzip,
> dann der Ablauf Schritt für Schritt mit den jeweiligen Entscheidungen, dann die
> kritischen Punkte, und ganz unten eine TODO-Liste.

---

## 0. Worum geht es? (Das Ziel in zwei Sätzen)

Ein Studierender der Uni Tübingen — egal aus welchem Fachbereich — soll einen passenden
Platz für die **Masterarbeit** finden. Zwei Wege sind möglich: eine Arbeit an einem
**Uni-Lehrstuhl** oder eine Arbeit in einer **Firma in Baden-Württemberg (BW)**.

Das Werkzeug ist kein klassisches Such-Backend, sondern eine Sammlung von **Skills**
(strukturierte Anleitungen für ein LLM). Fünf Skills greifen ineinander:

| Skill | Aufgabe |
|---|---|
| `thesis-finder` | **Single Entry Point** — erkennt ob es einen neuen oder rückkehrenden Nutzer gibt, baut das Profil inline auf, routet zu den Discovery-Skills |
| `build-student-profile` | Interviewt den Studierenden und legt ein Profil an (standalone nutzbar) |
| `find-university-chairs` | Findet passende Lehrstühle an der Uni Tübingen |
| `find-company-thesis-options` | Findet passende Firmen in BW |
| `draft-thesis-contact` | Entwirft eine Erst-Kontakt-Mail für eine gefundene Option |

Der rote Faden über alle Skills: **erst verstehen, wen wir vor uns haben (Profil),
dann gezielt im Web suchen — aber abgesichert, ehrlich und ohne Halluzination.**

---

## 1. Das Grundprinzip: Keine Datenbank, Live-Websuche + „Backbone"

### Entscheidung
Es gibt **kein laufendes Backend, keine Datenbank, keine gespeicherten Stellen**. Die
einzige Laufzeit-Quelle ist das **Live-Web**. Der einzige statische Bestandteil ist ein
sogenanntes **Backbone** — eine kleine, von Hand gepflegte Markdown-Liste (bei Firmen
~107 Einträge; bei der Uni die offizielle Fakultätsstruktur).

### Warum
- **Portabilität:** Ein Skill ohne Backend läuft überall, muss nicht betrieben, gehostet
  oder gewartet werden. Keine Server, keine Ausfälle, keine Kosten.
- **Aktualität:** Stellen und Forschungsthemen ändern sich ständig. Eine Datenbank wäre
  sofort veraltet. Das Live-Web ist immer aktuell.
- **Das Backbone löst das „Kaltstart-Problem":** Würde man einfach „Masterarbeit KI BW"
  googeln, kämen vor allem **SEO-optimierte Jobbörsen** (StepStone, Indeed) — also Rauschen
  statt relevanter Akteure. Das Backbone gibt der Suche stattdessen eine **kuratierte
  Startmenge bekannter, relevanter Firmen/Lehrstühle**, von der aus angereichert wird.
  Es wirkt also als **Anti-SEO-Bias-Anker**.

### Was crucial ist
Das Backbone darf **klein und kuratiert** bleiben (Relevanz schlägt Vollständigkeit).
Sobald man versucht, „alle Firmen in BW" abzubilden, verliert man genau den Vorteil
(Wartbarkeit + Anti-SEO-Bias). Diese Spannung — Relevanz vs. Abdeckung — zieht sich durch
das ganze Projekt (siehe §10).

---

## 2. Der Ablauf im Überblick

`thesis-finder` ist der Orchestrator. Er entscheidet zuerst ob der Nutzer neu ist oder
wiederkommt (§9), baut dann ggf. das Profil auf und routet danach zu den Discovery-Skills:

```
   thesis-finder (Einstiegspunkt)
        │
        ├─ Neuer Nutzer → Profil aufbauen (build-student-profile inline)
        │                  → Uni / Firma / Beides?
        │
        └─ Rückkehrender Nutzer → Session-Log lesen → Kurzupdate → neu suchen
                                  (§9 Session-Persistenz)

   PROFIL              PASS 1 (offline)          PASS 2 (live)            OUTPUT
┌───────────┐      ┌──────────────────┐     ┌──────────────────┐    ┌──────────────┐
│ 6 Dimen-  │ ──▶  │ Backbone filtern  │ ──▶ │ Web-Anreicherung │──▶ │ Options-Map  │
│ sionen    │      │ (kein Web)        │     │ pro Kandidat     │    │ + Caveat     │
└───────────┘      └──────────────────┘      └──────────────────┘    └──────────────┘
```

Der Trick ist die **Zwei-Pass-Struktur**: Erst billig und offline die Kandidaten
eingrenzen (Pass 1), dann nur für die wenigen verbleibenden Kandidaten teuer im Web
recherchieren (Pass 2). Das hält die Suche fokussiert und vermeidet Rauschen.

---

## 3. Zuerst das Profil — die 6 Dimensionen

### Entscheidung
Bevor **irgendeine** Suche startet, muss ein vollständiges Profil mit sechs Dimensionen
vorliegen:

1. **Interessen** — Kernthemen
2. **Methoden** — wie man arbeiten will (empirisch, Labor, Engineering, …)
3. **Domäne** — Anwendungsfeld (Medizin, Automotive, Bildung, …)
4. **Thesis-Stil** — gewünschte Art des Ergebnisses (angewandt, theoretisch, …)
5. **Skills** — konkrete Werkzeuge (Python, PyTorch, fMRT, CAD, …)
6. **No-Gos** — harte Ausschlüsse (keine Hardware, kein Klinikkontakt, …)

Ist eine Dimension leer oder nur ein Einzeiler („Ich mag KI"), **stoppt der Such-Skill**
und ruft zuerst `build-student-profile` auf.

### Warum
Eine Suche ist nur so gut wie ihr Input. Ohne Methoden, Domäne und No-Gos liefert jede
Suche generische Treffer („diese Firma macht auch KI"). Die **No-Gos sind besonders
wertvoll**, weil sie früh ganze Kandidatengruppen ausschließen und so Pass 2 sparen.

### Was crucial ist
Die Qualität des ganzen Outputs hängt am Profil. Deshalb wird hier bewusst eine **harte
Schranke** gesetzt statt „best effort" auf dünner Basis.

---

## 4. Die Konversation — eine Frage pro Schritt

### Entscheidung
Das Profil-Interview stellt **eine Frage pro Antwort** (maximal zwei, wenn sie eng
zusammenhängen). Niemals ein ganzer Fragebogen auf einmal.

### Warum
- Ein Fragebogen-Block **überfordert** und wird oberflächlich beantwortet.
- Eine Frage nach der anderen hält das Gespräch **fokussiert und nicht-divergent** — der
  Berater kann auf jede Antwort eingehen und gezielt nachhaken („das trennt Robotik-Lernen
  von reiner Wahrnehmung").
- Es fühlt sich an wie ein echter Studienberater, nicht wie eine Suchmaschine.

---

## 5. Pass 1 — Das Backbone filtern (ohne Web)

### Entscheidung
Pass 1 liest **nur die Backbone-Datei** und filtert sie anhand der Profil-Tags. Kein
einziger Web-Aufruf. Ziel: eine Kandidatenliste von **5–20 Einträgen**.

- Bei **Firmen**: die Markdown-Liste der ~107 BW-Firmen wird nach Sektor-Tags gefiltert,
  die zu Interessen/Domäne passen. No-Gos werden hier schon angewendet.
- Bei der **Uni**: statt einer Firmenliste dient die **offizielle Fakultätsstruktur** als
  Backbone. Eine Routing-Tabelle wählt 1–3 relevante Fakultäten, deren offizielle
  Lehrstuhl-Listen dann die Kandidaten liefern. (Wichtig: für KI/ML reicht die Informatik-
  Seite nicht — MPI-IS, ELLIS und Cyber Valley müssen mitgecrawlt werden.)

### Warum
- **Kosten und Fokus:** Erst grob offline eingrenzen ist billig und vermeidet, dass man
  20+ irrelevante Firmen teuer im Web recherchiert.
- **Anti-SEO-Bias:** Die Kandidaten stammen aus einer bekannten, relevanten Menge — nicht
  aus dem, was eine Suchmaschine gerade nach oben spült.

### Was crucial ist
- **Zielgröße 5–20:** >20 → Tags enger schneiden; <5 → einen Sekundär-Tag dazunehmen.
- **No-Gos nicht stillschweigend droppen:** Mehrdeutige Fälle (z. B. „Robotik" bei No-Go
  „keine Hardware") werden **markiert und behalten**, nicht gelöscht — die Entscheidung
  fällt erst in Pass 2, wenn mehr Information da ist.

---

## 6. Pass 2 — Live-Anreicherung pro Kandidat

### Entscheidung
Für jeden Kandidaten aus Pass 1 läuft eine feste Reihe von Web-Teilschritten:

| Teilschritt | Frage |
|---|---|
| 2a — Fokus | Bestätigt die eigene Seite, dass sie am Thema arbeiten? |
| 2b — Thesis-Signal | Gibt es eine Stelle / ein Programm / kein öffentliches Signal? |
| 2c — Kontaktweg | Karriereportal-URL oder „direkt R&D anfragen" (nie Namen raten) |
| 2d — Aktualität | Beleg von 2022 oder neuer? Älteres wird als „stale" markiert |
| 2e — Existenz + Personen-Verifikation | Lebt die Firma/Lehrstuhl noch? Jede genannte Person wird auf der eigenen Seite bestätigt |

### Warum
- **Eigene Domain vor Jobbörsen:** Ein Thesis-Signal zählt nur von der **firmeneigenen
  Seite** — niemals von StepStone/Indeed/Glassdoor. Diese erzeugen Rauschen und SEO-Bias.
- **Spezifität schlägt Allgemeinheit:** Eine Seite, die das konkrete Thema des Studierenden
  nennt, schlägt eine generische „Wir nutzen KI"-Seite.
- **Drei klare Thesis-Signal-Zustände** statt Bauchgefühl: `explicit opening` /
  `active program` / `unclear`. Das Feld bleibt **nie leer** und es wird **nie eine Stelle
  erfunden**.
- **Personen-Verifikation (2e)** wurde nach dem Task-I-Live-Test nachgerüstet: Das Modell
  hatte Prof. Karnath fälschlicherweise für einen Lehrstuhl attributiert, der tatsächlich
  Hans-Christoph Nürk gehört. Seither gilt: ein Name wird nur genannt, wenn er auf der
  offiziellen Seite der Einheit steht.

### Was crucial ist
`thesis signal: unclear` ist **ein gültiges Ergebnis, kein Fehler**. ~80 % der Firmen
schreiben Masterarbeiten gar nicht öffentlich aus. Genau deshalb haben wir uns **gegen
das Scrapen konkreter Stellen** entschieden (siehe §7).

---

## 7. Kernentscheidung: Konkrete Stellen scrapen — oder nicht?

> Dies war die zentrale Diskussion (2026-06-30). Ausführlich, weil sie das Design prägt.

### Die Frage
Soll der Skill konkrete Stellenausschreibungen für Masterarbeiten aus den Firmenseiten
auslesen und auflisten — oder nur passende **Firmen** ausgeben?

### Die Entscheidung
**Nicht** systematisch alle Stellen scrapen. Stattdessen: Firmen-Discovery + Thesis-Signal-
Check + **klare Outreach-Anleitung**.

### Warum
1. **Fragilität:** Stellen-Scraping bricht, sobald sich das HTML einer Seite ändert. Hoher
   Wartungsaufwand, geringe Verlässlichkeit.
2. **Geringe Ausbeute:** ~80 % der Firmen publizieren Masterarbeits-Stellen ohnehin nicht.
   Das Ergebnis wäre meist `unclear` — viel Scraping-Aufwand für wenig Mehrwert.
3. **SEO-Bias:** Wer auf Stellen-Listen optimiert, landet wieder bei den Jobbörsen, die wir
   bewusst meiden.

**Kernsatz: Eine klare Anleitung, *wie* man eine Firma anschreibt, ist mehr wert als noch
mehr gescrapte Daten.**

### Die Lösung im Detail

**(a) Doppelte URL-Verifikation** — jede Kontakt-/Portal-/Team-URL wird **zweimal** geprüft:
1. beim ersten Fund (Pass 2, Teilschritt 2e)
2. unmittelbar vor dem finalen Output (Schritt 5)

Eine URL, die in Pass 2 erreichbar war, in Schritt 5 aber nicht mehr, wird mit
`⚠ contact URL not confirmed — verify before use` markiert und ans Ende sortiert — aber
nicht entfernt (der Studierende kann es trotzdem versuchen). Eine URL, die **nie**
erreichbar war, kommt gar nicht in den Output.

**(b) Größenabhängige Outreach-Strategie** bei `unclear`:

| Firmengröße | Empfohlenes Vorgehen | Warum |
|---|---|---|
| **Konzerne** (Bosch, SAP, ZF, Zeiss …) | Karriereportal nutzen, nach 2 Wochen nachhaken | Große Orgs haben langsame, formale HR-Prozesse |
| **KMU / Startups** | **Direkt das R&D-Team anschreiben** | Schneller, keine HR-Warteschlange; Seiten oft nicht gepflegt |

Wichtig: Bei kleinen Firmen heißt „keine Stelle gelistet" **nicht** „nicht anschreiben" —
deren Seiten sind oft einfach nicht aktuell.

---

## 8. Output — gruppiert nach Interesse, mit ehrlichem Caveat

### Entscheidung
Das Ergebnis ist eine **Options-Map, gruppiert nach den Interessen des Studierenden**
(z. B. „LLMs / Enterprise NLP", „Computer Vision in der Medizin") — **nicht** nach Sektor
oder Firmengröße. Jeder Eintrag hat Pflichtfelder (Firma, Team, Tags, Größe, Ort, Relevanz-
Begründung, Pro/Contra, Kontaktweg) und optionale Live-Felder (Forschungsfokus, Thesis-
Signal, bestätigter Kontakt).

### Warum
- **Nach Interesse gruppieren** spiegelt die Denkweise des Studierenden wider, nicht die
  interne Org-Logik der Firmen. Das macht die Map sofort nutzbar.
- **Pro & Schwierigkeiten ehrlich nennen** (Startup-Chaos vs. Konzern-Bürokratie,
  IP-/Geheimhaltung, Arbeitssprache) — das Tool berät, es verkauft nicht.

### Der Coverage-Caveat (Pflicht, steht oben in der Map)
Ein fest formulierter Hinweis macht **drei Dinge ehrlich**:
1. Die meisten Firmen schreiben Masterarbeiten **nicht** öffentlich aus → `unclear` heißt
   nicht „keine Chance".
2. Konkrete Outreach-Anleitung je nach Firmengröße (siehe §7).
3. **Das Backbone ist bewusst unvollständig** — neue Startups, Nischenfirmen und Quereinstiege
   fehlen evtl.

---

## 9. Session-Persistenz — Suche über mehrere Wochen

### Das Problem
Die Suche nach einer Masterarbeit ist ein **mehrstufiger Prozess über Wochen**. Ohne
Persistenz muss der Studierende beim nächsten Aufruf komplett von vorne beginnen —
das Profil wird neu abgefragt, bereits geprüfte Optionen werden nochmals ausgegeben,
Dead-Ends werden nochmals gesucht.

### Die Entscheidung
`thesis-finder` pflegt eine **Session-Log-Datei** unter `~/.claude/thesis-finder/session.md`.
Beim ersten Aufruf wird sie angelegt, bei jedem weiteren Aufruf gelesen und fortgeschrieben.

### Warum diese Ablage
- `references/` ist für **statische, gebündelte Daten** — sie werden in jedem Release mit
  ausgeliefert. Ein mutierbares Suchprotokoll gehört nicht dort rein.
- `~/.claude/` ist der natürliche Ort für Claude-eigene Laufzeit-Daten (Skills, Memory,
  Settings). Ein Unterordner `thesis-finder/` hält die Session-Daten **nutzer-scoped, nicht
  projekt-scoped** — die Suche läuft über Wochen und über verschiedene Arbeitsverzeichnisse.
- Das `SKILL.md` enthält nur die **Pfadkonvention** (statisch, wird ausgeliefert). Die
  eigentliche Datei ist Nutzer-eigener Laufzeitzustand und wird **nie gebündelt**.

### Ablauf bei rückkehrendem Nutzer

```
~/.claude/thesis-finder/session.md gefunden?
        │
        └── JA → Session lesen → Einzeiler-Zusammenfassung anzeigen
                  → "In 1–2 Sätzen: aktueller Stand?" (KEIN neues Interview)
                  → Situation einschätzen:
                       Gute Kandidaten vorhanden? → draft-thesis-contact empfehlen
                       Profil zu eng, alles Dead-Ends? → 1–2 gezielte Fragen → Profil erweitern
                       Neue Richtung gewünscht? → notieren, Profil updaten
                  → Discovery starten (Dead-Ends aus Session-Log ausschließen)
                  → Session-Log aktualisieren
```

**Warum nur 1–2 Sätze:** Ein komplettes Re-Interview würde das Profil verfälschen und
die Suche in die falsche Richtung lenken. Der Skill braucht nur ein kurzes Delta zum
gespeicherten Stand — nicht den vollständigen Kontext neu aufgebaut.

### Session-Log-Format (Kurzform)

```markdown
## Student Profile (updated: YYYY-MM-DD)
[kompaktes 6D-Profil]

## Active Candidates
| Name | Institution / Firma | Track | Status | Zuletzt aktualisiert |

## Dead-Ends (bei künftigen Suchen überspringen)
- [Name]: [Grund — warum kein Fit]

## Search Log
### Session N — YYYY-MM-DD — [university | company | both]
Searched: ... / New candidates: ... / Dead-ends: ... / Notes: ...
```

---

## 10. Was crucial ist und bekannte Risiken

Diese Punkte sind die **bekannten Schwachstellen** — wichtig für eine ehrliche Bewertung:

1. **Backbone-Abdeckung über Fachbereiche (größtes offenes Risiko).**
   Das Firmen-Backbone deckt KI/ML, Robotik, Medtech und Fertigung gut ab. Schwächer sind
   z. B. **Psychologie** (Human Factors, UX), **Bildung/EdTech**, **Umweltwissenschaften**,
   kleinere **Life-Science-Spinouts**. Da das Tool für **alle** Tübinger Fachbereiche
   funktionieren soll, ist das eine echte Lücke. Entscheidung: Lücke **ehrlich im Caveat
   benennen** statt sie durch exhaustives Scrapen zu „schließen" (das würde Wartbarkeit und
   Anti-SEO-Bias opfern). Für die Uni hat der 2e-Fix (MPI-IS/ELLIS als explizite Pass-1-Quelle)
   die schlimmsten Lücken bei CS und Psych behoben; generelle Lücken bleiben.

2. **Zirkuläre Evaluation (Firmen, offen).**
   Die Uni-Eval wurde durch Task I live validiert (+65 pp über Baseline, alle 4 Fakultäten ≥70 %
   live recall nach dem I-Fix). Die **Firmen-Eval** hingegen ist noch zirkulär: Ground Truth und
   Skill filtern aus **demselben** BW-Backbone. Das misst nur „findet der Skill, was im Backbone
   steht", nicht „deckt das Backbone die Realität ab". Eine unabhängige externe Validation durch
   eine andere Person/Gruppe steht noch aus.

3. **Veraltende URLs.**
   Firmenseiten ändern sich. Abgefangen durch die doppelte Verifikation (§7a), aber nie
   ganz auszuschließen — daher die Markierung statt stiller Löschung.

4. **Keine erfundenen Kontakte.**
   Firmen-Org-Infos sind schlechter strukturiert als Uni-Fakultätsseiten. Regel: **Ein Name
   wird nur genannt, wenn er auf der firmeneigenen Seite steht** — niemals aus LinkedIn oder
   Konferenzlisten abgeleitet. Verstärkt nach dem Task-I-Fehlattributierungs-Vorfall (§6).

5. **Live-Mehrwert bei Firmen gemessen — aber zirkulär.**
   Phase-2-Eval: +26 pp über Baseline (100 % Recall alle 3 Profile vs. 74 % Baseline-Mittelwert).
   Caveat: Ground Truth stammt aus demselben Backbone wie der Skill. Ob der Skill bei einer
   „fremd" zusammengestellten Firma-Liste genauso gut abschneidet, ist noch unbekannt.

---

## 11. TODO-Liste

Kompakt, mit Impact (Hoch/Mittel/Niedrig) und ob es nötig ist.
**Impact** = Effekt auf Ergebnisqualität/Vertrauen. **Nötig** = blockiert es einen sauberen Stand?

| # | TODO | Impact | Nötig? | Kurznotiz |
|---|---|---|---|---|
| 1 | **Unabhängige Validation durch externe Person/Gruppe** — jemanden außerhalb des Projekts (z. B. Fachschaft, Kommiliton:in) das Tool mit einem echten Profil testen lassen und Recall manuell prüfen. | Hoch | Ja | Behebt die Zirkularität bei Firmen (§10.2). Branch ist package-ready, der Schritt fehlt noch. |
| 2 | **Distribution anstoßen** — Fachschaft Informatik, Hennig-GitHub, Ersti-Heft ansprechen; ggf. auf Uni-Seiten „Masterarbeit finden" verlinken. | Hoch | Ja | Package ist fertig; die Übergabe ist der einzige noch offene Schritt (Phase 3, außerhalb Branch). |
| 3 | **Backbone-Lücken für Nicht-MINT-Fächer schließen** — gezielt je ein paar Firmen für Psychologie, EdTech, Umwelt, Life Science ergänzen. | Mittel | Optional | Direkt am „für alle Fachbereiche"-Anspruch (§10.1). Klein halten, kuratiert. |
| 4 | **PhD-/Direkt-Anschreiben im Output erklären** — zuerst auf Prof-Seite den Bewerbungsweg prüfen; freundlich, konkret; zweimal nachfragen ist okay. | Mittel | Optional | Macht den Uni-Pfad handlungsfähiger; bisher nur in der Strategie implizit. |
| 5 | **„Last-verified"-Datum + jährlicher Refresh-Prozess** fürs Backbone festschreiben. | Mittel | Optional | Firmen restrukturieren, Startups verschwinden; ohne Datum altert die Liste unbemerkt. |
| 6 | **Outreach-/Kontakt-Templates** (Konzern vs. Startup) als fertige Bausteine in den Output legen. | Niedrig | Optional | Senkt die Hürde für den Studierenden; Strategie ist schon definiert (§7b). `draft-thesis-contact` deckt das teilweise ab. |
| 7 | **Crowdsourced „Gap-Fill"** — Formular, über das fehlende Firmen gemeldet werden. | Niedrig | Nein | Explizit out of scope; erst sinnvoll, wenn das Tool breiter genutzt wird. |
