---
name: fumadocs-i18n
description: >
  Set up complete internationalization (i18n) for a Fumadocs project following
  official best practices. Configures multi-language routing, language switcher,
  sidebar filtering, and proper content organization for Next.js. Use this skill
  when the user wants to add i18n support to their Fumadocs documentation site.
---

# Fumadocs Internationalization Setup

Automate the complete setup of internationalization (i18n) in a Fumadocs project with language routing, switcher UI, and proper content organization.

## When to Use This Skill

Use this skill when:
- Setting up a new Fumadocs project with multi-language support
- Adding i18n to an existing Fumadocs project
- The user mentions: "add multi-language", "internationalization", "i18n", "translate docs"
- They want language-specific sidebars and navigation
- They need a language switcher in the UI

## Prerequisites

Before using this skill, verify:
- Fumadocs project is initialized (with `fumadocs-core`, `fumadocs-ui`, `fumadocs-mdx`)
- Next.js App Router is being used
- Project has the following structure:
  ```
  app/
  ├── layout.tsx
  ├── (home)/
  └── docs/
  content/docs/
  lib/
  ```

## What This Skill Does

This skill will automatically:

1. **Create i18n Configuration** (`lib/i18n.ts`)
   - Define supported languages
   - Set default language
   - Configure directory parser

2. **Set Up Middleware** (`middleware.ts`)
   - Auto-redirect to appropriate locale
   - Handle language detection

3. **Restructure App Directory**
   - Move routes under `[lang]` dynamic segment
   - Update all layouts for i18n support

4. **Configure Language Switcher**
   - Add language toggle to navigation
   - Set up display names and translations

5. **Organize Content by Language**
   - Structure `content/docs/` with language directories
   - Ensure sidebar only shows current language

6. **Update All Configurations**
   - Modify `source.ts` for i18n
   - Update `layout.shared.tsx` to pass locale
   - Configure page trees per language

## Supported Languages

Default configuration includes:
- **English** (en) - Default language
- **Chinese** (zh) - Simplified Chinese
- **French** (fr)
- **Korean** (ko)

You can customize this list based on user requirements.

## Workflow

See the detailed `README.md` for step-by-step implementation guide.

## Key Features

✅ **Official fumadocs Approach** - Follows fumadocs.dev documentation exactly
✅ **Language Switcher** - Beautiful dropdown in navigation bar
✅ **Filtered Sidebar** - Only shows content for current language
✅ **SEO-Friendly URLs** - Clean `/[lang]/docs` structure
✅ **Automatic Detection** - Middleware handles language routing
✅ **Type-Safe** - Full TypeScript support

## Common Issues Solved

This skill addresses common fumadocs i18n pitfalls:
- ❌ **Sidebar showing all languages** → ✅ Filtered by `source.pageTree[lang]`
- ❌ **Missing language switcher** → ✅ Auto-configured in DocsLayout
- ❌ **Wrong URL structure** → ✅ Correct `/[lang]/docs` routing
- ❌ **Content not organized** → ✅ Proper `en/`, `zh/`, etc. directories
- ❌ **Parser errors** → ✅ `parser: 'dir'` configuration

## Files Created/Modified

The skill will create or modify:
- `lib/i18n.ts` ← **New**
- `middleware.ts` ← **New**
- `app/layout.tsx` ← Modified
- `app/[lang]/layout.tsx` ← **New**
- `app/[lang]/(home)/layout.tsx` ← Moved
- `app/[lang]/docs/layout.tsx` ← Moved
- `app/[lang]/docs/[[...slug]]/page.tsx` ← Moved
- `lib/source.ts` ← Modified
- `lib/layout.shared.tsx` ← Modified
- `content/docs/[lang]/` ← **New structure**

## Success Criteria

After running this skill, the user should have:
- ✅ Language switcher visible in top-right navigation
- ✅ URLs like `/en/docs`, `/zh/docs`, `/fr/docs`, `/ko/docs`
- ✅ Sidebar showing only current language content
- ✅ Middleware redirecting root `/` to default language
- ✅ All content properly organized in language directories
- ✅ Build succeeds without errors
- ✅ Development server runs correctly

## Version History

- v1.0.0 (2025-11-16): Initial release
  - Complete i18n setup automation
  - Language switcher integration
  - Sidebar filtering by language
  - Content reorganization
  - Official fumadocs best practices
