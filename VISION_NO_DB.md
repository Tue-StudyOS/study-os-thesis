# Vision: Datenbankloser, universeller Thesis-Discovery-Skill

**Branch:** `feat/no-db-universal-skill`  
**Datum:** 2026-06-26  
**Status:** Entwurf — noch nicht implementiert

---

## Das Problem

Die Suche nach einer Masterarbeit ist strukturell kaputt:

- Möglichkeiten sind über Uni-Seiten, Lehrstuhl-Websites, LinkedIn, Firmen-Karriereseiten und Mundpropaganda verteilt.
- Studenten wissen nicht, was sie nicht wissen — sie suchen zu eng, zu spät, oder im falschen Fachbereich.
- Der Kaltstart ist das härteste: Ohne Orientierung weiß man nicht, wo man überhaupt anfängt.
- Das aktuelle Tool löst das nur für Informatik Tübingen — und nur solange die Datenbank aktuell ist.

---

## Die neue Richtung

**Kernprinzip:** Kein statisches Datenbankfundament. Der Skill definiert *wie gesucht wird*, nicht *was gespeichert ist*.

Das Tool führt ein Gespräch, extrahiert das Interessens- und Kompetenzbild des Studenten, und leitet dann systematisch an, welche Suchanfragen gestellt werden — so dass die LLM mit Live-Websearch die relevanten Möglichkeiten findet und strukturiert zurückgibt.

**Was das Tool tut:**

1. **Profil aufbauen** — Interessen, Skills, Erfahrungen, Präferenzen und No-Gos des Studenten per Gesprächs-Interview extrahieren (bestehender `build-student-profile`-Skill bleibt).
2. **Suchstrategie ableiten** — Aus dem Profil werden konkrete Suchanfragen generiert: für Uni-Lehrstühle (alle Fachbereiche Tübingen), für externe Unternehmen.
3. **Live-Discovery** — Die LLM führt die Suchen aus (WebSearch), aggregiert die Ergebnisse und filtert auf Relevanz.
4. **Übersicht erzeugen** — Strukturierter Output: welche Lehrstühle, Personen, Themenfelder, Firmen passen — mit Relevanz-Begründung.
5. **Nächste Schritte** — Konkrete Anlaufstellen, erste Kontakt-Empfehlungen, Hinweis auf Claude Projects für Kontinuität.

**Was das Tool nicht tut:**

- Nicht die komplette Thesis schreiben oder konkrete Proposals generieren.
- Nicht garantieren, dass alle Möglichkeiten gefunden werden.
- Nicht persistent Daten speichern.

---

## Ziel für den Nutzer

> "Ich weiß jetzt, was es gibt und wo ich anfangen soll."

Nicht: "Hier ist deine fertige Thesis." Sondern: "Hier ist dein Landkarte — du siehst die Bereiche, die Personen, die Firmen, die zu dir passen. Von hier aus kannst du gezielt vorgehen."

---

## Warum kein Backend / keine Datenbank

| Datenbank-Ansatz | Datenbankloser Ansatz |
|---|---|
| Veraltet innerhalb von Monaten | Immer aktuell (live web) |
| Nur Informatik Tübingen | Alle Fachbereiche, sofort |
| GitHub Actions für Updates nötig | Kein Wartungsaufwand |
| Nur was gepflegt wird | Alles was öffentlich existiert |
| Skaliert nicht auf Firmen | Firmen-Discovery gleiches Prinzip |

Der Skill ist die Intelligenz. Die Daten kommen von der Welt.

---

## Scope: Wer profitiert

**Primär:** Studenten der Universität Tübingen (alle Fachbereiche), die eine Masterarbeit suchen.

**Sekundär:** Studenten, die eine externe Masterarbeit bei einem Unternehmen schreiben wollen.

**Nicht im Scope:** Bachelorarbeiten, andere Universitäten (kann später erweitert werden).

---

## Kernfrage: Was macht diesen Skill besser als "Claude einfach fragen"?

Der Skill ist kein Chat. Er ist ein **strukturierter Prozess**:

1. **Tiefes Profiling** — Ohne den Skill fragt man Claude vage. Der Skill zwingt zur Präzision durch geführtes Interview.
2. **Systematische Search-Templates** — Der Skill definiert explizit, nach welchen Mustern gesucht wird. Ein normales Gespräch macht das ad hoc und vergisst Bereiche.
3. **Aggregation + Mapping** — Ergebnisse werden nicht nur aufgelistet, sondern zu Interessens-Dimensionen zugeordnet.
4. **Vollständigkeitsdruck** — Der Skill prüft aktiv, ob ganze Fachbereiche oder Firmentypen übersehen wurden.
5. **Handlungsanleitung** — Output ist nicht "hier ist Wissen" sondern "hier sind deine nächsten drei Schritte".

---

## Die Suchanfragen — Herzstück des Skills

Der Skill muss **Search-Templates** definieren, die systematisch alle relevanten Bereiche abdecken:

### Uni-Lehrstühle (Tübingen, alle Fachbereiche)

```
site:uni-tuebingen.de "{Themenfeld}" Masterarbeit
site:uni-tuebingen.de "{Themenfeld}" Lehrstuhl
"Universität Tübingen" "{Themenfeld}" Masterarbeit Betreuung
"Universität Tübingen" Fachbereich "{relevanter Fachbereich}" Forschung "{Themenfeld}"
```

Ergänzend: Direkt-Crawl der Fachbereichsseiten (`uni-tuebingen.de/de/forschung/...`) für strukturierten Überblick.

### Externe Unternehmen

```
Masterarbeit "{Themenfeld}" Unternehmen "{Region/Remote}"
Masterarbeit extern "{Branche}" "{Methode/Technologie}"
"{Branche}" "Thesis" OR "Abschlussarbeit" "{Themenfeld}"
LinkedIn/StepStone: Masterarbeit "{Themenfeld}" Unternehmen
```

### Qualitäts-Filter

- Bevorzuge offizielle Uni-Seiten, Lehrstuhl-Homepages, aktuelle Publikationsseiten.
- Markiere Ergebnisse mit Datum (Aktualität).
- Trenne Forschungsgebiete von konkreten offenen Stellen.

---

## Phasenplan (Vorschlag, noch zu diskutieren)

**Phase 1 — Uni-weit (ohne Firmen)**
- Skill für alle Fachbereiche Tübingen, datenbanklos.
- Basiert auf Search-Templates + WebSearch.
- Testen: funktioniert die Suche wirklich, findet sie alle relevanten Lehrstühle?

**Phase 2 — Firmen-Discovery hinzufügen**
- Suchstrategie für externe Masterarbeiten definieren.
- LinkedIn, Karriereseiten, Jobbörsen in die Templates aufnehmen.
- Evaluation: Qualität der Firmenvorschläge.

**Phase 3 — Verteilung**
- Fachschaft Informatik als erster Kanal.
- Hennig-GitHub.
- Langfristig: Ersti-Heft, Uni-Seite.

---

## Offene Fragen (für /grillme)

1. Wie gut funktioniert WebSearch wirklich für diese Suchanfragen? Reicht das Coverage?
2. Was ist unser Fallback wenn ein Lehrstuhl keine Webpräsenz hat?
3. Wie verhindern wir, dass nur die SEO-starken Lehrstühle gefunden werden?
4. Ist Firmen-Discovery oder Uni-Erweiterung zuerst sinnvoller?
5. Wie evaluieren wir "gut genug"? Was ist der Mindestscore?
6. Wie halten wir die Search-Templates aktuell wenn sich Uni-Strukturen ändern?
