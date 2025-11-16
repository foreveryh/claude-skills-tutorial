# Complete i18n Setup Example

This document shows the complete file structure and code for a working fumadocs i18n implementation.

## Directory Structure

```
my-fumadocs-project/
├── app/
│   ├── layout.tsx                      # Minimal root layout
│   ├── global.css
│   ├── api/                            # API routes (no lang needed)
│   └── [lang]/                         # Language-specific routes
│       ├── layout.tsx                  # Main layout with i18n provider
│       ├── (home)/
│       │   ├── layout.tsx
│       │   └── page.tsx
│       └── docs/
│           ├── layout.tsx
│           └── [[...slug]]/
│               └── page.tsx
├── content/docs/
│   ├── en/
│   │   ├── index.mdx
│   │   ├── getting-started.mdx
│   │   └── advanced/
│   │       └── configuration.mdx
│   ├── zh/
│   │   ├── index.mdx
│   │   ├── getting-started.mdx
│   │   └── advanced/
│   │       └── configuration.mdx
│   ├── fr/
│   │   └── ...
│   └── ko/
│       └── ...
├── lib/
│   ├── i18n.ts
│   ├── source.ts
│   └── layout.shared.tsx
├── middleware.ts
└── source.config.ts
```

## Complete Code Files

### 1. `lib/i18n.ts`

```typescript
import { defineI18n } from 'fumadocs-core/i18n';

export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'fr', 'ko', 'zh'],
  parser: 'dir',
});
```

### 2. `middleware.ts`

```typescript
import { createI18nMiddleware } from 'fumadocs-core/i18n/middleware';
import { i18n } from '@/lib/i18n';

export default createI18nMiddleware(i18n);

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

### 3. `app/layout.tsx`

```typescript
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
```

### 4. `app/[lang]/layout.tsx`

```typescript
import { RootProvider } from 'fumadocs-ui/provider/next';
import { defineI18nUI } from 'fumadocs-ui/i18n';
import { i18n } from '@/lib/i18n';
import '../global.css';
import { Inter } from 'next/font/google';

const inter = Inter({
  subsets: ['latin'],
});

const { provider } = defineI18nUI(i18n, {
  translations: {
    en: {
      displayName: 'English',
    },
    fr: {
      displayName: 'Français',
      search: 'Rechercher dans la documentation',
    },
    ko: {
      displayName: '한국어',
      search: '문서 검색',
    },
    zh: {
      displayName: '中文',
      search: '搜索文档',
    },
  },
});

export default async function RootLayout({
  params,
  children,
}: {
  params: Promise<{ lang: string }>;
  children: React.ReactNode;
}) {
  const lang = (await params).lang;

  return (
    <html lang={lang} className={inter.className} suppressHydrationWarning>
      <body className="flex flex-col min-h-screen">
        <RootProvider i18n={provider(lang)}>{children}</RootProvider>
      </body>
    </html>
  );
}
```

### 5. `app/[lang]/(home)/layout.tsx`

```typescript
import { HomeLayout } from 'fumadocs-ui/layouts/home';
import { baseOptions } from '@/lib/layout.shared';

export default async function Layout({
  params,
  children,
}: {
  params: Promise<{ lang: string }>;
  children: React.ReactNode;
}) {
  const lang = (await params).lang;

  return <HomeLayout {...baseOptions(lang)}>{children}</HomeLayout>;
}
```

### 6. `app/[lang]/docs/layout.tsx`

```typescript
import { source } from '@/lib/source';
import { DocsLayout } from 'fumadocs-ui/layouts/docs';
import { baseOptions } from '@/lib/layout.shared';

export default async function Layout({
  params,
  children,
}: {
  params: Promise<{ lang: string }>;
  children: React.ReactNode;
}) {
  const lang = (await params).lang;

  return (
    <DocsLayout tree={source.pageTree[lang]} {...baseOptions(lang)}>
      {children}
    </DocsLayout>
  );
}
```

### 7. `app/[lang]/docs/[[...slug]]/page.tsx`

```typescript
import { getPageImage, source } from '@/lib/source';
import {
  DocsBody,
  DocsDescription,
  DocsPage,
  DocsTitle,
} from 'fumadocs-ui/page';
import { notFound } from 'next/navigation';
import { getMDXComponents } from '@/mdx-components';
import type { Metadata } from 'next';
import { createRelativeLink } from 'fumadocs-ui/mdx';

export default async function Page(
  props: PageProps<'/[lang]/docs/[[...slug]]'>,
) {
  const params = await props.params;
  const page = source.getPage(params.slug, params.lang);
  if (!page) notFound();

  const MDX = page.data.body;

  return (
    <DocsPage toc={page.data.toc} full={page.data.full}>
      <DocsTitle>{page.data.title}</DocsTitle>
      <DocsDescription>{page.data.description}</DocsDescription>
      <DocsBody>
        <MDX
          components={getMDXComponents({
            a: createRelativeLink(source, page),
          })}
        />
      </DocsBody>
    </DocsPage>
  );
}

export async function generateStaticParams() {
  return source.generateParams();
}

export async function generateMetadata(
  props: PageProps<'/[lang]/docs/[[...slug]]'>,
): Promise<Metadata> {
  const params = await props.params;
  const page = source.getPage(params.slug, params.lang);
  if (!page) notFound();

  return {
    title: page.data.title,
    description: page.data.description,
    openGraph: {
      images: getPageImage(page).url,
    },
  };
}
```

### 8. `lib/source.ts`

```typescript
import { docs } from '@/.source';
import { type InferPageType, loader } from 'fumadocs-core/source';
import { lucideIconsPlugin } from 'fumadocs-core/source/lucide-icons';
import { i18n } from '@/lib/i18n';

