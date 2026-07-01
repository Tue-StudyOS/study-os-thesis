#!/usr/bin/env python3
"""Run an end-to-end eval for the external company thesis workflow.

The eval is intentionally evidence-fixture based. A real student may spend
around an hour with the advisor before generation; this runner represents that
long profile phase as a scripted transcript, then performs only one live
generation turn and one live judge turn. That keeps the eval reliable and avoids
timeouts while still testing whether generation uses a nuanced profile.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT_DIR = Path("/private/tmp/study-os-thesis-external-thesis-e2e-eval")
MAX_TURNS = 24
TIMEOUT = 300
# Timeout guard: one live generation turn and one live judge turn.


INITIAL_USER = (
    "Hi, ich bin im 6. Semester Informatik und suche eine Bachelorarbeit. "
    "Mein starker Fokus ist Reinforcement Learning und autonome Systeme. "
    "Ich moechte nicht in Medizin oder allgemeiner Robotik arbeiten, sondern "
    "nur an Auto-/Automotive-bezogenen Themen. Kannst du mir passende "
    "Bachelorarbeiten bei Unternehmen und an der Uni suchen?"
)


USER_PROFILE = """
Student persona:
- 6th semester computer science bachelor student at the University of Tuebingen.
- Thesis level: bachelor thesis in computer science.
- Strongest interests: reinforcement learning, autonomous driving, decision making, planning, simulation, control for vehicle-related systems.
- Explicit no-gos: medicine, medical AI, hospital data, general robotics, manipulation, warehouse robots, drones, pure embedded work without learning.
- Wants only car-related or automotive/autonomous-driving contexts.
- Has taken ML intro, algorithms/data structures, statistics, software engineering, and an autonomous systems seminar.
- Practical skills: Python, PyTorch basics, NumPy/pandas, gymnasium-style RL environments, basic Linux/git, some C++ from university.
- Project evidence: implemented tabular Q-learning and DQN for small simulated driving/gridworld tasks; tuned reward functions; evaluated success rate, collisions, off-road cases, training curves, and seed stability; wrote a short report with plots.
- Thesis style: practical/experimental, simulation-heavy, clear evaluation metrics; not pure theory and not a pure literature review.
- Work constraints: based around Tuebingen/Stuttgart; can commute within about 80 km; prefers hybrid but can do on-site for a strong automotive topic.
- Sectors to exclude: medicine/healthcare, defense, general robotics companies unrelated to vehicles.
- Technologies to avoid: heavy ROS hardware bring-up, physical robot setup, medical data pipelines.
Disclosure:
- Start by introducing yourself with the initial user message.
- The profile conversation is scripted in this eval as a one-hour-equivalent
  advising baseline so the live model call can focus on generation quality
  without timing out.
- Do not invent company postings, supervisors, or web results.
"""


EVIDENCE_FIXTURE = """
Evidence fixture for the generation phase. Treat these as the only public
evidence available in this eval. Do not invent additional openings.

University/chair evidence:
1. University of Tuebingen, Autonomous Learning group. Public page snippet:
   research areas include autonomous learning, reinforcement learning, model-
   based control, robot learning, and learning from interaction. Evidence date:
   2026-06-29. Caveat: no advertised bachelor thesis opening in the snippet.
2. University of Tuebingen / AI Center, machine learning for sequential
   decision-making seminar page. Public snippet: topics include reinforcement
   learning, planning under uncertainty, simulation benchmarks, and evaluation.
   Evidence date: 2026-06-29. Caveat: seminar page, not a thesis posting.
3. University of Stuttgart, Institute of Automotive Engineering style public
   snippet: autonomous driving, ADAS, simulation, trajectory planning, and
   evaluation appear as research areas. Evidence date: 2026-06-29. Caveat:
   outside the student's home university, supervision process must be verified.

