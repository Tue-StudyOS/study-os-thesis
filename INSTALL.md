# Install — Thesis-Option Finder

**What this is.** A set of Markdown instruction files ("Agent Skills") that turn a capable
coding agent into a thesis-search advisor: it interviews you about your interests, then
searches the live web for University of Tübingen chairs or Baden-Württemberg companies that
fit, and hands you a map of real options with contact paths.

**Who it is for.** Students at the University of Tübingen looking for a Bachelor's or
Master's thesis, in any faculty. You do not need to be able to program — Routes A and B below
are a file upload and some copy-paste, in Claude, ChatGPT, or Gemini.

---

## Before you start

| You need | Why | How to check |
|---|---|---|
| An AI assistant — **Claude**, **ChatGPT**, **Gemini**, or a terminal agent | These are instructions *for an assistant*. They do nothing on their own. | Pick a route below |
| **Web search / browsing enabled**, with quota to spare | Every run searches live. **One discovery run makes dozens of web calls** — expect it to be the most expensive thing you do that day, and expect it to take several minutes. | Ask your agent to search for something and see if it can |

There is no account, no database, no server, and nothing to configure. Nothing is installed
outside the skills folder.

---

## Pick your route

| | Route A — Claude app | Route B — ChatGPT, Gemini, or any chat | Route C — Claude Code, Codex, Gemini CLI |
|---|---|---|---|
| For | Claude Pro/Max users | Anyone else, including free ChatGPT and Gemini | People already working in a terminal agent |
| Install | Upload **one zip** | Attach **one file**, paste one text block | One command, or copy **ten folders** into a directory |
| Terminal needed | No | No | Yes |

All three run the same searches and produce the same output. Whichever you pick,
**read "Never type it all again" below before your first run** — that is the part that
decides whether you have to repeat the interview next month.

---

# Route A — Claude app (no terminal)

Custom skills in the Claude app need a **Pro, Max, Team, or Enterprise** plan, with **code
execution and file creation** switched on.

1. Download **`thesis-finder-app-vX.Y.Z.zip`** from
   <https://github.com/Tue-StudyOS/study-os-thesis/releases/latest>. **Do not unpack it** —
   the zip is what you upload.
2. In Claude, open **Settings** and enable **code execution and file creation**, and **web
   search**. Both are under the capabilities/features section; the exact wording of the menu
   changes from time to time.
3. Still in Settings, find **Skills**, add a skill, and pick the zip you downloaded.
4. **Create a project** for your thesis search (see "Never type it all again").
5. Open a chat inside that project and type `thesis-finder`. Continue at **Run it**.

The single zip contains the entry-point skill and everything it hands off to, so there is
nothing else to upload.

---

# Route B — ChatGPT, Gemini, or any other assistant

ChatGPT and Gemini do not load Agent Skills. They do let you build a container — a Project,
a Custom GPT, a Gem — that holds an instructions text and a few files. The portable edition
is built for exactly that: **one file, plus one block of text to paste.**

1. Download **`thesis-finder-portable-vX.Y.Z.md`** from
   <https://github.com/Tue-StudyOS/study-os-thesis/releases/latest>.
2. Create the container:
   - **ChatGPT:** a **Project** (best — you can add files to it later), or a **Custom GPT**.
   - **Gemini:** a **Gem**.
   - **Claude:** a **Project**, if you would rather not install the skill from Route A.
3. Attach `thesis-finder-portable-vX.Y.Z.md` to it as a knowledge or project file.
4. Open the file, copy the block between `-----BEGIN INSTRUCTIONS-----` and
   `-----END INSTRUCTIONS-----`, and paste it into the container's instructions field. (It is
   also shipped separately as `thesis-finder-portable-instructions-vX.Y.Z.txt` if that is
   easier.) It is under 3000 characters, so it fits every instructions box.
5. Make sure web search is on for that assistant.
6. Start a chat **inside the container** and type `thesis-finder`. Continue at **Run it**.

**Why one file and not ten.** ChatGPT and Gemini cap a container at roughly ten knowledge
files, and ChatGPT caps instructions at 8000 characters. The full instruction set is far
larger than that, so it travels as a single document with named sections, and the pasted
block tells the assistant how to navigate it.

**Quick try without any setup:** attach the file to a normal chat and type `thesis-finder`. It
works, but nothing is remembered once that chat ends.

---

# Route C — Claude Code, Codex, Gemini CLI

**Install all ten skills, not a subset.** `thesis-finder` calls the other skills by name and
they call each other. A partial install fails at the first hand-off. (Routes A and B have no
such trap — everything travels in one artifact.)

## Step 0 — The one-command shortcut (optional)

If you have **Node 22.20 or newer**, one command installs all ten skills into the client you
use — Claude Code, Codex, Cursor, OpenCode and some seventy others:

