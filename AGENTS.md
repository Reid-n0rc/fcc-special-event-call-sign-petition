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

## Formatting and style conventions (PDF)

`PETITION.md` is the single source of truth; `Petition_for_Rulemaking.pdf` is a rendered artifact and should never be hand-edited — regenerate it with `python3 build_pdf.py` (see `README.md`) after any markdown change, and a GitHub Actions workflow (`.github/workflows/build-pdf.yml`) also does this automatically on push. The PDF's look is modeled on a real Petition for Rulemaking / Request for Waiver filed with the FCC (Association of American Railroads, filed by Hogan Lovells) that the user supplied as a reference, plus standard legal-filing rules the user gave directly. Any future change to `PETITION.md`'s structure should preserve these conventions unless the user says otherwise:

- **Page**: US Letter, 1in margins on all sides (keeps the printed text area within the required 6.5 x 9.5in).
- **Font**: Times New Roman (serif fallback), 12pt minimum everywhere, **including footnotes** — this was an explicit user rule, even though the real reference filing actually uses smaller footnote text.
- **Spacing**: double-spaced body text (`line-height: 2`), left-aligned (not justified). Paragraphs are first-line indented (`text-indent: 0.5in`) with no extra gap between paragraphs (`margin: 0`) — spacing comes from the double line height alone, matching the reference filing's continuous flow. Exceptions with `text-indent: 0`: the front-matter block, blockquotes, and list items.
- **Caption**: plain (not bold) text, centered — "Before the / FEDERAL COMMUNICATIONS COMMISSION / Washington, DC 20554" — followed by a borderless two-column "In the Matter of" table with the docket/RM number.
- **Document title** (e.g. "PETITION FOR RULE MAKING"): centered, plain weight (not bold).
- **Section headings (I., II., ...)**: left-aligned, bold, upper case (`text-transform: uppercase` in CSS — the markdown source itself stays mixed-case for readability).
- **Lettered subheadings (A., B., ...)**: left-aligned, bold, indented (`margin-left: 0.5in`), title case (no uppercase transform).
- **No decorative color/shading** — black text and rules only. The one deliberate exception: proposed rule-text redlines use `<u>underline</u>` for insertions (standard legislative drafting convention, not decoration).
- **Footnotes**: real page-bottom footnotes via WeasyPrint's CSS `float: footnote`, not endnotes. The build script extracts python-markdown's `[^N]` footnote definitions and re-injects each one inline as a `<span class="fn">` at its point of reference so it lands on the correct page automatically.
- **Table of Contents**: dotted-leader entries with **live page numbers** computed by WeasyPrint's `target-counter()` CSS function (needs the `toc` markdown extension purely for its side effect of giving headings predictable slug `id`s to link against) — not hardcoded numbers, so it can never go stale.
- **Numbered paragraphs**: the substantive numbered paragraphs (`1.`, `2.`, ...) in `PETITION.md` must have the period **escaped** (`1\.`, `2\.`) — a bare `21. text` at the start of a line is parsed by python-markdown as an ordered-list item, and a new `<ol>` silently restarts numbering at 1 every time a heading interrupts the list. This bit twice during drafting; always verify with a script that greps the *rendered* PDF text for sequential paragraph numbers, not just the markdown source, after any edit that adds/moves/renumbers paragraphs.
- Raw HTML blocks in the markdown (e.g. `<div class="frontmatter" markdown="1">`) need `markdown="1"` and the `md_in_html` extension, or nothing inside them (headings, tables, bold, etc.) gets processed as markdown.
