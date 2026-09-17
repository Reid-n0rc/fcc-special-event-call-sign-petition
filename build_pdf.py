import re
import markdown
import weasyprint

with open("PETITION.md") as f:
    src = f.read()

# Convert markdown (with footnotes + tables extensions) to HTML. "toc" is used
# only for its side effect of giving headings predictable slug ids, which the
# hand-written Table of Contents links against for real, WeasyPrint-computed
# page numbers (via CSS target-counter()) -- its own generated <div class="toc">
# output is unused and stripped below.
html_body = markdown.markdown(
    src,
    extensions=["footnotes", "tables", "toc", "md_in_html"],
    extension_configs={"footnotes": {"BACKLINK_TEXT": ""}},
)

# Extract footnote definition texts from the generated <div class="footnote"> block,
# keyed by their fn:N id, then delete that block -- we'll re-inject each footnote
# inline (as a CSS float:footnote span) at its point of reference instead of as endnotes.
footnote_div_match = re.search(
    r'<div class="footnote">.*?</div>\s*$', html_body, flags=re.DOTALL
)
footnote_texts = {}
if footnote_div_match:
    div_html = footnote_div_match.group(0)
    for li_match in re.finditer(
        r'<li id="fn:([^"]+)">\s*<p>(.*?)&#160;.*?</p>\s*</li>', div_html, flags=re.DOTALL
    ):
        fid, text = li_match.groups()
        footnote_texts[fid] = text.strip()
    html_body = html_body[: footnote_div_match.start()]

# Drop the now-empty "## Footnotes" heading (and preceding <hr>) that led into the
# stripped endnote list. The "toc" extension adds an id="..." attribute to every
# heading, so match that loosely rather than assuming a bare <h2>.
html_body = re.sub(r'(<hr\s*/?>\s*)?<h2[^>]*>Footnotes</h2>\s*$', "", html_body.rstrip())

# Replace each inline footnote reference marker
#   <sup id="fnref:N"><a class="footnote-ref" href="#fn:N">N</a></sup>
# with (a) a small clickable superscript number that stays inline at the
# reference point, immediately followed by (b) a span carrying the actual
# footnote text with float:footnote, which WeasyPrint pulls out of normal
# flow and places at the bottom of whichever page it lands on. Both the
# forward reference and the footnote's own number are real <a> links (not
# CSS-generated counter content), so they're clickable in the PDF and jump
# to/from each other.
def replace_ref(m):
    fid = m.group(1)
    text = footnote_texts.get(fid, "")
    return (
        f'<sup class="fnref"><a href="#fn-{fid}" id="fnref-{fid}">{fid}</a></sup>'
        f'<span class="fn" id="fn-{fid}">'
        f'<a class="fnnum" href="#fnref-{fid}">{fid}</a> {text}</span>'
    )

html_body = re.sub(
    r'<sup id="fnref:([^"]+)"><a class="footnote-ref" href="#fn:[^"]+">\d+</a></sup>',
    replace_ref,
    html_body,
)

