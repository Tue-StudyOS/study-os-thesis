# Zusammenfassung: StudyOS Thesis Advisor als Claude Skill

**Datum:** 11.06.2026 · **Kontext:** Auswertung des Prof-Meetings + technische Klärung zu Agent Skills
**Verwandte Dokumente:** [ideen_bewertung.md](ideen_bewertung.md), [produktpositionierung.md](produktpositionierung.md), [technische_roadmap.md](technische_roadmap.md)

Alle Angaben zu Skills sind gegen die offizielle Anthropic-Dokumentation (Agent Skills Overview, Skills API Guide, Claude Code Skills) geprüft.

---

## 1. Ausgangslage — was im Meeting vorgeschlagen wurde

Der Professor schlägt einen **Architektur-Schwenk** vor:

- Die gesamte App **nicht** als gehostete Web-App mit eigener UI ausliefern, sondern als **einen Claude Skill**, den der Fachbereich bereitstellen kann.
- Für **jede betreuungsberechtigte Person** (Professor bzw. PhD-Student) wird **eine Markdown-Datei** erstellt — eine Kombination aus Lehrstuhl-Info und der konkreten Forschung/den Themen dieser Person.
- Auf Basis dieser kuratierten **„Datenbank"** und der herausgearbeiteten Interessen/Vorkenntnisse des Studenten findet das Tool **passende Betreuer**.

Diese Richtung ist technisch tragfähig und löst sogar mehrere bestehende Probleme (siehe §8). Der kritische Punkt ist nicht die Technik des Skills selbst, sondern die **Verteilung an „den Fachbereich"** und die **monatliche Aktualisierung** (§5, §6).

---

## 2. Wie ein Skill funktioniert (Kurzüberblick)

Ein Skill ist **kein einzelnes Skript**, sondern ein **Verzeichnis** — wie ein Onboarding-Ordner für einen neuen Mitarbeiter. Es enthält eine Pflichtdatei `SKILL.md` (YAML-Frontmatter mit `name` + `description`, dann ein Markdown-Body mit Anweisungen) und **beliebig viele weitere Dateien**: zusätzliche Anleitungen, ausführbare Skripte und Daten/Ressourcen.

Der Schlüssel ist **„progressive disclosure"** in drei Ebenen — nur das jeweils Nötige landet im Kontext:

| Ebene | Wann geladen | Token-Kosten | Inhalt |
|---|---|---|---|
| **1: Metadaten** | immer (beim Start) | ~100 Tokens/Skill | nur `name` + `description` |
| **2: Anweisungen** | wenn der Skill ausgelöst wird | < 5k Tokens | der `SKILL.md`-Body |
| **3: Ressourcen** | nur bei Bedarf | **praktisch unbegrenzt** | gebündelte Dateien, einzeln per `bash` gelesen |

Drei Inhaltstypen mit unterschiedlichen Stärken:
- **Anweisungen** (Markdown) — flexibel interpretiert, nicht starr.
- **Skripte** (z. B. Python) — deterministisch; der Code landet *nicht* im Kontext, nur das Ergebnis.
- **Ressourcen** (MD/JSON/CSV) — Faktenabruf, on-demand gelesen.

### Wir brauchen nur **einen** Skill für das Ganze

Es ist **kein Bündel mehrerer Skills** nötig. Ein einziger, gut strukturierter Skill genügt: Die `SKILL.md` dirigiert den gesamten Ablauf und verweist bei Bedarf auf Unterdateien (Matching-Logik, Thesis-Leitfaden, die Personen-Datenbank, das GPA-Skript). Das hält die Wartung einfach und übersichtlich.

---

## 3. Die „Datenbank" als gebündelte Dateien

> Frage aus dem Meeting: *Kann man die Daten schon als „Datenbank" bereitstellen, ohne dass jeder User extra scrapt?*

**Ja — genau so.** Laut Doku gibt es *„no practical limit on bundled content"*, weil Dateien erst beim Lesen Kontext kosten.