Company/external evidence:
1. Mercedes-Benz Careers public snippet, provider `company_careers`:
   "Abschlussarbeit / Bachelorarbeit: Reinforcement Learning for automated
   driving simulation", Stuttgart/Sindelfingen, hybrid possible, Python and
   simulation, evaluation of driving scenarios. Visible posting date unclear.
   Evidence tier B because only the snippet is available in this eval.
   Source URL: https://example.invalid/mercedes-bachelor-rl. Mirror URL:
   none found in fixture.
2. StepStone public snippet, provider `stepstone`:
   "Bachelorarbeit: Safe reinforcement learning in autonomous driving
   simulation", Stuttgart, Python, simulation, scenario evaluation, posted date
   unclear. Evidence tier B because only the snippet is available in this eval.
   Source URL: https://example.invalid/stepstone-bachelor-safe-rl. Mirror URL:
   https://example.invalid/company-careers-safe-rl.
3. Bosch Careers public snippet, provider `company_careers`:
   "Masterarbeit: Trajectory prediction for automated driving", Stuttgart,
   Python/PyTorch, perception-heavy camera data. Visible posting date unclear.
   Evidence tier B. Caveat: master thesis and perception-heavy, likely not fit.
   Source URL: https://example.invalid/bosch-master-trajectory.
4. Generic Robotics GmbH LinkedIn snippet, provider `linkedin_public`:
   "Working student robotics software, ROS, warehouse robots", Stuttgart.
   Evidence tier B. Caveat: working-student role, not a thesis, and conflicts
   with no general robotics.
   Source URL: https://example.invalid/linkedin-working-student-robotics.
5. Medical AI Mobility Lab StepStone snippet, provider `stepstone`:
   "Bachelorarbeit Deep Learning for medical time series", remote. Evidence
   tier C. Caveat: medicine sector, excluded.
   Source URL: https://example.invalid/stepstone-medical-ai.
6. StepStone provider count, provider `stepstone`:
   StepStone listing page says many "Bachelorarbeit Stuttgart" results exist,
   but no visible result text is available for this fixture item. Evidence tier
   C. Caveat: provider count only; it is discovery evidence, not a candidate.

Required generated output:
- A ranked university/chair lane with evidence and caveats.
- A ranked external company thesis lane with included and excluded results.
  Every company candidate must include provider label, source URL, mirror URL
  when available, evidence tier, visible date, access date, and exact exclusion
  reason when excluded.
- At least two proposal sketches grounded in the student profile and the
  evidence: one university-led proposal and one external/company-led proposal.
- Each proposal must include working title, research question, methods/data/
  evaluation, fit rationale, feasibility risks, and first validation step.
- Each proposal must label evidence status: external posting/snippet-derived
  lead, university research-area conversation starter, or hybrid/external
  feasibility hypothesis.
- Because the profile is Bachelor-level, the output must not generate or rank
  Masterarbeit-only leads as eligible proposals.
- Werkstudent/working-student roles must be excluded completely from the
  external thesis lane even if the stack looks relevant.
- Provider counts must not be ranked as postings. If no eligible company
  postings survive in another run, the assistant must say "no qualifying
  results after searched providers" rather than claiming no postings exist
  anywhere.
"""


ASSISTANT_SYSTEM = f"""
You are the thesis-advising agent for this repository. Use Codex-native skill
discovery and the local Agent Skills. The relevant workflow is:
build a deep student profile first, then use find-university-chairs,
find-linkedin-company-theses, match-thesis-advisors, and
generate-thesis-directions as needed.

The transcript already contains a one-hour-equivalent deep advising profile.
Do not ask another profile question. Move directly into the generation phase:
produce the university/chair lane, the external/company thesis lane, and
proposal sketches.
In this eval, use only the following fixture evidence for Uni and external
company matching:

{EVIDENCE_FIXTURE}

Fixture-only mode: do not mention unavailable skills, unavailable web search,
or tool limitations. Just state that the output is based on the provided
fixture evidence.