page_css = """
/*
 * Formatting modeled on a real FCC Petition for Rulemaking / Request for
 * Waiver filing (Hogan Lovells, for the Association of American Railroads),
 * plus standard legal-filing rules:
 * - Letter size, printed text area not exceeding 6.5 x 9.5 in (1in margins
 *   give a 6.5 x 9 in text area, within that limit).
 * - 12pt minimum, including footnotes.
 * - Double-spaced body text (line-height 2 on a 12pt font gives 24pt of
 *   line pitch, well above the 7/32in (~15.75pt) minimum).
 * - Left-aligned, not justified; first-line-indented paragraphs, no
 *   inter-paragraph gap (spacing comes from the double line height alone).
 * - Caption in plain (non-bold) type; roman-numeral section headings
 *   left-aligned, bold, upper case; lettered subheadings left-aligned,
 *   bold, title case, indented.
 * - No decorative color or shading; black text and rules only. Redlines to
 *   the proposed rule text use underline for insertions (no color).
 */
@page normal {
    size: letter;
    margin: 1in;
    @bottom-center {
        content: counter(page);
        font-family: "Times New Roman", Times, serif;
        font-size: 12pt;
    }
    /* Rule separating the footnote area from the body text above it, drawn
       once per page regardless of how many footnotes land there. Do not
       set a width here -- the @footnote box is the actual footnote content
       area, not just a decorative header, and constraining its width also
       constrains (and badly wraps) every footnote's text. */
    @footnote {
        border-top: 1px solid #000;
        padding-top: 6pt;
        margin-top: 6pt;
    }
}
/* Wide tables (e.g. Table 1's six columns) get their own landscape-oriented
   page so columns have room to breathe instead of cramming into a 6.5in
   portrait text width across three pages. Content must explicitly declare
   `page: normal` (on body) so that whatever follows a `page: landscape`
   block returns to a fresh portrait page -- without it, WeasyPrint just
   keeps appending normal-flow content onto the last-used page orientation. */
@page landscape {
    size: letter landscape;
    margin: 1in;
    @bottom-center {
        content: counter(page);
        font-family: "Times New Roman", Times, serif;
        font-size: 12pt;
    }
    @footnote {
        border-top: 1px solid #000;
        padding-top: 6pt;
        margin-top: 6pt;
    }
}
body { page: normal; orphans: 2; widows: 2; }
.landscape-table { page: landscape; }
html {
    font-family: "Times New Roman", Times, serif;
    font-size: 12pt;
    line-height: 2;
    color: #000;
}
h1, h2, h3 { font-family: "Times New Roman", Times, serif; font-weight: bold; margin: 0; }

/* Default h2 = roman-numeral section headings (I.-VIII.): left-aligned, bold, upper case */
h2 {
    font-size: 12pt;
    text-align: left;
    text-transform: uppercase;
    margin-top: 1.5em;
}
/* Within the front matter, the only two h2s are the doc title and "Table of Contents",
   both centered -- override the default left/uppercase section-heading style for them. */
.frontmatter h2:nth-of-type(1) {
    font-weight: bold;
    text-align: center;
    text-transform: none;
    margin-top: 2.5em;
    margin-bottom: 2.5em;
}
.frontmatter h2:nth-of-type(2) {
    text-align: center;
}
/* Lettered subheadings: left-aligned, bold, title case, indented */
h3 {
    font-size: 12pt;
    text-align: left;
    margin-left: 0.5in;
    margin-top: 1em;
}
p { margin: 0; text-align: left; text-indent: 0.5in; }
/* Lettered sub-items (a., b., ...) under a numbered paragraph, e.g. Section
   VI's list of consequences. Indented as a block, no further first-line
   indent since the "a." literal already serves as the marker. */
.sublist { margin-left: 0.5in; }
.sublist p { text-indent: 0; }
/* Front matter (caption, title block, signature-style intro, TOC) stays
   single-spaced, like a real filing's cover page -- only the substantive
   numbered-paragraph body is double-spaced. */
.frontmatter, .frontmatter p, .signature, .signature p { line-height: 1.15; }
.frontmatter p, .signature p, blockquote p, li p { text-indent: 0; }
/* Extra breathing room between the closing argument paragraph and
   "Respectfully submitted," -- the signature block's first line. */
.signature > p:first-child { margin-top: 2em; }
/* "Before the / FEDERAL COMMUNICATIONS COMMISSION / Washington, DC 20554" --
   the very first paragraph in the front matter. */
.frontmatter > p:first-child { text-align: center; font-weight: bold; }
li p { text-align: left; }
/* Table caption: the bold "Table N. ..." paragraph immediately preceding
   a table, centered and not first-line-indented like ordinary body text. */
.landscape-table > p:first-child {
    text-indent: 0;
    text-align: center;
    margin-bottom: 8pt;
}
table { border-collapse: collapse; width: 100%; margin: 12pt 0; font-size: 12pt; line-height: 1.3; }
/* Never split a single row's cells across a page break -- without this, a
   row can leave some cells' content on one page and the rest blank on the
   next. */
tr { break-inside: avoid; page-break-inside: avoid; }
table th, table td { border: 1px solid #000; padding: 4pt 6pt; vertical-align: top; text-align: left; }
table th { font-weight: bold; }
/* First table in the doc is the FCC caption block -- render borderless, per convention */
body > div.frontmatter > table:first-of-type,
body > div.frontmatter > table:first-of-type th,
body > div.frontmatter > table:first-of-type td {
    border: none;
    padding: 0;
}
body > div.frontmatter > table:first-of-type thead { display: none; }
body > div.frontmatter > table:first-of-type td:first-child { width: 50%; }
blockquote {
    margin: 12pt 0.5in;
    padding-left: 12pt;
    border-left: 1px solid #000;
    font-size: 12pt;
}
hr { border: none; border-top: 1px solid #000; margin: 18pt 0; }
strong { font-weight: bold; }
em { font-style: italic; }
u { text-decoration: underline; }
ol, ul { margin: 0 0 12pt 0; }

/* Table of contents: label, dotted leader, page number. Uses WeasyPrint's
   native leader() generated-content function (CSS Generated Content for
   Paged Media) rather than a flexbox or table-cell row: those box-layout
   approaches broke the leader whenever a label wrapped to two lines (the
   dotted line either vanished or only spanned the last line). leader()
   flows as part of the same inline run as the wrapping label text, so it
   naturally continues on whichever line the label text ends on. */
.toc { margin-top: 1.5em; }
.toc-entry {
    text-indent: 0;
    margin: 6pt 0;
}
.toc-entry.toc-sub { margin-left: 0.5in; }
.toc-entry .dots::after { content: leader(dotted); }
.toc-entry .pagenum {
    text-decoration: none;
    color: #000;
}
.toc-entry .pagenum::after { content: target-counter(attr(href), page); }

/* Real page-bottom footnotes -- 12pt minimum applies to the footnote's
   substantive text (.fn); the reference numeral itself (.fnref, .fnnum) is
   a small superscript locator, conventionally smaller than body text in
   every real filing examined, including the reference filing, and is a
   real clickable link rather than CSS-generated counter content. */
.fn {
    float: footnote;
    font-size: 12pt;
    line-height: 1.3;
    text-indent: 0;
}
.fnref a, .fn .fnnum {
    font-size: 8pt;
    vertical-align: super;
    text-decoration: none;
    color: #000;
}
/* line-height: 0 previously applied here (a leftover from the earlier
   CSS-generated-content design) collapsed these real <a> links' clickable
   hit area to zero height in the rendered PDF -- they looked right but
   were unclickable. Do not reintroduce it on the anchor itself. */
.fn .fnnum { margin-right: 3px; }
/* Suppress WeasyPrint's own auto-generated "1." marker in front of each
   floated footnote -- .fnnum above is our real, clickable replacement. */
::footnote-marker { content: normal; }
/* Also suppress WeasyPrint's auto-generated call marker at the reference
   point itself -- without this, a second, unstyled, plain-sized number
   renders immediately after our real .fnref link at every single
   reference (this was the actual cause of the doubled-up superscript
   numbers throughout the document, not just in tables). */
::footnote-call { content: normal; }
"""

html_doc = f"<html><head><meta charset='utf-8'><style>{page_css}</style></head><body>{html_body}</body></html>"

with open("_petition_render.html", "w") as f:
    f.write(html_doc)

weasyprint.HTML(string=html_doc, base_url=".").write_pdf("Petition_for_Rulemaking.pdf")
print("PDF written: Petition_for_Rulemaking.pdf")
print("Footnotes found:", len(footnote_texts))
