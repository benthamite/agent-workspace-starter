---
name: meeting-debrief
description: 'Use for "meeting debrief", "debrief", "process meeting notes", or "meeting followup": turn notes from a recent meeting into a dated meeting file and mirror action items into the relevant project briefs.'
user-invocable: true
argument-hint: "[person or meeting name] [date, defaults to today]"
---

# Meeting debrief

After a meeting, capture the notes into `meetings/<person>/YYYY-MM-DD.md` and
mirror your action items into the projects they belong to.

## Step 0: Identify the meeting

From `$ARGUMENTS` and the conversation, determine who the meeting was with and
on what date (default: today). The person's folder is
`meetings/<first-name>/`, lowercase; create it if this is the first meeting
with them. If two colleagues share a first name, use `<first-name>-<last-name>`
for the newer one (and note the collision in the root `CLAUDE.md` so future
sessions pick the right folder). For a recurring group meeting, use a group
slug instead of a name.

## Step 1: Obtain the notes

In priority order:

1. **Notes in the conversation** — the user pasted them or dictated them.
2. **A file path the user named.**
3. **A configured transcript source** — see *Plugging in a transcript source*
   below. If none is configured and no notes were provided, ask the user to
   paste their notes; do not invent content.

## Step 2: Write the meeting file

Create `meetings/<person>/YYYY-MM-DD.md` (append under a horizontal rule if it
exists):

```markdown
# YYYY-MM-DD: <meeting title>

## Summary

<2–5 sentences: what the meeting was about and what it concluded.>

## Decisions

- <Each decision made, one line each. Omit the section if none.>

## Action items

### Mine

1. [ ] <action> → mirrored to [projects/<slug>](../../projects/<slug>/<slug>.md)
2. [ ] <action>

### Theirs

- [ ] <person>: <action>

## Notes

<Anything else worth keeping: context, numbers, positions taken.>
```

Number *your* action items — the numbers are stable IDs that mirrored TODOs
and the post-update-log hook use to find the item again even after wording is
edited. Never renumber existing items when appending.

Record only what the notes support. Do not embellish, and keep the
participants' own wording for anything contentious.

## Step 3: Mirror action items into project briefs

For each of *your* action items that belongs to an existing project, add a
TODO to that project's brief under **Active TODOs**, with a back-link naming
the item number:

```markdown
- [ ] <action> (from [meetings/<person>/YYYY-MM-DD.md](../../meetings/<person>/YYYY-MM-DD.md), item 1)
```

Then regenerate each touched project's `CLAUDE.md` Current focus by applying
step 3 of `projects/context/post-update-log-hook.md` — that file is the single
owner of the derivation; do not restate its rules here. An action item that
fits no existing project stays in the meeting file only; suggest
`/new-project` if it clearly deserves one.

## Step 4: Validate, commit, and report

Run `python3 scripts/check-conventions.py` from the workspace root and fix any
failure. Then commit the meeting file, every brief you touched, and every
regenerated map with message `Debrief YYYY-MM-DD <person> meeting`. Commit
with an explicit pathspec (`git commit -m "<message>" -- <files>`) so
pre-staged unrelated changes are not swept in, and confirm with
`git show --stat HEAD`. Report: the meeting file path, action items captured
(yours vs. theirs), and which projects received mirrored TODOs.

## Plugging in a transcript source

If your calendar tooling generates meeting summaries (Google Gemini notes,
Granola, Otter, Zoom AI Companion), replace Step 1's manual path with
retrieval, following this pattern:

1. Query your calendar CLI for the selected date's events and match the
   meeting by attendee or title.
2. Search the summary source for that event (e.g. Gemini summaries arrive by
   email from `gemini-notes@google.com` with the event title in the subject
   and a link to the full notes doc).
3. Fetch the full notes, then continue from Step 2 above.

Document your exact commands here once wired, so the skill runs unattended.