- Ihr scrapt/kuratiert **einmalig im Team** und legt **eine `.md`-Datei pro Person** in den Skill (z. B. unter `researchers/`).
- Der einzelne Student **scrapt nichts** — die Daten sind im Skill enthalten.
- Bei einer Anfrage liest Claude **nur die wenigen relevanten Personen-Dateien**, nicht alle. Auch bei hunderten Dateien explodiert der Kontext nicht.
- Der Detailgrad ist **effektiv unbegrenzt**. Limitierend ist nicht die Datenmenge, sondern die **Auffindbarkeit** — daher braucht es eine Index-Datei (Stichworte pro Person), auf die die `SKILL.md` verweist.

Die **GPA-Berechnung** wird als deterministisches Skript gebündelt — das löst zugleich den Schwankungs-Bug aus [ideen_bewertung.md](ideen_bewertung.md) (Idee 10), weil die Berechnung dann nicht mehr vom LLM-Zufall abhängt.

---

## 4. Empfohlene Skill-Struktur

```
thesis-advisor/
├── SKILL.md                  # Dach-Anweisungen: Ablauf, Matching-Regeln,
│                             #   Balance der Empfehlungen, Kontakt-Coaching
├── MATCHING.md               # detaillierte Matching-Heuristik (bei Bedarf)
├── THESIS_GUIDE.md           # generischer Ablauf + Links zu Prüfungsamt etc.
├── researchers/
│   ├── INDEX.md              # Stichwort-Index aller Personen (Auffindbarkeit!)
│   ├── prof-mustermann.md    # Forschung, betreute Themen, Voraussetzungen
│   ├── phd-xyz.md
│   └── …                     # eine Datei pro Person, beliebig detailliert
└── scripts/
    └── compute_gpa.py        # deterministische GPA-Berechnung (mit ÜBK-Ausschluss)
```

---

## 5. Monatliche Aktualisierung der Daten

> Ziel: einmal im Monat neu scrapen, damit der Skill-Kontext aktuell bleibt.

**Der Re-Scrape selbst ist der einfache Teil** — eine normale Pipeline (am natürlichsten ein **GitHub-Actions-`schedule:`-Cron**), die monatlich: scrapt → `researchers/*.md` neu generiert → den Skill paketiert → ausliefert. Schritt 1–3 ist euer bestehender Code als Batch-Job.

**Ob ihr „neue Versionen hochladen" müsst, hängt von der Plattform ab:**

- **Claude-API (sauberer Weg):** Versionierung wird voll unterstützt. Der **`skill_id` bleibt stabil**; ihr erzeugt nur eine neue Version (`POST /v1/skills/{skill_id}/versions`). Konsumenten, die `version: "latest"` referenzieren, **bekommen die frische Version automatisch** — ohne Nutzeraktion. Damit ist das Monats-Update **ein einziger automatisierter API-Call** aus der Pipeline. (Limit: 30 MB pro Upload.)
- **claude.ai (zäher Weg):** **Keine** zentrale Versionsverwaltung, kein automatisches „latest". Jeder Nutzer müsste das neue ZIP **manuell** herunter- und hochladen — bei Monatskadenz untragbar.
- **Claude Code:** dateibasiert bzw. via Plugin/Marketplace → Update per `git pull` / Plugin-Update. Sauber automatisierbar, erreicht aber nur Claude-Code-Nutzer.

**Warum nicht zur Laufzeit von einem Server nachladen, statt zu bündeln?** Weil die Laufzeitumgebung das meist verbietet: **API-Skills haben *keinen* Netzzugang**, claude.ai nur variabel, und externe Fetches gelten als Sicherheitsrisiko. Deshalb: **Daten bündeln + monatlicher Versions-Bump** ist der robuste Weg. Der Scrape passiert in der Pipeline (mit Netz), nicht zur Skill-Laufzeit.

---

## 6. Verteilung an den Fachbereich — der eigentliche Knackpunkt

Verteilung und Aktualisierung sind **dieselbe Frage**; die Monatskadenz verschärft sie:

