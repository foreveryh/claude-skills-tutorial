# meta.json Best Practices for Article Importer

This guide provides comprehensive best practices for handling meta.json files when importing articles into a multi-language fumadocs project.

## Table of Contents

1. [Understanding meta.json](#understanding-metajson)
2. [Multi-Language Strategy](#multi-language-strategy)
3. [Category Management](#category-management)
4. [Pages Array Handling](#pages-array-handling)
5. [Icon Selection](#icon-selection)
6. [Existing File Management](#existing-file-management)
7. [Root meta.json Updates](#root-metajson-updates)
8. [Verification Checklist](#verification-checklist)

## Understanding meta.json

### What is meta.json?

In fumadocs, `meta.json` files serve two critical purposes:

1. **Sidebar Navigation**: Control what appears in the documentation sidebar
2. **URL vs Display Separation**: Decouple URL paths (SEO-friendly) from display names (localized)

### Example Structure

```json
{
  "title": "AI & Machine Learning",
  "icon": "Brain",
  "pages": ["skills-explained", "prompt-engineering", "ai-agents"],
  "defaultOpen": false
}
```

### Key Properties

- **title**: Localized display name shown in sidebar
- **icon**: Lucide icon name (optional but recommended)
- **pages**: Array of page slugs in display order
- **defaultOpen**: Whether category is expanded by default (boolean)

## Multi-Language Strategy

### Directory Structure

For a multi-language project supporting en, zh, fr, ko:

```
content/docs/
├── en/
│   ├── meta.json (root)
│   └── ai-ml/
│       ├── meta.json
│       └── article.mdx
├── zh/
│   ├── meta.json (root)
│   └── ai-ml/
│       ├── meta.json
│       └── article.mdx
├── fr/
│   ├── meta.json (root)
│   └── ai-ml/
│       ├── meta.json
│       └── article.mdx
└── ko/
    ├── meta.json (root)
    └── ai-ml/
        ├── meta.json
        └── article.mdx
```

### Language-Specific Titles

Always create meta.json for ALL languages when adding a new category:

```json
// content/docs/en/ai-ml/meta.json
{
  "title": "AI & Machine Learning",
  "icon": "Brain"
}

// content/docs/zh/ai-ml/meta.json
{
  "title": "AI 与机器学习",
  "icon": "Brain"
}

// content/docs/fr/ai-ml/meta.json
{
  "title": "IA et Apprentissage Automatique",
  "icon": "Brain"
}

// content/docs/ko/ai-ml/meta.json
{
  "title": "AI 및 머신러닝",
  "icon": "Brain"
}
```

### Translation Reference

Use the category translations from `references/category-translations.json`:

| Category | English | 中文 | Français | 한국어 |
|----------|---------|------|----------|--------|
| ai-ml | AI & Machine Learning | AI 与机器学习 | IA et Apprentissage Automatique | AI 및 머신러닝 |
| development | Development | 开发 | Développement | 개발 |
| data | Data | 数据 | Données | 데이터 |
| design | Design | 设计 | Design | 디자인 |
| content | Content | 内容 | Contenu | 콘텐츠 |
| business | Business | 商业 | Affaires | 비즈니스 |
| devops | DevOps | DevOps | DevOps | DevOps |
| security | Security | 安全 | Sécurité | 보안 |

## Category Management

### When to Create New Category

Create a new category meta.json when:
1. Importing the first article into a new category
2. The category doesn't exist in any language directory
3. User explicitly requests a new category

### When to Update Existing Category

Update existing category meta.json when:
1. Category folder already exists
2. meta.json file already exists
3. Adding article to existing category

### New Category Workflow

```bash
# 1. Check if category exists
ls content/docs/en/ai-ml/meta.json 2>/dev/null

# 2. If not exists, create for all languages
# Create category directories
mkdir -p content/docs/{en,zh,fr,ko}/ai-ml

# 3. Create meta.json for each language
# (Use translation mapping from references)

# 4. Update root meta.json for each language
# (Add category to pages array if not present)
```

## Pages Array Handling

### Initial Creation

When creating new meta.json:

```json
{
  "title": "AI & Machine Learning",
  "icon": "Brain",
  "pages": ["new-article-slug"],
  "defaultOpen": false
}
```

### Adding to Existing Pages

When meta.json already exists with pages:

**Option 1: Ask User for Placement**

```
Article Placement Options:
1. Add to top of category
2. Add to bottom of category
3. Insert alphabetically
4. Insert at specific position
```

**Option 2: Default to Bottom**

```json
// Before
{
  "pages": ["existing-article-1", "existing-article-2"]
}

// After
{
  "pages": ["existing-article-1", "existing-article-2", "new-article-slug"]
}
```

**Option 3: Alphabetical Insertion**

```javascript
// Pseudo-code
const pages = existingPages.concat(newSlug).sort();
```

### Pages Array Best Practices

1. **Consistency**: Use same page order across all languages
2. **Slugs Only**: Never use full paths, just the slug name
3. **No Extensions**: Don't include .mdx extension
4. **Kebab Case**: Use consistent slug naming (lowercase with hyphens)

### Example Multi-File Pages

```json
{
  "title": "AI & Machine Learning",
  "icon": "Brain",
  "pages": [
    "skills-explained",
    "prompt-engineering",
    "ai-agents",
    "machine-learning-basics",
    "neural-networks"
  ],
  "defaultOpen": false
}
```

## Icon Selection

### Icon Reference

Use icons from `references/category-icons.json`:

| Category | Primary Icon | Alternatives |
|----------|-------------|--------------|
| ai-ml | Brain | Cpu, Zap, Sparkles |
| development | Code | Terminal, Braces, FileCode |
| data | Database | BarChart, PieChart, TrendingUp |
| design | Palette | Paintbrush, Layers, Layout |
| content | FileText | BookOpen, Book, FileEdit |
| business | Briefcase | TrendingUp, DollarSign, Users |
| devops | Server | Cloud, Container, GitBranch |
| security | Shield | Lock, ShieldCheck, Key |

### Icon Guidelines

1. **Consistency**: Use same icon across all language versions
2. **Lucide Icons**: All icons from [Lucide Icons](https://lucide.dev/)
3. **Semantic Meaning**: Choose icons that represent category content
4. **Alternative Selection**: If primary icon conflicts, use alternatives

### Icon Configuration

Icons work through `lucideIconsPlugin()` in `lib/source.ts`:

```typescript
export const source = loader({
  baseUrl: '/docs',
  source: docs.toFumadocsSource(),
  plugins: [lucideIconsPlugin()],
  i18n,
});
```

## Existing File Management

### Checking for Existing meta.json

```bash
# Check single language
if [ -f "content/docs/en/ai-ml/meta.json" ]; then
  echo "meta.json exists - will update"
else
  echo "meta.json does not exist - will create"
fi

# Check all languages
for lang in en zh fr ko; do
  if [ -f "content/docs/$lang/ai-ml/meta.json" ]; then
    echo "Found: $lang/ai-ml/meta.json"
  fi
done
```

### Reading Existing meta.json

```javascript
// Pseudo-code for reading and parsing
const existingContent = readFile('content/docs/en/ai-ml/meta.json');
const meta = JSON.parse(existingContent);

// Check for pages array
if (meta.pages && Array.isArray(meta.pages)) {
  // Pages exist - need to update
  console.log(`Existing pages: ${meta.pages.length}`);
} else {
  // No pages - can add directly
  meta.pages = [];
}
```

### Updating Existing meta.json

**Preserve Existing Properties**:

```json
// Existing file
{
  "title": "AI & Machine Learning",
  "icon": "Brain",
  "pages": ["existing-article"],
  "defaultOpen": true
}

// Update (preserve defaultOpen)
{
  "title": "AI & Machine Learning",
  "icon": "Brain",
  "pages": ["existing-article", "new-article"],
  "defaultOpen": true  // ← preserved
}
```

**Handle Missing Properties**:

```javascript
// Pseudo-code
const meta = readExistingMeta();

// Add pages if missing
if (!meta.pages) {
  meta.pages = [];
}

// Add icon if missing
if (!meta.icon) {
  meta.icon = getCategoryIcon(category);
}

// Preserve other properties
const updated = {
  ...meta,  // Keep all existing properties
  pages: [...meta.pages, newSlug]  // Update pages
};
```

## Root meta.json Updates

### Root meta.json Purpose

The root meta.json controls category order in the sidebar:

```json
// content/docs/en/meta.json
{
  "title": "Documentation",
  "pages": [
    "index",
    "ai-ml",
    "development",
    "data"
  ]
}
```

### When to Update Root meta.json

Update root meta.json when:
1. Adding first article to a NEW category
2. Category doesn't appear in root pages array
3. User requests specific category order

### Root Update Workflow

```bash
# 1. Check if category in root meta.json
grep -q "ai-ml" content/docs/en/meta.json

# 2. If not found, add to root pages array
# (Ask user where to place, or add to bottom)

# 3. Repeat for all languages
for lang in en zh fr ko; do
  # Update content/docs/$lang/meta.json
done
```

### Root meta.json Example

```json
// Before (no ai-ml)
{
  "title": "Documentation",
  "pages": [
    "index",
    "getting-started"
  ]
}

// After (ai-ml added)
{
  "title": "Documentation",
  "pages": [
    "index",
    "getting-started",
    "ai-ml"
  ]
}
```

### Category Ordering Best Practices

1. **Index First**: Always keep "index" as first page
2. **Logical Grouping**: Group related categories together
3. **Frequency**: Popular categories towards top
4. **Alphabetical**: Consider alphabetical for many categories

## Verification Checklist

### Post-Import Verification

After importing an article and creating/updating meta.json files:

- [ ] **All Languages Created**: meta.json exists for en, zh, fr, ko
- [ ] **Correct Titles**: Each language has localized title
- [ ] **Same Icon**: All languages use same icon
- [ ] **Pages Array**: Article slug added to pages array
- [ ] **Valid JSON**: All meta.json files are valid JSON
- [ ] **Root Updated**: Root meta.json includes category (if new)
- [ ] **Sidebar Display**: Article appears in sidebar after build

### Verification Commands

```bash
# Check all meta.json files exist
for lang in en zh fr ko; do
  if [ -f "content/docs/$lang/ai-ml/meta.json" ]; then
    echo "✅ $lang: Found"
  else
    echo "❌ $lang: Missing"
  fi
done

# Validate JSON syntax
for lang in en zh fr ko; do
  if jq empty "content/docs/$lang/ai-ml/meta.json" 2>/dev/null; then
    echo "✅ $lang: Valid JSON"
  else
    echo "❌ $lang: Invalid JSON"
  fi
done

# Check article in pages array
for lang in en zh fr ko; do
  if grep -q "new-article-slug" "content/docs/$lang/ai-ml/meta.json"; then
    echo "✅ $lang: Article in pages array"
  else
    echo "❌ $lang: Article NOT in pages array"
  fi
done

# Test build
npm run build
# Look for: ✅ All pages generated successfully
```

### Visual Verification

After `npm run dev`:

1. Navigate to http://localhost:3000
2. Switch to each language (en, zh, fr, ko)
3. Verify:
   - Category appears in sidebar
   - Category title is localized
   - Icon displays correctly
   - Article appears under category
   - Article link works

## Common Pitfalls

### ❌ Creating Only English meta.json

**Wrong**:
```bash
# Only creates English version
echo '{"title": "AI & ML", "icon": "Brain"}' > content/docs/en/ai-ml/meta.json
```

**Right**:
```bash
# Creates all language versions
for lang in en zh fr ko; do
  # Create with appropriate translation
done
```

### ❌ Inconsistent Icons

**Wrong**:
```json
// en/ai-ml/meta.json
{"icon": "Brain"}

// zh/ai-ml/meta.json
{"icon": "Cpu"}  // ← Different!
```

**Right**:
```json
// All languages
{"icon": "Brain"}  // ← Same icon
```

### ❌ Forgetting Root meta.json

**Problem**: New category doesn't appear in sidebar

**Solution**: Always update root meta.json for all languages when adding new category

### ❌ Invalid JSON

**Wrong**:
```json
{
  "title": "AI & ML",
  "pages": ["article"],  // ← Trailing comma
}
```

**Right**:
```json
{
  "title": "AI & ML",
  "pages": ["article"]
}
```

### ❌ Using Full Paths in Pages Array

**Wrong**:
```json
{
  "pages": ["content/docs/en/ai-ml/article.mdx"]
}
```

**Right**:
```json
{
  "pages": ["article"]
}
```

## Advanced Patterns

### Nested Categories

```json
{
  "title": "AI & Machine Learning",
  "icon": "Brain",
  "pages": [
    "overview",
    "fundamentals",
    {
      "type": "separator",
      "title": "Advanced Topics"
    },
    "neural-networks",
    "deep-learning"
  ]
}
```

### External Links

```json
{
  "title": "Resources",
  "pages": [
    "guides",
    {
      "title": "Official Docs",
      "url": "https://example.com",
      "external": true
    }
  ]
}
```

### Category Descriptions

```json
{
  "title": "AI & Machine Learning",
  "description": "Explore artificial intelligence and machine learning concepts",
  "icon": "Brain",
  "pages": ["..."]
}
```

## Summary

When importing articles into a multi-language fumadocs project:

1. **Always create meta.json for ALL languages** (en, zh, fr, ko)
2. **Use translation mapping** from `references/category-translations.json`
3. **Use consistent icons** from `references/category-icons.json`
4. **Handle existing files** by preserving properties and updating pages array
5. **Update root meta.json** when adding new categories
6. **Verify** all files exist and are valid JSON
7. **Test** in development server to confirm sidebar display

This ensures a consistent, professional multi-language documentation experience.
