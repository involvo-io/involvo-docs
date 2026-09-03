# INVOLVO Documentation

Public product documentation for [INVOLVO](https://involvo.io), published at
**https://docs.involvo.io**.

Built with [Nextra 4](https://nextra.site) (Next.js App Router), exported as a static site and
served by GitHub Pages.

## What belongs here — and what does not

| Content | Home |
| --- | --- |
| Public product documentation — how to find events, apply, take part, publish and run events | **this repo** → docs.involvo.io |
| Internal/team knowledge, engineering and operations runbooks | BookStack → wiki.involvo.io |
| Legal and compliance documents (Terms, Privacy Policy, Cookie Policy, DPA, RoPA, …) | BookStack → wiki.involvo.io |

Legal documents are deliberately **not** mirrored here: the wiki is their authoritative home,
and this site links to them rather than duplicating them. There is no synchronisation between
the two systems — the MDX in `content/` is the source of truth for this site.

## Local development

```bash
npm install
npm run dev        # http://localhost:3000
npm run build      # static export into out/
npm run typecheck
```

## Structure

```
app/                  Next.js App Router entry: layout, catch-all MDX route, robots, sitemap
  brand.css           INVOLVO typography and accents on top of nextra-theme-docs
content/              The documentation itself — one .mdx per page, _meta.ts per folder
  get-started/        What INVOLVO is, how it works, accounts, first event
  participants/       Discovering, applying, taking part, meeting people, account
  organizers/         Publishing an event, running an event
  organizations/      Profiles and badges, following, plans and limits
  platform/           Privacy, moderation, Impact Points and Stars
lib/site.ts           Site identity and outbound links (app, wiki)
public/screenshots/   Product screenshots used in the docs
tools/build-content.py One-off migration script (see below)
```

Sidebar order and section titles live in the `_meta.ts` file of each folder.

## Content provenance

The initial content was migrated from the "Involvo Help" shelf of the internal BookStack wiki
(7 books, 36 pages) using `tools/build-content.py`, which rewrote the wiki's internal links to
this site's routes and repointed screenshots at `public/screenshots/`. That script is kept for
reference only — **it is not a sync**. Edit the MDX directly from here on.

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`, which builds the static export and
publishes it to GitHub Pages. `public/CNAME` binds the site to `docs.involvo.io`, and
`public/.nojekyll` stops Pages from stripping the `_next` directory.

Pull requests get a build check (`.github/workflows/build-check.yml`) rather than a preview
URL — GitHub Pages has no per-PR environments.

## A pinned dependency worth knowing about

`package.json` pins `zod` to `4.3.6` via `overrides`. Nextra 4.6.1 validates its theme props
with zod, and zod ≥ 4.5 rejects the theme's own `children` schema, which makes every page fail
to render with `Invalid input: expected nonoptional, received undefined`. Remove the override
only after confirming a Nextra release that works with the newer zod.
