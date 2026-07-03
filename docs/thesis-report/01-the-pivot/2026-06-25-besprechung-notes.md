# Erweitern auf Companies:
1. Scrapen welche Companies es gibt und welche in Frage kommen, das man eine Masterarbeit dort schreibt
1.1. Wie halten wir das up-to-date?
1.2 Einen Skill schreiben, der das gut definiert, wonach gesucht wird und das dann auch einmal im monat mit fetcht
1.3 In dem Skill definieren, wie genau gesucht wird nach solchen Companies. Aber müssen wir das überhaupt, oder wird das schon automatisch richtig gemacht von claude?

# Erweitern auf andere Fachbereiche

Wir müssen den skill fast schon so bauen, dass es nicht nur für Informatik funktioniert, sondern direkt für alle Fachbereiche und keine Hintergrundinfos braucht, sondern dass es wirklich "vollautomatisch" läuft. 

# Backend 
Brauchen wir dann überhaupt noch ein Backend? Können wir das irgendwie so gestalten, dass alles wirklich ohne funktioniert, also ohne Datenbank? Dann würde es auch "natürlich" für alle Fachbereiche funktionieren

Dann müssten wir auch nicht mehr das ganze up-to-date halten, dass es noch in 3 jahren funktioniert, also dass wir nur sagen, wie das Tool das webscraping macht und wie die konversation geführt wird, dass extrahiert wird, was es gibt und wie man die interessen herausfindet und die skills und so einem aufzeigt, was für bereiche oder firmen es gibt und welche personen?

# Key Challenges

Wie schaffen wir, dass das funktioniert (ohne Daten für alle Fachbereiche, sodas wir keine automatischen github actions laufen lassen müssen)? Wo ist der Unterschied, dass wir einfach Claude ohne skill benutzen? Wie schaffen wir es, dass es distributed ist und genutzt wird?

# API-Key
1. Fragen, ob wir das haben können
Aber brauchen wir überhaupt eine Datenbank?? Reicht nicht einfach die Liste von den möglichen Profs?

Bzw. wie können wir die Liste von den möglichen Profs automatisch richtig scrapen, sodass wir keine Ground-Truth liste bereitstellen müssen?

# Framing vom Tool

Wir wollen, dass man die Informationsüberladung, die es gibt für verschiedene Themen, Profs, Unternehmen, usw. sammeln, und mit den Interessen und Erfahrung von dem spezifischen Student alignen, sodass er weiß, welche Anlaufstellen und welche "Bereiche" und groben Topics es gibt bei welchen Personen oder Firmen. Möglicherweise keine exakten Proposals, sondern aus den Informationen und den Möglichkeiten herauszufiltern was es gibt und die Interessensdirection und die Possibilites zu alignen mit konkreten Anlaufstellen.

1. Was genau ist das Ziel?
1.1 Einen Research-Proposal? Eine Liste an Leuten mit Relevanz und Sinnvolligkeit? 
1.2 Alle Möglichkeiten die existieren und die mit den eigenen Interessen übereinstimmen aufzeigen.
1.3 Das manuelle Suchen eingrenzen und schneller an die gewünschten infos kommen. 

# Wie verteilen wir das Tool?
1. Fachschaft
2. Hennig-Github
3. Ersti-Heft
4. Uni-Seite? Also entweder nur Informatik-Seite, dass wenn man auf der Uni-Seite sucht, dass man das angezeigt bekommt mit: "Searching for a thesis - align your interests with the possibilites with this /skill". 
4.1 Ich glaube das ist unsere beste möglichkeit, weil viele das erst mal googlen und dann unseren skill vorgeschlagen bekommen
5. Menth's: "How to find a thesis"

# Wie halten wir das up-to-date, sodass es wirklich funtktioniert? 


# Zusatzinfos bereitstellen für die Konversation
Macht das sinn? Welche genau? Müssen wir da vorsichtig sein? 


# Wie tragen wir die Infos von Konversation zu Konversation weiter, wenn man den Skill in einer Konversation genutzt hat, dass man "nahtlos" weiterarbeiten kann, wenn das Thema sich über mehrere Wochen zieht?
Über eine zusammenfassung, die automatisch generiert wird? 
Über ein Projekt, dass man anlegen sollte? Dass ein Projekt anlegen dafür empfohlen wird? Also dass man sozusagen auf diese Possibility pointet, dass die infos aus der konversation nicht verloren gehen. (Einfach als kleiner Zusatz, für Leute die nicht wissen, dass die Möglichkeit existiert)