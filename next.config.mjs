import nextra from 'nextra'

const withNextra = nextra({
  defaultShowCopyCode: true,
  search: { codeblocks: false },
})

/** @type {import('next').NextConfig} */
export default withNextra({
  // Fully static: the site is deployed to GitHub Pages, which serves files only.
  // Nothing here needs a Node runtime — no API routes, no ISR, no image optimizer.
  output: 'export',
  reactStrictMode: true,
  cleanDistDir: true,
  // GitHub Pages resolves /participants/filters to participants/filters.html, so
  // extensionless URLs work without a trailing slash — and a trailing slash would
  // create a second indexable URL per page.
  trailingSlash: false,
  images: { unoptimized: true },
})
