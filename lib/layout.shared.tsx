import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';
import { i18n } from '@/lib/i18n';

export function baseOptions(locale: string): BaseLayoutProps {
  return {
    nav: {
      title: 'Claude Skills',
    },
    links: [
      {
        text: 'Why',
        url: `/${locale}/docs`,
        active: 'nested-url',
      },
      {
        text: 'How',
        url: `/${locale}/docs/automated-workflows`,
        active: 'nested-url',
      },
      {
        text: 'Author',
        url: `/${locale}/docs/about`,
        active: 'nested-url',
      },
      {
        text: 'GitHub',
        url: 'https://github.com/foreveryh/claude-skills-tutorial',
        external: true,
      },
    ],
    i18n,
  };
}
