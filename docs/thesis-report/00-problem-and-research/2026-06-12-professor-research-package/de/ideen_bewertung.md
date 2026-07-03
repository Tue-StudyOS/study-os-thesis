# Bewertung deiner Ideen — StudyOS Thesis Advisor

**Datum:** 11.06.2026 · **Grundlage:** [Ideen.md](Ideen.md), Professoren-Feedback (27 Antworten, siehe [marktanalyse.md](marktanalyse.md)), aktueller Code-Stand (verifiziert 11.06.2026)

Dieses Dokument geht jede Idee einzeln durch: **Macht das Sinn?**, **Warum (mit Beleg)?** und **Was konkret tun?**. Am Ende steht eine Priorisierung.

**Kurzfazit vorweg:** Die Ideen sind in der Summe sehr stimmig — und sie zeigen denselben Schwenk, den auch das Professoren-Feedback erzwingt: **weg von „Themenlisten der Profs", hin zu „Studierenden helfen, den richtigen Lehrstuhl zu finden und gut vorbereitet hinzugehen".** Drei Punkte verdienen besondere Aufmerksamkeit: die Balance der Empfehlungen (Idee 4), ein latenter Selbstwiderspruch bei den Formalien (Ideen 8/9 vs. deine eigene Stale-Info-Sorge in Idee 1) und ein echter Bug in der GPA-Berechnung (Idee 10), dessen Ursache ich im Code gefunden habe.

---

## Überblick: Bewertung auf einen Blick

| # | Idee | Bewertung |
|---|---|---|
| — | Sichtbarkeit über die Uni-Seite (Thesis-Finder) | ✅ Sehr sinnvoll — der richtige Vertriebskanal |
| 1 | Skepsis ggü. Themen-Scraper | ✅ Richtige Intuition, vom Feedback gestützt |
| 2 | Stattdessen Paper/Forschung extrahieren, exakte Lehrstuhlprofile | ✅ Genau richtig — Architektur unterstützt das bereits |
| 3 | Empfehlungen & Chat darauf stützen | ✅ Richtig, ist die geplante RAG-Richtung |
| 4 | Empfehlungen gut balancieren (Last verteilen) | ⚠️ Wichtig & subtil — Relevanz darf nicht leiden |
| 5 | Erwartungshaltung & Voraussetzungen der Profs | ⚠️ Sehr wertvoll, aber Datenquelle ist die Hürde |
| 6 | Wie man Kontakt aufnimmt / Thesis-Ablauf | ✅ Hoher Wert, kein Prof-Abhängigkeit |
| 7 | LaTeX-Vorlage verlinken | ✅ Trivial & nützlich |
| 8 | Allgemeine Thesis-Tipps & Formalien | ⚠️ Gut — aber verlinken statt nacherzählen |
| 9 | Offizieller Anmeldeablauf | ⚠️ Gut — gleiche Vorsicht wie 8 |
| 10 | GPA-Berechnung schwankt | 🔧 Echter Bug — Ursache im Code gefunden |

---

## Sichtbarkeit: Listung als „Thesis-Finder" auf der Fachbereichsseite

**Bewertung: ✅ Sehr sinnvoll. Das ist genau der richtige Vertriebsweg — und er passt exakt zur neuen Produktpositionierung.**

Warum das funktioniert:
- Es ist der **studierendenseitige Kanal**, und das Tool ist (nach dem Pivot in [produktpositionierung.md](produktpositionierung.md)) ein studierendenseitiges Produkt. Eine Listung „Fachbereich Informatik → Thesis-Finder" erreicht genau die Zielgruppe, ohne dass ein einziger Professor etwas tun muss.
- Es löst zugleich ein Problem, das mehrere Profs *selbst* benannt haben: Menth wünscht sich „ein System, mit dem Studierende leichter an Abschlussarbeiten kommen". Eine offizielle Listung kanalisiert genau diese Studierenden dorthin.

