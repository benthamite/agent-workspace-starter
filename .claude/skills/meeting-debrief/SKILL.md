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
with them. For a recurring group meeting, use a group slug instead of a name.

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

- [ ] <action> → mirrored to [projects/<slug>](../../projects/<slug>/<slug>.md)

### Theirs

- [ ] <person>: <action>

## Notes

<Anything else worth keeping: context, numbers, positions taken.>
```

Record only what the notes support. Do not embellish, and keep the
participants' own wording for anything contentious.

## Step 3: Mirror action items into project briefs

For each of *your* action items that belongs to an existing project, add a
TODO to that project's brief under **Active TODOs**, with a back-link:

```markdown
- [ ] <action> (from [meetings/<person>/YYYY-MM-DD.md](../../meetings/<person>/YYYY-MM-DD.md))
```

Then regenerate that project's `CLAUDE.md` Current focus if the new TODO
changes the top priorities. An action item that fits no existing project stays
in the meeting file only; suggest `/new-project` if it clearly deserves one.

## Step 4: Commit and report

Commit the meeting file and every brief you touched with message
`Debrief YYYY-MM-DD <person> meeting`. Report: the meeting file path, action
items captured (yours vs. theirs), and which projects received mirrored TODOs.

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
