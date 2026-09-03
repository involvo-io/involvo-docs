import type { MetadataRoute } from 'next'

// Required by `output: 'export'` — these are generated once at build time.
export const dynamic = 'force-static'
import { getPageMap } from 'nextra/page-map'
import { SITE } from '../lib/site'

/**
 * Flattens Nextra's page map into the routes that actually have a page.
 * Folders carry `children` and, unless they hold an `index` file, have no page of
 * their own — listing those would put 404s in the sitemap.
 */
function collectRoutes(items: any[], acc: string[] = []): string[] {
  for (const item of items) {
    if (Array.isArray(item.children)) {
      collectRoutes(item.children, acc)
      continue
    }
    if (typeof item.route === 'string' && !item.route.includes('#')) acc.push(item.route)
  }
  return acc
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const pageMap = await getPageMap()
  const routes = Array.from(new Set(collectRoutes(pageMap as any[])))
  const now = new Date()
  return routes.map((route) => ({
    url: `${SITE.url}${route === '/' ? '' : route}`,
    lastModified: now,
    changeFrequency: 'monthly' as const,
    priority: route === '/' ? 1 : route.split('/').length === 2 ? 0.8 : 0.6,
  }))
}
