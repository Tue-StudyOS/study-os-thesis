# Tübingen Faculty Backbone

The official organizational structure of the University of Tübingen, used as the
**anti-SEO-bias baseline** for discovery: crawl these listing pages first to get the
real set of faculties → departments → chairs, *before* running live topic queries.
This stops the search from only surfacing SEO-strong pages and silently missing
chairs with a weak web presence.

- **Scope:** University of Tübingen, all 7 faculties + the Center for Islamic Theology.
- **Last checked:** 2026-06-27 (whole document, unless a row says otherwise).
- **Language:** Pages are German by default. Most have an English mirror reachable by
  inserting `/en/` after the host: `uni-tuebingen.de/en/fakultaeten/...`. The medical
  faculty uses a separate host (`medizin.uni-tuebingen.de`) with `/de/` and `/en/` paths.

## How the structure nests

The university is **two- or three-level**, so a single "faculty" URL rarely lists
individual chairs directly:

```text
Faculty (Fakultät)
  └─ Department (Fachbereich / Fach / Abteilung)
       └─ Chair / Institute / Seminar (Lehrstuhl / Institut / Seminar / Arbeitsbereich)
```

- The **big faculties** (Science, Humanities, Economics & Social Sciences) list
  *departments* on their backbone page; you must drill into each department's own
  page (often `.../<department>/forschung...` or `.../<department>/abteilung...`) to
  reach the actual chairs.
- The **smaller faculties** (Law, both Theologies, ZITh) list *chairs/Lehrstühle*
  more or less directly.
- The **medical faculty** is organized as clinics + institutes on the
  Universitätsklinikum host, not as classic Lehrstühle.

## Master index

| # | Listing page | What it lists |
|---|---|---|
| — | https://uni-tuebingen.de/fakultaeten/ | All 7 faculties + Center for Islamic Theology (top-level entry point) |

## Faculty backbone table

