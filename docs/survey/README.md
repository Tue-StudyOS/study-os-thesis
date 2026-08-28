# Thesis-Finder feedback survey (SoSci Survey)

A consent page, a short framing page, 17 Likert items, one duration question and two open
fields. About four minutes, which is the point: the skill itself already takes 20–40 minutes,
so the survey has to be something a student will still finish afterwards.

## Importing

One file, one import: **[`thesis-finder-ux-survey.xml`](thesis-finder-ux-survey.xml)**. It is
a whole *Rubrik* (section) holding the consent page, the framing page and all six questions.

In your project: **Questionnaire → Compose questionnaire / List of questions**, then import the
XML as a section. SoSci accepts a section or a single question per file — not a whole project,
which would wipe the target project instead of adding to it.

The section carries the ID `UX`, so variables come out as `UX01_01` … `UX08_01` (`UX02` is
the display-only instructions page and produces no variable). If your
project already uses `UX`, SoSci assigns a free ID and the numbering below shifts with it.

SoSci only imports XML it wrote itself and the format is undocumented, so this file was built
against real SoSci output: a [question export](https://github.com/mluenich/sosci_survey), a
[multi-section import template written by SoSci's own author](https://github.com/BurninLeo/ExposureResearchTools/blob/master/resources/sosci.template.xml),
and two full project exports for the free-text question shape. It validates against
[`doctype.survey.dtd`](https://www.soscisurvey.de/templates/doctype.survey.dtd).

### Two things to do after importing

1. **Check that IP storage is off** — the consent text claims it is. Project settings →
   *Datenschutz / privacy*; SoSci does not store IPs by default, but the claim needs to be
   true for your project.
2. **Make consent actually gate the survey.** The import gives you the question, not the
   logic: put `UX01` alone on the first page and add a filter so that anyone answering
   "I do not agree" goes to the end instead of on to `UX02`.

The two free-text questions import as single-line fields. If you want boxes, switch them to
multi-line in the question editor after importing — that setting does not survive the export
format.

## What each question is for

Item order inside the three scale questions is **randomised** (`<order>random</order>`), so the
numbering below is the variable index, not what a participant sees. Scale is 1 = strongly
disagree … 5 = strongly agree throughout.

### UX01 — Informed consent

Single choice, 1 = agree, 2 = do not agree, forced answer. The consent text sits in the
question's `<lead>` as HTML, so it renders above the two options; edit it there.

### UX02 — Before you begin

Display only, no variable. States the survey's one prerequisite — that the respondent has
already run the tool — and links to [INSTALL.md](../../INSTALL.md) and the releases page for
anyone who has not. It deliberately invites people whose run broke off to answer anyway
rather than drop out, since a failed run is a result too. Put it on its own page after
consent.

### UX03 — Did it move their thinking?

The project's actual claim is that a student ends up with a sharper idea of what fits them,
whether or not they contact anyone. This is the question that tests it.

| # | Item | Note |
|---|---|---|
| 1 | Since the session I have thought about my thesis more concretely than before. | |
| 2 | I have a clearer idea of what kind of thesis would fit me. | |
| 3 | The session made me reconsider something I thought I wanted. | changed mind = success |
| 4 | My idea of my thesis is just as vague now as it was before. | **reverse** |
| 5 | I came across directions or research groups I would not have found on my own. | |
| 6 | Everything it showed me I already knew about. | **reverse** |

### UX04 — Were the results any good?

Has a residual option (`I cannot judge this`, coded 0 — treat as missing, not as a low score).

| # | Item | Note |
|---|---|---|
| 1 | The suggestions fit what I am actually interested in. | |
| 2 | The suggestions were concrete enough to act on. | |
| 3 | Most suggestions felt generic — they could have gone to any student. | **reverse** |
| 4 | I would trust the information enough to write to one of them. | |
| 5 | Please select "disagree" here … | **attention check**, expected answer 2 |
| 6 | I intend to contact at least one of the people or places suggested. | behavioural intention |

### UX05 — How was it to sit through?

| # | Item | Note |
|---|---|---|
| 1 | The questions I was asked were relevant to me. | |
| 2 | It felt like it understood what I actually care about, not just my keywords. | the "connection" item |
| 3 | Answering all the questions felt tedious. | **reverse** |
| 4 | The time it took was worth what I got out of it. | pair with UX06 |
| 5 | I would recommend it to a friend who is looking for a thesis topic. | |

### UX06 — Duration

Single item, 1 = under 15 min … 5 = over an hour. Only interesting crossed with `UX05_04`
("worth it") — a long session that felt worth it is a different result from a short one that
did not.

### UX07 / UX08 — Open feedback

- What was the single most useful thing about it?
- What annoyed you, or what did it get wrong?

## Careless-responding checks

Four reverse-keyed items (`UX03_04`, `UX03_06`, `UX04_03`, `UX05_03`) and one
instructed-response item (`UX04_05`). Before analysing, **recode the four reverse items**
(`6 - x`) and drop or flag respondents who agree both with a statement and with its reversal,
or who miss the attention check. With n this small, flag rather than drop, and say in the
write-up how many were flagged.

Two of the reverse items are worded as flat negations ("just as vague as before"), the form
most easily misread as positive by someone skimming. That is the intended trap, but it also
means a single failed reverse item is weak evidence on its own — the attention check is the
harder criterion.
