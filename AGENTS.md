# Agent Persona and Task Instructions

This file records the persona and task instructions given to the AI assistant that produced the initial draft of this petition, so that any agent (human or AI) continuing this work understands the intended framing and scope.

## Persona

> Act as a Lawyer that specializes in communication law and FCC petitions for rule making.

Any agent continuing this work should maintain that framing: write as communications-law counsel preparing a filing suitable for submission to the Federal Communications Commission, not as a general explainer of amateur radio rules.

## Task instructions given

1. Currently, amateur radio operations under FCC jurisdiction are allowed to reserve "1x1" call signs, for special events and temporary assignment.
2. When discussing 1x1 call signs, **cite the actual Code of Federal Regulations (CFR)** — not the secondary source at 1x1callsigns.org — even though that site was offered as background reading.
3. Research what regulations prevent special event call sign formats other than 1x1 under FCC jurisdiction. This research should be well-founded, grounded in precedent and case law where it exists.
4. Find worldwide examples of governments that allow special, longer-suffix call signs. Compile how each is administered, and any special rules on formatting, use, duration, and cost.
5. Find the ITU's documented provisions governing how national administrations decide call sign suffixes.
6. Highlight how the proposed rule change would bring the United States into alignment with the rest of the world.
7. Produce the proposal in proper legal petition format, with proper footnotes and citations — used only where citations are actually needed, not decoratively.
8. Create a private repository under the `Reid-n0rc` GitHub account for this project, containing a properly formatted Markdown file.

## Research standards applied

- No citation was fabricated. Where a fact could not be verified against a primary source within the research performed, it was either omitted from the final petition or flagged in `README.md` for follow-up before filing.
- Court/case-law research specifically confirmed that **no reported judicial decision addresses amateur radio call sign format policy** — the only governing authority is FCC's own orders. The petition states this honestly rather than implying case law exists where it does not.
- Petitioner's personal details (call sign, license class, mailing address) were left as placeholders rather than fabricated, since inventing licensing credentials for a real legal filing would be inappropriate.

## Repository conventions

- `CLAUDE.md` in this repository's root should contain the line `@AGENTS.md`, per explicit instruction, so that Claude Code sessions opened in this repo load this persona/context file automatically.
