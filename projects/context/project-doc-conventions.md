# Project documentation conventions

Every project under `projects/<slug>/` keeps three files with strictly
separated jobs. Each fact lives in exactly one of them.

## The brief: `projects/<slug>/<slug>.md`

The brief is concise ground truth, not a chronological dossier. It answers
"what is true now": durable facts, decisions, constraints, and open work.

```markdown
# <Title>

<One to three sentence orientation: what this project is and why it exists.>

## Background

<Why it exists, who requested it, source links.>

## Current state

<Durable facts and decisions. Not a session chronology — no "on <date> I
did X" narrative; that belongs in logs/.>

## Active TODOs

- [ ] <Concrete next action, highest priority first>
- [ ] <Next action> (waiting on <person/event> — asked YYYY-MM-DD)

## References

<Useful source material, code checkout path, links.>
```

Rules:

- Keep open work as checklist items under **Active TODOs**, highest priority
  first. Each item is a concrete action, not a topic.
- A claim that work is blocked, pending, or awaiting somebody belongs on the
  TODO itself, with the date it was last checked ("asked Alex 2026-01-10, no
  reply as of 2026-01-15"). Bare "waiting on Alex" reads as current however
  old it gets.
- An action item that came from a meeting carries a back-link naming the
  meeting file and the item's stable number in that file's "Mine" list:
  `(from [meetings/alex/2026-01-15.md](../../meetings/alex/2026-01-15.md), item 1)`.
- When completed work and historical narrative make the brief long, move them
  to `<slug>-archive.md` in the same directory. The brief stays short enough
  to read in one sitting.

## The map: `projects/<slug>/CLAUDE.md`

The map is what loads into every session, so it stays short and stable. It
contains pointers and a derived digest — never original content.

```markdown
# <Title>

<One-sentence identity and owner.>

## Read first

- **Current state, next steps, open questions** → `<slug>.md`
- **Code** → `<external checkout path>` (omit if no code)
- **Session history** → `logs/`

## Invariants

<Only durable guardrails, if any. Omit the section if empty.>

## Current focus

<Short digest derived from the brief's Active TODOs.>
```

Rules for **Current focus**:

- **Regenerate it from the brief's Active TODOs after every session, replacing
  the previous content — never append.** Appending is what turns it into a
  second log. Replacing loses nothing: the session log holds the narrative and
  the brief holds the state.
- One orientation line, then up to ~6 bullets of live open priorities, hard
  cap ~120 words. No dates, no session narrative.
- Carry each TODO's own wording or a link to it. A paraphrase is a second copy
  that can disagree with the original.
- Skip items that are waiting or deferred; if *everything* is blocked, say so
  in the orientation line and name what it is waiting on.
- **Never originate a claim here.** If the section says something the brief
  does not, fix the brief first.

## The log: `projects/<slug>/logs/YYYY-MM-DD.md`

One file per day, append-only, written only by `/update-log`. It answers "what
happened and why": work done, findings, results, reasoning behind non-obvious
choices, and open questions. Future sessions read it on demand via the map's
pointer; it never loads automatically, so it can be as detailed as needed.

## Enforcement

`scripts/check-conventions.py` checks the mechanical subset of these rules:
every project has a brief and a map, Current focus bullets appear verbatim in
Active TODOs (no paraphrase), Current focus has no dates and respects the word
cap, Current state has no "On YYYY-MM-DD" narrative, and meeting back-links
resolve. The skills run it before committing; you can run it any time from the
workspace root. It exists because these are exactly the rules an agent drifts
from first.
