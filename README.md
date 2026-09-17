# FCC Special Event Call Sign Petition for Rulemaking

This repository contains a draft Petition for Rulemaking asking the Federal Communications Commission to amend 47 C.F.R. Part 97 to authorize a second, longer amateur radio special event call sign format, in addition to the existing "1x1" format, bringing U.S. practice into alignment with other ITU member administrations.

- [`PETITION.md`](./PETITION.md) — the source of truth: the draft petition, in FCC filing format with footnoted citations. Edit this file.
- [`Petition_for_Rulemaking.pdf`](./Petition_for_Rulemaking.pdf) — a paginated PDF rendering of the petition, matching real FCC filing conventions (letter size, centered caption, serif body text, numbered pages, and true page-bottom footnotes). Generated from `PETITION.md`.
- [`build_pdf.py`](./build_pdf.py) — regenerates the PDF from `PETITION.md`. Run `pip install markdown weasyprint && python3 build_pdf.py` after editing the markdown source, then commit both files.
- [`AGENTS.md`](./AGENTS.md) — the persona and task instructions used to produce this draft, for any AI agent that continues this work.

## Status

This is a **draft** prepared with AI research assistance. Before filing with the FCC:

1. Add the filing date (petitioner name, call sign N0RC, Amateur Extra Class, and mailing address are already filled in).
2. Independently re-verify remaining citations against primary sources (eCFR.gov, docs.fcc.gov, itu.int, and the cited national regulators) — several were flagged as needing direct confirmation (see research notes for exact fee figures for Australia and Germany, and for New Zealand/South Africa practice, which was not verified to the same standard as the other jurisdictions and was excluded from the final draft). Also verify the FCC's "Amateur Call Sign Systems" webpage cited in footnote 6 (Group A/B/C/D terminology) directly — it returned a 403 error during later research and was reconstructed from secondary sources only.
3. **Click-check every web-page URL added to the footnotes** (footnotes 6, 13, 18, 19, 23, 24, 28-32) — these were reconstructed from citations noted during earlier research turns in this session, not re-fetched live when added. Confirm each link still resolves and still supports the cited proposition before filing, and add a final access date matching the actual day of filing rather than the date these citations were added.
3. ~~Pull the actual ECFS record for WT Docket No. 09-209 to read ARRL's 2010 comments verbatim.~~ **Done** — the user supplied the actual filing (ARRL Comments, WT Docket No. 09-209, filed Mar. 26, 2010). It confirms Petition § III.C's central claim word-for-word at ¶ 22, and footnote 12 now cites it directly with a pinpoint paragraph cite.
4. ~~Locate and read FCC 99-84.~~ **Done** — the user supplied the actual order. It denied a David B. Popkin petition seeking only administrative changes (identification timing, duration/reuse limits, coordinator compensation) — it never addressed call sign format or length, so it is not adverse to this Petition. Petition § III.C, ¶ 13 and footnote 17 now state this definitively.
5. Run a full-text search of the FCC's Electronic Comment Filing System (ECFS) at fcc.gov/ecfs to confirm no other pending or resolved petition addresses this exact request.
6. **Attorney review of the proposed rule text itself.** Paragraph 17's two-letter (AA-AL, etc.) prefix option is a genuinely novel policy proposal — none of the six comparator countries researched actually do this; it is not precedented the way the suffix-length extension is, and deserves the closest scrutiny before filing. The exact redline in Section VII is illustrative, and paragraph 22 already invites the Commission to refine it in an NPRM, but that isn't a substitute for review by counsel.
7. Have the final draft reviewed by a licensed attorney before submission. This document was prepared by an AI assistant and does not constitute legal advice.

## Prior attempts to change this rule

Research turned up several prior episodes bearing directly on this Petition (see Petition § III.C for full discussion and citations), listed chronologically. The first is in the *original* special event call sign docket (WT Docket No. 95-57, 1997); the next two are in a *later, separate* docket about vanity and club station call signs generally (WT Docket No. 09-209, 2009-2012) — the two dockets should not be confused.

- **1999 (WT Docket No. 95-57) — a reconsideration petition on the special event system was denied, but it doesn't touch this Petition's subject.** Verified against the actual order: FCC 99-84 denied a petition by David B. Popkin seeking only administrative changes to the special event system — end-of-series identification, a 15-day maximum duration, a 30-day reuse interval, codified first-come-first-served/no-charge assignment, and a bar on compensating the coordinators. It never addressed call sign format or length, so it does not need to be distinguished and is not adverse to this Petition. See Petition § III.C, ¶ 13.
- **2010 (WT Docket No. 09-209) — ARRL itself asked for this, and the FCC never ruled on it.** In comments filed in that docket (verified against the actual filing, ¶ 22), ARRL recommended the Commission take up, in a later proceeding, an expansion of the special event call sign format beyond 1x1 — citing the same 2003 ITU treaty amendment (RR No. 19.68A) this Petition relies on. The FCC's resulting Report and Order in that docket (FCC 10-189, 2010) addressed other issues and never acted on the suggestion one way or the other.
- **2011-12 (WT Docket No. 09-209) — ARRL sought reconsideration of that order, but not on this point, and the docket was formally terminated.** ARRL's Jan. 13, 2011 Petition for Partial Reconsideration addressed only unrelated club-station vanity call sign limits. The Commission denied it and expressly terminated WT Docket No. 09-209 in FCC 12-1 (Jan. 11, 2012) — verified against the actual order, which also shows (n.10) that the Commission separately declined, "at this time," a different ARRL request to increase the number of call signs available in certain sequential/vanity formats generally (a general-availability concern, not the special-event-specific ask here). With the docket now formally terminated and the reconsideration window closed for over a decade, a new Petition for Rulemaking is the only remaining vehicle — a stronger and more precise posture than the original draft's, since it rests on the docket's actual, quoted termination order rather than an inferred closure.
- **Not relevant, for comparison:** a 2017 petition (Alessi/K1TA) sought a new permanent vanity format and was dismissed for unrelated reasons (call sign scarcity, which the Bureau found unsupported); a 2018-19 petition (Dukish, RM-11826) concerned station-identification timing under § 97.119(a), an unrelated rule subsection. Neither bears on special event call sign length.

All three FCC orders above (99-84, 10-189, 12-1) and ARRL's 2010 comments have now been verified against the actual primary documents, not secondary summaries.

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