export const source = loader({
  baseUrl: '/docs',
  source: docs.toFumadocsSource(),
  plugins: [lucideIconsPlugin()],
  i18n,
});

export function getPageImage(page: InferPageType<typeof source>) {
  const segments = [...page.slugs, 'image.png'];

  return {
    segments,
    url: `/og/docs/${segments.join('/')}`,
  };
}

export async function getLLMText(page: InferPageType<typeof source>) {
  const processed = await page.data.getText('processed');

  return `# ${page.data.title}

${processed}`;
}
```

### 9. `lib/layout.shared.tsx`

```typescript
import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';
import { i18n } from '@/lib/i18n';

export function baseOptions(locale: string): BaseLayoutProps {
  return {
    nav: {
      title: 'My Documentation',
    },
    i18n,
  };
}
```

### 10. `source.config.ts`

```typescript
import {
  defineConfig,
  defineDocs,
  frontmatterSchema,
  metaSchema,
} from 'fumadocs-mdx/config';

export const docs = defineDocs({
  dir: 'content/docs',
  docs: {
    schema: frontmatterSchema,
    postprocess: {
      includeProcessedMarkdown: true,
    },
  },
  meta: {
    schema: metaSchema,
  },
});

export default defineConfig({
  mdxOptions: {
    // MDX options
  },
});
```

## Sample Content Files

### English: `content/docs/en/index.mdx`

```markdown
---
title: Welcome
description: Get started with our documentation
---

# Welcome to Our Documentation

This is the English version of our documentation.

## Getting Started

Follow these steps to get started:

1. Install dependencies
2. Configure your project
3. Start building!

<Cards>
  <Card title="Quick Start" href="/en/docs/getting-started" />
  <Card title="Configuration" href="/en/docs/advanced/configuration" />
</Cards>
```

### Chinese: `content/docs/zh/index.mdx`

```markdown
---
title: 欢迎
description: 开始使用我们的文档
---

# 欢迎来到我们的文档

这是文档的中文版本。

## 入门指南

按照以下步骤开始：

1. 安装依赖
2. 配置你的项目
3. 开始构建！

<Cards>
  <Card title="快速开始" href="/zh/docs/getting-started" />
  <Card title="配置" href="/zh/docs/advanced/configuration" />
</Cards>
```

### French: `content/docs/fr/index.mdx`

```markdown
---
title: Bienvenue
description: Commencer avec notre documentation
---

# Bienvenue dans notre documentation

Ceci est la version française de notre documentation.

## Démarrage

Suivez ces étapes pour commencer :

1. Installer les dépendances
2. Configurer votre projet
3. Commencer à construire !

<Cards>
  <Card title="Démarrage rapide" href="/fr/docs/getting-started" />
  <Card title="Configuration" href="/fr/docs/advanced/configuration" />
</Cards>
```

### Korean: `content/docs/ko/index.mdx`

```markdown
---
title: 환영합니다
description: 문서 시작하기
---

# 문서에 오신 것을 환영합니다

이것은 문서의 한국어 버전입니다.

## 시작하기

다음 단계를 따라 시작하세요:

1. 의존성 설치
2. 프로젝트 구성
3. 빌드 시작!

<Cards>
  <Card title="빠른 시작" href="/ko/docs/getting-started" />
  <Card title="구성" href="/ko/docs/advanced/configuration" />
</Cards>
```

## Expected Routes

After setup, your application will have these routes:

```
/                           → Redirects to /en
/en                         → English home page
/en/docs                    → English docs index
/en/docs/getting-started    → English getting started
/en/docs/advanced/configuration → English configuration

/zh                         → Chinese home page
/zh/docs                    → Chinese docs index
/zh/docs/getting-started    → Chinese getting started

/fr                         → French home page
/fr/docs                    → French docs index

/ko                         → Korean home page
/ko/docs                    → Korean docs index
```

## Generated Page Tree Structure

```typescript
source.pageTree = {
  en: [
    { type: 'page', name: 'Welcome', url: '/en/docs' },
    { type: 'page', name: 'Getting Started', url: '/en/docs/getting-started' },
    {
      type: 'folder',
      name: 'Advanced',
      children: [
        { type: 'page', name: 'Configuration', url: '/en/docs/advanced/configuration' }
      ]
    }
  ],
  zh: [
    { type: 'page', name: '欢迎', url: '/zh/docs' },
    { type: 'page', name: '入门指南', url: '/zh/docs/getting-started' },
    // ...
  ],
  fr: [...],
  ko: [...]
}
```

## Testing Your Setup

### Build Test

```bash
npm run build
```

Expected output should include:
```
Route (app)
├ ○ /_not-found
├ ƒ /[lang]
├ ● /[lang]/docs/[[...slug]]
│ ├ /en/docs
│ ├ /en/docs/getting-started
│ ├ /en/docs/advanced/configuration
│ ├ /zh/docs
│ ├ /zh/docs/getting-started
│ ├ /fr/docs
│ └ /ko/docs
```

### Development Server Test

```bash
npm run dev
```

Visit:
- http://localhost:3000 → Should redirect to /en
- http://localhost:3000/en/docs → English docs
- http://localhost:3000/zh/docs → Chinese docs
- Language switcher in top-right should show all 4 languages

---

This complete example demonstrates a fully working fumadocs i18n setup.