```bash
npx skills@latest add Tue-StudyOS/study-os-thesis --skill '*' --agent claude-code -g
```

- `--skill '*'` is **not optional**. Without it you are asked to pick from a list, and any
  pick short of all ten hits the hand-off trap above.
- `--agent` names your client — `claude-code`, `codex`, `cursor`, … Leave the flag out and it
  asks you.
- `-g` installs for your whole account (`~/.claude/skills/`). Drop it and the skills land in
  the current folder only (`./.claude/skills/`), which is what you want if you keep one
  directory per thesis search.
- The command tracks `main`. To pin a release instead, give the full URL with the tag in it:

  ```bash
  npx skills@latest add https://github.com/Tue-StudyOS/study-os-thesis/tree/skills-v2.1.0 --skill '*' --agent claude-code -g
  ```

  The shorter `repo@tag` form is accepted but the tag is ignored, so you silently get `main`.

Restart your client afterwards and continue at **Run it**.

`skills` is a third-party installer made by Vercel, not part of this project. It downloads
this repository and copies the ten folders from `skills/` into your client's skills
directory — by hand, that is exactly Steps 1 and 2 below, and the result is the same files.
If you would rather not run an unfamiliar installer, or you have no Node, just start at
Step 1.

---

## Step 1 — Get the files

Download the latest release archive from
<https://github.com/Tue-StudyOS/study-os-thesis/releases/latest> — either
`study-os-thesis-skills-vX.Y.Z.zip` or `study-os-thesis-skills-vX.Y.Z.tar.gz` — and unpack
it:

```bash
# .tar.gz — works on macOS and Linux out of the box
tar xzf study-os-thesis-skills-vX.Y.Z.tar.gz

# .zip — if `unzip` is not installed (it often isn't on a bare Linux/WSL box):
python3 -m zipfile -e study-os-thesis-skills-vX.Y.Z.zip .
```

Either way you get **one folder named after the version**, containing one directory per
skill:

```text
study-os-thesis-skills-vX.Y.Z/     ← this wrapper folder is NOT what you copy
├── INSTALL.md                     ← this guide; leave it here
├── build-student-profile/
│   ├── SKILL.md
│   └── references/
├── thesis-finder/
│   └── SKILL.md
└── ...  (10 skills in total)
```

You copy the **ten skill directories** out of that folder — not the folder itself, and not
`INSTALL.md`. That is what the `*/` in the next step is for: the trailing slash matches
directories only, so this guide stays behind.

---

## Step 2 — Put them where your client looks

### Claude Code

1. Create the personal skills directory if it does not exist:
   `mkdir -p ~/.claude/skills`
2. Copy **all** skill folders into it — the trailing slash on `*/` copies the ten
   directories and leaves `INSTALL.md` behind:
   `cp -r study-os-thesis-skills-vX.Y.Z/*/ ~/.claude/skills/`
3. Confirm the layout is `~/.claude/skills/thesis-finder/SKILL.md` — one folder per skill,
   each with its own `SKILL.md`. If you see `~/.claude/skills/study-os-thesis-skills-vX.Y.Z/`,
   you copied the wrapper folder instead of its contents; move them up one level.
4. Restart Claude Code so it picks up the new skills.
5. Verify: ask `which skills do you have?` — `thesis-finder` should be listed.

### Codex

1. Create the skills directory your Codex install is configured to read
   (`~/.codex/skills` unless you changed it): `mkdir -p ~/.codex/skills`
2. Copy all skill folders into it, same as above — one folder per skill, `SKILL.md` directly
   inside each.
3. Restart Codex.
4. Verify: ask `which skills do you have?`.

If your Codex version does not read a skills directory, use the fallback below — the skills
are plain Markdown and work when pasted in.

### Gemini CLI / other clients

Any client that loads Agent Skills works the same way: copy the skill folders into whatever
directory that client reads, keeping the `<skill-name>/SKILL.md` layout.

**Fallback for clients without skill support:** open
`thesis-finder/SKILL.md` and paste its full contents into the chat as your first message,
followed by "follow these instructions". You lose automatic routing to the other skills, so
paste `find-university-chairs/SKILL.md` (or `find-company-thesis-options/SKILL.md`) when the
conversation reaches that step.

---

# Run it

Start your agent — or open a new chat in the Claude app — and type exactly:

```
thesis-finder
```

That is the whole first prompt. The skill takes over from there: it explains what it does,
then asks you one question at a time to build a profile of your interests, methods, domain,
preferred thesis style, skills, and no-gos. Answer as precisely as you can — vague answers
produce vague results — but there is no minimum. When the profile is complete it asks
whether you want to search university chairs, companies, or both.

**It will take a while.** The search phase makes many live web requests and verifies what it
finds. Let it run.

