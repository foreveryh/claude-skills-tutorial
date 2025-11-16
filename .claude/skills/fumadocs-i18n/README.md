# Fumadocs Internationalization (i18n) Implementation Guide

This guide provides a step-by-step process to implement complete internationalization in a Fumadocs project, based on official fumadocs documentation and real-world testing.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites Check](#prerequisites-check)
3. [Step-by-Step Implementation](#step-by-step-implementation)
4. [Verification & Testing](#verification--testing)
5. [Troubleshooting](#troubleshooting)
6. [Reference](#reference)

## Overview

This implementation will:
- Set up multi-language routing with Next.js App Router
- Add a language switcher to the navigation
- Ensure sidebar shows only current language content
- Organize content in language-specific directories
- Follow fumadocs official best practices

**Supported Languages (default):**
- English (en) - Default
- Chinese (zh) - Simplified
- French (fr)
- Korean (ko)

**Estimated Time:** 15-20 minutes for complete setup

## Prerequisites Check

Before starting, verify the project structure:

```bash
# Check current directory structure
ls -la app/
ls -la content/docs/
ls -la lib/

# Verify package.json has required dependencies
grep -E "fumadocs-core|fumadocs-ui|fumadocs-mdx" package.json
```

Required dependencies:
- `fumadocs-core` (>=16.0.0)
- `fumadocs-ui` (>=16.0.0)
- `fumadocs-mdx` (>=13.0.0)
- `next` (>=14.0.0)

## Step-by-Step Implementation

### Step 1: Create i18n Configuration

**File:** `lib/i18n.ts`

```typescript
import { defineI18n } from 'fumadocs-core/i18n';

export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'fr', 'ko', 'zh'],
  parser: 'dir', // CRITICAL: Use 'dir' for directory-based language structure
});
```

**Why `parser: 'dir'`?**
- Directory structure: `content/docs/en/`, `content/docs/zh/`, etc.
- Alternative `parser: 'dot'` is for file-based: `page.en.mdx`, `page.zh.mdx`
- See: https://fumadocs.dev/docs/headless/page-conventions#internationalization

### Step 2: Create Middleware

**File:** `middleware.ts` (root directory)

```typescript
import { createI18nMiddleware } from 'fumadocs-core/i18n/middleware';
import { i18n } from '@/lib/i18n';

export default createI18nMiddleware(i18n);

export const config = {
  // Matcher ignoring `/_next/`, `/api/`, and static assets
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

**What this does:**
- Redirects `/` to `/en` (default language)
- Detects browser language preference
- Handles language switching
- Rewrites URLs for proper routing

### Step 3: Restructure App Directory

#### 3.1 Create `[lang]` Dynamic Route

```bash
mkdir -p app/[lang]
```

#### 3.2 Create Main Layout with i18n

**File:** `app/[lang]/layout.tsx`

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

**Key Points:**
- `defineI18nUI` sets up language switcher
- `translations` object defines display names for each language
- `provider(lang)` passes current language to RootProvider
- This enables the language switcher dropdown in the UI

#### 3.3 Move Existing Routes

```bash
# Move (home) route
mv app/(home) app/[lang]/(home)

# Move docs route
mv app/docs app/[lang]/docs
```

#### 3.4 Update Root Layout

**File:** `app/layout.tsx`

```typescript
// Minimal root layout - actual layout is in app/[lang]/layout.tsx
export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
```

**Why?**
- Root layout should be minimal when using `[lang]` routing
- Actual HTML/body rendering happens in `app/[lang]/layout.tsx`
- This prevents hydration issues

### Step 4: Update Layouts for i18n

#### 4.1 Update Home Layout

**File:** `app/[lang]/(home)/layout.tsx`

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

#### 4.2 Update Docs Layout

**File:** `app/[lang]/docs/layout.tsx`

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

**CRITICAL:** `source.pageTree[lang]`
- This ensures sidebar only shows current language content
- Without `[lang]`, sidebar would show all languages mixed together

#### 4.3 Update Docs Page

**File:** `app/[lang]/docs/[[...slug]]/page.tsx`

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

**Key Changes:**
- `PageProps<'/[lang]/docs/[[...slug]]'>` - Updated path type
- `source.getPage(params.slug, params.lang)` - Pass language parameter
- `generateStaticParams()` - Automatically generates routes for all languages

### Step 5: Update Source Configuration

#### 5.1 Update lib/source.ts

**File:** `lib/source.ts`

```typescript
import { docs } from '@/.source';
import { type InferPageType, loader } from 'fumadocs-core/source';
import { lucideIconsPlugin } from 'fumadocs-core/source/lucide-icons';
import { i18n } from '@/lib/i18n';

export const source = loader({
  baseUrl: '/docs',
  source: docs.toFumadocsSource(),
  plugins: [lucideIconsPlugin()],
  i18n, // Add i18n configuration
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

**CRITICAL:** Adding `i18n` to `loader()`
- Enables multi-language page tree generation
- Creates `source.pageTree[lang]` for each language
- Required for language-specific sidebars

#### 5.2 Update lib/layout.shared.tsx

**File:** `lib/layout.shared.tsx`

```typescript
import type { BaseLayoutProps } from 'fumadocs-ui/layouts/shared';
import { i18n } from '@/lib/i18n';

export function baseOptions(locale: string): BaseLayoutProps {
  return {
    nav: {
      title: 'Your App Name',
    },
    i18n, // Pass i18n configuration
  };
}
```

**Changes:**
- Accept `locale: string` parameter
- Add `i18n` to returned options
- This enables language switcher in navigation

### Step 6: Organize Content by Language

#### 6.1 Create Language Directories

```bash
mkdir -p content/docs/en
mkdir -p content/docs/zh
mkdir -p content/docs/fr
mkdir -p content/docs/ko
```

#### 6.2 Move Existing Content

```bash
# Move any existing content to English directory
mv content/docs/*.mdx content/docs/en/ 2>/dev/null || true
mv content/docs/*/ content/docs/en/ 2>/dev/null || true
```

#### 6.3 Create Placeholder Content

For each language, create an `index.mdx`:

**English** (`content/docs/en/index.mdx`):
```markdown
---
title: Welcome
description: Your first document
---

Welcome to the documentation!

## What's Next?

<Cards>
  <Card title="Learn more about Next.js" href="https://nextjs.org/docs" />
  <Card title="Learn more about Fumadocs" href="https://fumadocs.dev" />
</Cards>
```

**Chinese** (`content/docs/zh/index.mdx`):
```markdown
---
title: 欢迎
description: 你的第一个文档
---

欢迎来到文档！

## 下一步是什么？

<Cards>
  <Card title="了解更多关于 Next.js" href="https://nextjs.org/docs" />
  <Card title="了解更多关于 Fumadocs" href="https://fumadocs.dev" />
</Cards>
```

**French** (`content/docs/fr/index.mdx`):
```markdown
---
title: Bienvenue
description: Votre premier document
---

Bienvenue dans la documentation !

## Et ensuite ?

<Cards>
  <Card title="En savoir plus sur Next.js" href="https://nextjs.org/docs" />
  <Card title="En savoir plus sur Fumadocs" href="https://fumadocs.dev" />
</Cards>
```

**Korean** (`content/docs/ko/index.mdx`):
```markdown
---
title: 환영합니다
description: 첫 번째 문서
---

문서에 오신 것을 환영합니다!

## 다음 단계는?

<Cards>
  <Card title="Next.js에 대해 더 알아보기" href="https://nextjs.org/docs" />
  <Card title="Fumadocs에 대해 더 알아보기" href="https://fumadocs.dev" />
</Cards>
```

**Directory Structure:**
```
content/docs/
├── en/
│   ├── index.mdx
│   └── ...other docs
├── zh/
│   ├── index.mdx
│   └── ...other docs
├── fr/
│   ├── index.mdx
│   └── ...other docs
└── ko/
    ├── index.mdx
    └── ...other docs
```

### Step 7: Clean Up and Build

#### 7.1 Remove Build Cache

```bash
rm -rf .next
rm -rf .source  # fumadocs-mdx generated files
```

#### 7.2 Build and Test

```bash
npm run build
```

**Expected Output:**
```
Route (app)
├ ○ /_not-found
├ ƒ /[lang]
├ ● /[lang]/docs/[[...slug]]
│ ├ /en/docs
│ ├ /zh/docs
│ ├ /fr/docs
│ └ /ko/docs
├ ƒ /api/search
└ ...
```

✅ **Success Indicators:**
- Routes include `/en/docs`, `/zh/docs`, `/fr/docs`, `/ko/docs`
- No TypeScript errors
- Build completes successfully

## Verification & Testing

### Test Checklist

1. **Language Switcher**
   - [ ] Visible in top-right corner of navigation
   - [ ] Shows "EN", "ZH", "FR", "KO" or display names
   - [ ] Dropdown shows all available languages
   - [ ] Clicking switches to correct language

2. **URL Routing**
   - [ ] Root `/` redirects to `/en`
   - [ ] `/en/docs` loads English content
   - [ ] `/zh/docs` loads Chinese content
   - [ ] `/fr/docs` loads French content
   - [ ] `/ko/docs` loads Korean content

3. **Sidebar Content**
   - [ ] English sidebar only shows English pages
   - [ ] Chinese sidebar only shows Chinese pages
   - [ ] French sidebar only shows French pages
   - [ ] Korean sidebar only shows Korean pages
   - [ ] No mixed language content in sidebar

4. **Build & Development**
   - [ ] `npm run build` succeeds without errors
   - [ ] `npm run dev` starts without errors
   - [ ] No hydration mismatches in browser console
   - [ ] Hot reload works correctly

### Manual Testing

```bash
# Start development server
npm run dev

# Test URLs
open http://localhost:3000          # Should redirect to /en
open http://localhost:3000/en/docs  # English docs
open http://localhost:3000/zh/docs  # Chinese docs
open http://localhost:3000/fr/docs  # French docs
open http://localhost:3000/ko/docs  # Korean docs
```

### Debugging

**Check generated page tree:**

```typescript
// In browser console or Node.js:
console.log(Object.keys(source.pageTree));
// Expected: ['en', 'zh', 'fr', 'ko']

console.log(source.pageTree.en);
// Should show English page tree only
```

## Troubleshooting

### Problem: Sidebar Shows All Languages

**Symptom:** Sidebar displays "En", "Fr", "Ko", "Zh" folders/items

**Cause:** Not using language-filtered page tree

**Solution:**
```typescript
// ❌ Wrong
<DocsLayout tree={source.pageTree} {...baseOptions(lang)}>

// ✅ Correct
<DocsLayout tree={source.pageTree[lang]} {...baseOptions(lang)}>
```

### Problem: Routes are `/en/docs/en` Instead of `/en/docs`

**Symptom:** Double language prefix in URLs

**Cause:** Missing `parser: 'dir'` in i18n config

**Solution:**
```typescript
// lib/i18n.ts
export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'fr', 'ko', 'zh'],
  parser: 'dir', // ADD THIS LINE
});
```

Then rebuild:
```bash
rm -rf .next .source
npm run build
```

### Problem: Language Switcher Not Visible

**Symptom:** No language dropdown in navigation

**Cause 1:** Missing `i18n` in `baseOptions()`

**Solution:**
```typescript
// lib/layout.shared.tsx
export function baseOptions(locale: string): BaseLayoutProps {
  return {
    nav: { title: 'Your App' },
    i18n, // ADD THIS LINE
  };
}
```

**Cause 2:** Not passing i18n provider to RootProvider

**Solution:**
```typescript
// app/[lang]/layout.tsx
<RootProvider i18n={provider(lang)}>{children}</RootProvider>
```

### Problem: Build Errors About Language Not Supported

**Symptom:** Error messages like "Language 'ko' is not supported"

**Cause:** OG image generation doesn't support Korean/Chinese fonts

**Impact:** ⚠️ Warning only - does not affect core functionality

**Solution:** This is expected and can be safely ignored. To suppress:
- Images will fall back to default font
- Core i18n features work perfectly
- Only affects Open Graph preview images

### Problem: Middleware Deprecation Warning

**Symptom:** `⚠ The "middleware" file convention is deprecated. Please use "proxy" instead.`

**Cause:** Next.js 16 naming change

**Impact:** ⚠️ Warning only - middleware still works

**Solution:** Wait for fumadocs to update, or rename when ready:
```bash
# Future (when fumadocs supports it):
mv middleware.ts proxy.ts
```

### Problem: Content Not Updating After Adding Language

**Cause:** Cached generated files

**Solution:**
```bash
rm -rf .next .source
npm run dev
```

## Reference

### Official Documentation

- **Fumadocs i18n (Next.js):** https://fumadocs.dev/docs/ui/internationalization/next
- **Fumadocs Core i18n:** https://fumadocs.dev/docs/headless/internationalization
- **Page Conventions:** https://fumadocs.dev/docs/headless/page-conventions

### File Structure Summary

```
your-project/
├── app/
│   ├── layout.tsx                      # Minimal root layout
│   └── [lang]/
│       ├── layout.tsx                  # Main i18n layout
│       ├── (home)/
│       │   ├── layout.tsx              # Home layout with lang param
│       │   └── page.tsx
│       └── docs/
│           ├── layout.tsx              # Docs layout with lang param
│           └── [[...slug]]/
│               └── page.tsx            # Page with lang param
├── content/docs/
│   ├── en/                             # English content
│   │   ├── index.mdx
│   │   └── ...
│   ├── zh/                             # Chinese content
│   ├── fr/                             # French content
│   └── ko/                             # Korean content
├── lib/
│   ├── i18n.ts                         # i18n configuration
│   ├── source.ts                       # Source loader with i18n
│   └── layout.shared.tsx               # Layout options with i18n
├── middleware.ts                       # i18n middleware
└── source.config.ts                    # Fumadocs MDX config
```

### Key Configuration Values

| File | Key Configuration | Purpose |
|------|------------------|---------|
| `lib/i18n.ts` | `parser: 'dir'` | Parse languages from directory structure |
| `lib/source.ts` | `i18n` in `loader()` | Enable multi-language page trees |
| `lib/layout.shared.tsx` | `i18n` in return | Enable language switcher |
| `app/[lang]/docs/layout.tsx` | `tree={source.pageTree[lang]}` | Filter sidebar by language |
| `app/[lang]/layout.tsx` | `i18n={provider(lang)}` | Pass language to RootProvider |

## Success Checklist

After completing this guide, you should have:

- ✅ Language switcher in navigation (top-right dropdown)
- ✅ Clean URLs: `/en/docs`, `/zh/docs`, `/fr/docs`, `/ko/docs`
- ✅ Language-filtered sidebars (no mixing of languages)
- ✅ Middleware auto-redirecting `/` to default language
- ✅ Content organized in language directories
- ✅ Build succeeding without errors
- ✅ All routes generating correctly
- ✅ TypeScript types working properly

## Next Steps

After setting up i18n:

1. **Add More Content**
   - Create pages in each language directory
   - Use `meta.json` to organize sidebar navigation

2. **Customize Translations**
   - Update display names in `defineI18nUI()`
   - Add more UI translations (search placeholders, etc.)

3. **Add More Languages**
   - Add language code to `languages` array in `lib/i18n.ts`
   - Create corresponding directory in `content/docs/`
   - Add translation in `defineI18nUI()`

4. **Configure Search**
   - Set up i18n for your search solution
   - See: https://fumadocs.dev/docs/headless/search/orama#internationalization

## Need Help?

If you encounter issues not covered in this guide:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review fumadocs official documentation
3. Check your file structure matches the expected layout
4. Verify all configurations have been applied
5. Clear build cache and rebuild

---

**Last Updated:** 2025-11-16
**Fumadocs Version:** 16.0.11+
**Next.js Version:** 16.0.1+
