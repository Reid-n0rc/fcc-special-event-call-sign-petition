import html
import os
import re

import markdown

REPO_URL = "https://github.com/Reid-n0rc/fcc-special-event-call-sign-petition"
PDF_URL = f"{REPO_URL}/raw/main/Petition_for_Rulemaking.pdf"
OUT_DIR = "site"

with open("PETITION.md") as f:
    src = f.read()

body = markdown.markdown(
    src,
    extensions=["footnotes", "tables", "toc", "md_in_html"],
    extension_configs={"footnotes": {"BACKLINK_TITLE": "Back to reference %d"}},
)

# The PDF's table of contents uses CSS leaders and page numbers, which mean
# nothing on a web page. Turn each entry into a plain link to its heading.
def toc_entry(m):
    sub = " toc-sub" if "toc-sub" in m.group(1) else ""
    return f'<li class="toc-item{sub}"><a href="{m.group(3)}">{m.group(2)}</a></li>'

body = re.sub(
    r'<div class="toc-entry([^"]*)"><span>(.*?)</span><span class="dots"></span>'
    r'<a class="pagenum" href="([^"]+)"></a></div>',
    toc_entry,
    body,
)
body = body.replace('<div class="toc">', '<nav class="toc" aria-label="Table of contents"><ol>', 1)
body = re.sub(r'(<li class="toc-item[^"]*">.*?</li>)\s*</div>', r'\1</ol></nav>', body, count=1, flags=re.S)

# The toc extension's own generated table of contents is unused.
body = re.sub(r'<div class="toc">.*?</div>', "", body, flags=re.S)

# The "Footnotes" heading introduced the PDF's footnote list; python-markdown
# renders the notes themselves at the end, so give them a proper heading.
body = re.sub(r'(<hr\s*/?>\s*)?<h2[^>]*>Footnotes</h2>\s*', "", body)
body = body.replace('<div class="footnote">', '<section class="footnote" aria-label="Footnotes"><h2 id="footnotes">Footnotes</h2>', 1)
body = re.sub(r'</ol>\s*</div>\s*$', "</ol></section>", body.rstrip())

# Make every bare URL inside the footnotes a real link.
def linkify_urls(section):
    return re.sub(
        r'(?<!href=")(?<!">)(https?://[^\s<)"]+)',
        lambda m: f'<a href="{m.group(1)}">{m.group(1)}</a>',
        section,
    )

fn_start = body.find('<section class="footnote"')
if fn_start != -1:
    body = body[:fn_start] + linkify_urls(body[fn_start:])

# Wide tables scroll sideways on narrow screens instead of breaking the layout,
# except the borderless caption table in the front matter.
body = body.replace("<table>", '<div class="table-scroll"><table>').replace("</table>", "</table></div>")
caption_at = body.find('<div class="table-scroll"><table>', body.find('<div class="frontmatter">'))
caption_end = body.find("</table></div>", caption_at)
body = (
    body[:caption_at]
    + '<table class="caption">'
    + body[caption_at + len('<div class="table-scroll"><table>'):caption_end]
    + "</table>"
    + body[caption_end + len("</table></div>"):]
)

title = "Special Event Call Sign Petition"
description = (
    "Petition for Rulemaking asking the FCC to authorize extended amateur radio "
    "special event call sign formats alongside the 1x1 format."
)