---

# Never type it all again

Finding a thesis takes weeks, not one afternoon. The interview that produces your profile is
the expensive part — the searching can always be repeated, your answers cannot, and nobody
wants to reconstruct them from memory a month later.

So the advisor writes a **session file**: your profile, what was already searched, what you
ruled out, and how your own thinking about the thesis changed. It hands you that file
**twice** — once the moment the interview is done, before any searching, and again at the end
of the run. The early one exists precisely because searches are long and tabs get closed.

**What you have to do: put that file somewhere the next chat can see it.**

| Where you run it | Where the session file goes | Next time |
|---|---|---|
| Claude project (Route A or B) | The project's knowledge base | New chat in the same project |
| ChatGPT project (Route B) | The project's files | New chat in the same project |
| ChatGPT Custom GPT (Route B) | Edit the GPT, add it to its knowledge | Any chat with that GPT |
| Gemini Gem (Route B) | Edit the Gem, add it to its knowledge | Any chat with that Gem |
| Claude Code / Codex / Gemini CLI (Route C) | Nothing to do — written to disk automatically | Start the agent in the same directory |
| A plain chat, no container | Nowhere. Keep the file and attach it by hand | Attach it to your first message |

The advisor checks all of these at the start of every run before it asks you anything: the
files attached to the conversation, the container's knowledge, and whatever it remembers
about you. If it finds a session file it tells you which one it used and confirms your
profile back to you in a sentence or two — correct it there if something has changed.

**Route C** is the only one where this is fully automatic: `thesis-finder` prefers
`~/.claude/thesis-finder/session.md`, falls back to `./thesis-finder-session.md` in the
directory you started the agent in, and tells you which one it picked.

**One habit is enough:** when the advisor hands you a file, drop it into your project. That
single step is the difference between continuing and starting over.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent says it doesn't know `thesis-finder`, or just chats normally | Skill not loaded — the upload did not finish, the client was not restarted, or it does not support Agent Skills | Restart the client, then ask `which skills do you have?`. If nothing is listed, use Route B instead — it needs no skill support at all. |
| **Route A:** the upload is rejected, or the skill appears with the wrong name | The wrong file was uploaded, or it was unpacked first | Upload `thesis-finder-app-vX.Y.Z.zip` as downloaded. The ten-folder `study-os-thesis-skills-vX.Y.Z.zip` is for Route C and will not upload as one skill. |
| **Routes A/B:** it asks the full interview again on a later visit | The chat was not started inside the project/GPT/Gem, or the session file was never added to it | Open a chat inside the container holding your session file and type `thesis-finder` again. If no session file was ever saved, the interview has to be redone. |
| **Route B:** it answers from general knowledge instead of following the instructions | The document was attached but the instructions block was never pasted in | Paste the block from `-----BEGIN INSTRUCTIONS-----` into the container's instructions field. Without it the assistant has no reason to open the document. |
| **Route C:** agent finds *some* skills but breaks partway ("I don't have a skill called `discover-university-candidates`"), or the folder listing looks wrong | Wrong folder level, or a partial install | The path must be `<skills-dir>/thesis-finder/SKILL.md`, **not** `<skills-dir>/study-os-thesis-skills-vX.Y.Z/thesis-finder/SKILL.md`. Move the contents up one level and make sure **all** skill folders are there. |
| **Route C:** `npx skills` refuses to start, or warns `EBADENGINE` | Node is older than 22.20, or missing entirely | Skip Step 0 and install by hand from Step 1 — same files, no Node needed. |
| Results are thin, generic, or the agent says it cannot verify anything | No web access, or search quota exhausted | Confirm web search is enabled in your client and that you have quota left. These skills cannot work offline — everything they output is verified live, by design. |

---

## What it does *not* do

- It does not write your thesis.
- It does not guarantee an open topic. Every option must be confirmed with the chair or
  company directly — the tool tells you how, but you send the message.
- It is not an official University of Tübingen service.
- It does not store your data. The skills have no database and no server: your profile
  lives in the conversation and in the session log, and the skills send it nowhere. Your
  conversation itself is of course handled by whichever agent provider you run it on, under
  their terms — that is true of anything you type into that agent.

---

## Tell us how it went

This is a non-commercial student course project, and the only way we find out whether it
actually helps anyone is if the people who run it say so. When your session is over, please
fill in our short feedback survey — about four minutes:

**<https://www.soscisurvey.de/thesis-skill/>**

**Answer it even if the run went badly**, or you broke it off halfway, or the suggestions
were useless. A failed run is a result too, and those are the answers that change the tool.
The survey is anonymous and you can stop at any point.

If something is broken in a way that needs fixing rather than measuring, open an issue at
<https://github.com/Tue-StudyOS/study-os-thesis/issues>.