Return only the next assistant message.
Do not append judge labels, "Evaluation JSON:", tool commentary, or unfinished
sections to the assistant message.
"""


SCRIPTED_PROFILE_TURNS = [
    {"role": "user", "content": INITIAL_USER},
    {
        "role": "assistant",
        "content": (
            "Verstanden. Bevor ich suche, brauche ich dein Profil. Was hat dein "
            "Interesse an RL fuer autonome Fahrzeuge konkret ausgeloest?"
        ),
    },
    {
        "role": "user",
        "content": (
            "Mich hat das durch ein Uni-Projekt und ein Seminar gepackt. Ich "
            "habe tabular Q-Learning und spaeter eine einfache DQN-Variante fuer "
            "simulierte Driving-/Gridworld-Aufgaben implementiert. Spannend "
            "waren Reward Design, Zustandsrepraesentation, Decision-Making, "
            "Planning, Spurwechsel, Kreuzungen und Interaktion in Simulation."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "Das klingt nach Automotive-RL in Simulation. Welche Tools und "
            "Frameworks kannst du praktisch nutzen?"
        ),
    },
    {
        "role": "user",
        "content": (
            "Python, NumPy/pandas und einfache PyTorch-Modelle. Ich kann kleine "
            "DQN-Modelle nachvollziehen und anpassen, Gymnasium-artige "
            "Environments nutzen, Training Loops bauen und Metriken/Plots "
            "auswerten. Stable-Baselines3 nur oberflaechlich. CARLA/SUMO kenne "
            "ich noch nicht praktisch, highway-env waere passend. Linux/Git okay, "
            "Docker wenig, C++ nur Uni-Grundlagen."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "Was war dein groesstes technisches Projekt oder deine wichtigste "
            "praktische Erfahrung?"
        ),
    },
    {
        "role": "user",
        "content": (
            "Kein Automotive-Praktikum und kein Werkstudentenjob in ML. Im "
            "Uni-Projekt habe ich Training Loop, Environment-Anbindung, Rewards, "
            "Evaluation ueber Seeds, Erfolgsrate, Kollisionen, Off-road-Faelle "
            "und einen kurzen Bericht mit Grafiken selbst gemacht. Dazu ein "
            "Software-Engineering-Teamprojekt mit Python-Backend, Tests, Git und CI."
        ),
    },
    {
        "role": "assistant",
        "content": "Welche Art Bachelorarbeit passt zu dir und was sind klare No-gos?",
    },
    {
        "role": "user",
        "content": (
            "Praktisch-empirische ML/RL-Arbeit mit Experimenten, Ablations zu "
            "Rewards/Observations, Safety/Fehlverhalten und klaren Metriken. "
            "Keine reine Theorie, keine Literaturarbeit, keine Medizin, keine "
            "allgemeine Robotik, keine Manipulation, keine Sensorik-/Perception-"
            "Schwerpunktarbeit, kein schweres ROS/Hardware-Bringup."
        ),
    },
    {
        "role": "assistant",
        "content": "Welche Uni, Region und Arbeitsform soll ich fuer die Suche ansetzen?",
    },
    {
        "role": "user",
        "content": (
            "Uni Tuebingen, Informatik B.Sc., 6. Semester. Externe "
            "Unternehmensarbeit ist interessant, wenn ein Uni-Betreuer passt "
            "und es wissenschaftlich genug ist. Raum Tuebingen/Stuttgart bis "
            "ca. 80 km, hybrid bevorzugt, aber fuer ein sehr gutes Automotive-"
            "Thema auch mehr Praesenz."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "Damit ist die Suchregion klar. Welche Kurse, Seminare oder "
            "Assignments waren fachlich am wichtigsten, und was mochtest oder "
            "mochtest du daran nicht?"
        ),
    },
    {
        "role": "user",
        "content": (
            "Wichtig waren Machine Learning Einfuehrung, Algorithmen und "
            "Datenstrukturen, Statistik, Software Engineering und das Seminar "
            "Autonome Systeme. In ML mochte ich Generalisierung und Evaluation, "
            "aber nicht reine Standardklassifikation. Algorithmen half bei "
            "Planning/Suche, aber reine Theorie will ich vermeiden. Statistik "
            "passt fuer Seeds, Konfidenz und Methodenvergleich. Software "
            "Engineering hilft fuer sauberen Code und Tests. Im Seminar mochte "
            "ich RL, Simulation und Entscheidungsfindung, nicht Hardware oder "
            "allgemeine Manipulationsrobotik."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "Welche Tradeoffs waeren dir wichtig: sichere, klar betreute Arbeit "
            "vs. offenes Forschungsthema; bekannte Tools vs. neue Tools; "
            "Uni-led vs. Company-led?"
        ),
    },
    {
        "role": "user",
        "content": (
            "Ich will lieber eine klar eingegrenzte Arbeit mit vorhandener "
            "Simulation oder Baseline, die ich systematisch verbessere und "
            "evaluiere. Neue Tools sind okay, wenn sie nicht den ganzen Scope "
            "auffressen. Uni-led waere sicherer, company-led waere spannend, "
            "wenn es wirklich Bachelorarbeit ist und wissenschaftlich bleibt. "
            "Ich will nicht am Ende nur Unternehmenssoftware bauen."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "Was wuerde die Thesis fuer dich am Ende erfolgreich machen, und "
            "welche Risiken sollten die Vorschlaege vermeiden?"
        ),
    },
    {
        "role": "user",
        "content": (
            "Erfolgreich waere: klare Forschungsfrage, reproduzierbare "
            "Experimente, gute Plots, ein paar sinnvolle Ablations und ein "
            "ehrliches Kapitel zu Failure Cases. Vermeiden moechte ich: riesige "
            "Simulator-Installation, unklare Daten/IP-Situation, Thema zu gross "
            "fuer Bachelor, viel C++/ROS, oder Automotive nur als Buzzword ohne "
            "RL/Planning-Kern."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "Gibt es formale oder praktische Randbedingungen wie Startzeit, "
            "Sprache, Betreuung und Dokumente?"
        ),
    },
    {
        "role": "user",
        "content": (
            "Start waere in den naechsten Monaten realistisch. Deutsch oder "
            "Englisch ist okay. Bei externer Arbeit brauche ich vermutlich "
            "Uni-Betreuung und ein Thema, das als Informatik-Bachelorarbeit "
            "zaehlt. Transcript oder Projektbericht koennte ich spaeter "
            "bereitstellen, aber fuer die erste Auswertung reicht das Profil."
        ),
    },
    {
        "role": "assistant",
        "content": (
            "Kurzprofil: Bachelor Informatik Tuebingen, Automotive-only RL/"
            "Planning in Simulation, Python/PyTorch/Gymnasium, Evaluation ueber "
            "Seeds und Safety-Metriken, klare No-gos gegen Medizin, allgemeine "
            "Robotik, Perception-Schwerpunkt, ROS/Hardware und reine Theorie. "
            "Ich wuerde jetzt mit Uni- und Company-Lane plus Proposal-Sketches "
            "fortfahren."
        ),
    },
    {
        "role": "user",
        "content": (
            "Bitte mach jetzt die eigentliche Auswertung: Uni-/Chair-Lane, "
            "External-Company-Thesis-Lane inklusive Ausschlussgruenden und "
            "daraus konkrete Proposal-Sketches. Nutze nur die bereitgestellte "
            "Evidenz und erfinde keine Live-Treffer."
        ),
    },
]


JUDGE_PROMPT = f"""
Evaluate this end-to-end external thesis skill conversation.

