# Install — Thesis-Option Finder

**What this is.** A set of Markdown instruction files ("Agent Skills") that turn a capable
coding agent into a thesis-search advisor: it interviews you about your interests, then
searches the live web for University of Tübingen chairs or Baden-Württemberg companies that
fit, and hands you a map of real options with contact paths.

**Who it is for.** Students at the University of Tübingen looking for a Bachelor's or
Master's thesis, in any faculty. You do not need to be able to program — but you do need to
be able to install and run one of the agent clients below.

---

## Before you start

| You need | Why | How to check |
|---|---|---|
| A capable coding agent — **Claude Code**, **Codex**, or **Gemini CLI** | The skills are instructions *for an agent*. They do nothing on their own. | The client starts and answers a question |
| Agent Skills support in that client | The client must load `SKILL.md` folders | See the per-client step 2 below |
| **Web search / browsing enabled**, with quota to spare | Every run searches live. **One discovery run makes dozens of web calls** — expect it to be the most expensive thing you do that day, and expect it to take several minutes. | Ask your agent to search for something and see if it can |

There is no account, no database, no server, and nothing to configure. Nothing is installed
outside the skills folder.

**Install all the skills, not a subset.** `thesis-finder` calls the other skills by name and
they call each other. A partial install fails at the first hand-off.

---

## Step 1 — Get the files (all clients)

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
├── build-student-profile/
│   ├── SKILL.md
│   └── references/
├── thesis-finder/
│   └── SKILL.md
└── ...  (10 skills in total)
```

You copy the **contents** of that folder — the ten skill directories — not the folder
itself. That is what the `/*` in the next step is for.

---

## Step 2 — Put them where your client looks

### Claude Code

1. Create the personal skills directory if it does not exist:
   `mkdir -p ~/.claude/skills`
2. Copy **all** skill folders into it:
   `cp -r study-os-thesis-skills-vX.Y.Z/* ~/.claude/skills/`
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

## Step 3 — Run it

Start your agent in any directory and type exactly:

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
interview. It prefers `~/.claude/thesis-finder/session.md`; if your client cannot write
there it uses `./thesis-finder-session.md` in the directory you started the agent in, and
tells you which one it picked. Start the agent in the same directory next time, and type
`thesis-finder` again.

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Agent says it doesn't know `thesis-finder`, or just chats normally | Skill not loaded — the client was not restarted, or does not support Agent Skills | Restart the client. Then ask `which skills do you have?`. If nothing is listed, use the paste fallback in Step 2. |
| Agent finds *some* skills but breaks partway ("I don't have a skill called `discover-university-candidates`"), or the folder listing looks wrong | Wrong folder level, or a partial install | The path must be `<skills-dir>/thesis-finder/SKILL.md`, **not** `<skills-dir>/study-os-thesis-skills-vX.Y.Z/thesis-finder/SKILL.md`. Move the contents up one level and make sure **all** skill folders are there. |
| Results are thin, generic, or the agent says it cannot verify anything | No web access, or search quota exhausted | Confirm web search is enabled in your client and that you have quota left. These skills cannot work offline — everything they output is verified live, by design. |

---

## What it does *not* do

- It does not write your thesis.
- It does not guarantee an open topic. Every option must be confirmed with the chair or
  company directly — the tool tells you how, but you send the message.
- It is not an official University of Tübingen service.
- It does not store your data. Your profile lives in the conversation and in the session log
  on your own machine; nothing is uploaded anywhere by the skills themselves.

---

## Feedback

This is a non-commercial student course project. If you try it, we want to hear what broke:
open an issue at <https://github.com/Tue-StudyOS/study-os-thesis/issues>.
