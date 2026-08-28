---
name: new-project
description: 'Use when the user says "new project"/"create project" or wants to spin off the current conversation or seed context into a dedicated project with a brief, a map, and a commit.'
user-invocable: true
argument-hint: "[project description or seed context]"
---

# Create a project

Create one project record under `projects/<slug>/`. The target shapes for the
brief and the map are defined in
`projects/context/project-doc-conventions.md` — read it first.

## Inputs and naming

Use `$ARGUMENTS` as the project description or seed context; if empty, use the
current conversation. Ask only when no clear project exists or when two
plausible names would lead to different identities.

Determine:

- a short kebab-case directory slug (name the domain or workflow; no generic
  suffixes like `project` or `workflow`);
- a title;
- a one-sentence summary;
- background, durable decisions, references, and concrete next actions;
- whether the project has code, and if so where its checkout lives (code stays
  *outside* this workspace, e.g. `~/repos/<name>`; the brief records the path).

Verify `projects/<slug>/` does not already exist. If it does, stop — merging
into an existing project is the user's decision.

## Create the brief

Create `projects/<slug>/<slug>.md` in the brief shape from the conventions
doc: orientation, **Background**, **Current state**, **Active TODOs** (each a
concrete next action, highest priority first), **References** (including the
code checkout path if any).

Put all seed context needed by the next session in the brief. Do not create or
edit anything under `logs/` — the `update-log` skill alone owns session-log
writes.

## Create the map

Create `projects/<slug>/CLAUDE.md` in the map shape from the conventions doc:
one-line identity, **Read first** pointers (brief, code path, `logs/`),
optional **Invariants**, and a **Current focus** digest derived from the
Active TODOs you just wrote.

If this workspace also mirrors maps to `AGENTS.md` for other agent CLIs,
create it as a byte-identical copy and verify with
`diff projects/<slug>/CLAUDE.md projects/<slug>/AGENTS.md`.

## Commit and hand off

Commit the new directory with message `Add <slug> project`. Do not push unless
the user asked to.

Then report the project path and the exact next task, and suggest continuing
in a session started inside `projects/<slug>/` so the project's map loads
automatically.