Was du dabei bedenken musst:
- **Die Listung selbst ist eine politische Entscheidung des Fachbereichs**, kein technisches Feature. Genau hier greift Hennigs Warnung: „It's all about the internal dynamics of the CS department." Wer entscheidet über die Aufnahme? Vermutlich der Studiendekan / die Studienberatung. Das ist dieselbe Stelle, die 2022 den gescheiterten Listing-Versuch betrieb — d. h. dort gibt es Vorerfahrung *und* möglicherweise Skepsis.
- **Stabilitätsfrage (Hennig):** Eine offizielle Listung erhöht den Anspruch „Existiert das in 3 Jahren noch?". Bevor das Tool prominent verlinkt wird, sollte die Betriebsfrage (wer pflegt es nach dem 01.07.?) zumindest eine ehrliche Antwort haben (siehe [detaillierte_analyse.md](detaillierte_analyse.md), §6.5).

**Konkret:**
1. Den kurzen Beschreibungstext bewusst studierendenzentriert formulieren („Finde heraus, welcher Lehrstuhl zu deinen Interessen passt und wie du ihn ansprichst" — *nicht* „Datenbank aller Themen").
2. Früh das Gespräch mit dem Studiendekanat suchen — am besten mit einer laufenden Demo des studierendenseitigen Tools (knüpft an Luxburgs/Hennigs Gesprächsangebote an).
3. Die Listung als **Ziel für Wochen 22–28** einplanen (nach Deployment), nicht vorher.

---

## Kritische Sachen

### 1. Skepsis gegenüber dem Themen-Scraper der Profs

> *„Weiß nicht ob das so viel hilft, weil das ganze ja auch oft veraltet ist und man dann ‚Fehlinfos' bekommt oft."*

**Bewertung: ✅ Deine Intuition ist richtig — und sie deckt sich exakt mit dem Professoren-Feedback.**

Du hast hier dasselbe erkannt, was die Professoren unabhängig voneinander gesagt haben:
- Häufle: „research moves too fast and by the time students look at the thesis topics, they are outdated."
- Winther: Studierende sahen 4–5 gelistete Themen und dachten, das sei das ganze Labor — die Liste hat das Matching **aktiv verschlechtert**.
- Zell: „>50 % der Themen, die ich betreue, schaffen es nie auf die Liste."

Heißt: Ein Scraper, der **Themenlisten** abgreift, reproduziert genau die veralteten „Fehlinfos", vor denen du warnst. Deine Skepsis ist berechtigt.

**Wichtige Klarstellung zum Code-Stand:** Der bereits existierende Scraper ([backend/app/scraper/pipeline.py](backend/app/scraper/pipeline.py)) ist **gar kein Themenlisten-Scraper** — er zieht über OpenAlex **Paper** und ordnet sie Forschenden zu (`OpenAlexSourceClient`, `ResearcherRepository`, `RecencyPaperRanker`). Das ist bereits die paper-basierte Richtung aus deiner Idee 2. Was als „chair-discovery agent" (PR #37 / Issue #22/#36) firmiert, sammelt **Lehrstuhl-Stammdaten** von der Uni-Seite (wer ist der Lehrstuhl, wer gehört dazu) — nicht konkrete, schnell veraltende Themen.

**Konkret:**
- Den Begriff sauber trennen: **Lehrstuhl-Stammdaten** (selten veraltet — Name, Team, Forschungsbereiche) ja; **konkrete Themenlisten** (schnell veraltet) nein.
- Falls PR #37 doch konkrete Themen von Lehrstuhlseiten abgreifen sollte: jedes solche Item mit **Quelle + Scrape-Datum** versehen und im UI als „Stand: TT.MM.JJJJ, bitte beim Lehrstuhl verifizieren" kennzeichnen. Niemals undatierte Themen anzeigen.

### 2. Stattdessen Paper / Forschungsbeschreibungen extrahieren — exakte Lehrstuhlprofile

