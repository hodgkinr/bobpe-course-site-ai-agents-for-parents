# Reproducible course-to-site-to-Canvas workflow

This repository assembles one course package, but the steps apply to any valid Course Package Specification 1.0.0 course.

## 1. Author and validate a package

Create a self-contained package directory with `course.json`, Markdown content, quiz JSON, and relative local assets. Keep stable IDs independent of display order. Validate with the shared tool:

```sh
course-package validate /path/to/course-package
```

The schema and validator enforce the package contract; course-specific requirements such as a fixed weekly quiz length can be checked separately by the course authoring project.

## 2. Generate the site

Install the package spec and publisher into a local environment (non-editable installation keeps their repositories read-only), then run:

```sh
course-publisher build \
  --package /path/to/course-package \
  --theme generic \
  --output /tmp/course-site-build
```

Select `cu-boulder` or `colorado-state` instead of `generic` for those visual palettes. The output path must not already exist. The publisher validates input and writes a static site plus `site-manifest.json`; it does not deploy.

For this demonstration course, `./scripts/build-site.sh generic` performs the build in temporary staging and installs only the result under this repository's `site/` directory. It adds a site-level notice for unrecorded lectures while preserving scripts from the package.

## 3. Preview and prepare Pages

Serve the generated output locally with `python3 -m http.server 8000` from the output directory. Review the home page, all module and activity routes, local assets, quiz interactions, and the `?embed=1` presentation. Before a first release, establish the final Pages base URL and verify that every manifest `site_path` resolves under it. This repository's Pages workflow is manual-only and was not dispatched as part of implementation.

## 4. Generate a Canvas cartridge

After the site URL is established and the publisher manifest is available, provide the Canvas exporter with the course package, generated `site-manifest.json`, a separate Canvas mapping/config file, and a new explicit output path. For example:

```sh
course-canvas-export \
  --package /path/to/course-package \
  --site-manifest /path/to/site/site-manifest.json \
  --canvas-config /path/to/canvas-mapping.json \
  --output /tmp/course.imscc \
  --dry-run
```

Use the exporter's actual CLI help and configuration example for the installed version. Review the dry-run inventory and generated ZIP/XML checks before handing the cartridge to an authorized Canvas administrator. The initial implementation targets unpublished Canvas objects and Classic Quizzes with QTI 1.2; New Quizzes compatibility is not claimed. Deterministic IDs can overwrite existing Canvas objects on re-import, so select a sandbox and scope deliberately. No Canvas import is performed by the build workflow.

## Boundaries

Keep package source, publisher, site artifact, and Canvas configuration separate. Theme choice belongs to the publisher invocation. Do not embed secrets in a course package or site. Publishing to Pages and importing into Canvas are human-controlled release actions.
