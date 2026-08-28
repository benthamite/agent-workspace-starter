---
name: update-log
description: End-of-session bookkeeping. Run only when the user explicitly asks (the user types /update-log or says update log, close out, wrap up, or asks to save progress). Do NOT invoke this on your own initiative, and do NOT hand-write a session log yourself instead of invoking it — writing or editing any file under a logs/ directory is this skill's job alone.
user-invocable: true
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: "[optional summary of what was done]"
---

# End-of-session log update

Preserve this session's work for future sessions.

> **The prohibition is on the act, not just on the skill.** Do not write a
> session log by hand as a substitute for invoking this skill; creating or
> editing any file under `logs/` is this skill's job, and only when invoked.
> And do not invoke it on your own initiative — run it only when the user
> asks. If you think a log would help, suggest it, then stop.

## Triage first (may be a no-op)

Decide whether this session changed durable project state:

- code, docs, configuration, or data changes;
- new findings, debugging results, or service-state changes future sessions
  should know;
- decisions, new or completed TODOs, blockers, or status changes.

If nothing durable changed (purely conversational Q&A, a quick read-only
lookup), write nothing, commit nothing, report `No durable changes — skipping
update-log.`, and stop. Doing nothing is a valid, friction-free outcome.
Exception: if the user asked for specific bookkeeping, honor it.

## Step 0: Find the project root

The project root is the nearest ancestor of the working directory that sits
directly under `projects/` (e.g. `projects/<slug>/`), or the workspace root
itself for sessions started there. The log directory is `<project-root>/logs/`;
create it if missing.

## Step 1: Write the session log

Create `<log_dir>/YYYY-MM-DD.md` using the session date. If a file for today
already exists, append to it under a horizontal rule.

Contents:

- **Title**: `# YYYY-MM-DD: <brief title>`
- **What was done**: summary of the work performed.
- **Key findings**: discoveries, bugs found or fixed, validated or invalidated
  hypotheses.
- **Results**: exact numbers where available (counts, timings, outcomes).
- **Open questions**: what was left unfinished or should be explored next.

Be concise but specific. Future sessions may need to understand *why* choices
were made, so record the reasoning behind non-obvious decisions.

## Step 2: Run post-update-log hooks

Walk up ancestor directories from the project root to the workspace root
(inclusive). For each ancestor, if `<ancestor>/context/post-update-log-hook.md`
exists, read and follow it. Run all matching hooks, innermost first. In this
workspace, `projects/context/post-update-log-hook.md` refreshes the project
brief from the log and reconciles meeting action items.

## Step 3: Update the map's Current focus

After the hooks have refreshed the brief, regenerate the `## Current focus`
section of the project's `CLAUDE.md` from the brief's Active TODOs, following
the rules in `projects/context/project-doc-conventions.md`: replace the
previous content entirely (never append), one orientation line plus up to ~6
bullets, ~120-word cap, no dates or session narrative, carry each TODO's own
wording, and never state anything here that the brief does not already say.

For a session at the workspace root, update the root `CLAUDE.md`'s
`## Latest session` section instead: a 2–4 sentence summary plus a pointer
line `Full details: logs/YYYY-MM-DD.md`. Do not paste the log itself.

## Step 4: Commit

Commit the new log file, the refreshed brief, the updated map, and any files
changed by hooks, with a descriptive message. Stage only these files: if
unrelated changes are dirty in the working tree, leave them out (use
hunk-level staging if a file mixes both). Inspect `git diff --cached` before
committing to confirm only bookkeeping changes are staged. Do not push unless
the user asked to.

## Report

Report in a few lines: the log file path, files changed by hooks, the
Current-focus update, and the commit hash.

$ARGUMENTS
