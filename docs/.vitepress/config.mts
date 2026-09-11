import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

// GitHub Pages project site: https://<user>.github.io/falconx-architecture-docs/
// Local / custom root host: DOCS_BASE=/ npm run docs:dev
const base = process.env.DOCS_BASE ?? '/falconx-architecture-docs/'

export default withMermaid(
  defineConfig({
    base,
    title: 'FalconX Architecture',
    description:
      'Single source of truth for FalconX system architecture — C4, ADRs, catalog, infra, flows',
    lang: 'en-US',
    cleanUrls: true,
    lastUpdated: true,
    ignoreDeadLinks: [
      // Local-only examples in how-to-use
      /^http:\/\/localhost/,
      // Built LikeC4 app (generated into public/ at build time)
      /\/c4-workspace/,
    ],
    themeConfig: {
      nav: [
        { text: 'Home', link: '/' },
        { text: 'How to use', link: '/guide/how-to-use' },
        { text: 'C4', link: '/c4/' },
        {
          text: 'Open diagrams',
          link: '/c4-workspace/',
          target: '_blank',
        },
        { text: 'Catalog', link: '/catalog/services' },
        { text: 'Flows', link: '/flows/' },
        { text: 'Infra', link: '/infra/' },
        { text: 'ADRs', link: '/adr/' },
      ],
      sidebar: {
        '/guide/': [
          {
            text: 'Guide',
            items: [
              { text: 'How to use this site', link: '/guide/how-to-use' },
              { text: 'How we decide', link: '/guide/how-we-decide' },
              { text: 'Reading this site', link: '/guide/reading-this-site' },
              { text: 'Updating the SSOT', link: '/guide/updating-ssot' },
              { text: 'Tooling', link: '/guide/tooling' },
            ],
          },
        ],
        '/c4/': [
          {
            text: 'C4 model',
            items: [
              { text: 'Overview', link: '/c4/' },
              { text: 'Views', link: '/c4/views' },
              { text: 'Interactive workspace', link: '/c4/interactive' },
            ],
          },
        ],
        '/catalog/': [
          {
            text: 'Catalog',
            items: [
              { text: 'Services', link: '/catalog/services' },
              { text: 'Libraries', link: '/catalog/libraries' },
              { text: 'Legacy / excluded', link: '/catalog/legacy' },
            ],
          },
        ],
        '/flows/': [
          {
            text: 'Critical flows',
            items: [
              { text: 'Overview', link: '/flows/' },
              { text: 'Place bet → settle', link: '/flows/place-and-settle' },
              { text: 'Odds ingest', link: '/flows/odds-ingest' },
              { text: 'Catalogue sync', link: '/flows/catalogue-sync' },
            ],
          },
        ],
        '/infra/': [
          {
            text: 'Infrastructure',
            items: [
              { text: 'Overview', link: '/infra/' },
              { text: 'Environments', link: '/infra/environments' },
              { text: 'Data stores', link: '/infra/data-stores' },
              { text: 'Compute & deploy', link: '/infra/compute-and-deploy' },
              { text: 'Networking', link: '/infra/networking' },
              { text: 'Observability', link: '/infra/observability' },
              { text: 'Local & isolated stack', link: '/infra/local-stack' },
            ],
          },
        ],
        '/adr/': [
          {
            text: 'ADRs',
            items: [
              { text: 'Index', link: '/adr/' },
              { text: 'Template', link: '/adr/template' },
              {
                text: '0001 Record architecture decisions',
                link: '/adr/0001-record-architecture-decisions',
              },
              { text: '0002 Git docs as SSOT', link: '/adr/0002-git-docs-as-ssot' },
              { text: '0003 C4 as code with LikeC4', link: '/adr/0003-c4-as-code-likec4' },
            ],
          },
        ],
      },
      socialLinks: [
        {
          icon: 'github',
          link: 'https://github.com/AyushKumar-RFE/falconx-architecture-docs',
        },
      ],
      search: { provider: 'local' },
      editLink: {
        pattern:
          'https://github.com/AyushKumar-RFE/falconx-architecture-docs/edit/main/docs/:path',
        text: 'Edit this page',
      },
      footer: {
        message: 'FalconX architecture SSOT — hosted for the team; edit via pull requests.',
        copyright: 'Internal — RFE Technology',
      },
    },
    mermaid: {},
  }),
)
