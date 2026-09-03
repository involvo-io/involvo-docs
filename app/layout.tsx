import type { Metadata } from 'next'
import { Footer, Layout, Navbar } from 'nextra-theme-docs'
import { Head } from 'nextra/components'
import { getPageMap } from 'nextra/page-map'
import Image from 'next/image'
import { GeistSans } from 'geist/font/sans'
import { GeistMono } from 'geist/font/mono'
import 'nextra-theme-docs/style.css'
import './brand.css'
import { SITE } from '../lib/site'

export const metadata: Metadata = {
  metadataBase: new URL(SITE.url),
  title: {
    default: SITE.title,
    template: `%s — ${SITE.name} Docs`,
  },
  description: SITE.description,
  applicationName: SITE.name,
  generator: 'Nextra',
  alternates: { canonical: './' },
  openGraph: {
    type: 'website',
    siteName: `${SITE.name} Documentation`,
    locale: 'en_GB',
    url: './',
    title: SITE.title,
    description: SITE.description,
    images: [{ url: '/og.png', width: 1200, height: 630, alt: `${SITE.name} Documentation` }],
  },
  twitter: {
    card: 'summary_large_image',
    title: SITE.title,
    description: SITE.description,
    images: ['/og.png'],
  },
  robots: { index: true, follow: true },
  icons: { icon: '/icon.png', apple: '/icon.png' },
}

const navbar = (
  <Navbar
    logo={
      <span className="involvo-logo">
        <Image src="/logo.png" alt="INVOLVO" width={132} height={33} priority />
        <span className="involvo-logo__label">Docs</span>
      </span>
    }
    logoLink={SITE.url}
    projectLink={SITE.app}
    projectIcon={<span className="involvo-navlink">Open INVOLVO</span>}
  />
)

const footer = (
  <Footer>
    <div className="involvo-footer">
      <p>
        <strong>{SITE.name}</strong> — join events, shape your future.
      </p>
      <p className="involvo-footer__links">
        <a href={SITE.app}>Platform</a>
        <a href={`${SITE.wiki}/books/legal-documentation/page/terms-of-service`}>Terms of Service</a>
        <a href={`${SITE.wiki}/books/legal-documentation/page/privacy-policy`}>Privacy Policy</a>
        <a href={`${SITE.wiki}/books/legal-documentation`}>Legal Documentation</a>
      </p>
      <p className="involvo-footer__meta">© {new Date().getFullYear()} INVOLVO</p>
    </div>
  </Footer>
)

export default async function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html
      lang="en"
      dir="ltr"
      className={`${GeistSans.variable} ${GeistMono.variable}`}
      suppressHydrationWarning
    >
      <Head
        color={{ hue: 210, saturation: 90, lightness: { light: 45, dark: 60 } }}
        backgroundColor={{ light: '#f7f7f7', dark: '#0a0a0a' }}
      >
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <body>
        {/* editLink / feedback / lastUpdated are switched off deliberately: this is
            product documentation, not a wiki — no edit links, no comments, no revision
            metadata. */}
        <Layout
          navbar={navbar}
          footer={footer}
          pageMap={await getPageMap()}
          docsRepositoryBase="https://github.com/involvo-io/involvo-docs/tree/main"
          editLink={null}
          feedback={{ content: null }}
          darkMode
          sidebar={{ defaultMenuCollapseLevel: 1, autoCollapse: true, toggleButton: true }}
          toc={{ backToTop: 'Back to top', title: 'On this page', float: true }}
          navigation={{ prev: true, next: true }}
        >
          {children}
        </Layout>
      </body>
    </html>
  )
}
