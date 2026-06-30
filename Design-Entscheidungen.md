# Backbone
## Firmensuche
Ein backbone (Firmennamen) ist necessary für die firmensuche, da das das webscraping auf die in frage kommenden firmen bündelt. Dazu kommt, dass die Firmenliste sich nicht zu stark verändert und so eine statische liste ausreicht. Die frage ist nur wie groß und genau die liste sein muss. (Eigentlich umso genauer, desto besser)
## Uni
Für die Uni reicht es einfach auf die hauptseite von uni tübingen zu verweisen, da von dort aus alles gesucht werden kann und eine grobe richtlinie wie gesucht werden muss.

# Websuche
## Firmen
Konkrete Stellensuche oder nur Firmen die Overlap zu den interessen haben ausgeben? Beides falls möglich, aber sichergehen, dass die Stellen auch wirklich existieren und sinn machen. Aber trotzdem darauf hinweisen, dass es oft keine Stellen gibt und man eigenitiative an den Tag legen muss, und die firmen selbst anschreiben soll, wenn das der firma einen interessiert oder die firma allgemein. Konkrete Stellen nur möglich bei großen firmen mit expliziten stellenausschreibungen, aber oft ergibt auch das nichts. Und bei kleineren firmen oder startups wird die internetseite oft mit den stellen nicht gepflegt und das heißt nicht, dass man deshalb nicht dahin schreiben soll.

**Diskussion 2026-06-30 — Konkrete Stellen scrapen vs. Firmen-Discovery:**
- **Problem:** Backbone (~100–130 Firmen) deckt AI/ML + Medtech + Software gut ab, aber nicht alle Disziplinen (Psychology, EdTech, etc.). Phase-2 Eval zeigte 100% Recall, aber **circular** (GT + Skill nutzen beide Backbone).
- **Entscheidung:** NICHT systematisch alle Stellen scrapen → fragil (HTML ändert sich), meist `unclear` sowieso, fördert SEO-Bias.
- **Besser:** Bleib bei Backbone + Pass-2 Thesis-Signal-Check. **Doppelte URL-Verifikation**: Pass 2 + Step 5 vor Output. URLs die dann broken sind: `⚠ contact URL not confirmed` markieren, Rang unten.
- **Outreach-Strategie nach Firmengröße:** 
  - Corporates: Careers-Portal + in 2 Wochen nochmal checken
  - Startups/SMEs: Direkt R&D-Team anschreiben (schneller, kein HR)
- **Coverage Caveat:** Backbone-Lücken honest erwähnen + Cross-Search-Guidance ("`{topic} BW unternehmen` selbst suchen").
- **Warum funktioniert das:** ~80% der Firmen publicieren Masterarbeit gar nicht → Scraping hätte wenig Mehrwert. **Klare Outreach-Instruktion > mehr Daten scrapen.**

## Uni
Konkrete Professoren und deren Forschung anschauen und den overlap finden. Dabei werden auch paper angeschaut.

# Konversation
Erst Profil des Studenten anlegen mit seinen interessen. Dabei eine bis maximal zwei Fragen pro Output stellen, dass das nicht divergiert. Danach dann Websuche gezielt

Todo: Erklären, dass es oft sinn macht konkrete Phds anzuschreiben. Aber immer zuerst auf den Seiten der Profs nachschauen, wie der Bewerbungsvorgang dort explizit ist, falls es was gibt. Und auch zwei mal schreiben, ist nichts falsches und nett nachfragen, weil oft übersehen wird oder man keine Zeit hat. 