| Faculty | Official listing URL | Lang | How chairs are listed | Last checked |
|---|---|---|---|---|
| Mathematisch-Naturwissenschaftliche Fakultät (Science) | https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/ | DE | Lists 8 **Fachbereiche** (Biologie, Mathematik, Chemie, Pharmazie & Biochemie, Geowissenschaften, Physik, Informatik, Psychologie); drill into each for its chairs/Arbeitsbereiche. | 2026-06-27 ✓ resolved, lists departments |
| ↳ interfaculty institutes & centers (Science) | https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/interfakultaere-institute-und-zentren.html | DE | Cross-department institutes/centers (BCCN, IFIB, IMIT, IFIZ, …) not owned by a single Fachbereich. | 2026-06-27 |
| Philosophische Fakultät (Humanities) | https://uni-tuebingen.de/fakultaeten/philosophische-fakultaet/fachbereiche.html | DE | Lists 5 **Fachbereiche** (FB1 Altertums-/Kunstwissenschaften, FB2 Asien-Orient-Wissenschaften, FB3 Geschichtswissenschaft, FB4 Neuphilologie, FB5 Philosophie–Rhetorik–Medien), each with its Institute/Seminare. | 2026-06-27 ✓ resolved, lists departments |
| Wirtschafts- und Sozialwissenschaftliche Fakultät (Economics & Social Sciences) | https://uni-tuebingen.de/fakultaeten/wirtschafts-und-sozialwissenschaftliche-fakultaet/faecher/ | DE | Lists **Fächer** under two divisions: Sozialwissenschaften (Empirische Kulturwissenschaft, Erziehungswissenschaft, Politikwissenschaft, Soziologie, Sportwissenschaft, Hector-Institut, …) and Wirtschaftswissenschaft; drill into each Fach for chairs. | 2026-06-27 ✓ resolved, lists subjects |
| Juristische Fakultät (Law) | https://uni-tuebingen.de/fakultaeten/juristische-fakultaet/lehrstuehle-und-personen/ | DE | Lists **Lehrstühle** directly, grouped Bürgerliches Recht / Öffentliches Recht / Strafrecht, plus junior professorships & Lehrstuhlvertreter. | 2026-06-27 ✓ resolved, lists chairs |
| Medizinische Fakultät (Medicine) — institutes | https://www.medizin.uni-tuebingen.de/de/das-klinikum/einrichtungen/institute | DE | Lists **Institute** of the faculty/Universitätsklinikum (theoretical medicine, e.g. Hertie Institute for Clinical Brain Research). Separate host. | 2026-06-27 |
| Medizinische Fakultät (Medicine) — clinics | https://www.medizin.uni-tuebingen.de/de/das-klinikum/einrichtungen/kliniken | DE | Lists **Kliniken** (Innere Medizin I–…, Kinderheilkunde, etc.); clinical research groups live under these. Separate host. | 2026-06-27 |
| Evangelisch-Theologische Fakultät (Protestant Theology) | https://uni-tuebingen.de/fakultaeten/evangelisch-theologische-fakultaet/lehrstuehle-und-institute/ | DE | Lists **Lehrstühle & Institute** by theological discipline (Altes/Neues Testament, Kirchengeschichte, Systematische/Praktische Theologie, Religionswissenschaft & Judaistik), each with multiple chairs. | 2026-06-27 ✓ resolved, lists chairs |
| Katholisch-Theologische Fakultät (Catholic Theology) | https://uni-tuebingen.de/fakultaeten/katholisch-theologische-fakultaet/lehrstuehle/ | DE | Lists **Lehrstühle/Abteilungen**; companion Personenverzeichnis below. | 2026-06-27 |
| ↳ person directory (Catholic Theology) | https://uni-tuebingen.de/fakultaeten/katholisch-theologische-fakultaet/fakultaet/personen/ | DE | Full Personenverzeichnis (professors per chair). | 2026-06-27 |
| Zentrum für Islamische Theologie (ZITh) | https://uni-tuebingen.de/fakultaeten/zentrum-fuer-islamische-theologie/professuren/ | DE | Lists the **Professuren** (Glaubenslehre, Koranwissenschaften, Islamisches Recht, Hadithwissenschaften, Islamische Geschichte & Gegenwartskultur, Religionspädagogik incl. IIRF institute). Center, ranks alongside the 7 faculties. | 2026-06-27 |

## Department drill-down examples

When the backbone page lists only departments, follow the department's own page to
reach chairs. Pattern examples (not exhaustive):

| Department | Chair-level listing example |
|---|---|
| Informatik (Computer Science) | https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/informatik/forschung.html (research groups / Arbeitsbereiche) |
| Mathematik | https://uni-tuebingen.de/fakultaeten/mathematisch-naturwissenschaftliche-fakultaet/fachbereiche/mathematik/fachbereich/forschung-arbeitsbereiche/ |

General rule for a `Fachbereich` under `.../fachbereiche/<name>/`: look for a
`forschung`, `forschung-arbeitsbereiche`, `arbeitsbereiche`, `abteilungen`, or
`institute` sub-page to enumerate its chairs.

## Caveats

- **Drill-down required:** the science/humanities/economics backbone URLs list
  *departments*, not chairs — discovery must descend one more level per relevant
  department.
- **Medicine is on a different host** (`medizin.uni-tuebingen.de`) and is structured
  as clinics + institutes, not Lehrstühle; the `uni-tuebingen.de/fakultaeten/`
  index links out to it.
- **URL drift:** Tübingen's CMS occasionally renames paths (`.html` vs trailing
  slash, restructured sub-trees). Re-check dates and re-derive a dead link from the
  faculty's `fakultaeten/<faculty>/` root.
- **Interfaculty institutes & centers** (e.g. BCCN, Tübingen AI Center, Hertie
  Institute) span faculties and may not appear under a single faculty page — the
  Science interfaculty page above and `uni-tuebingen.de/forschung/zentren-und-institute/`
  are additional entry points.
