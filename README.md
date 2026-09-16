# FCC Special Event Call Sign Petition for Rulemaking

This repository contains a draft Petition for Rulemaking asking the Federal Communications Commission to amend 47 C.F.R. Part 97 to authorize a second, longer amateur radio special event call sign format, in addition to the existing "1x1" format, bringing U.S. practice into alignment with other ITU member administrations.

- [`PETITION.md`](./PETITION.md) — the source of truth: the draft petition, in FCC filing format with footnoted citations. Edit this file.
- [`Petition_for_Rulemaking.pdf`](./Petition_for_Rulemaking.pdf) — a paginated PDF rendering of the petition, matching real FCC filing conventions (letter size, centered caption, serif body text, numbered pages, and true page-bottom footnotes). Generated from `PETITION.md`.
- [`build_pdf.py`](./build_pdf.py) — regenerates the PDF from `PETITION.md`. Run `pip install markdown weasyprint && python3 build_pdf.py` after editing the markdown source, then commit both files.
- [`AGENTS.md`](./AGENTS.md) — the persona and task instructions used to produce this draft, for any AI agent that continues this work.

## Status

This is a **draft** prepared with AI research assistance. Before filing with the FCC:

1. Add the filing date (petitioner name, call sign N0RC, Amateur Extra Class, and mailing address are already filled in).
2. Independently re-verify every citation against primary sources (eCFR.gov, docs.fcc.gov, itu.int, and the cited national regulators) — several citations in the research process were flagged as needing direct confirmation (see research notes for exact fee figures for Australia and Germany, and for New Zealand/South Africa practice, which was not verified to the same standard as the other jurisdictions and was excluded from the final draft).
3. **Pull the actual ECFS record for WT Docket No. 09-209** to read ARRL's 2010 comments verbatim (Petition § III.C relies on ARRL's own published summary of those comments, not the primary filing), and confirm the FCC's Report and Order in that docket (FCC 10-189) truly never addressed the special event call sign suggestion.
4. **Locate and read FCC 99-84** (Memorandum Opinion and Order on Reconsideration, WT Docket No. 95-57, 14 FCC Rcd 8812 (1999)) — it reportedly denied an unspecified petition for reconsideration seeking "changes . . . in the special event call sign system." The substance of that 1999 petition could not be confirmed in research and must be checked before filing; it may need to be distinguished or addressed head-on in the final petition (see Petition § III.C, ¶ 11).
5. Run a full-text search of the FCC's Electronic Comment Filing System (ECFS) at fcc.gov/ecfs to confirm no other pending or resolved petition addresses this exact request.
6. Have the final draft reviewed by a licensed attorney before submission. This document was prepared by an AI assistant and does not constitute legal advice.

## Prior attempts to change this rule

Research turned up two prior episodes bearing directly on this Petition (see Petition § III.C for full discussion and citations):

- **2010 — ARRL itself asked for this, and the FCC never ruled on it.** In comments filed in WT Docket No. 09-209, ARRL recommended the Commission take up, in a later proceeding, an expansion of the special event call sign format beyond 1x1 — citing the same 2003 ITU treaty amendment (RR No. 19.68A) this Petition relies on. The FCC's resulting order in that docket addressed other issues and never acted on the suggestion one way or the other. This Petition is, in effect, formalizing and requesting a ruling on that sixteen-year-old, unaddressed proposal — a favorable posture, since it shows the amateur community's own national association already identified this need and the FCC has never rejected it on the merits.
- **1999 — a reconsideration petition on the special event system was denied, but the substance is unconfirmed.** FCC 99-84 reportedly denied a petition for reconsideration seeking unspecified changes to the special event call sign system. This could not be verified beyond the docket citation. **This needs to be tracked down and read before filing** — if it addressed call sign length/format, it may need to be distinguished; if it addressed something else entirely, it can likely be dropped from the final petition.
- **Not relevant, for comparison:** a 2017 petition (Alessi/K1TA) sought a new permanent vanity format and was dismissed for unrelated reasons (call sign scarcity, which the Bureau found unsupported); a 2018-19 petition (Dukish, RM-11826) concerned station-identification timing under § 97.119(a), an unrelated rule subsection. Neither bears on special event call sign length.

## Origin

This project was generated from the following prompt:

> Act as a Lawyer that specializes in communication law and FCC petitions for rule making. Currently amateur radio operations under FCC jurisdiction are allowed to reserve what is referred to 1x1 call signs. These are for special events and temporary assignment. Information on FCC regulations pertaining to this are noted here https://1x1callsigns.org/index.php/fcc-regulations
>
> When discussing 1x1 callsigns the actual CFR should be cited, not https://1x1callsigns.org/index.php/fcc-regulations
>
> I want to find what regulations are preventing other special event call sign formats beyond the 1x1 in areas under FCC jurisdiction. This needs to be well researched, based in precedence and case law if possible.
>
> Find other examples world wide of governments that allow special long suffix call signs. Compile how these are administered and any special rules on formatting, use, duration, and cost.
>
> Find document provisions the ITU has for governments to decide call sign suffixes.
>
> Highlight how the proposed rule brings the United States in to alignment with the rest of the world.
>
> Create the proposal in the proper format. Use proper footnotes and citations where needed. Do not do that where not needed.
>
> Create a private repo on Reid-n0rc GitHub for this project. Should be a properly formatted .md file.

Follow-up prompt:

> Have there been other attempts to change the rules to allow long special suffixes? Learn from those if they exist.
