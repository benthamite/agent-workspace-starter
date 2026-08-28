# Website redesign

Rebuild the marketing site on the new design system before the March launch.
(This is an **example project** — delete it once you have seen the shape.)

## Background

Requested by Alex on 2026-01-08: the current site predates the rebrand and the
bounce rate on the pricing page is twice the industry benchmark. Scope agreed
in [meetings/alex/2026-01-15.md](../../meetings/alex/2026-01-15.md): homepage,
pricing, and docs landing page; blog stays on the old stack for now.

## Current state

- Design system tokens are final; the component library covers everything the
  homepage needs except the testimonial carousel.
- Decision (2026-01-15): static site generator stays — no framework migration
  in this pass. Revisit after launch.
- Staging environment is up; deploys from the `redesign` branch.

## Active TODOs

- [ ] Build the testimonial carousel component to close the homepage gap
- [ ] Draft the new pricing page copy and send it to Alex for review
- [ ] Audit docs landing page for broken deep links before the cutover
      (from [meetings/alex/2026-01-15.md](../../meetings/alex/2026-01-15.md))
- [ ] Get launch-week freeze dates from marketing (asked 2026-01-15, no reply
      as of 2026-01-15)

## References

- Code: `~/repos/marketing-site`, branch `redesign`
- Design system: <link to Figma / tokens>
- Staging: <staging URL>