> *„Lieber auf die Paper zurückgreifen … sodass jeder Lehrstuhl seine ‚optimale' Beschreibung hat (mit allen Doktoranden die dort arbeiten und Themen betreuen)."*

**Bewertung: ✅ Genau die richtige Richtung. Sie ist feedback-validiert und die Architektur unterstützt sie bereits.**

Das deckt sich mit den konstruktivsten Antworten:
- Macke: „If you have a system that reads the relevant section in our website and posts topics … that would be something I am much more excited about."
- Bob: aggregiere „**the set of problems the prof and their team are interested in**" — und genau diese Beschreibungen „would not need revision very often." Das ist der Kern: Forschungs*bereiche* sind stabil, konkrete Themen nicht.

Und der Code ist schon darauf ausgelegt: Paper über OpenAlex + `ResearcherRepository` + LLM-Enricher, der Paper anreichert. Daraus lässt sich pro Lehrstuhl ein stabiles, daten-gestütztes Profil bauen.

**Ein wichtiger Vorbehalt, den du einplanen solltest:** „mit allen Doktoranden, die dort arbeiten und Themen betreuen" ist der schwierigste Teil — und birgt **genau die Stale-Info-Gefahr aus Idee 1**:
- Paper liefern **Ko-Autoren**, nicht „wer betreut aktuell Theses und hat Kapazität". Ein Postdoc auf einem Paper von 2023 kann längst weg sein (vgl. Zell: „after Ph.D. students leave the group").
- Die Zuordnung „Ko-Autor → aktuell betreuender Doktorand" ist nicht automatisch korrekt und veraltet schnell.

**Konkret:**
- Lehrstuhlprofil aus **stabilen Signalen** bauen: Forschungsbereiche/Keywords (aus Paper-Abstracts via LLM-Enricher aggregiert), Schwerpunktthemen der letzten ~3 Jahre, repräsentative Paper.
- Personen mit **Vorsicht und Datierung**: Forschende nur dann als „betreut Theses" labeln, wenn es eine belastbare Quelle gibt (Lehrstuhlseite), sonst neutral als „forscht zu X (Paper 2023–2025)".
- Das verbindet sich direkt mit dem Vertrauensthema aus [technische_roadmap.md](technische_roadmap.md) §1: **keine erfundenen/abgeleiteten Personendaten anzeigen, die ein Prof als falsch erkennen würde.**

### 3. Empfehlungen und Chat darauf stützen

**Bewertung: ✅ Richtig — und es ist die ohnehin geplante RAG-Richtung.**

Wenn die Lehrstuhlprofile aus Idee 2 sauber sind, ist „Chat + Empfehlungen darauf stützen" die natürliche Konsequenz: Retrieval über Paper/Profile, Antworten mit Quellenbezug. Das ist exakt die RAG-Phase (Wochen 15–21, Issues #7, #6, #32).

