"""Render realtime-audio-pc-architecture-and-design-r1.md to the house-styled HTML sibling."""
import html
import re
import sys
from pathlib import Path

SRC = Path(r"E:\dev\corpora\realtime-audio-pc-architecture-and-design-r1.md")
DST = Path(r"E:\dev\corpora\realtime-audio-pc-architecture-and-design-r1.html")

text = SRC.read_text(encoding="utf-8")
lines = text.split("\n")


def slug(s: str) -> str:
    s = re.sub(r"[`*]", "", s)
    s = re.sub(r"[^0-9A-Za-z]+", "-", s).strip("-").lower()
    return s or "sec"


def inline(s: str) -> str:
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+(?:\*(?!\*)[^*]*)*)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])", r"<em>\1</em>", s)
    return s


out = []
toc = []  # (level, text, anchor)
i = 0
in_code = False
code_buf = []
para = []
li_buf = None  # current list item text
li_val = None
list_kind = None  # 'ul' | 'ol'
quote_buf = []
seen_slugs = {}


def uniq(a):
    n = seen_slugs.get(a, 0)
    seen_slugs[a] = n + 1
    return a if n == 0 else f"{a}-{n}"


def flush_para():
    global para
    if para:
        out.append(f"<p>{inline(' '.join(para))}</p>")
        para = []


def flush_item():
    global li_buf, li_val
    if li_buf is not None:
        v = f' value="{li_val}"' if (list_kind == "ol" and li_val is not None) else ""
        out.append(f"<li{v}>{inline(' '.join(li_buf))}</li>")
        li_buf = None
        li_val = None


def close_list():
    global list_kind
    flush_item()
    if list_kind:
        out.append(f"</{list_kind}>")
        list_kind = None


def flush_quote():
    global quote_buf
    if quote_buf:
        out.append(f"<blockquote><p>{inline(' '.join(quote_buf))}</p></blockquote>")
        quote_buf = []


def close_blocks():
    flush_para()
    close_list()
    flush_quote()


def parse_table(rows):
    head_cells = [c.strip() for c in rows[0].strip().strip("|").split("|")]
    body = []
    for r in rows[2:]:
        body.append([c.strip() for c in r.strip().strip("|").split("|")])
    h = "".join(f"<th>{inline(c)}</th>" for c in head_cells)
    b = "".join(
        "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in row) + "</tr>" for row in body
    )
    return (
        '<div class="tablewrap"><table><thead><tr>'
        + h
        + "</tr></thead><tbody>"
        + b
        + "</tbody></table></div>"
    )


while i < len(lines):
    ln = lines[i]

    if in_code:
        if ln.startswith("```"):
            out.append(
                "<pre><code>" + html.escape("\n".join(code_buf), quote=False) + "</code></pre>"
            )
            code_buf = []
            in_code = False
        else:
            code_buf.append(ln)
        i += 1
        continue

    if ln.startswith("```"):
        close_blocks()
        in_code = True
        i += 1
        continue

    # table start
    if (
        ln.lstrip().startswith("|")
        and i + 1 < len(lines)
        and re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1])
    ):
        close_blocks()
        rows = []
        while i < len(lines) and lines[i].lstrip().startswith("|"):
            rows.append(lines[i])
            i += 1
        out.append(parse_table(rows))
        continue

    m = re.match(r"^(#{1,3}) (.*)$", ln)
    if m:
        close_blocks()
        lvl = len(m.group(1))
        txt = m.group(2).strip()
        a = uniq(slug(txt))
        if lvl == 1 and out:  # part heading (not the title)
            toc.append((1, txt, a))
            out.append(f'<h2 class="part" id="{a}">{inline(txt)}</h2>')
        elif lvl == 1:
            out.append(f'<h1 id="{a}">{inline(txt)}</h1>')
        elif lvl == 2:
            toc.append((2, txt, a))
            out.append(f'<h3 class="chap" id="{a}">{inline(txt)}</h3>')
        else:
            out.append(f'<h4 id="{a}">{inline(txt)}</h4>')
        i += 1
        continue

    if ln.strip() == "---":
        close_blocks()
        out.append("<hr>")
        i += 1
        continue

    if ln.startswith("> "):
        flush_para()
        close_list()
        quote_buf.append(ln[2:].strip())
        i += 1
        continue

    mb = re.match(r"^- (.*)$", ln)
    mo = re.match(r"^(\d+)\. (.*)$", ln)
    if mb or mo:
        flush_para()
        flush_quote()
        kind = "ul" if mb else "ol"
        if list_kind != kind:
            close_list()
            out.append(f"<{kind}>")
            list_kind = kind
        else:
            flush_item()
        if mb:
            li_buf = [mb.group(1).strip()]
        else:
            li_buf = [mo.group(2).strip()]
            li_val = mo.group(1)
        i += 1
        continue

    if ln.strip() == "":
        close_blocks()
        i += 1
        continue

    # continuation line
    if li_buf is not None:
        li_buf.append(ln.strip())
    elif quote_buf:
        quote_buf.append(ln.lstrip("> ").strip())
    else:
        para.append(ln.strip())
    i += 1

close_blocks()

body = "\n".join(out)

