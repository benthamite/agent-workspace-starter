# Agent workspace starter

A template for running Claude Code as a project manager and thinking partner
across many parallel projects, with durable memory between sessions. The whole
system is a directory layout, three writing conventions, three skills, and one
small validator script.
There is no database, no plugin, and no server: just Markdown files in a
private git repository.

This is a genericized extract of a working setup. The original uses org-mode
and has grown a validation harness around it; this starter keeps the part that
makes the workflow work and leaves out the hardening (see [Adapting](#adapting)).

## The idea

You keep one private **workspace repository** holding the notes for everything
you work on: one folder per project, one folder per person you meet with.

Claude Code loads every `CLAUDE.md` file between your current directory and the
workspace root. That single built-in behavior is the context mechanism: start a
session inside `projects/website-redesign/` and Claude automatically has both
the project's own map and your workspace-wide context (who you are, what your
role is, your conventions). No tooling required.

Memory between sessions comes from ending each session with `/update-log`. It
writes a dated session log, refreshes the project's durable notes from what
happened, regenerates the short digest that future sessions load, and commits.
The next session starts already knowing where the last one left off.

## Layout

```
workspace/
├── CLAUDE.md                  # workspace-wide context: you, your role, conventions
├── .claude/skills/            # new-project, update-log, meeting-debrief
├── projects/
│   ├── context/               # shared conventions and the post-update-log hook
│   └── <slug>/
│       ├── <slug>.md          # the brief: durable ground truth
│       ├── CLAUDE.md          # the map: pointers plus a current-focus digest
│       └── logs/              # dated session logs
└── meetings/
    └── <person>/
        └── YYYY-MM-DD.md      # one file per meeting
```

Project *code* lives outside this repository (e.g. `~/repos/<name>`), and the
brief records where. Keeping code out keeps the workspace small, private, and
safe to load into context.

## The three layers

Each fact lives in exactly one place. This is the core discipline; everything
else follows from it.

| Layer | File | Holds | When it changes |
|-------|------|-------|-----------------|
| Brief | `projects/<slug>/<slug>.md` | Durable state: decisions, constraints, open TODOs | When reality changes |
| Map | `projects/<slug>/CLAUDE.md` | Stable pointers plus a short current-focus digest | Derived from the brief after each session |
| Log | `projects/<slug>/logs/YYYY-MM-DD.md` | What happened in one session, and why | Append-only, one file per day |

Why bother separating them? Because the naive alternative (one growing notes
file per project) fails in both directions at once. Loading the full history
into every session wastes context and buries the current state; keeping only a
summary loses the reasoning you need when a decision comes back into question.
The split gives each question one home: the brief answers "what is true now",
the log answers "what happened and why", and the map is the only thing that
loads into every session, so it stays short.

Two rules keep the layers from bleeding into each other (spelled out in
[projects/context/project-doc-conventions.md](projects/context/project-doc-conventions.md)):

- **The current-focus digest is regenerated, never appended to.** Appending is
  what turns it into a second chronological log. Nothing is lost by replacing
  it: the narrative is in the log, the state is in the brief.
- **Derived sections never originate claims.** "Waiting on Alex" belongs on a
  TODO in the brief, where it carries a date and can be closed, not in a
  summary, where it silently goes stale.

## Session lifecycle

1. `cd projects/<slug> && claude` — the map and workspace `CLAUDE.md` load
   automatically.
2. Work. The brief is in context via the map's pointers; Claude reads deeper
   (old logs, meeting notes) on demand.
3. Say `/update-log` when you finish. It triages first (a purely conversational
   session gets no log), then writes the log, refreshes the brief, regenerates
   the map's current focus, and commits.

Sessions started at the workspace root log to a top-level `logs/` directory,
and `/update-log` applies the same hook-driven brief and map refresh to every
project the session touched, so root sessions leave project state as current
as project sessions do.

## Meetings

Meetings live in `meetings/<person>/`, one dated file each. After a meeting,
run `/meeting-debrief`: it takes your notes (pasted, from a file, or from a
transcript tool you have plugged in), writes the dated meeting file, and
mirrors your action items into the relevant project briefs as TODOs with a
back-link to the meeting. The post-update-log hook closes the loop in the
other direction: when a session completes a TODO that came from a meeting, the
meeting file gets marked too.

## The skills

| Skill | What it does |
|-------|--------------|
| `/new-project` | Creates `projects/<slug>/` with a brief and a map from a description or the current conversation, and commits. |
| `/update-log` | End-of-session bookkeeping: log, brief refresh, map digest, commit. Owns all writes under `logs/`. |
| `/meeting-debrief` | Turns meeting notes into `meetings/<person>/YYYY-MM-DD.md` and mirrors action items into project briefs. |

## Getting started

1. Create your own **private** copy — session logs accumulate unfiltered
   working notes, so treat the whole workspace as confidential:

   ```bash
   gh repo create my-workspace --template benthamite/agent-workspace-starter --private --clone
   cd my-workspace
   ```

   (Or click "Use this template" on GitHub, or clone and re-init:
   `git clone <this repo> my-workspace && cd my-workspace && rm -rf .git && git init && git add -A && git commit -m "Init workspace"`.)
2. Smoke test: `python3 scripts/check-conventions.py` from the root should
   print `Convention check passed.` (needs Python 3.8+; the kit was exercised
   with Claude Code 2.1.247).
3. Rewrite the root `CLAUDE.md`; it is a template with placeholders for your
   name, role, and conventions.
4. Look at the example project (`projects/website-redesign/`) and example
   meeting (`meetings/alex/`) to see the target shape, then delete them.
5. Start your first real project: open Claude Code at the workspace root and
   say `/new-project <description>`.

## Adapting

- **Org-mode instead of Markdown.** The original setup uses org files for
  briefs and meetings, which adds TODO keywords, properties, and agenda
  integration for Emacs users. Nothing in the workflow depends on the format;
  if you live in Emacs, translate the templates and keep the structure.
- **Meeting notes source.** `meeting-debrief` accepts pasted notes out of the
  box. If your calendar tool generates summaries (Gemini notes, Granola,
  Otter, Zoom AI), wire the retrieval step to it (the skill marks where).
- **Other agents.** If you also use Codex or another CLI that reads
  `AGENTS.md`, keep it as a byte-identical mirror of each `CLAUDE.md` and sync
  it whenever the map changes.
- **Hardening.** This kit ships exactly one check, `scripts/check-conventions.py`,
  because testing showed it is needed: agents drift from the digest rules
  (paraphrasing TODOs, slipping narrative into state sections) even with the
  conventions in context, so the skills run it before every commit. The
  original system goes much further (receipts, an isolated commit harness,
  generated project registries), each piece added after a real failure at real
  complexity cost. Start with just the one check, and add more only after the
  mistake it prevents has actually bitten you.