| Weg | Verteilung | Monats-Update | Eignung |
|---|---|---|---|
| **API / dünnes Backend** | zentral über euer Integrations-Endpoint | vollautomatisch („latest") | **Beste Lösung**, wenn zentral & aktuell gewünscht |
| **claude.ai (ZIP pro Nutzer)** | jeder lädt selbst hoch | manuell, pro Nutzer → untragbar | nur als Fallback / Demo |
| **Claude Code (Plugin/Git)** | Plugin-Install / `git pull` | automatisierbar | nur für technische Nutzer |

**Wichtig fürs nächste Prof-Gespräch:** „Monatlich frische Daten **ohne Aufwand für die Nutzer**" ist realistisch **nur über die API (oder ein Plugin)** — **nicht** über manuell hochgeladene claude.ai-ZIPs. Der API-Weg bedeutet allerdings: Es braucht doch wieder eine **kleine gehostete Komponente** (über die die Messages-API mit `container.skills` angesprochen wird). Das relativiert das „UI komplett vergessen" teilweise — aus dem großen Web-Stack wird ein dünnes Backend, aber ganz ohne Server geht eine zentrale, automatisch aktuelle Lösung nicht.

---

## 7. Andere LLM-Plattformen (OpenAI, Gemini, DeepSeek)

**Das „Skill"-Format ist ein Anthropic-Mechanismus.** ChatGPT, Gemini und DeepSeek **lesen keine `SKILL.md`** und kennen weder progressive disclosure noch die Code-Execution-VM. Es gibt also **nicht** „denselben Skill, pro LLM optimiert" — ihr baut **nicht** vier parallele Skill-Varianten.

**Portabel ist der Inhalt**, nicht der Mechanismus: eure kuratierten Markdown-Dateien (die Personen-Datenbank) und die Instruktions-Texte sind reines Markdown und lassen sich wiederverwenden. Lösungen pro Plattform:

- **OpenAI:** „Custom GPT" mit hochgeladenen Dateien + File Search (RAG über dieselbe MD-Sammlung). Kommt dem Skill-Erlebnis am nächsten.
- **Gemini:** „Gem" bzw. System-Prompt + Datei-Grounding über dieselben Dateien.
- **DeepSeek:** kein natives Custom-GPT-/Skill-Äquivalent → benötigt ein **eigenes RAG-Backend** (System-Prompt + Retrieval über die MD-Datenbank).
- **Generisch & plattformunabhängig:** System-Prompt + RAG über die MD-Sammlung — funktioniert mit jedem hinreichend fähigen LLM, ist aber am meisten Eigenbau.

**Empfehlung:** Den Skill **für Claude** bauen (dort funktioniert der Mechanismus „out of the box" am besten) und **Daten/Instruktionen sauber vom Mechanismus trennen**, damit ihr die Inhalte bei Bedarf für andere LLMs neu paketieren könnt. Plant keine Mehrfach-Implementierung auf Vorrat (vgl. CLAUDE.md §2: keine unnötige „Flexibilität").

---

## 8. Vor- und Nachteile

### Vorteile

- **Security-Blocker verschwinden.** Kein gehostetes Backend (bzw. nur ein sehr dünnes) → das WebSocket-JWT-in-URL-Problem aus [technische_roadmap.md](technische_roadmap.md) entfällt weitgehend.
- **Hennigs Stabilitätssorge entschärft sich.** Ein Skill ist ein Satz Dateien, keine laufende Web-App, die „auseinanderfällt, sobald die HiWis weg sind". Deutlich langlebiger.
- **Massive Vereinfachung.** Postgres, pgvector, Celery, Redis, Ollama-Hosting und die React-UI fallen weitgehend weg. Bei ein paar hundert Personen liest und schließt Claude direkt über die MD-Dateien — keine Embedding-Infrastruktur nötig.
- **Deterministische GPA.** Als gebündeltes Skript ausgeführt → kein Temperatur-Rauschen mehr (behebt Idee 10).
- **Wartungsarm für Profs.** Pflege = periodischer Dev-Job (Pipeline neu laufen lassen), **kein Professor muss etwas tun** — passt exakt zur Produktpositionierung.

### Nachteile

- **Weniger UX-Kontrolle.** Ihr reitet auf dem jeweiligen Chat-Client; kein eigenes geführtes Interface.
- **Verteilung als Selbstbedienung** (auf claude.ai), kein echtes org-weites Rollout.
- **Zugangsbarriere.** claude.ai-Skills erfordern bezahlten Zugang (Pro/Max/Team/Enterprise) **mit aktivierter Code-Ausführung** — nicht im Gratis-Tarif.
- **Plattform-Bindung an Claude** für das native Erlebnis (siehe §7).
- **Doch ein Backend nötig**, sobald es zentral & automatisch aktuell sein soll (API-Weg).

---

## 9. Kritische Punkte & externe Abhängigkeiten

Was ihr „extern" braucht und im Blick behalten müsst:

- **Anthropic API-Key** — für den automatisierten Upload der Skill-Versionen und (beim API-Weg) für die Messages-API-Aufrufe mit `container.skills`. Muss als **GitHub-Actions-Secret** hinterlegt werden, nie im Repo.
- **OpenAlex-Zugang fürs Scraping** — i. d. R. ohne Key nutzbar, aber **Rate-Limits / „polite pool"** beachten (Mail-Header). Beim monatlichen Batch unkritisch.
- **GitHub-Actions-Secrets-Verwaltung** — alle Tokens dort, plus eine Stelle, die den Cron-Job am Leben hält.
- **30-MB-Upload-Limit** der Skills-API — bei reinen MD-Forschungsbeschreibungen unkritisch, aber im Auge behalten (keine großen Binärdateien bündeln).
- **Beta-Header / Code-Execution** — die Skills-Nutzung über die API setzt aktuelle Beta-Flags (Code-Execution, Skills, Files-API) voraus; das kann sich ändern.
- **Betriebsverantwortung nach dem 01.07.** — wer hält Pipeline, API-Key und (ggf.) das dünne Backend am Laufen? Genau die unbeantwortete Hennig-Frage; vor einer Fachbereichs-Listung klären.
- **Datenschutz.** Agent Skills sind **nicht ZDR-fähig** (Zero Data Retention) — Daten werden nach Standard-Policy gespeichert. **Transcript-/GPA-Daten der Studierenden** sollten lokal verarbeitet werden und **nicht** in die gebündelte, geteilte Datenbank wandern.
- **Sicherheit.** Skills nur aus vertrauenswürdiger Quelle; externe Laufzeit-Fetches sind ausdrücklich riskant (ein weiterer Grund, Daten zu bündeln statt nachzuladen).

---

## 10. Empfehlung & offene Entscheidung

Die Richtung des Profs ist gut — sie vereinfacht den Stack erheblich und entschärft Security- und Langlebigkeitsprobleme. **Wir brauchen dafür nur einen einzigen Skill.**

**Die eine Entscheidung, die alles andere festlegt, ist die Plattform/Verteilung:**

- Für **„zentral + monatlich automatisch aktuell"** führt kein Weg an einem **API-basierten Ansatz (oder einem Plugin)** vorbei — mit einem dünnen Backend und automatisiertem Versions-Upload aus GitHub Actions.
- Der **claude.ai-ZIP-Weg** ist nur als Demo/Fallback brauchbar, weil das monatliche Update jeden Nutzer manuell betrifft.

**Konkret als nächstes mit dem Prof zu klären:** Soll „dem Fachbereich bereitstellen" zentral & automatisch aktuell sein (→ API/Plugin + dünnes Backend, etwas Betriebsaufwand) oder reicht „Studierende laden sich den Skill selbst" (→ claude.ai-ZIP, aber Monatsupdate praktisch nur quartalsweise/manuell sinnvoll)? Diese Antwort bestimmt Architektur, Verteilung und Update-Story zugleich.