toc_html = []
for lvl, txt, a in toc:
    short = re.sub(r"\s+—.*$", "", txt)
    cls = "t1" if lvl == 1 else "t2"
    toc_html.append(f'<a class="{cls}" href="#{a}">{inline(short)}</a>')
toc_block = "\n".join(toc_html)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Real-Time Audio on the Unconstrained Machine — child booklet (r1)</title>
<style>
  :root{{
    --paper:#F6F5F0; --panel:#FFFFFF; --ink:#22261F; --mut:#6E7268; --line:#DDDCD4;
    --acc:#46549B; --acc-bg:#EBEDF8; --warm:#8F6E1E; --warm-bg:#F5EEDA; --green:#14705A;
    --serif:Charter,"Bitstream Charter","Iowan Old Style","Sitka Text",Cambria,Georgia,serif;
    --sans:ui-sans-serif,system-ui,"Segoe UI","Helvetica Neue",Arial,sans-serif;
    --mono:ui-monospace,"SF Mono","Cascadia Code",Consolas,monospace;
  }}
  *{{box-sizing:border-box}}
  html{{scroll-behavior:smooth}}
  @media (prefers-reduced-motion: reduce){{ html{{scroll-behavior:auto}} }}
  body{{margin:0;background:var(--paper);color:var(--ink);font-family:var(--sans);font-size:16.5px;line-height:1.68}}
  .wrap{{max-width:900px;margin:0 auto;padding:0 28px}}
  header.page{{padding:52px 0 34px;border-bottom:1px solid var(--line)}}
  .eyebrow{{font-family:var(--mono);font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--mut)}}
  h1{{font-family:var(--serif);font-weight:500;font-size:clamp(30px,4.5vw,46px);line-height:1.12;margin:.35em 0 .3em;text-wrap:balance}}
  .meta{{font-family:var(--mono);font-size:12.5px;color:var(--mut);margin-top:14px}}
  nav.toc{{position:sticky;top:0;z-index:50;background:var(--paper);border-bottom:1px solid var(--line);
    display:flex;gap:4px 14px;flex-wrap:wrap;padding:10px 28px;font-family:var(--mono);font-size:11.5px}}
  nav.toc a{{color:var(--mut);text-decoration:none;padding:2px 6px;border-radius:5px}}
  nav.toc a:hover{{color:var(--ink);background:var(--panel)}}
  nav.toc a.t1{{color:var(--acc);font-weight:600}}
  main{{padding:10px 0 80px}}
  h2.part{{font-family:var(--serif);font-weight:500;font-size:30px;margin:2.2em 0 .4em;padding-top:1.2em;border-top:2px solid var(--ink)}}
  h3.chap{{font-family:var(--serif);font-weight:500;font-size:24px;margin:2em 0 .5em}}
  h4{{font-family:var(--sans);font-weight:650;font-size:16.5px;margin:1.8em 0 .4em}}
  p{{max-width:74ch;margin:.85em 0}}
  li{{max-width:72ch;margin:.45em 0}}
  ul,ol{{padding-left:1.4em}}
  blockquote{{margin:1.2em 0;padding:.7em 1.1em;border-left:3px solid var(--acc);background:var(--acc-bg);border-radius:0 8px 8px 0}}
  blockquote p{{margin:.2em 0;font-family:var(--serif);font-size:17.5px}}
  code{{font-family:var(--mono);font-size:.86em;background:var(--panel);border:1px solid var(--line);border-radius:4px;padding:.08em .3em;white-space:nowrap}}
  pre{{background:#22261F;color:#E8E6DD;border-radius:10px;padding:14px 18px;overflow-x:auto;font-size:13.5px;line-height:1.5}}
  pre code{{background:none;border:none;color:inherit;padding:0;white-space:pre}}
  .tablewrap{{overflow-x:auto;margin:1.2em 0;border:1px solid var(--line);border-radius:10px;background:var(--panel)}}
  table{{border-collapse:collapse;width:100%;font-size:14px}}
  th{{font-family:var(--mono);font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;color:var(--mut);text-align:left;padding:10px 12px;border-bottom:1px solid var(--line);background:var(--paper)}}
  td{{padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}}
  tr:last-child td{{border-bottom:none}}
  td code{{white-space:normal}}
  hr{{border:none;border-top:1px solid var(--line);margin:2.4em 0}}
  strong{{font-weight:650}}
  ::selection{{background:var(--warm-bg)}}
</style>
</head>
<body>
<header class="page"><div class="wrap">
  <div class="eyebrow">E:\\dev\\corpora — child booklet · r1 · 2026-08-12 · parent: embedded C r1.5</div>
  <h1>Real-Time Audio on the Unconstrained Machine</h1>
  <div class="meta">PC-class real-time audio in C · Linux + Windows NT, one codebase · clang/LLVM + MSYS2 CLANG64 · architecture, design, and mechanical sympathy — grounded in the SWE element catalogs</div>
</div></header>
<nav class="toc">{toc_block}</nav>
<main><div class="wrap">
{body}
</div></main>
</body>
</html>
"""

DST.write_text(page, encoding="utf-8")
print(f"wrote {DST} ({DST.stat().st_size} bytes); toc entries: {len(toc)}")