**Konkret:**
- **Jede Empfehlung mit Begründung + Quelle** ausgeben („passt, weil Lehrstuhl X zu deinem Schwerpunkt Y publiziert — siehe Paper Z"). Das schafft Vertrauen und ist überprüfbar.
- Voraussetzung: die Eval-Harness (deepeval, #6) **zuerst** aufsetzen, sonst ist „der Chat empfiehlt gut" nicht messbar (siehe [technische_roadmap.md](technische_roadmap.md) §4).
- Abhängigkeit beachten: Die Qualität der Empfehlung hängt am **echten Kompetenzprofil** — und das ist heute noch ein Dummy (#16/PR #21). Solange das Dummy ist, sind Matches dekorativ.

### 4. Empfehlungen gut balancieren, damit nicht einzelne PhDs/Profs überlaufen

> *„weil sonst manche PHDs und Profs viel mehr Anfragen bekommen."*

**Bewertung: ⚠️ Wichtiger und subtiler Punkt — aber mit einer echten Zielkollision, die du bewusst auflösen musst.**

Das ist eine deiner besten Beobachtungen, weil sie das **Kernproblem aus dem Feedback** direkt adressiert: Menth (20 betreut, 50+ Anfragen), Macke („way larger than we can supervise"), Butz. Wenn dein Tool alle Studierenden auf dieselben 3 „Star-Lehrstühle" lenkt, verschärfst du genau dieses Problem — und machst dir die Profs zum Gegner.

**Aber Vorsicht vor der naheliegenden Falle:** Last-Balancing darf **nicht** dazu führen, dass schlechtere Matches empfohlen werden, nur um zu verteilen. Das würde Studierende fehlleiten und dein Vertrauensversprechen brechen. Relevanz muss zuerst kommen.

**Konkret — so löst du die Kollision:**
1. **Mehrere gute Matches statt Top-1.** Statt „der eine perfekte Lehrstuhl" zeige 3–5 thematisch passende. Das verteilt auf natürliche Weise, ohne Relevanz zu opfern.
2. **Breite statt Spitze betonen.** Gerade kleinere/weniger sichtbare Lehrstühle, die thematisch passen, aktiv mit anzeigen — das hilft sowohl überlaufenen Profs (Entlastung) als auch unterausgelasteten (Sichtbarkeit).
3. **Kapazitäts-/Lastsignale nur, wenn echt verfügbar.** Falls je ein optionales „nehme aktuell (keine) Anfragen an"-Signal von Lehrstühlen kommt (Idee 5), das einbeziehen. Niemals erfinden.
4. **Kein verstecktes Hard-Tuning.** Falls überhaupt ein Lastfaktor ins Ranking einfließt, transparent halten — sonst entsteht ein intransparentes, schwer testbares System (vgl. CLAUDE.md §2: keine ungewollte „Cleverness").
5. **Explizit als Erfolgsmetrik führen:** „Wie breit streut das Tool die Empfehlungen?" gehört in die Survey-Phase (verteilen sich Kontakte oder klumpen sie?).

### 5. Erwartungshaltung der Profs & benötigte Voraussetzungen bereitstellen

**Bewertung: ⚠️ Sehr wertvoll für Studierende — die Hürde ist die Datenquelle, nicht die Idee.**

Das ist genau das, was Studierenden den meisten Frust erspart und Profs Fehlanfragen. Es ist auch direkt durch Feedback belegt:
- Zell: „students who write a B.S./M.S. thesis must at least have passed one of my lectures or lab courses." Das ist eine harte Voraussetzung, die ein Studierender vorher kennen sollte.
- Menth, Macke: Überlast durch unpassende Anfragen — klare Erwartungen filtern vorab.

**Die Schwierigkeit:** Diese Infos (Voraussetzungen, Erwartungen) stehen **selten strukturiert** auf Webseiten und lassen sich kaum zuverlässig scrapen. Sie sind außerdem genau die Art von Information, die — wenn falsch dargestellt — Profs verärgert (vgl. Trust-Thema). Hier reproduzierst du sonst wieder das Stale-Info-Problem.

**Konkret:**
- **Generische, lehrstuhl-unabhängige Erwartungen** kannst du sofort und risikoarm bereitstellen (z. B. „die meisten Lehrstühle erwarten, dass du eine einschlägige Vorlesung/ein Praktikum belegt hast" — als allgemeiner Hinweis).
- **Lehrstuhl-spezifische** Voraussetzungen nur, wenn die Quelle belastbar ist — idealerweise als **optionales Opt-in-Feld** für die Typ-B-Lehrstühle (Wichmann, Huson, Kerstin), die ohnehin kooperationsbereit sind. Das ist Ebene 2 aus [produktpositionierung.md](produktpositionierung.md) und gehört **nicht** ins MVP, sondern nach hinten.
- Bis dahin: das Tool kann Studierende coachen, **selbst danach zu fragen** („Frag im Erstkontakt, ob es Voraussetzungen gibt") — das ist sicher und passt zu Idee 6.

### 6. Wie man (im besten Fall) mit dem Prof in Kontakt tritt & wie der Thesis-Ablauf ist

**Bewertung: ✅ Hoher Wert, geringes Risiko, keine Prof-Abhängigkeit — sehr gut für's MVP.**

Das ist Kern der neuen Positionierung: Das Tool **bereitet den menschlichen Erstkontakt vor**, statt ihn zu ersetzen. Winther sagt explizit, Themenwahl „merits person-to-person interaction" — genau dorthin soll dein Tool die Studierenden gut vorbereitet schicken. Das senkt zugleich die Fehlanfragen, die Menth/Macke beklagen.

**Konkret:**
- Ein **„Kontakt vorbereiten"-Modul**: Hilfe beim Formulieren einer knappen, signalstarken ersten Mail (wer bin ich, was kann ich, warum genau dieser Lehrstuhl — gestützt auf das Profil aus Idee 2/3).
- Ein **generischer Ablauf-Leitfaden**: typische Schritte einer Thesis (Erstkontakt → Themengespräch → Exposé → Anmeldung → Bearbeitung → Abgabe → Kolloquium). Generisch und damit stabil/wartungsarm.
- Das ist eine der wenigen Funktionen, die du **sofort** und ohne externe Daten bauen kannst.

### 7. LaTeX-Vorlage verlinken

**Bewertung: ✅ Trivial und nützlich. Einfach machen.**

Eine statische Ressource, kein Wartungsproblem. Wenn der Fachbereich/eine Gruppe eine offizielle Vorlage hat, diese verlinken; sonst eine etablierte (z. B. eine gängige Uni-Tübingen-CS-Vorlage). Geringer Aufwand, klarer Nutzen.

**Konkret:** Als statischen Link/Ressource in den Thesis-Tipps (Idee 8) unterbringen — kein eigenes Feature nötig.

### 8. Allgemeine Thesis-Tipps & Formalien (Abgabe, Pflichtbestandteile)

**Bewertung: ⚠️ Guter Nutzen — aber Achtung auf einen Selbstwiderspruch zu deiner eigenen Idee 1.**

Das ist genau die Info-Lücke, die du selbst erlebt hast („Ich war damals da nicht sicher") — also realer Bedarf. **Aber:** Formalien (Pflichtbestandteile, Eigenständigkeitserklärung, Seitenränder, Fristen) sind **prüfungsordnungs- und studiengangsabhängig** und ändern sich. Wenn du sie im Tool **nacherzählst**, baust du genau die „veralteten Fehlinfos", vor denen du in Idee 1 zu Recht warnst — nur diesmal bei Formalien, wo Falschinfo besonders teuer ist (verpasste Frist, abgelehnte Arbeit).

**Konkret — Konsistenz mit Idee 1:**
- **Verlinken statt nacherzählen.** Auf die offiziellen Quellen (Prüfungsamt, Prüfungsordnung, Studiengangsseite) verweisen, statt Inhalte zu kopieren.
- Was du **selbst** bereitstellen kannst, ist das **Stabile & Generische**: Tipps zur Arbeitsweise, Zeitplanung, Struktur, Umgang mit dem Betreuer — das veraltet nicht.
- Wo du doch konkrete Formalien zeigst: mit **Datum + Quelllink + Hinweis „verbindlich ist die Prüfungsordnung"**.

### 9. Offizieller Anmeldeablauf der Thesis

**Bewertung: ⚠️ Sinnvoll als Zusatzinfo — gleiche Vorsicht wie Idee 8.**

Studierende suchen das tatsächlich, und es passt gut zum Ablauf-Leitfaden (Idee 6). Aber der Anmeldeprozess (Formulare, Fristen, Prüfungsamt vs. Lehrstuhl) ist amtlich geregelt und ändert sich.

**Konkret:**
- Den **generischen Ablauf** beschreiben (Anmeldung erfolgt i. d. R. über das Prüfungsamt nach Themenfixierung, Bearbeitungszeit startet mit Anmeldung, …) und für die **verbindlichen Details auf das Prüfungsamt verlinken**.
- Nicht das offizielle Formular/Detailregeln im Tool duplizieren.

### 10. GPA-Berechnung gibt jedes Mal etwas anderes aus

> *„Dass die übk nicht rein gerechnet wird … extract von LLM und dann wird es berechnet mit fester Funktion?"*

**Bewertung: 🔧 Echter Bug — ich habe die Ursache im Code gefunden. Und ja: dein vorgeschlagener Ansatz ist exakt richtig.**

Dein mentales Modell („LLM extrahiert, feste Funktion rechnet") ist genau die korrekte Architektur — und sie ist im Code **bereits angelegt**, aber an drei Stellen gebrochen:

**Ursache der schwankenden Werte (der eigentliche Bug):**
Die GPA wird zwar deterministisch berechnet — [`_compute_gpa()` in service.py:49](backend/app/students/service.py#L49), aufgerufen in [service.py:136](backend/app/students/service.py#L136). **Aber ihr Input** (`parse_result.courses`) kommt aus der LLM-Extraktion in [`_parse_transcript_with_llm()` (service.py:174–184)](backend/app/students/service.py#L174-L184), und dieser Aufruf setzt **kein `temperature=0`** (kein `options`-Parameter übergeben). Das LLM extrahiert also bei jedem Lauf leicht unterschiedlich — mal fehlt ein Kurs, mal werden Credits/Note anders gelesen — und die feste Funktion bekommt **jedes Mal andere Eingaben** → anderes Ergebnis. Das ist die Quelle von „gibt jedes Mal was anderes aus".

**ÜBK wird nirgends ausgeschlossen.** `_compute_gpa` zählt **jede** numerische Note zwischen 1,0 und 5,0 — also auch überfachliche/berufsqualifizierende Kompetenzen (ÜBK), die laut Prüfungsordnung **nicht** in den Schnitt sollen. Dein Wunsch („dass die übk nicht rein gerechnet wird") ist berechtigt und aktuell nicht umgesetzt.

**Redundante zweite Berechnung.** Der Prompt fordert das LLM zusätzlich auf, selbst eine `gpa` zu berechnen ([`_TRANSCRIPT_PROMPT`, das `gpa`-Feld in `TranscriptParseResult`](backend/app/students/service.py#L20)). Dieser Wert wird **nirgends gespeichert** (die Python-Funktion gewinnt), ist also toter, verwirrender Code — und falls er irgendwo doch angezeigt würde, widerspräche er dem berechneten Wert.

**Konkret — der Fix (genau dein Ansatz, zu Ende geführt):**
1. **Determinismus erzwingen:** Beim Extraktions-Aufruf `options={"temperature": 0}` (und idealerweise einen festen `seed`) übergeben. Das allein beseitigt den Großteil der Schwankung. Der LiteLLM-Adapter mappt `temperature` bereits durch ([litellm_adapter.py:183](backend/app/llm/litellm_adapter.py#L183)).
2. **ÜBK ausschließen:** Das LLM pro Kurs ein Flag/eine Kategorie extrahieren lassen (z. B. `is_uebk` / `category: "ÜBK" | "Fach" | …`) **oder** ÜBK-Kurse in `_compute_gpa` per Namens-/Kategorie-Regel überspringen. Die deterministische Funktion bleibt die Autorität — sie bekommt nur die korrekte Kursmenge.
3. **Redundanz entfernen:** Das `gpa`-Feld aus dem Prompt und aus `TranscriptParseResult` streichen. Das LLM extrahiert **nur Kurse**, die feste Funktion rechnet. Eine einzige Wahrheit.
4. **Absichern mit Test:** Es gibt bereits [test_compute_gpa.py](backend/tests/unit/test_compute_gpa.py) — dort einen Fall ergänzen, der ÜBK-Kurse einschließt und prüft, dass sie **nicht** in den Schnitt eingehen (CLAUDE.md §4: erst der Test, der den Bug reproduziert, dann der Fix).

Das hängt direkt an **Issue #16 / PR #21** (Dummy-Skill-Berechnung ersetzen) — beides ist die „Profil-Genauigkeit"-Baustelle und sollte gemeinsam gemacht werden.

---

## Synthese & Priorisierung

Deine Ideen zerfallen in vier saubere Gruppen. So würde ich sie einsortieren:

**A. Bestätigt die Strategie — weitermachen (Ideen 1, 2, 3)**
Die Skepsis gegenüber Themen-Scraping und der Fokus auf paper-/forschungsbasierte Lehrstuhlprofile sind goldrichtig und vom Professoren-Feedback gestützt. Die Architektur (OpenAlex-Scraper + Researcher-Profile + RAG) trägt das bereits. Einziger Vorbehalt: Personendaten („welche Doktoranden betreuen") mit Vorsicht und Datierung behandeln, um nicht die Stale-Info-Falle aus Idee 1 selbst zu treten.

**B. Studierenden-Inhalte mit hohem Wert & geringem Risiko — gutes MVP-Material (Ideen 6, 7)**
Kontakt-Vorbereitung, generischer Thesis-Ablauf, LaTeX-Link. Sofort baubar, keine externen Daten, kein Prof nötig. Diese Funktionen machen den „<1 Stunde bis Mehrwert"-Anspruch aus Plan.docx konkret.

**C. Wertvoll, aber mit Datenquellen-/Aktualitäts-Vorsicht — verlinken statt nacherzählen (Ideen 5, 8, 9)**
Erwartungen/Voraussetzungen und Formalien/Anmeldung sind echter Bedarf. Aber: lehrstuhl-spezifische bzw. amtliche Infos **nicht im Tool duplizieren** (sonst baust du genau die veralteten Fehlinfos, die du in Idee 1 vermeiden willst). Generisches selbst bereitstellen, Verbindliches verlinken, lehrstuhl-spezifisches Opt-in nach hinten (Ebene 2).

**D. Produkt-Design-Frage, jetzt schon mitdenken (Idee 4)**
Empfehlungen so balancieren, dass nicht einzelne Profs überlaufen — aber **nie auf Kosten der Relevanz**. Lösung über „mehrere gute Matches + Breite betonen", nicht über verstecktes Last-Tuning. Als Survey-Metrik mitführen.

**E. Echter Bug — bald fixen (Idee 10)**
Die GPA-Schwankung hat eine konkrete, behebbare Ursache (`temperature=0` fehlt + keine ÜBK-Filterung + redundante LLM-Berechnung). Dein vorgeschlagener Ansatz ist exakt richtig. Zusammen mit #16/PR #21 angehen.

**Empfohlene nächste Schritte:**
1. **Sofort, klein:** GPA-Fix (Idee 10) — `temperature=0`, ÜBK-Ausschluss, redundantes Feld raus, Test ergänzen. Klar abgegrenzt, hoher Frust-Abbau.
2. **MVP-Phase:** Studierenden-Inhalte (Ideen 6, 7) bauen — niedrigstes Risiko, direkter Nutzen.
3. **Laufend:** Lehrstuhlprofile (Ideen 2, 3) schärfen, mit dem Personendaten-Vorbehalt.
4. **Design-Entscheidung treffen:** Empfehlungs-Balance (Idee 4) — Ranking-Verhalten festlegen, bevor die RAG-Phase startet.
5. **Nach Deployment:** Uni-Seiten-Listung anstoßen (Gespräch mit Studiendekanat) und Formalien/Anmeldung als verlinkte Inhalte (Ideen 5, 8, 9, Sichtbarkeit).
