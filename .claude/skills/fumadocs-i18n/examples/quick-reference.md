# Quick Reference - Fumadocs i18n

Fast reference for common tasks and configurations.

## Quick Start Commands

```bash
# 1. Create i18n config
cat > lib/i18n.ts << 'EOF'
import { defineI18n } from 'fumadocs-core/i18n';

export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'fr', 'ko', 'zh'],
  parser: 'dir',
});
EOF

# 2. Create middleware
cat > middleware.ts << 'EOF'
import { createI18nMiddleware } from 'fumadocs-core/i18n/middleware';
import { i18n } from '@/lib/i18n';

export default createI18nMiddleware(i18n);

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
EOF

# 3. Restructure app directory
mkdir -p app/[lang]
mv app/(home) app/[lang]/(home)
mv app/docs app/[lang]/docs

# 4. Create language directories
mkdir -p content/docs/{en,zh,fr,ko}

# 5. Clean and rebuild
rm -rf .next .source
npm run build
```

## Essential Code Snippets

### lib/i18n.ts
```typescript
import { defineI18n } from 'fumadocs-core/i18n';

export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'fr', 'ko', 'zh'],
  parser: 'dir', // CRITICAL
});
```

### app/[lang]/layout.tsx
```typescript
const { provider } = defineI18nUI(i18n, {
  translations: {
    en: { displayName: 'English' },
    zh: { displayName: '中文', search: '搜索文档' },
    fr: { displayName: 'Français', search: 'Rechercher' },
    ko: { displayName: '한국어', search: '문서 검색' },
  },
});

// In component:
<RootProvider i18n={provider(lang)}>{children}</RootProvider>
```

### app/[lang]/docs/layout.tsx
```typescript
const lang = (await params).lang;
<DocsLayout tree={source.pageTree[lang]} {...baseOptions(lang)}>
```

### lib/source.ts
```typescript
export const source = loader({
  baseUrl: '/docs',
  source: docs.toFumadocsSource(),
  plugins: [lucideIconsPlugin()],
  i18n, // ADD THIS
});
```

### lib/layout.shared.tsx
```typescript
export function baseOptions(locale: string): BaseLayoutProps {
  return {
    nav: { title: 'My App' },
    i18n, // ADD THIS
  };
}
```

## Common Patterns

### Getting Current Language

```typescript
// In Server Component
const lang = (await params).lang;

// In Client Component
import { useParams } from 'next/navigation';
const { lang } = useParams();
```

### Language-Specific Links

```typescript
import { DynamicLink } from 'fumadocs-core/dynamic-link';

<DynamicLink href="/[lang]/docs/page">Link</DynamicLink>
// Automatically becomes: /en/docs/page, /zh/docs/page, etc.
```

### Conditional Content by Language

```typescript
const lang = (await params).lang;

{lang === 'zh' && <ChineseOnlyContent />}
{lang === 'en' && <EnglishOnlyContent />}
```

## Directory Structure Cheat Sheet

```
✅ CORRECT (parser: 'dir')
content/docs/
├── en/
│   └── page.mdx
├── zh/
│   └── page.mdx
└── fr/
    └── page.mdx

URL: /en/docs/page

❌ WRONG (parser: 'dot')
content/docs/
├── page.en.mdx
├── page.zh.mdx
└── page.fr.mdx

URL: /en/docs/page.en
```

## Troubleshooting Quick Fixes

### Problem: Sidebar Shows All Languages

```typescript
// Fix: Use lang-filtered tree
<DocsLayout tree={source.pageTree[lang]} {...baseOptions(lang)}>
```

### Problem: URLs Have Double Prefix (/en/docs/en)

```typescript
// Fix: Add parser to i18n.ts
export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'fr', 'ko', 'zh'],
  parser: 'dir', // THIS LINE
});
```

### Problem: No Language Switcher

```typescript
// Fix 1: Add i18n to layout.shared.tsx
export function baseOptions(locale: string): BaseLayoutProps {
  return {
    nav: { title: 'App' },
    i18n, // THIS LINE
  };
}

// Fix 2: Pass i18n provider in app/[lang]/layout.tsx
<RootProvider i18n={provider(lang)}>{children}</RootProvider>
```

### Problem: Build Errors

```bash
# Clear cache and rebuild
rm -rf .next .source
npm run build
```

## Language Configuration Table

| Language | Code | Display Name | Search Placeholder |
|----------|------|--------------|-------------------|
| English  | en   | English      | Search docs       |
| Chinese  | zh   | 中文          | 搜索文档          |
| French   | fr   | Français     | Rechercher        |
| Korean   | ko   | 한국어        | 문서 검색         |

## File Modification Checklist

When setting up i18n, you need to:

- [ ] Create `lib/i18n.ts`
- [ ] Create `middleware.ts`
- [ ] Update `app/layout.tsx` (make minimal)
- [ ] Create `app/[lang]/layout.tsx`
- [ ] Update `app/[lang]/(home)/layout.tsx`
- [ ] Update `app/[lang]/docs/layout.tsx`
- [ ] Update `app/[lang]/docs/[[...slug]]/page.tsx`
- [ ] Update `lib/source.ts` (add i18n)
- [ ] Update `lib/layout.shared.tsx` (add locale param & i18n)
- [ ] Organize `content/docs/` by language

## URL Structure Reference

| Path | Description |
|------|-------------|
| `/` | Redirects to `/en` (default language) |
| `/en` | English home page |
| `/en/docs` | English docs index |
| `/en/docs/page` | English doc page |
| `/zh` | Chinese home page |
| `/zh/docs` | Chinese docs index |
| `/fr/docs` | French docs |
| `/ko/docs` | Korean docs |

## Key Configuration Values

```typescript
// i18n config
defaultLanguage: 'en'     // Which lang to redirect to
languages: ['en', ...]    // Supported languages
parser: 'dir'             // CRITICAL for directory structure

// In loader()
i18n                      // Enables multi-lang page trees

// In DocsLayout
tree={source.pageTree[lang]}  // Filters sidebar by language

// In RootProvider
i18n={provider(lang)}     // Enables language switcher
```

## Meta.json Example

For organizing navigation per language:

```json
{
  "title": "Getting Started",
  "pages": [
    "index",
    "installation",
    "configuration"
  ]
}
```

Place in: `content/docs/{lang}/getting-started/meta.json`

---

**Quick Tip:** Keep this reference handy when setting up or debugging fumadocs i18n!
