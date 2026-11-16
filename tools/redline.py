#!/usr/bin/env python3
"""Make a redline: a Word file that shows every change from OLD to NEW as a tracked change.

Uses LibreOffice's Compare Document, so the formatting of NEW is kept.

    python3 tools/redline.py OLD.docx NEW.docx OUT.docx [--author "Name"] [--pdf]

Author. Every tracked change the comparison creates is attributed to track_changes_author in
team.config.yaml (the lead's name if that is empty), with the actual time it was made. Changes
and comments already in NEW keep their own authors. Timestamps are never altered.

Use it to:
- show what changed between two versions (for the lead, co-authors or a funder);
- turn a clean edited copy of an existing Word file into tracked changes against the baseline.

OLD and NEW should hold no tracked changes of their own; accept or reject them first.

Needs LibreOffice. The script finds LibreOffice's own Python when the system Python cannot
import its 'uno' module (as on macOS).
"""

import argparse
import datetime as dt
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from pathlib import Path

LO_PYTHONS = [
    "/Applications/LibreOffice.app/Contents/Resources/python",
    "/usr/lib/libreoffice/program/python",
    "/opt/libreoffice/program/python",
    r"C:\Program Files\LibreOffice\program\python.exe",
]

try:
    import uno  # noqa: F401
    from com.sun.star.beans import PropertyValue
except ImportError:
    if not os.environ.get("AGENT_TEAM_REDLINE_REEXEC"):
        for candidate in LO_PYTHONS:
            if Path(candidate).exists():
                os.environ["AGENT_TEAM_REDLINE_REEXEC"] = "1"
                os.execv(candidate, [candidate, *sys.argv])
    sys.exit("Cannot load LibreOffice's Python bridge (uno). Install LibreOffice, or run this script with its Python.")


def config_value(key):
    """Read a top-level "key: value" from team.config.yaml without a YAML library."""
    here = Path(__file__).resolve().parent.parent
    cfg = here / "team.config.yaml"
    if not cfg.exists():
        return ""
    m = re.search(rf'^{key}:\s*"?([^"#\n]*)"?', cfg.read_text(encoding="utf-8"), re.M)
    return m.group(1).strip() if m else ""


def prop(name, value):
    p = PropertyValue()
    p.Name, p.Value = name, value
    return p


def set_lo_user(ctx, author):
    """Set the LibreOffice user name, which Compare Document writes as the change author."""
    provider = ctx.ServiceManager.createInstanceWithContext("com.sun.star.configuration.ConfigurationProvider", ctx)
    access = provider.createInstanceWithArguments(
        "com.sun.star.configuration.ConfigurationUpdateAccess", (prop("nodepath", "/org.openoffice.UserProfile/Data"),))
    given, _, family = author.rpartition(" ")
    if not given:
        given, family = author, ""
    access.setPropertyValue("givenname", given)
    access.setPropertyValue("sn", family)
    access.commitChanges()


def existing_authors(path):
    with zipfile.ZipFile(path) as z:
        names = set(z.namelist())
        text = "".join(z.read(n).decode("utf-8") for n in ("word/document.xml", "word/comments.xml") if n in names)
    return set(re.findall(r'w:author="([^"]*)"', text))


def compare(old, new, out, author):
    profile = Path(tempfile.mkdtemp(prefix="agentteam_lo_"))
    pipe = f"agentteam_redline_{os.getpid()}"
    proc = subprocess.Popen(["soffice", "--headless", "--invisible", "--nologo", "--norestore",
                             f"-env:UserInstallation={profile.as_uri()}",
                             f"--accept=pipe,name={pipe};urp;StarOffice.ComponentContext"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        local = uno.getComponentContext()
        resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
        for _ in range(60):
            try:
                ctx = resolver.resolve(f"uno:pipe,name={pipe};urp;StarOffice.ComponentContext")
                break
            except Exception:
                time.sleep(1)
        else:
            raise RuntimeError("could not connect to LibreOffice")
        set_lo_user(ctx, author)
        smgr = ctx.ServiceManager
        desktop = smgr.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
        doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(str(new)), "_blank", 0, (prop("Hidden", True),))
        frame = doc.getCurrentController().getFrame()
        dispatcher = smgr.createInstanceWithContext("com.sun.star.frame.DispatchHelper", ctx)
        dispatcher.executeDispatch(frame, ".uno:CompareDocuments", "", 0,
                                   (prop("URL", uno.systemPathToFileUrl(str(old))), prop("NoAcceptDialog", True)))
        doc.storeToURL(uno.systemPathToFileUrl(str(out)), (prop("FilterName", "MS Word 2007 XML"),))
        doc.close(True)
    finally:
        proc.terminate()
        proc.wait(timeout=30)
        shutil.rmtree(profile, ignore_errors=True)


def fix_unattributed(out, author, keep):
    """Attribute changes LibreOffice left without a known author. Authors already in NEW are kept."""
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    tmp = out.with_suffix(".tmp.docx")
    fixed, total = 0, 0
    pattern = re.compile(r'<w:(ins|del|moveFrom|moveTo|rPrChange|pPrChange)\b[^>]*>')

    def repl(m):
        nonlocal fixed, total
        tag = m.group(0)
        total += 1
        name = re.search(r'w:author="([^"]*)"', tag)
        current = name.group(1) if name else ""
        if current == author or (current and current in keep):
            return tag
        fixed += 1
        if name:
            tag = tag.replace(name.group(0), f'w:author="{author}"')
        else:
            tag = tag.replace(f"<w:{m.group(1)}", f'<w:{m.group(1)} w:author="{author}"', 1)
        if 'w:date="' not in tag:
            tag = tag.replace(f'w:author="{author}"', f'w:author="{author}" w:date="{now}"', 1)
        return tag

    with zipfile.ZipFile(out) as zin, zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/document.xml":
                data = pattern.sub(repl, data.decode("utf-8")).encode("utf-8")
            zout.writestr(item, data)
    tmp.replace(out)
    return total, fixed


def main():
    p = argparse.ArgumentParser(description="Make a tracked-change redline between two Word files")
    p.add_argument("old")
    p.add_argument("new")
    p.add_argument("out")
    p.add_argument("--author", default="", help="defaults to track_changes_author in team.config.yaml, then the lead")
    p.add_argument("--pdf", action="store_true", help="also write a PDF of the redline")
    a = p.parse_args()
    author = a.author or config_value("track_changes_author") or config_value("lead")
    if not author:
        sys.exit("No author: set track_changes_author in team.config.yaml or pass --author.")
    old, new, out = (Path(x).resolve() for x in (a.old, a.new, a.out))
    out.parent.mkdir(parents=True, exist_ok=True)
    keep = existing_authors(new)
    compare(old, new, out, author)
    total, fixed = fix_unattributed(out, author, keep)
    print(f"redline written: {out} ({total} tracked-change elements; author {author}"
          + (f"; {fixed} set from an unknown author" if fixed else "") + ")")
    if a.pdf:
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(out.parent), str(out)],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"redline PDF: {out.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
