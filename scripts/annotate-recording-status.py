#!/usr/bin/env python3
"""Label unrecorded lectures in the site output without changing course sources."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--package", type=Path, required=True)
    parser.add_argument("--site", type=Path, required=True)
    args = parser.parse_args()
    package = args.package.resolve()
    site = args.site.resolve()
    course = json.loads((package / "course.json").read_text(encoding="utf-8"))
    manifest = json.loads((site / "site-manifest.json").read_text(encoding="utf-8"))
    expected = {(a["id"], a["type"]) for m in course["modules"] for a in m["activities"]}
    found = {(a["id"], a["type"]) for m in manifest["modules"] for a in m["activities"]}
    if expected != found:
        raise SystemExit("site manifest activity IDs/types do not match the source package")
    notice = (
        '<small class="permissions-notice">'
        '© 2026 Robert Hodgkinson. All rights reserved. Viewing permitted; reuse requires '
        'prior written permission. Contact '
        '<a href="mailto:hodgkinr@gmail.com">hodgkinr@gmail.com</a>.'
        '</small>'
    )
    for page in site.rglob("*.html"):
        html = page.read_text(encoding="utf-8")
        # Keep this notice outside the footer so iframe mode can hide course chrome
        # while retaining the attribution and permission contact.
        html = re.sub(r'<small class="permissions-notice">.*?</small>', "", html, count=1)
        html, count = re.subn(r"</footer>", "</footer>" + notice, html, count=1)
        if count != 1:
            raise SystemExit(f"could not place permissions notice on {page.relative_to(site)}")
        page.write_text(html, encoding="utf-8")

    stylesheet = site / "style.css"
    if not stylesheet.is_file():
        raise SystemExit("site stylesheet is missing")
    css = stylesheet.read_text(encoding="utf-8")
    if ".permissions-notice" not in css:
        stylesheet.write_text(
            css.rstrip() + "\n.permissions-notice{display:block;margin-top:.25rem;font-size:.75rem;line-height:1.4}\n",
            encoding="utf-8",
        )

    annotated = 0
    for module in course["modules"]:
        for activity in module["activities"]:
            if activity["type"] != "lecture" or activity.get("video_url"):
                continue
            script = activity.get("script")
            if not script or not (package / script).is_file():
                raise SystemExit(f"unrecorded lecture {activity['id']} has no readable script")
            site_activity = next(
                a for m in manifest["modules"] for a in m["activities"] if a["id"] == activity["id"]
            )
            page = (site / site_activity["site_path"]).resolve()
            if not page.is_relative_to(site) or not page.is_file():
                raise SystemExit(f"unsafe or missing lecture page for {activity['id']}")
            html = page.read_text(encoding="utf-8")
            if "recording-status" not in html:
                note = ('<p class="recording-status" role="status">'
                        'Recording not yet available. Read the lecture script below.'
                        '</p>')
                html, count = re.subn(r"</h1>", "</h1>" + note, html, count=1)
                if count != 1:
                    raise SystemExit(f"could not place recording note on {activity['id']}")
                page.write_text(html, encoding="utf-8")
            annotated += 1
    print(f"Marked {annotated} unrecorded lecture pages; course source was not changed.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
