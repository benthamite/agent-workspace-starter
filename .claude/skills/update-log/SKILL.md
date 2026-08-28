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

## Step 0: Find the bookkeeping root and the affected projects

The bookkeeping root is the nearest ancestor of the working directory that
sits directly under `projects/` (e.g. `projects/<slug>/`), or the workspace
root itself for sessions started there. The log directory is
`<bookkeeping-root>/logs/`; create it if missing.

Separately, list the **affected projects**: every `projects/<slug>/` whose
files this session changed (check `git status` plus your session memory).
For a project session this is normally just the project itself; a root
session may have touched several.

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

## Step 2: Run post-update-log hooks for every affected project

Walk up ancestor directories from the bookkeeping root to the workspace root
(inclusive). For each ancestor, if `<ancestor>/context/post-update-log-hook.md`
exists, read and follow it, innermost first. In this workspace,
`projects/context/post-update-log-hook.md` refreshes the project brief from
the log, reconciles meeting action items, and regenerates the project map's
`## Current focus` — it is the single owner of that derivation; do not
re-derive the map outside it.

For a session at the workspace root, apply that hook to **each affected
project** from Step 0, so a root session that touched projects still leaves
their briefs, maps, and meeting items current.

## Step 3: Update the root map (root sessions only)

For a session at the workspace root, update the root `CLAUDE.md`'s
`## Latest session` section: a 2–4 sentence summary plus a pointer line
`Full details: logs/YYYY-MM-DD.md`. Do not paste the log itself. For a
project session, the hook in Step 2 already updated the project map; there
is nothing to do here.

## Step 4: Validate, then commit

Run `python3 scripts/check-conventions.py` from the workspace root and fix
any failure before committing — it catches the drift (paraphrased digest
bullets, narrative in state sections, broken meeting links) that these
conventions exist to prevent.

Then commit the new log file, the refreshed briefs, the updated maps, and any
other files changed by hooks, with a descriptive message. Stage only these
files: if unrelated changes are dirty or already staged, leave them out (use
hunk-level staging if a file mixes both, and commit with an explicit pathspec
— `git commit -m "<message>" -- <files>` — so pre-staged unrelated changes
are not swept in). Inspect the result with `git show --stat HEAD` to confirm
only bookkeeping changes were committed. Do not push unless the user asked
to.

## Report

Report in a few lines: the log file path, files changed by hooks, the
Current-focus update, and the commit hash.

$ARGUMENTS