Pass/fail criteria:
1. The student starts by introducing themself.
2. The assistant behaves like a thesis study advisor first, not a simple search engine.
3. The assistant builds a deep enough profile before generating results.
4. The assistant generates and evaluates a university/chair lane using the fixture evidence, with caveats that research areas are not confirmed open thesis topics.
5. The assistant generates and evaluates an external/company thesis lane using the fixture evidence, includes the Mercedes-style bachelor thesis lead and the StepStone bachelor lead if supported, and excludes generic robotics, medicine, provider-count-only evidence, Werkstudent/working-student roles, and non-bachelor/perception-heavy mismatches with reasons.
6. The assistant generates at least two proposal sketches, including one university-led and one external/company-led sketch.
7. The proposal sketches are grounded in the student's prior knowledge and profile: RL/autonomous systems, automotive-only, Python/PyTorch/Gymnasium, simulation, reward design, evaluation metrics, no medicine, no general robotics, no heavy ROS/hardware.
8. The assistant labels uncertainty, evidence tier/date, missing verification, and does not invent live web results, openings, supervision capacity, deadlines, salary, or company willingness.
9. The assistant includes provider labels, source URLs, mirror URLs when available, evidence tiers, visible dates, access dates, and exact exclusion reasons for company candidates.
10. The assistant must not upgrade snippets into confirmed live availability; company leads should remain posting/snippet-derived until verified.
11. Provider counts must be treated as discovery evidence only, not as recommendations or confirmed postings.
12. Each proposal sketch labels its evidence status: external posting/snippet-derived lead, university research-area conversation starter, or hybrid/external feasibility hypothesis.
13. Because the student is a Bachelor student, no Masterarbeit-only lead may be ranked as eligible or turned into a proposal.
14. Working-student/Werkstudent roles must be fully excluded, not treated as adjacent thesis opportunities.

