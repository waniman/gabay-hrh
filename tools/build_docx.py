#!/usr/bin/env python3
"""Build a Word file (and optionally a PDF) from a Markdown master copy.

Needs pandoc. The PDF needs LibreOffice (soffice). Python standard library otherwise.

    python3 tools/build_docx.py --source project/wp/WP1-concept-note/work/draft.md --out project/wp/WP1-concept-note/work/exports/draft.docx \
        [--refs project/wp/WP1-concept-note/work/references.csv] [--cite superscript] \
        [--reference-doc template.docx] [--font "Times New Roman" --size 12 --double-spacing] \
        [--line-numbers] [--page-numbers] [--pdf]

Citations. Write [@key] or [@key1; @key2] in the Markdown. With --refs (a CSV with columns
key and citation, one verified entry per source), keys are numbered in order of first citation,
ranges are compressed ([1, 3-5]) and the reference list is placed at the line
<!-- references --> or, if that line is absent, at the end. An unknown key stops the build.
The exact text rendered is saved next to the output as <name>.numbered.md, for checks.

A journal manuscript usually needs:
    --font "Times New Roman" --size 12 --double-spacing --line-numbers --page-numbers
"""

import argparse
import csv
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def compress(nums):
    nums = sorted(set(nums))
    parts, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        if j > i + 1:
            parts.append(f"{nums[i]}-{nums[j]}")
        elif j == i + 1:
            parts += [str(nums[i]), str(nums[j])]
        else:
            parts.append(str(nums[i]))
        i = j + 1
    return ", ".join(parts)


