# AI Agents for Parents — course site

This repository assembles the static website for the three-week **AI Agents for Parents** demonstration course. The instructional source of truth lives in the separate `bobpe-course-design-ai-workforce/ai-agents-for-parents` package. The renderer is `bobpe-course-publisher`; validation and the frozen package contract are in `bobpe-course-package-spec` (v1.0.0).

The `site/` directory is generated output. Do not edit course text there: update the source package and rebuild. The build script stages output in a temporary directory and replaces only this repository's `site/` directory after a successful build. It never writes to the source, publisher, or specification repositories.

No course videos have been recorded. Lecture pages contain the written lecture content and full script, display a clear recording-unavailable note, and do not link to nonexistent video files.

## Local setup

The three repositories are expected as sibling directories beneath one parent directory. Override the source course location with `COURSE_PACKAGE_DIR` if needed.

```sh
python3 -m venv .venv
.venv/bin/python -m pip install ../bobpe-course-package-spec ../bobpe-course-publisher
./scripts/build-site.sh generic
```

The install is non-editable and installs packages into this repository's ignored `.venv`; it does not modify the two source repositories. The selected build theme is only the initial fallback: every generated page contains all three themes and a header selector. Learners can switch themes without a rebuild; `?theme=generic`, `?theme=cu-boulder`, and `?theme=colorado-state` select themes on direct links. Theme choice changes presentation only. The same package and stable activity routes are used for every theme.

Set `SITE_BASE_URL` to the canonical Pages URL when it is known (for example, `SITE_BASE_URL=https://owner.github.io/repository ./scripts/build-site.sh generic`) to include canonical `site_url` values in the manifest. Omit it until the URL is confirmed. The publisher validates the package before output is created. Its output includes `index.html`, module and activity pages, `style.css`, and `site-manifest.json`. The manifest uses stable IDs and explicit paths. By default it omits canonical `site_url` values; set `SITE_BASE_URL` once the final GitHub Pages URL is confirmed.

## Preview

After building, run a local static server from the generated directory:

```sh
cd site
python3 -m http.server 8000
```

Open <http://localhost:8000/>. Check an activity page in Canvas-style embed mode by appending `?embed=1` to its URL. Stop the local server with Ctrl+C.

## Rebuild after course edits

1. Update the course package in the design repository and validate it with `course-package validate /path/to/ai-agents-for-parents`.
2. Run `./scripts/build-site.sh generic` (or choose `cu-boulder` / `colorado-state`).
3. Review the generated `site/` and `site/site-manifest.json`; verify the theme selector, all activities, and any referenced assets. Test a direct activity URL with `?theme=cu-boulder&embed=1` and navigate between course pages to confirm both parameters persist.
4. To prepare a Pages release, review the changed files, choose the repository's intended GitHub Pages environment and URL, and have an owner explicitly authorize the deployment. The included Pages workflow is manual-only (`workflow_dispatch`) and has not been run.

The workflow deploys only the committed `site/` artifact when manually dispatched. Do not dispatch it until the site, URL, access, and release timing have been approved. A publicly accessible Pages site from a private source repository requires a GitHub plan that supports private-repository Pages publishing; verify the account plan before setup. The source repositories should remain private under the current project policy.

## Quiz and Canvas notes

Quizzes are formative and scored entirely in the browser. The page supports radio-button answers, submission, score reporting, option-specific feedback, correct-answer explanations, unanswered-question prompts, and reset/retry. As with any client-scored public quiz, correct answers are inspectable in the page source. No accounts, tracking, or backend are used.

`site/site-manifest.json` is the interface for the standalone Canvas exporter. It contains one entry for each source activity and each `site_path` is relative to the generated site root. The exporter should combine those paths with the deployed site base URL and use `?embed=1` for embedded pages. No Canvas import is performed by this repository.

The generic, CU Boulder-inspired, and Colorado State-inspired themes are publisher palettes, not official brand certification. No logos or institution-specific instructional content are duplicated here.

## Usage, permissions, and third-party materials

Copyright © 2026 Robert Hodgkinson. All rights reserved. The published educational website may be viewed; reproduction, modification, redistribution, republication, or commercial reuse of original course/site materials requires prior written permission. Contact [hodgkinr@gmail.com](mailto:hodgkinr@gmail.com). The generated site uses local HTML/CSS and contains no external images or media. GitHub Actions and Python build/test dependencies retain their own licenses; the All Rights Reserved notice does not claim rights over them. See `LICENSE.md`.
