# INVOLVO Documentation

Public product documentation for [INVOLVO](https://involvo.io), published at
**https://docs.involvo.io**.

Built with [Nextra 4](https://nextra.site) on the Next.js App Router, exported as a fully
static site and served by GitHub Pages. No server, no database, no API routes — the deployed
artifact is plain HTML, CSS and JS.

## Where things live

INVOLVO's documentation is split across three hosts. Knowing which one you want saves a lot of
time:

| Host | What it is | Edited how |
| --- | --- | --- |
| `involvo.io` | The product itself | the main application repo |
| **`docs.involvo.io`** | **Public product documentation — this repo** | **MDX in `content/`, via pull request** |
| `wiki.involvo.io` | BookStack: internal knowledge, ops runbooks, and the authoritative Legal & Compliance book | the BookStack web UI |

Before 2026-09-03, BookStack answered on `docs.involvo.io`. It now answers on
`wiki.involvo.io`, and this site took over the old hostname. Old BookStack URLs still resolve —
see [Preserved old URLs](#preserved-old-urls).

### What belongs here — and what does not

| Content | Home |
| --- | --- |
| How to find events, apply, take part, publish and run events | **this repo** |
| Internal/team knowledge, engineering and operations runbooks | wiki |
| Legal and compliance documents (Terms, Privacy Policy, Cookie Policy, DPA, RoPA, …) | wiki |

Legal documents are deliberately **not** mirrored here: the wiki is their authoritative home,
and this site links to them rather than duplicating them. There is **no synchronisation**
between the two systems — the MDX in `content/` is the source of truth for this site, and
BookStack is the source of truth for the wiki.

Of the six pages in the wiki's public Legal chapter, only **Privacy Policy** and **Terms of
Service** are visible to anonymous visitors; Cookie Policy, Organizer Terms, Organizer DPA and
Subprocessor List are restricted on the wiki (a deliberate, pre-existing setting, unrelated to
the docs split). This site therefore links only to those two pages plus the book itself. If the
other four are opened up later, add them back to the footer in `app/layout.tsx` and to
`content/platform/index.mdx`.

Also out of scope for now, by decision rather than by accident: **no API reference**, and no
documentation of functionality that does not exist in the product yet.

## Local development

```bash
npm ci             # not `npm install` — see Gotchas
npm run dev        # http://localhost:3000
npm run build      # static export into out/
npm run typecheck  # tsc --noEmit
```

`npm run build` is the check that matters: it is the same command CI runs, and it catches
broken internal links, missing `_meta.ts` entries and MDX syntax errors that `dev` tolerates.

## Structure

```
app/
  layout.tsx           Navbar, footer, <Head> theme colours, site-wide metadata
  [[...mdxPath]]/      Catch-all route that renders content/**/*.mdx
  sitemap.ts           Generated from the page map (pages only, not folders)
  robots.ts
  brand.css            INVOLVO typography and accents on top of nextra-theme-docs
content/               The documentation itself — one .mdx per page, _meta.ts per folder
  get-started/         What INVOLVO is, how it works, accounts, first event
  participants/        Discovering, applying, taking part, meeting people, account
  organizers/          Publishing an event, running an event
  organizations/       Profiles and badges, following, plans and limits
  platform/            Privacy, moderation, Impact Points and Stars
lib/site.ts            Site identity and outbound links (app, wiki) — change hostnames here
public/screenshots/    Product screenshots used in the docs
public/books/          Static redirect stubs for old BookStack URLs (generated)
public/shelves/
tools/                 One-off generator scripts — see Content provenance
```

47 MDX pages in five sections. Sidebar order and section titles come from the `_meta.ts` file
in each folder.

## Writing a page

Every page starts with the same front matter:

```mdx
---
title: "Registration and applications"
description: "Getting into an event on INVOLVO: applying and being selected, registering directly, and what every status along the way means."
theme:
  timestamp: false
---
```

- `title` is the `<h1>`, the sidebar label fallback, the `<title>` and the OG title.
- `description` is the meta description and the OG/Twitter description — write a real sentence,
  it is what shows up in search results.
- `theme.timestamp: false` suppresses the "Last updated" line. This site has no meaningful
  per-page timestamps, so every page sets it.

Then register the page in its folder's `_meta.ts`, which controls both **order** and the
**sidebar label** (often shorter than the title):

```ts
export default {
  index: 'What is INVOLVO',
  'how-involvo-works': 'How INVOLVO works',
  accounts: 'Do I need an account?',
}
```

Conventions worth following:

- **Every folder needs an `index.mdx`.** Nextra renders a folder without one as a dead sidebar
  link, and the folder also lands in the sitemap. All 13 folders have one; adding a folder
  without one reintroduced 287 broken links once already.
- Those landing pages use `<Cards>` from `nextra/components` to link onward, so a reader who
  arrives from search has somewhere to go.
- Internal links are absolute site paths (`/participants/applying/statuses`), never relative.
- The product is written **INVOLVO**, in caps.
- Screenshots go in `public/screenshots/` and are referenced as `/screenshots/<name>.png`, with
  real alt text describing what the image shows.

## Preserved old URLs

`tools/build-redirects.py` generates 54 static stubs under `public/books/**` and
`public/shelves/**` — one per old BookStack URL. Each is an `index.html` with a canonical link,
a `<meta http-equiv="refresh">`, a JS `location.replace`, and `noindex`. Pages that moved here
point at their new route; pages that stayed on the wiki point at `wiki.involvo.io`.

All six legal pages keep a stub so existing bookmarks resolve, even though only two of them are
publicly visible on the wiki.

Re-run the script if the routes change:

```bash
python3 tools/build-redirects.py
```

## SEO

Handled centrally, so pages don't have to think about it: canonical URLs per page,
`metadataBase`, an OG/Twitter card falling back to `/og.png`, a generated `sitemap.xml`
(47 real pages, folders excluded) and `robots.txt`. Both route handlers are
`export const dynamic = 'force-static'` — without that, a static export refuses to build them.

## Content provenance

The initial content was migrated from the "Involvo Help" shelf of the BookStack wiki (7 books,
36 pages) by `tools/build-content.py`, which rewrote the wiki's internal links to this site's
routes and repointed screenshots at `public/screenshots/`. Both scripts in `tools/` are kept
for reference and for regenerating redirects — **neither is a sync**. Edit the MDX directly
from here on.

## Deployment

Pushing to `main` triggers `.github/workflows/deploy.yml`: build the static export, upload it
as a Pages artifact, deploy. `public/CNAME` binds the site to `docs.involvo.io` and
`public/.nojekyll` stops Pages from stripping the `_next` directory. DNS is a CNAME in
Cloudflare; the certificate and "Enforce HTTPS" are managed by GitHub Pages.

Pull requests get a build check (`.github/workflows/build-check.yml`) rather than a preview
URL — GitHub Pages has no per-PR environments.

## Gotchas

**Use `npm ci`, not `npm install`.** `zod` resolves as a nested dependency under
`node_modules/nextra*/`, not at the top level. If a stale hoisted `node_modules/zod` is ever
deleted by hand, `npm install` reports "up to date" while the dev server fails with
`ENOENT … node_modules/zod/index.js`. `npm ci` fixes it.

**`zod` is pinned to `4.3.6`** via `overrides` in `package.json`. Nextra 4.6.1 validates its
theme props with zod, and zod ≥ 4.5 rejects the theme's own `children` schema, which makes
every page fail to render with `Invalid input: expected nonoptional, received undefined`.
Remove the override only after confirming a Nextra release that works with newer zod.

**`trailingSlash: false`.** `/platform` is the canonical URL and returns 200; `/platform/`
returns 404. Link and test without the trailing slash.

**Changing a hostname** means editing `lib/site.ts` and regenerating the redirect stubs. If the
*wiki's* hostname ever changes, note that BookStack bakes absolute URLs into stored page HTML
at save time — updating `APP_URL` there is not enough on its own.