def number_citations(text, refs_path, style):
    with open(refs_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        if not {"key", "citation"} <= set(reader.fieldnames or []):
            sys.exit(f"{refs_path} needs the columns 'key' and 'citation'.")
        refs = {r["key"].strip(): r["citation"].strip() for r in reader if r["key"].strip()}
    order, unknown = [], []

    def repl(m):
        keys = [k.strip().lstrip("@") for k in m.group(1).split(";")]
        nums = []
        for k in keys:
            if k not in refs:
                unknown.append(k)
                continue
            if k not in order:
                order.append(k)
            nums.append(order.index(k) + 1)
        if not nums:
            return m.group(0)
        return f"^{compress(nums).replace(' ', '')}^" if style == "superscript" else f"[{compress(nums)}]"

    body = re.sub(r"\[(@[^\]]+)\]", repl, text)
    if unknown:
        sys.exit(f"Unknown citation keys (not in {refs_path}): {', '.join(sorted(set(unknown)))}")
    reflist = "# References\n\n" + "\n".join(f"{i + 1}. {refs[k]}" for i, k in enumerate(order)) + "\n"
    if "<!-- references -->" in body:
        body = body.replace("<!-- references -->", reflist, 1)
    else:
        body = body.rstrip() + "\n\n" + reflist
    return body, order


def patch_styles(styles, font, size, double):
    if font:
        styles = re.sub(r"<w:rFonts\b[^>]*/>",
                        f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:eastAsia="{font}" w:cs="{font}"/>', styles)
    rpr = ""
    if font:
        rpr += f'<w:rFonts w:ascii="{font}" w:hAnsi="{font}" w:eastAsia="{font}" w:cs="{font}"/>'
    if size:
        half = int(round(float(size) * 2))
        rpr += f'<w:sz w:val="{half}"/><w:szCs w:val="{half}"/>'
    ppr = '<w:spacing w:after="120" w:line="480" w:lineRule="auto"/>' if double else ""
    defaults = (f"<w:docDefaults><w:rPrDefault><w:rPr>{rpr}</w:rPr></w:rPrDefault>"
                f"<w:pPrDefault><w:pPr>{ppr}</w:pPr></w:pPrDefault></w:docDefaults>")
    if re.search(r"<w:docDefaults>.*?</w:docDefaults>", styles, re.S):
        styles = re.sub(r"<w:docDefaults>.*?</w:docDefaults>", defaults, styles, count=1, flags=re.S)
    else:
        styles = re.sub(r"(<w:styles\b[^>]*>)", r"\1" + defaults, styles, count=1)
    if double:
        # Body text styles carry their own spacing; give them double line spacing too.
        styles = re.sub(r'(<w:style w:type="paragraph"[^>]*w:styleId="(?:BodyText|FirstParagraph|Normal)".*?<w:spacing\b)([^>]*?)(/>)',
                        lambda m: m.group(1) + re.sub(r'\sw:line(Rule)?="[^"]*"', "", m.group(2)) + ' w:line="480" w:lineRule="auto"' + m.group(3),
                        styles, flags=re.S)
    return styles


def rewrite_docx(path, edit):
    """Apply edit(name, text) -> text to the XML parts of a .docx, in place."""
    tmp = path.with_suffix(".tmp.docx")
    with zipfile.ZipFile(path) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        names = zin.namelist()
        extra = edit("__names__", names) or {}
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename.endswith(".xml") or item.filename.endswith(".rels"):
                data = edit(item.filename, data.decode("utf-8")).encode("utf-8")
            zout.writestr(item, data)
        for name, text in extra.items():
            zout.writestr(name, text)
    tmp.replace(path)


# Elements that follow lnNumType inside w:sectPr, in schema order. Word rejects out-of-order children.
AFTER_LNNUM = ("pgNumType", "cols", "formProt", "vAlign", "noEndnote", "titlePg", "textDirection", "bidi",
               "rtlGutter", "docGrid", "printerSettings", "sectPrChange")


def patch_section(block, line_numbers, page_numbers):
    opening = re.match(r"<w:sectPr\b[^>]*>", block).group(0)
    if page_numbers and 'w:footerReference w:type="default"' not in block:
        # Header and footer references come first in a section.
        block = block.replace(opening, opening + '<w:footerReference w:type="default" r:id="rIdAgentTeamFooter"/>', 1)
    if line_numbers and "<w:lnNumType" not in block:
        tag = '<w:lnNumType w:countBy="1" w:restart="continuous"/>'
        m = re.search(r"<w:(?:%s)\b" % "|".join(AFTER_LNNUM), block)
        block = block[:m.start()] + tag + block[m.start():] if m else block.replace("</w:sectPr>", tag + "</w:sectPr>")
    return block


def add_numbering(path, line_numbers, page_numbers):
    footer = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:ftr xmlns:w="{W_NS}"><w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
              '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
              '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r><w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:ftr>')

    def edit(name, text):
        if name == "__names__":
            return {"word/agentteam_footer.xml": footer} if page_numbers else {}
        if name == "word/_rels/document.xml.rels" and page_numbers:
            return text.replace("</Relationships>", f'<Relationship Id="rIdAgentTeamFooter" Type="{R_NS}/footer" Target="agentteam_footer.xml"/></Relationships>')
        if name == "[Content_Types].xml" and page_numbers:
            return text.replace("</Types>", '<Override PartName="/word/agentteam_footer.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/></Types>')
        if name == "word/document.xml":
            text = re.sub(r"<w:sectPr(\s[^>]*)?/>", lambda m: f"<w:sectPr{m.group(1) or ''}></w:sectPr>", text)
            text = re.sub(r"<w:sectPr\b[^>]*>.*?</w:sectPr>", lambda m: patch_section(m.group(0), line_numbers, page_numbers),
                          text, flags=re.S)
            if page_numbers and "xmlns:r=" not in text[:3000]:
                text = text.replace("<w:document ", f'<w:document xmlns:r="{R_NS}" ', 1)
        return text

    rewrite_docx(path, edit)


def main():
    p = argparse.ArgumentParser(description="Build a Word file from Markdown")
    p.add_argument("--source", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--refs", help="CSV with columns key, citation")
    p.add_argument("--cite", choices=["brackets", "superscript"], default="brackets")
    p.add_argument("--reference-doc", help="a .docx whose styles the output should use")
    p.add_argument("--font")
    p.add_argument("--size", type=float)
    p.add_argument("--double-spacing", action="store_true")
    p.add_argument("--line-numbers", action="store_true")
    p.add_argument("--page-numbers", action="store_true")
    p.add_argument("--pdf", action="store_true", help="also write a PDF with LibreOffice")
    a = p.parse_args()

    if not shutil.which("pandoc"):
        sys.exit("pandoc is not installed. Install it (https://pandoc.org) and run again.")
    src, out = Path(a.source), Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    text = src.read_text(encoding="utf-8")
    order = []
    if a.refs:
        text, order = number_citations(text, a.refs, a.cite)
    numbered = out.with_name(out.stem + ".numbered.md")
    numbered.write_text(text, encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmp:
        ref = Path(tmp) / "reference.docx"
        if a.reference_doc:
            shutil.copy(a.reference_doc, ref)
        else:
            subprocess.run(["pandoc", "-o", str(ref), "--print-default-data-file", "reference.docx"], check=True)
        if a.font or a.size or a.double_spacing:
            rewrite_docx(ref, lambda name, t: patch_styles(t, a.font, a.size, a.double_spacing)
                         if name == "word/styles.xml" else ({} if name == "__names__" else t))
        subprocess.run(["pandoc", str(numbered), "-o", str(out), "--reference-doc", str(ref),
                        "--resource-path", os.pathsep.join([str(src.parent.resolve()), str(Path.cwd())])], check=True)

    if a.line_numbers or a.page_numbers:
        add_numbering(out, a.line_numbers, a.page_numbers)
    print(f"built {out}" + (f" with {len(order)} references" if a.refs else "") + f"; rendered text in {numbered}")

    if a.pdf:
        if not shutil.which("soffice"):
            sys.exit("LibreOffice (soffice) is not installed; the PDF was not made.")
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out.parent), str(out)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"built {out.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