Fixture evidence:
{EVIDENCE_FIXTURE}

Return compact JSON with keys: passed, score_0_to_1, findings, risks, recommended_skill_improvements.
"""


def run_codex(prompt: str) -> str:
    codex_bin = os.getenv("CODEX_BIN") or shutil.which("codex")
    if not codex_bin:
        raise RuntimeError("codex executable not found")
    cmd = [
        codex_bin,
        "exec",
        "--sandbox",
        "read-only",
        "--skip-git-repo-check",
        prompt,
    ]
    completed = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        env=os.environ.copy(),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=TIMEOUT,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"codex exec failed with exit code {completed.returncode}\n"
            f"STDERR:\n{completed.stderr.strip()}\nSTDOUT:\n{completed.stdout.strip()}"
        )
    return completed.stdout.strip()


def format_transcript(turns: list[dict[str, str]]) -> str:
    return "\n\n".join(
        f"### Turn {index}: {turn['role'].upper()}\n{turn['content'].strip()}"
        for index, turn in enumerate(turns, start=1)
    )


def next_assistant(turns: list[dict[str, str]]) -> str:
    transcript = format_transcript(turns)
    return run_codex(
        f"{ASSISTANT_SYSTEM}\n\nConversation so far:\n{transcript}\n\nNext assistant message:"
    )


def judge(turns: list[dict[str, str]]) -> str:
    transcript = format_transcript(turns)
    return run_codex(f"{JUDGE_PROMPT}\n\nConversation:\n{transcript}\n\nEvaluation JSON:")


def write_outputs(run: dict[str, object], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "external-thesis-e2e-eval.json"
    log_path = output_dir / "external-thesis-e2e-eval.log"
    json_path.write_text(json.dumps(run, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# External Thesis Skill End-to-End Eval Log",
        "",
        f"Created at: {run['created_at']}",
        f"Repository: {REPO_ROOT}",
        f"Max turns: {MAX_TURNS}",
        "",
        "## Persona",
        "",
        USER_PROFILE.strip(),
        "",
        "## Evidence Fixture",
        "",
        EVIDENCE_FIXTURE.strip(),
        "",
        "## Conversation",
        "",
        format_transcript(run["turns"]),  # type: ignore[arg-type]
        "",
        "## Judge Evaluation",
        "",
        str(run["judge_evaluation"]).strip(),
        "",
    ]
    log_path.write_text("\n".join(lines), encoding="utf-8")
    print(log_path)


def main(argv: list[str] | None = None) -> int:
    output_dir = Path(argv[0]) if argv else DEFAULT_OUT_DIR
    turns: list[dict[str, str]] = list(SCRIPTED_PROFILE_TURNS)
    turns.append({"role": "assistant", "content": next_assistant(turns)})

    run = {
        "created_at": datetime.now(UTC).isoformat(),
        "repo": str(REPO_ROOT),
        "max_turns": MAX_TURNS,
        "turns": turns,
        "judge_evaluation": judge(turns),
    }
    write_outputs(run, output_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
