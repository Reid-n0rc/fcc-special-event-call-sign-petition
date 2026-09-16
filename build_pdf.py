import re
import markdown
import weasyprint

with open("PETITION.md") as f:
    src = f.read()

# Convert markdown (with footnotes + tables extensions) to HTML.
html_body = markdown.markdown(
    src,
    extensions=["footnotes", "tables"],
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
# stripped endnote list.
html_body = re.sub(r'(<hr\s*/?>\s*)?<h2>Footnotes</h2>\s*$', "", html_body.rstrip())

# Replace each inline footnote reference marker
#   <sup id="fnref:N"><a class="footnote-ref" href="#fn:N">N</a></sup>
# with a WeasyPrint CSS float-footnote span carrying the actual footnote text.
def replace_ref(m):
    fid = m.group(1)
    text = footnote_texts.get(fid, "")
    return f'<span class="fn">{text}</span>'

html_body = re.sub(
    r'<sup id="fnref:([^"]+)"><a class="footnote-ref" href="#fn:[^"]+">\d+</a></sup>',
    replace_ref,
    html_body,
)

page_css = """
/*
 * Standard legal / FCC filing formatting:
 * - Letter size, printed text area not exceeding 6.5 x 9.5 in (1in margins
 *   give a 6.5 x 9 in text area, within that limit).
 * - 12pt minimum, including footnotes.
 * - Double-spaced body text (line-height 2 on a 12pt font gives 24pt of
 *   line pitch, well above the 7/32in (~15.75pt) minimum).
 * - Left-aligned, not justified.
 * - No decorative color or shading; black text and rules only.
 */
@page {
    size: letter;
    margin: 1in;
    @bottom-center {
        content: counter(page);
        font-family: "Times New Roman", Times, serif;
        font-size: 12pt;
    }
}
html {
    font-family: "Times New Roman", Times, serif;
    font-size: 12pt;
    line-height: 2;
    color: #000;
}
body { orphans: 2; widows: 2; }
h1, h2, h3 { font-family: "Times New Roman", Times, serif; font-weight: bold; }
h1 {
    font-size: 13pt;
    text-align: center;
    margin-top: 0;
}
h2 {
    font-size: 12pt;
    text-align: center;
    margin-top: 1.5em;
}
h3 {
    font-size: 12pt;
    margin-top: 1em;
}
p { margin: 0 0 12pt 0; text-align: left; }
li p { text-align: left; }
table { border-collapse: collapse; width: 100%; margin: 12pt 0; font-size: 12pt; line-height: 1.3; }
table th, table td { border: 1px solid #000; padding: 4pt 6pt; vertical-align: top; text-align: left; }
table th { font-weight: bold; }
/* First table in the doc is the FCC caption block -- render borderless, per convention */
body > table:first-of-type, body > table:first-of-type td {
    border: none;
    padding: 0;
}
body > table:first-of-type td:first-child { width: 75%; }
blockquote {
    margin: 12pt 24pt;
    padding-left: 12pt;
    border-left: 1px solid #000;
    font-size: 12pt;
}
hr { border: none; border-top: 1px solid #000; margin: 18pt 0; }
strong { font-weight: bold; }
em { font-style: italic; }
ol, ul { margin: 0 0 12pt 0; }

/* Real page-bottom footnotes -- 12pt minimum applies to footnotes too */
.fn {
    float: footnote;
    font-size: 12pt;
    line-height: 1.3;
}
::footnote-marker {
    content: counter(footnote);
    font-size: 12pt;
    vertical-align: super;
    line-height: 0;
}
::footnote-call {
    content: counter(footnote);
    font-size: 12pt;
    vertical-align: super;
    line-height: 0;
}
"""

html_doc = f"<html><head><meta charset='utf-8'><style>{page_css}</style></head><body>{html_body}</body></html>"

with open("_petition_render.html", "w") as f:
    f.write(html_doc)

weasyprint.HTML(string=html_doc, base_url=".").write_pdf("Petition_for_Rulemaking.pdf")
print("PDF written: Petition_for_Rulemaking.pdf")
print("Footnotes found:", len(footnote_texts))
