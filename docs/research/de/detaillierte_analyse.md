# Detaillierte Analyse & Entscheidungsprotokoll

**StudyOS Thesis Advisor — Forschungspaket, Bericht 5 von 5**
**Datum:** 11.06.2026 · **Zielgruppe:** Interne Team-Aufzeichnung
**Quellen:** 27 Professorenrückmeldungen (Mai 2026), StudyOS-Bot-Externer-Review, Live-Repo-Stand (5 offene PRs / 16 offene Issues, verifiziert 11.06.2026), Plan.docx

---

## 1. Detailanalyse Professoren-Feedback

### 1.1 Methodologische Anmerkung

Der Outreach erfolgte in zwei Varianten: Lehrstühle, die bereits öffentlich listen („wie läuft die Pflege?"), und Lehrstühle, die es nicht tun („warum nicht — einschließlich ‚wir wollen das nicht'"). Die zweite Formulierung hat ungewöhnlich offene Antworten erzeugt; mehrere Professoren bedankten sich dafür, dass sie direkt sein durften. Eine Antwort (Carsten, Spam-/Scoop-Risiko) wurde in unseren Unterlagen abgeschnitten — die Position ist aus dem Einstieg klar. Einige Antworten befinden sich noch im Draft-Status auf unserer Seite (in der Quelldatei als „Draft geschrieben" markiert) — diese sollten wir noch beantworten.

### 1.2 Typ A — Kapazitätsbedingte Ablehnung (Butz, Menth, Mähl)

Diese Lehrstühle sind in die entgegengesetzte Richtung nachfragebeschränkt als eine Listing-Plattform annimmt. Butz: „we have no problems getting students these days." Menth ist der Extremfall: 20 betreute Abschlussarbeiten gegen 50+ Anfragen, Themen entstehen „fast nur auf Anfrage" — und trotzdem kein Schritt voraus.

**Interpretation:** Öffentliche Sichtbarkeit ist für diese Lehrstühle streng negativ. Aber Menths Schlussabsatz ist der strategisch interessanteste Satz des gesamten Datensatzes: *„Ich wäre sehr froh, wenn es ein System gäbe, mit dem Studierende leichter an Abschlussarbeiten kommen können. Dann werde ich vielleicht auch nicht so überhäuft mit Anfragen."* Er lehnt den Mechanismus (Listing) ab, befürwortet aber das Ergebnis (Studierende zum richtigen Ort geleitet). Ein Discovery-Tool, das Studierende *weg* von überlasteten Lehrstühlen zu solchen mit Kapazität leitet, dient Typ A, ohne etwas von ihnen zu verlangen.

**Spannung:** Menth sagt „Es gibt schlicht keine Themen, die ich öffentlich stellen könnte", aber er generiert Themen auf Anfrage. Die Themen existieren — als latente Kapazität, die durch den *richtigen* Studierenden freigesetzt wird. Das ist dieselbe Ko-Kreations-Dynamik, die Typ C beschreibt — hier aus Erschöpfung, nicht aus Prinzip heraus entstanden.

### 1.3 Typ B — Bereit, wenn trivial (Hennig, Zell, Kerstin, Georg, Huson, Wichmann, Bob/Rabanus, Anna)

Der aktuelle Stand der Technik bei kooperativen Lehrstühlen ist aufschlussreich:

- **Hennig:** einmal pro Semester ein „Workshop", bei dem PhD-Studierende je eine Folie zu einem gemeinsamen Overleaf-Beamer-Deck hinzufügen (8–15 Themen/Semester). Das Frischhaltungs-Mechanismus ist elegant: PhD-Studierende sind als Ansprechpartner eingetragen, veraltete Einträge erzeugen E-Mails an sie, „and that usually ensures they take the project down swiftly."
- **Zell:** schätzt, dass **>50 % der betreuten Abschlussarbeiten nie auf der Liste auftauchen** — sie entstehen aus PhD-/Studierenden-Gesprächen. „I always have to run behind my Ph.D. students … now I only monitor it infrequently."
- **Kerstin:** internes Google-Doc, auf Anfrage an Interessenten versandt, „hard to keep up-to-date."
- **Georg:** interne Overleaf-Liste, „constantly moving and outdated", mit echter Einschränkung: Themen sind Papierideen, also muss die Sichtbarkeit auf Uni-Tübingen-Studierende beschränkt werden.
- **Huson:** Der Aufwand liegt nicht in der Webseiten-Bearbeitung — „the hard part is coming up with viable topics." Updates passieren „ad hoc when too many students contact me asking about topics that are no longer relevant."

Selbst die *kooperativsten* Lehrstühle beschreiben Systeme, die chronisch veraltet sind — und die Veraltung ist nicht werkzeug-bedingt.

**Hennigs drei Bedingungen** verdienen eine wortgetreue Aufzeichnung, da sie effektiv unsere Akzeptanzkriterien für jede Ebene-2-Arbeit darstellen:
1. *Anreize:* „There absolutely must be a good incentive for the research groups to list theses there … This is something you likely won't get right as student developers, because it doesn't have much to do with the interface or the frontend."
2. *Reibungslosigkeit:* „Updating the list must be easy, quick, and transparent."
3. *Stabilität:* „The website must be stable for at least a few years (i.e., also after you are long gone)" — mit Verweis auf courses.cs.uni-tuebingen.de als mahnendes Beispiel.

Er hat uns auch eine User-Research-Roadmap gegeben: Luxburg, Grust, Martius interviewen. Luxburg hat selbständig ein Kaffee-Gespräch nach ihrer SML-Vorlesung angeboten (Di/Do 8:15–9:45, MvL1). Diese Einladungen haben ein Verfallsdatum; wir sollten sie in den nächsten 2–3 Wochen nutzen.

### 1.4 Typ C — Prinzipielle Ablehnung (Macke, Luxburg, Berens, Winther, Stephan, Niels, Bob teils)

Die Einwände dieser Gruppe sind *erfahrungsbasiert*, nicht hypothetisch:

- **Winther hat das Experiment gemacht, und es scheiterte in beide Richtungen:** „The topics that we wanted to work on urgently no student applied for. Students had the impression that the four or five topics we had published were the only thing we worked on and then did not talk to us." Eine statische Liste scheiterte darin, dringende Themen zu besetzen *und* unterdrückte organischen Kontakt. Das ist das stärkste Einzelargument gegen das Katalog-Modell.
- **Luxburg hat Abteilungsgeschichte:** „an up-to-date platform doesn't work, profs never update the topics. We've had many attempts in the department already."
- **Mackes Antwort ist die reichhaltigste im Datensatz.** Drei strukturelle Punkte: (a) Pflege „is really intellectual work that a tool only helps slightly with"; (b) Themen „emerge pretty spontaneously and fluidly … not 'planned ahead of time'" und Betreuung ist im Labor verteilt; (c) das Systems-Müdigkeitsargument, mit dem denkwürdigen Schluss, er würde lieber ein System *entfernen* als eines hinzufügen. Sein konstruktiver Gegenvorschlag: „If you have a system that reads the relevant section in our website and posts topics … that would be something I am much more excited about."
- **Bob** reformuliert das Datenmodell: aggregiert „not 'projects,' or even 'thesis topics,' but the set of problems the prof and their team are interested in" — mit der Ergänzung, solche Aussagen „would not need revision very often." Er hat auch Disclaimer-Text formuliert, den wir nahezu wörtlich auf Lehrstuhl-Seiten übernehmen sollten: Themen sind „starting points only; an essential part of doing a thesis is the formulation and refinement of the problem itself."
- **Stephan** ergänzt das Pädagogik-Argument klar: Er mag es nicht, wenn Abschlussarbeiten „fixed packages you can browse and choose" sind.
- **Niels** nennt die Netzwerkeffekt-Falle: „I do not think we would use it unless it is adopted by the whole department" — ein Henne-Ei-Problem, das kein Studierenden-Team erzwingen kann.

### 1.5 Typ D — Nischenpipelines (Peter, Mario, Häufle teils)

Peters Studierende kommen via GTC; Mario hat breite Dauerinteressen einmal gepostet, die weiterhin gültig sind. Häufle: „for us, it works well at the moment." Diese Lehrstühle sind nicht resistant — das Problem existiert für sie schlicht nicht. Die richtige Produkt-Antwort: über gescrapte öffentliche Daten einschließen, ansonsten in Ruhe lassen.

### 1.6 Übergreifende Spannungen

1. **Geäußerte vs. offenbarte Präferenzen.** Mehrere „bereite" Lehrstühle (Zell, Huson) beschreiben Verhalten — seltene Überwachung, Ad-hoc-Updates ausgelöst durch Beschwerden — das vorhersagt, dass sie *unser* System ebenfalls unter-pflegen würden. Wichmanns „I'd be willing to at least give it a try" ist aufrichtig, aber dieselbe Haltung, die dem 2022er Scheitern vorausging.
2. **Die Studierenden-Perspektive ist anerkannt, aber nicht repräsentiert.** Macke und Menth merken beide explizit an, dass sie von der Betreuer-Seite argumentieren. Unser Datensatz hat 27 Professoren und 0 Studierende. Die geplante Umfrage (Wochen 29–01.07) ist derzeit unser einziger studentenseitiger Evidenzkanal — es lohnt sich, einige leichte Studierenden-Interviews früher einzuplanen.
3. **Ostermanns Ein-Zeiler ist ein Datenpunkt, keine Abweisung.** „Your assumption is wrong: https://ps.cs.uni-tuebingen.de/teaching/thesis/" zeigt: (a) unsere Lehrstuhl-Coverage-Recherche hatte mindestens einen Fehler — den Rest unserer Annahmen über wer was listet nochmals prüfen; (b) maschinenlesbare Thesis-Infos existieren bereits in Inseln, und Scraping ist der respektvolle Integrationspfad.

---

## 2. Zeitplan-Realitätscheck

**Wochen 8–14 (Auto-Discovery).** PR #37 existiert bereits — materiell besser als der Plan, der implizit „jetzt anfangen" bedeutet. Das Risiko ist Breite: 27+ Lehrstühle mit Typo3, Custom-Seiten, PDF-Listen und Google Docs. Realistisches Woche-14-Exitkriterium: Agent verarbeitet zuverlässig die **häufigsten Seitenstrukturen für ~20 Lehrstühle**, mit manuellen Seed-Daten für den Rest. Schema-PR #35 muss zuerst gemergt werden; er ist der Rebase-Anker für alles Nachgelagerte.

**Wochen 15–21 (RAG).** „RAG optimieren" (#7) ist ohne Begrenzung als Aufgabe offen. Begrenzen: Wochen 15–16 deepeval (#6) aufsetzen und Baseline-Retrieval-/Antwort-Metriken erfassen; Wochen 17–19 iterieren (Chunking, Embeddings, Reranking, Paper-Tags #32) plus Skill-Berechnung (#21, schließt #16) und DeepSeek-Dedup (#33); Wochen 20–21 gegen Baseline retesten. Ohne Eval-Harness zuerst ist „verbessertes RAG" eine nicht falsifizierbare Behauptung — genau das, wovor CLAUDE.md §4 warnt.

**Wochen 22–28 (Deployment).** Der versteckte Scope hier ist die Security- und Trust-Arbeit (§5 unten), die derzeit in keinem Issue erfasst ist. Issues jetzt anlegen, damit die Arbeit sichtbar und schätzbar ist. Staging-Deployment sollte spätestens in Woche 25 starten, um zwei Wochen echter Einsatz zu ermöglichen.

**Wochen 29–01.07 (Umfrage).** Plan.docx kennzeichnet das als „if wanted". Als Puffer-Ablassventil behandeln: Wenn Wochen 8–21 sich verzögern, absorbiert diese Phase das Deployment-Überrollen, und die Umfrage schrumpft zu einem minimalen Google-Form. Wo ist der Puffer im Zeitplan insgesamt? Fast ausschließlich in (a) RAG-Scope und (b) dieser Abschlussphase. In Wochen 8–14 gibt es praktisch **keinen Puffer** — daher ist #35/#37 das Gate.

---

## 3. Technische Entscheidungen (Protokoll)

| Entscheidung | Status | Begründung |
|---|---|---|
| Bei Ollama/Local-LLM als Standard bleiben | **Bestätigt** | Privacy-Geschichte passt zu Professoren-Sensibilitäten (Georgs Scoop-Risiko, Carstens Spam-Sorge); entspricht Local-First TOR-Import-Richtlinie |
| Celery/Redis behalten | **Bestätigt** | Funktioniert; Scrape-Jobs aus #37 passen in bestehende Queue |
| PostgreSQL + pgvector behalten | **Bestätigt** | Ausgereift, keine Änderungen nötig |
| WebSocket-Auth: JWT im URL → kurzlebiges Ticket oder Secure Cookie | **Muss vor Hosting geändert werden** | Tokens in URLs landen in Logs/Proxies/History. Geschätzt 3–5 Tage. Betrifft `frontend/src/api/jobEvents.ts`, `backend/app/ws/controller.py` |
| ChairExplorer Hardcoded-Metriken | **Vor jeder Demo entfernen/deaktivieren** | Erfundene Zahlen einer vertrauenssensiblen Zielgruppe gezeigt; als „nicht verfügbar" markieren bis #37 echte Daten liefert |
| README vs. Config-Drift | **Docs-Pass, Wochen 22–24** | Ehrlichkeit in Docs ist Teil der Vertrauensgeschichte |
| Port-Adapter-Refactoring (#5) | **Auf unbestimmte Zeit zurückgestellt** | Architektur-Polish ohne MVP-Nutzen; CLAUDE.md-Einfachheitsregel gilt |
| OCR-Engine (#4) | **Zurückgestellt** | Aktuelle LLM-basierte Extraktion funktioniert; erneut prüfen, wenn Transcript-Parsing-Fehlerberichte sich häufen |

---

## 4. Produktstrategie-Entscheidungsbaum

**Branch A — Feedback akzeptieren (zentrale Plattform ist ein schwerer Verkauf):**
→ Alle Energie auf das studentenseitige Chat: Beraterfindung, Kompetenzprofilierung, Kontext-Prep für Outreach. Chair-Management wird ein optionaler, späterer Add-on. Scraping (#37) ist der Ingestion-Rückhalt. Benötigte Professorenbeteiligung: **null**. Risikoprofil: niedrig — Wertlieferung hängt nicht davon ab, jemanden zu überzeugen.

**Branch B — Trotzdem für Professorenakzeptanz kämpfen:**
→ Erfordert Lösung des Anreiz-Alignments (das Hennig für Studierende unlösbar hält), Garantie mehrjähriger Betriebsstabilität (die wir ehrlich nicht versprechen können — wer betreibt das 2028, auf wessen Budget?), und Integration mit Typo3/Gruppenwebseiten-Workflows (Scope-Explosion). Drei harte Voraussetzungen, keine bis 01.07. erfüllbar.

**Entscheidung: Branch A.** Aufgezeichnet 11.06.2026. Die Voraussetzungen von Branch B sind keine Deliverables, die ein Masterprojekt erbringen kann; Branch A liefert das Plan.docx-Mindestziel ohne sie. Erneut prüfen nur, wenn der Fachbereich (z. B. Studiendekan) institutionelle Eigentümerschaft anbietet — das, nicht ein besseres Frontend, wäre das, was Hennigs Kalkül ändern würde.

---

## 5. Datenqualitätsprobleme (priorisiert)

1. **ChairExplorer Hardcoded-Metriken** — vor jeder Demo entfernen oder deaktivieren. Ein Professor, der eine erfundene Zitationszahl für seinen eigenen Lehrstuhl sieht, würde die Beziehung beenden.
2. **DeepSeek-Duplikate (#33)** — doppelte Publikationsdaten untergraben sichtbar den Anspruch „wir repräsentieren Ihren Lehrstuhl akkurat"; vor Showcase beheben.
3. **Dummy-Skill-Berechnung (#16 / PR #21)** — Kompetenzprofile treiben das Matching; ein Dummy-Modell bedeutet, Matches sind dekorativ. Muss real sein, bevor die Umfrage Matching-Qualität misst, also bis Woche 19 landen.
4. **Markdown-Rendering (#25)** — kosmetisch; Woche 27–28 Polish.
5. **Coverage-Annahme-Fehler** — der Ostermann-Vorfall: unsere „wer listet was"-Übersicht hatte mindestens einen Fehler. Vor Veröffentlichung einer fachbereichsweiten Ansicht nochmals prüfen.

---

## 6. Bekannte Unbekannte

1. **Skaliert der Scraping-Agent über Heterogenität?** 27 Lehrstühle, sehr unterschiedliche Webseiten. Testplan: #37 gegen 5 strukturell unterschiedliche Lehrstühle ausführen (Typo3-Standard, ps.cs.uni-tuebingen.de, ein PDF-Listen-Lehrstuhl wie Zell, eine MPI-gehostete Seite, ein Google-Doc/intern-only-Lehrstuhl) und Extraktionsqualität messen, bevor Allgemeingültigkeit beansprucht wird.
2. **Wie oft ändern sich Professoreninteressen wirklich?** Bob und Mario behaupten: fast nie (für Bereiche, nicht Themen). Falls wahr, kann die Re-Scrape-Frequenz quartalsweise erfolgen. Test mit 2–3 freiwilligen Lehrstühlen (Wichmann, Huson, Kerstin sind die freundlichsten Kandidaten).
3. **Werden Studierende den Chat wirklich nutzen?** Heute null studentenseitige Daten. Benötigt Signup- + Session-Tracking im Staging-Deployment (datenschutzkonform, aggregierte Counts) und 3–5 Studierenden-Testsessions vor der Umfragephase.
4. **Wie groß ist die echte Onboarding-Hürde?** Der „<1 Stunde bis Wert"-MVP-Anspruch ist end-to-end ungetestet. Zeit-bis-erstem-Match im Staging instrumentieren.
5. **Wer betreibt das nach dem 01.07.?** Die Hennig-Frage, unbeantwortet. Ehrliche Optionen: Übergabe an den Fachbereich, Übergabe an ein Nachfolger-Studierenden-Team, oder Veröffentlichung als self-hostbares Open Source mit dokumentierter Datenpipeline. Entscheiden vor der Umfrage, da „Was passiert mit meinen Daten?" gefragt werden wird.

---

## 7. Empfehlung an die Projektleitung

1. **Produkt-Narrativ jetzt verschieben** — von „Professoren bei Themen-Management helfen" zu „Studierenden den richtigen Thesis-Betreuer finden helfen." README, Pitch-Deck und jede fachbereichsseitige Kommunikation aktualisieren.
2. **Scope auf der Lehrstuhlseite reduzieren.** Keine Prof-Dashboards, keine Reminder-E-Mails, keine Schreib-Workflows im MVP. Lehrstühle werden über gescrapte öffentliche Daten + optionales Schlüsselwort-Layer repräsentiert. Professoren-Akzeptanz ist explizit **keine** Erfolgskennzahl.
3. **Am kritischen Pfad festhalten.** #35 → #37 bis Woche 14 ist das Gate; alles in der RAG-Phase kann schrumpfen, die Security/Trust-Fixes in Wochen 22–24 nicht.
4. **Vertrauensoberfläche vor jeder Demo fixen.** JWT-in-URL und hardkodierte ChairExplorer-Metriken sind beide günstig zu beheben und katastrophal, wenn sie entdeckt werden. Diese Woche Issues anlegen.
5. **Goodwill nutzen, solange er warm ist.** Luxburg und Hennig haben Gespräche angeboten; Hennig hat weitere Gesprächspartner benannt; Wichmann/Huson/Kerstin haben Bereitschaft signalisiert. Eine zweite Runde 20-Minuten-Gespräche in Wochen 12–14 — diesmal mit Demo des *studentenseitigen* Tools — wandelt Kritiker in Informanten und ist die günstigste verfügbare Validierung vor dem Deployment.
