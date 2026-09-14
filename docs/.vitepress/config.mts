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
        { text: 'Feature flags', link: '/feature-flags/' },
        { text: 'Infra', link: '/infra/' },
        { text: 'ADRs', link: '/adr/' },
      ],
      sidebar: {
        '/c4/': [
          {
            text: 'C4 model',
            items: [
              { text: 'Overview', link: '/c4/' },
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
        '/feature-flags/': [
          {
            text: 'Feature flags',
            items: [{ text: 'Overview', link: '/feature-flags/' }],
          },
        ],
        '/infra/': [
          {
            text: 'Handbook',
            items: [
              { text: 'Overview', link: '/infra/' },
              { text: 'Visual map', link: '/infra/diagrams' },
              { text: 'Environments', link: '/infra/environments' },
              { text: 'Kubernetes', link: '/infra/kubernetes' },
              { text: 'Networking', link: '/infra/networking' },
              { text: 'Data stores', link: '/infra/data-stores' },
              { text: 'Dependencies', link: '/infra/dependencies' },
              { text: 'IAM & secrets', link: '/infra/iam-and-secrets' },
              { text: 'Compute & deploy', link: '/infra/compute-and-deploy' },
              { text: 'Observability', link: '/infra/observability' },
              { text: 'Where to change', link: '/infra/changes' },
              { text: 'Provisioning', link: '/infra/provisioning' },
              { text: 'Troubleshooting', link: '/infra/troubleshooting' },
              { text: 'Local & isolated stack', link: '/infra/local-stack' },
            ],
          },
          {
            text: 'Repos',
            items: [
              { text: 'Four repos', link: '/infra/repos/' },
              { text: 'Creating things', link: '/infra/repos/creating' },
              { text: 'tf-modules', link: '/infra/repos/tf-modules' },
              { text: 'rfetech-infra', link: '/infra/repos/rfetech-infra' },
              { text: 'rfetech-gitops', link: '/infra/repos/rfetech-gitops' },
              { text: 'rfetech-github-actions', link: '/infra/repos/rfetech-github-actions' },
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
