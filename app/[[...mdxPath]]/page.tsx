import { generateStaticParamsFor, importPage } from 'nextra/pages'
import { useMDXComponents as getMDXComponents } from '../../mdx-components'

export const generateStaticParams = generateStaticParamsFor('mdxPath')

type PageProps = Readonly<{ params: Promise<{ mdxPath: string[] }> }>

export async function generateMetadata(props: PageProps) {
  const params = await props.params
  const { metadata } = await importPage(params.mdxPath)
  const path = params.mdxPath?.length ? `/${params.mdxPath.join('/')}` : '/'
  return {
    ...metadata,
    // The home page's own title is already the site title; running it through the
    // "%s — INVOLVO Docs" template would print the brand twice.
    ...(path === '/' ? { title: { absolute: 'INVOLVO Documentation' } } : {}),
    alternates: { canonical: path },
    // Page front matter supplies title/description; the card image is site-wide, and
    // spreading the page's own openGraph would otherwise drop it.
    openGraph: {
      ...(metadata.openGraph ?? {}),
      url: path,
      images: [{ url: '/og.png', width: 1200, height: 630, alt: 'INVOLVO Documentation' }],
    },
    twitter: {
      card: 'summary_large_image' as const,
      images: ['/og.png'],
    },
  }
}

// `wrapper` is optional in the MDXComponents type but always provided by nextra-theme-docs.
const Wrapper = getMDXComponents().wrapper!

export default async function Page(props: PageProps) {
  const params = await props.params
  const result = await importPage(params.mdxPath)
  // `rest` carries toc, metadata and sourceCode — all required by the theme wrapper.
  const { default: MDXContent, ...rest } = result
  return (
    <Wrapper {...rest}>
      <MDXContent {...props} params={params} />
    </Wrapper>
  )
}
