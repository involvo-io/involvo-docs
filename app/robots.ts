import type { MetadataRoute } from 'next'

// Required by `output: 'export'` — these are generated once at build time.
export const dynamic = 'force-static'
import { SITE } from '../lib/site'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [{ userAgent: '*', allow: '/' }],
    sitemap: `${SITE.url}/sitemap.xml`,
    host: SITE.url,
  }
}
