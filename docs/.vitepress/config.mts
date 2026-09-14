import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

// GitHub Pages: https://<user>.github.io/falconx-architecture-docs/
// Local root preview: DOCS_BASE=/ npm run docs:dev
const base = process.env.DOCS_BASE ?? '/falconx-architecture-docs/'

export default withMermaid(
  defineConfig({
    base,
    title: 'BigBash Architecture',
    description:
      'Architecture documentation for BigBash, That Act as a single source of truth for any info related to the architecture and infrastructure.',
    lang: 'en-US',
    cleanUrls: true,
    lastUpdated: true,
    ignoreDeadLinks: [
      // Built LikeC4 app (generated into public/ at build time)
      /\/c4-workspace/,
    ],
    themeConfig: {
      nav: [
        { text: 'Home', link: '/' },
        { text: 'C4', link: '/c4/' },
        {
          text: 'Open C4 Diagrams',
          link: '/c4-workspace/',
          target: '_blank',
        },
        { text: 'Catalog', link: '/catalog/services' },
        { text: 'Infra', link: '/infra/' },
        { text: 'ADRs', link: '/adr/' },
      ],
      sidebar: {
        '/c4/': [
          {
            text: 'C4 model',
            items: [
              { text: 'Overview', link: '/c4/' }
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
          link: 'https://github.com/AyushKumar-RFE/bigbash-architecture-docs',
        },
      ],
      search: { provider: 'local' },
      editLink: {
        pattern:
          'https://github.com/AyushKumar-RFE/bigbash-architecture-docs/edit/main/docs/:path',
        text: 'Edit this page',
      },
      footer: {
        message: 'BigBash architecture SSOT — hosted for the team; edit via pull requests.',
        copyright: 'Internal — RFE Technology',
      },
    },
    mermaid: {},
  }),
)
