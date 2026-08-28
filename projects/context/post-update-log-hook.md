# Post-`/update-log` hook (all projects)

Read and follow these instructions after `/update-log` writes a session log in
any project under `projects/`. The target shape of every file mentioned here
is defined in [project-doc-conventions.md](project-doc-conventions.md); this
file says *when* to update, that one says *what the result looks like*.

1. **Refresh the brief.** Update `projects/<slug>/<slug>.md` from the session
   log just written:
   - refresh **Current state** with durable facts and decisions (not a
     session chronology);
   - update **Active TODOs** first — add new tasks, check off completed ones
     with a one-line note of what closed them, re-order by priority;
   - keep only durable decisions, constraints, and references in the brief;
     move stale narrative to `<slug>-archive.md` if the brief is getting long.

2. **Reconcile meeting action items.** For each TODO in the brief that carries
   a meeting back-link and was completed this session, open the linked
   `meetings/<person>/YYYY-MM-DD.md` file and mark the corresponding action
   item done. This keeps the meeting record and the project brief agreeing
   about what is outstanding.

3. **Regenerate the map's Current focus** from the refreshed brief's Active
   TODOs, per the rules in project-doc-conventions.md. The order matters:
   TODOs first, then the digest — deriving the digest from the session log
   instead of the refreshed brief mints a confident sentence about live state
   that nothing will ever correct.