css = """
:root {
  --bg: #fbfaf7; --fg: #1d1b18; --muted: #5c574f; --rule: #d9d4ca;
  --link: #1f4f8a; --panel: #f1eee7; --mark: #fff3c4;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #16181c; --fg: #e8e6e1; --muted: #a8a39a; --rule: #3a3d44;
    --link: #8fb8ee; --panel: #1f2227; --mark: #4a3f14;
  }
}
:root[data-theme="dark"] {
  --bg: #16181c; --fg: #e8e6e1; --muted: #a8a39a; --rule: #3a3d44;
  --link: #8fb8ee; --panel: #1f2227; --mark: #4a3f14;
}
* { box-sizing: border-box; }
html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0; background: var(--bg); color: var(--fg);
  font-family: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, "Times New Roman", serif;
  font-size: 18px; line-height: 1.6;
}
a { color: var(--link); }
.bar {
  border-bottom: 1px solid var(--rule); background: var(--panel);
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 15px;
}
.bar-inner {
  max-width: 46rem; margin: 0 auto; padding: 0.75rem 16px;
  display: flex; flex-wrap: wrap; gap: 0.5rem 1.25rem; align-items: center; justify-content: space-between;
}
.bar strong { font-weight: 600; }
.bar nav { display: flex; gap: 1rem; flex-wrap: wrap; }
main { max-width: 46rem; margin: 0 auto; padding: 2rem 16px 4rem; }
.draft-note {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 15px; color: var(--muted); border-left: 3px solid var(--rule);
  padding: 0.25rem 0 0.25rem 0.75rem; margin: 0 0 2rem;
}
.frontmatter > p:first-child { text-align: center; font-weight: 700; letter-spacing: 0.02em; }
table.caption { border-collapse: collapse; margin: 1.5rem auto; width: 100%; }
table.caption td { border: 0; padding: 0 0.5rem; vertical-align: top; }
table.caption td:last-child { white-space: nowrap; width: 1%; }
table.caption thead { display: none; }
.frontmatter h2 { text-align: center; }
h1, h2, h3 { line-height: 1.3; }
h2 { font-size: 1.25rem; text-transform: uppercase; letter-spacing: 0.03em; margin: 2.5rem 0 1rem; }
h3 { font-size: 1.1rem; margin: 2rem 0 0.75rem; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 2rem 0; }
nav.toc ol { list-style: none; padding: 0; margin: 0; }
nav.toc li { margin: 0.35rem 0; }
nav.toc li.toc-sub { padding-left: 1.5rem; }
p { margin: 0 0 1rem; }
blockquote {
  margin: 1.5rem 0; padding: 0.75rem 1rem; background: var(--panel);
  border-left: 3px solid var(--rule);
}
blockquote p { margin: 0 0 0.75rem; }
blockquote u { text-decoration-thickness: 1.5px; text-underline-offset: 3px; }
.sublist { margin-left: 1.5rem; }
.table-scroll { overflow-x: auto; margin: 1.5rem 0; -webkit-overflow-scrolling: touch; }
.table-scroll table { border-collapse: collapse; min-width: 40rem; font-size: 15px; line-height: 1.45; }
.table-scroll th, .table-scroll td { border: 1px solid var(--rule); padding: 0.5rem 0.6rem; text-align: left; vertical-align: top; }
.table-scroll th { background: var(--panel); }
.landscape-table > p:first-child, .table-block > p:first-child { text-align: center; margin-bottom: 0.5rem; }
.signature { margin-top: 2.5rem; }
.signature p { margin: 0 0 0.5rem; }
.verification { margin-top: 2.5rem; }
sup { line-height: 0; }
sup a, a.footnote-ref { text-decoration: none; }
.footnote { margin-top: 3rem; border-top: 1px solid var(--rule); font-size: 16px; }
.footnote ol { padding-left: 1.75rem; }
.footnote li { margin: 0 0 0.75rem; overflow-wrap: anywhere; }
.footnote li p { margin: 0; }
.footnote-backref { text-decoration: none; margin-left: 0.25rem; }
:target { background: var(--mark); }
@media (max-width: 600px) {
  body { font-size: 17px; }
  main { padding-top: 1.25rem; }
  h2 { font-size: 1.1rem; }
}
"""

favicon = (
    "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'>"
    "<text y='.9em' font-size='90'>📡</text></svg>"
)

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(description)}">
<link rel="icon" href="{favicon}">
<style>{css}</style>
</head>
<body>
<header class="bar">
  <div class="bar-inner">
    <strong>Petition for Rulemaking: Special Event Call Signs</strong>
    <nav>
      <a href="{PDF_URL}">Download PDF</a>
      <a href="{REPO_URL}">GitHub</a>
    </nav>
  </div>
</header>
<main>
<p class="draft-note">Draft petition, not yet filed with the FCC. The PDF is the formatted filing copy; this page shows the same text for reading online.</p>
{body}
</main>
</body>
</html>
"""

os.makedirs(OUT_DIR, exist_ok=True)
with open(os.path.join(OUT_DIR, "index.html"), "w") as f:
    f.write(page)
print(f"Wrote {OUT_DIR}/index.html")
