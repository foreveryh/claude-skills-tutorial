# Troubleshooting Guide - Fumadocs i18n

Common issues and their solutions when implementing fumadocs internationalization.

## Table of Contents

1. [Sidebar Issues](#sidebar-issues)
2. [URL/Routing Issues](#urlrouting-issues)
3. [Language Switcher Issues](#language-switcher-issues)
4. [Build Errors](#build-errors)
5. [Content Organization](#content-organization)
6. [TypeScript Errors](#typescript-errors)

---

## Sidebar Issues

### Issue 1: Sidebar Shows All Languages Mixed

**Symptoms:**
- Sidebar displays "En", "Fr", "Ko", "Zh" folders
- Content from multiple languages appears together
- Navigation shows paths like "/en/page" and "/zh/page" mixed

**Root Cause:**
Not using language-filtered page tree in DocsLayout

**Solution:**

❌ **Wrong:**
```typescript
<DocsLayout tree={source.pageTree} {...baseOptions(lang)}>
```

✅ **Correct:**
```typescript
<DocsLayout tree={source.pageTree[lang]} {...baseOptions(lang)}>
```

**Location:** `app/[lang]/docs/layout.tsx`

**Verification:**
```bash
# Check browser console or add debug log:
console.log('Page tree keys:', Object.keys(source.pageTree));
// Should show: ['en', 'fr', 'ko', 'zh']

console.log('Current tree:', source.pageTree[lang]);
// Should only show pages for current language
```

---

### Issue 2: Sidebar Empty or Missing

**Symptoms:**
- Sidebar shows no content
- Pages exist but don't appear in navigation

**Possible Causes & Solutions:**

**Cause 1:** Content not in correct directory structure

```bash
# Check your content structure
ls -R content/docs/

# Should see:
# content/docs/en/...
# content/docs/zh/...
# NOT:
# content/docs/page.en.mdx (wrong parser)
```

**Cause 2:** Missing `parser: 'dir'` in i18n config

```typescript
// lib/i18n.ts
export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'fr', 'ko', 'zh'],
  parser: 'dir', // ADD THIS
});
```

**Cause 3:** Build cache issue

```bash
rm -rf .next .source
npm run build
```

---

## URL/Routing Issues

### Issue 3: Double Language Prefix in URLs

**Symptoms:**
- URLs look like `/en/docs/en/page` instead of `/en/docs/page`
- Routes like `/zh/docs/zh` instead of `/zh/docs`

**Root Cause:**
Missing `parser: 'dir'` in i18n configuration

**Solution:**

```typescript
// lib/i18n.ts
export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'fr', 'ko', 'zh'],
  parser: 'dir', // CRITICAL - tells fumadocs how to parse language folders
});
```

**After fix:**
```bash
rm -rf .next .source  # Clear cache
npm run build         # Rebuild
```

**Verification:**
Check build output for correct routes:
```
Route (app)
├ ● /[lang]/docs/[[...slug]]
│ ├ /en/docs           ✅ Correct
│ ├ /en/docs/page      ✅ Correct
│ ├ /en/docs/en        ❌ Wrong
```

---

### Issue 4: Root `/` Not Redirecting

**Symptoms:**
- Visiting `/` shows 404 or error
- No automatic redirect to `/en`

**Root Cause:**
Middleware not properly configured

**Solution:**

Check `middleware.ts` exists and is correct:

```typescript
import { createI18nMiddleware } from 'fumadocs-core/i18n/middleware';
import { i18n } from '@/lib/i18n';

export default createI18nMiddleware(i18n);

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

**Common mistakes:**
- File named `middleware.tsx` instead of `middleware.ts`
- Missing export of `config`
- Wrong matcher pattern
- Middleware not in root directory

---

### Issue 5: API Routes Breaking

**Symptoms:**
- `/api/*` routes return 404 or redirect to language pages
- API endpoints not working after i18n setup

**Root Cause:**
Middleware is catching API routes

**Solution:**

Ensure middleware matcher excludes `/api`:

```typescript
export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
  //              ^^^^ Excludes /api routes
};
```

**Alternative:** Keep API routes outside `[lang]` folder:
```
app/
├── api/           ✅ Outside [lang], no language prefix
│   └── search/
└── [lang]/        ✅ Language-specific routes
    └── docs/
```

---

## Language Switcher Issues

### Issue 6: No Language Switcher Visible

**Symptoms:**
- Language dropdown not appearing in navigation
- No way to switch languages in UI

**Possible Causes & Solutions:**

**Cause 1:** Missing `i18n` in baseOptions

```typescript
// lib/layout.shared.tsx
import { i18n } from '@/lib/i18n';

export function baseOptions(locale: string): BaseLayoutProps {
  return {
    nav: { title: 'My App' },
    i18n, // ADD THIS LINE
  };
}
```

**Cause 2:** Not passing i18n provider to RootProvider

```typescript
// app/[lang]/layout.tsx
const { provider } = defineI18nUI(i18n, { translations: {...} });

// In return statement:
<RootProvider i18n={provider(lang)}>{children}</RootProvider>
//            ^^^^^^^^^^^^^^^^^^ CRITICAL
```

**Cause 3:** Missing `defineI18nUI` setup

```typescript
// app/[lang]/layout.tsx
import { defineI18nUI } from 'fumadocs-ui/i18n';
import { i18n } from '@/lib/i18n';

const { provider } = defineI18nUI(i18n, {
  translations: {
    en: { displayName: 'English' },
    zh: { displayName: '中文' },
    // ... other languages
  },
});
```

---

### Issue 7: Language Switcher Shows Wrong Names

**Symptoms:**
- Languages shown as "en", "zh" instead of "English", "中文"
- No display names in dropdown

**Solution:**

Add `displayName` for each language:

```typescript
const { provider } = defineI18nUI(i18n, {
  translations: {
    en: {
      displayName: 'English', // Shows in dropdown
    },
    zh: {
      displayName: '中文',    // Shows in dropdown
      search: '搜索文档',      // Optional: localizes search placeholder
    },
    fr: {
      displayName: 'Français',
      search: 'Rechercher',
    },
    ko: {
      displayName: '한국어',
      search: '문서 검색',
    },
  },
});
```

---

## Build Errors

### Issue 8: "Language not supported" Errors

**Symptoms:**
```
Error: Language "ko" is not supported.
Supported languages are:
 - english
 - french
 - ...
```

**Root Cause:**
OG (Open Graph) image generation doesn't support Korean/Chinese fonts

**Impact:** ⚠️ **Warning only** - core functionality works fine

**Solution:**
This is expected and can be safely ignored. The error only affects:
- Open Graph preview images (social media shares)
- Korean and Chinese OG images will use fallback font

Core i18n features (routing, sidebar, language switcher) work perfectly.

**To suppress (if needed):**
- Wait for fumadocs to update OG font support
- Or implement custom OG image generation

---

### Issue 9: TypeScript Type Errors After i18n Setup

**Symptoms:**
```
Type error: Property 'lang' does not exist on type 'PageProps'
```

**Solution:**

Update page component types:

❌ **Before:**
```typescript
export default async function Page(props: PageProps<'/docs/[[...slug]]'>) {
```

✅ **After:**
```typescript
export default async function Page(props: PageProps<'/[lang]/docs/[[...slug]]'>) {
  //                                                   ^^^^^^ Add [lang]
```

Similar fix for:
- `generateMetadata`
- Any other functions using `PageProps`

---

### Issue 10: Module Not Found Errors

**Symptoms:**
```
Module not found: Can't resolve '@/lib/i18n'
```

**Solution:**

1. Verify file exists: `ls lib/i18n.ts`
2. Check tsconfig.json has path alias:
   ```json
   {
     "compilerOptions": {
       "paths": {
         "@/*": ["./*"]
       }
     }
   }
   ```
3. Restart TypeScript server in IDE
4. Clear cache: `rm -rf .next`

---

## Content Organization

### Issue 11: Content Not Generating Routes

**Symptoms:**
- MDX files exist but pages don't generate
- Build output shows fewer routes than expected

**Solution:**

Check content structure matches parser type:

✅ **For `parser: 'dir'`:**
```
content/docs/
├── en/
│   └── page.mdx
└── zh/
    └── page.mdx
```

❌ **Wrong (for `parser: 'dir'`):**
```
content/docs/
├── page.en.mdx
└── page.zh.mdx
```

**Verification:**
```bash
# Check generated source files
cat .source/index.ts

# Should show imports like:
# import * as d_docs_0 from "../content/docs/en/page.mdx"
# import * as d_docs_1 from "../content/docs/zh/page.mdx"
```

---

### Issue 12: Meta.json Not Working

**Symptoms:**
- Sidebar order not matching meta.json
- Navigation customization not applying

**Solution:**

Ensure meta.json is in correct location:

```
content/docs/
└── en/
    ├── getting-started/
    │   ├── meta.json      ✅ Correct - in category folder
    │   ├── index.mdx
    │   └── installation.mdx
    └── meta.json          ✅ Correct - in language root
```

**meta.json format:**
```json
{
  "title": "Category Name",
  "pages": [
    "index",
    "installation",
    "..."
  ]
}
```

---

## TypeScript Errors

### Issue 13: Params Type Errors

**Symptoms:**
```
Argument of type 'string | string[]' is not assignable to parameter of type 'string'
```

**Root Cause:**
Next.js 15+ changed params to be async

**Solution:**

❌ **Old (Next.js <15):**
```typescript
export default function Layout({ params }: { params: { lang: string } }) {
  const lang = params.lang;
```

✅ **New (Next.js 15+):**
```typescript
export default async function Layout({ params }: { params: Promise<{ lang: string }> }) {
  const lang = (await params).lang;
```

Apply to all:
- Layouts
- Pages
- `generateMetadata`
- `generateStaticParams`

---

## General Debugging Steps

### Debug Checklist

When something isn't working:

1. **Clear cache:**
   ```bash
   rm -rf .next .source
   npm run build
   ```

2. **Check file structure:**
   ```bash
   tree app/[lang] content/docs lib
   ```

3. **Verify i18n config:**
   ```typescript
   // Check lib/i18n.ts has:
   - defaultLanguage
   - languages array
   - parser: 'dir'
   ```

4. **Check imports:**
   ```bash
   grep -r "from '@/lib/i18n'" app/ lib/
   # Should find imports in:
   # - middleware.ts
   # - app/[lang]/layout.tsx
   # - lib/source.ts
   # - lib/layout.shared.tsx
   ```

5. **Inspect generated source:**
   ```bash
   cat .source/index.ts | grep "from.*content/docs"
   # Should show language prefixes: en/, zh/, etc.
   ```

6. **Test in browser console:**
   ```javascript
   // Check page tree structure
   console.log(window.__NEXT_DATA__.props.pageProps)
   ```

---

## Still Having Issues?

### Diagnostic Commands

```bash
# Check package versions
npm list fumadocs-core fumadocs-ui fumadocs-mdx next

# Verify middleware is running
npm run dev 2>&1 | grep middleware

# Check route generation
npm run build 2>&1 | grep "/[lang]"

# Inspect source generation
ls -la .source/
cat .source/index.ts | head -20
```

### Common Gotchas

1. **Parser must match structure** - `parser: 'dir'` for folders, `parser: 'dot'` for files
2. **Cache issues** - Always `rm -rf .next .source` after config changes
3. **Middleware matcher** - Must exclude static assets and API routes
4. **Root layout** - Must be minimal when using `[lang]` routing
5. **Page tree** - Must use `[lang]` index: `source.pageTree[lang]`
6. **Provider** - Must pass `i18n={provider(lang)}` to RootProvider

---

## Prevention Tips

✅ **Do:**
- Use `parser: 'dir'` for directory-based structure
- Filter sidebar with `source.pageTree[lang]`
- Pass `i18n` to both `loader()` and `baseOptions()`
- Clear cache after configuration changes
- Test all languages after setup

❌ **Don't:**
- Mix directory and file-based structures
- Forget to await params in Next.js 15+
- Put content files in root `content/docs/`
- Modify fumadocs core files
- Skip clearing cache

---

**Last Updated:** 2025-11-16
**Fumadocs Version:** 16.0.11+
