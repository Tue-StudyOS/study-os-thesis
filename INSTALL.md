# Install — Thesis-Option Finder

**What this is.** A set of Markdown instruction files ("Agent Skills") that turn a capable
coding agent into a thesis-search advisor: it interviews you about your interests, then
searches the live web for University of Tübingen chairs or Baden-Württemberg companies that
fit, and hands you a map of real options with contact paths.

**Who it is for.** Students at the University of Tübingen looking for a Bachelor's or
Master's thesis, in any faculty. You do not need to be able to program: Route A below is a
single file upload in the Claude app.

---

## Before you start

| You need | Why | How to check |
|---|---|---|
| An agent that loads Agent Skills — the **Claude app**, **Claude Code**, **Codex**, or **Gemini CLI** | The skills are instructions *for an agent*. They do nothing on their own. | See Route A or Route B below |
| **Web search / browsing enabled**, with quota to spare | Every run searches live. **One discovery run makes dozens of web calls** — expect it to be the most expensive thing you do that day, and expect it to take several minutes. | Ask your agent to search for something and see if it can |

There is no account, no database, no server, and nothing to configure. Nothing is installed
outside the skills folder.

---

## Pick your route

| | Route A — Claude app | Route B — Claude Code / Codex / Gemini CLI |
|---|---|---|
| For | Anyone. No terminal needed. | People who already work in a terminal agent. |
| Install | Upload **one file** | Copy **ten folders** into a directory |
| Picking up weeks later | You re-attach the session file yourself | Automatic — the session log stays on disk |

Route A is the short path and the one to use if you are unsure. Both run the same
searches and produce the same output.

---

# Route A — Claude app (no terminal)

You need a Claude plan that includes Skills, and the Skills capability switched on.

1. Download **`thesis-finder-app-vX.Y.Z.zip`** from
   <https://github.com/Tue-StudyOS/study-os-thesis/releases/latest>. Do not unpack it.
2. In the Claude app, open **Settings → Capabilities** and make sure **Skills** is enabled,
   along with **web search**.
3. Under **Skills**, choose to upload a skill and pick the zip you just downloaded.
4. Start a new chat and type `thesis-finder`. Continue at **Run it** below.

That is the whole install. The single zip contains the entry-point skill and everything it
hands off to, so there is nothing else to upload.

**Coming back later.** The Claude app does not keep files between conversations. At the end
of a run, ask for the session file and save it. Next time, attach that file to your first
message and type `thesis-finder` — the search resumes without repeating the interview.

---

# Route B — Claude Code, Codex, Gemini CLI

**Install all ten skills, not a subset.** `thesis-finder` calls the other skills by name and
they call each other. A partial install fails at the first hand-off.

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

### Coming back later

`thesis-finder` writes a session log so you can resume weeks later without repeating the
interview.

- **Route B:** it prefers `~/.claude/thesis-finder/session.md`; if your client cannot write
  there it uses `./thesis-finder-session.md` in the directory you started the agent in, and
  tells you which one it picked. Start the agent in the same directory next time, and type
  `thesis-finder` again.
- **Route A:** nothing survives the end of a conversation, so save the session file when the
  run ends and attach it to your first message next time.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent says it doesn't know `thesis-finder`, or just chats normally | Skill not loaded — the upload did not finish, the client was not restarted, or it does not support Agent Skills | Restart the client, then ask `which skills do you have?`. If nothing is listed, use the paste fallback at the end of Route B Step 2. |
| **Route A:** the upload is rejected, or the skill appears with the wrong name | The wrong file was uploaded, or it was unpacked first | Upload `thesis-finder-app-vX.Y.Z.zip` as downloaded. The ten-folder `study-os-thesis-skills-vX.Y.Z.zip` is for Route B and will not upload as one skill. |
| **Route A:** it asks the full interview again on a later visit | The session file was not attached | Attach the session file you saved to your first message, then type `thesis-finder`. If you did not save one, the interview has to be redone. |
| **Route B:** agent finds *some* skills but breaks partway ("I don't have a skill called `discover-university-candidates`"), or the folder listing looks wrong | Wrong folder level, or a partial install | The path must be `<skills-dir>/thesis-finder/SKILL.md`, **not** `<skills-dir>/study-os-thesis-skills-vX.Y.Z/thesis-finder/SKILL.md`. Move the contents up one level and make sure **all** skill folders are there. |
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

## Feedback

This is a non-commercial student course project. If you try it, we want to hear what broke:
open an issue at <https://github.com/Tue-StudyOS/study-os-thesis/issues>.
