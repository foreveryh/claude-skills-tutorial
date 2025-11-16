---
name: fumadocs-article-importer
description: >
  Import external articles into a Fumadocs project with automatic multi-language
  translation (en, zh, fr, ko), AI-powered classification into 8 categories,
  image processing, and MDX conversion. Use this skill when the user wants to
  import an article from a URL into their Fumadocs documentation site.
---

# Fumadocs Article Importer

Automate importing external articles into a Fumadocs project with multi-language support, auto-classification, and proper MDX formatting.

## Prerequisites

Before using this skill, verify:
- Fumadocs project is initialized in the current directory
- **Jina MCP** is configured for article fetching (highly recommended)
  - Repository: https://github.com/jina-ai/MCP
  - Provides 15 tools for content extraction, search, and processing
  - See "MCP Configuration" section below for setup
  - Alternative: Jina API access (via curl)
- **Translator Skill** is available for professional translation
  - Located in `.claude/skills/translator/`
  - Provides professional translation using Claude's native capabilities
  - Automatically activated when translation is needed
  - No external dependencies or configuration required
- `curl` is installed for image downloads
- Write access to `content/docs/` and `public/images/` directories

## MCP Configuration

This skill works best with:
1. **Jina MCP** - For article fetching and content extraction
2. **Translator Skill** - For professional translation (built-in, no configuration needed)

### Jina MCP Setup (Article Fetching)

**Public Jina MCP Server** (Recommended):

Add to your Claude configuration:
```json
{
  "mcpServers": {
    "jina": {
      "url": "https://mcp.jina.ai/sse",
      "headers": {
        "Authorization": "Bearer ${JINA_API_KEY}"  // Optional, for higher rate limits
      }
    }
  }
}
```

**Note**: Works without API key but has rate limits. For production use, get a free API key at https://jina.ai

**Self-Hosted Jina MCP** (Optional):
```bash
git clone https://github.com/jina-ai/MCP.git
cd MCP && npm install && npm run start
```

**Available Tools**:
- `read_url` - Convert webpage to markdown ✨ (primary tool)
- `guess_datetime_url` - Get publication date
- `search_web`, `search_arxiv`, `search_images` - Search capabilities
- `sort_by_relevance`, `deduplicate_strings` - Content processing

### Translation Setup

**Translation Strategy**: This skill uses Claude's native translation capabilities through the **translator skill**.

The translator skill provides:
- Professional-grade translation quality
- Preservation of Markdown formatting and code blocks
- Consistent technical terminology handling
- Language-specific best practices (zh, fr, ko, en)
- No external dependencies or API keys required

**How it works**: When this skill needs to translate content, it will automatically trigger Claude to use the translator skill. You don't need to configure anything - Claude will compose the two skills automatically based on the task requirements.

## Workflow

### Step 1: Get Article Information

Ask the user for the following information:
1. "What is the URL of the article you want to import?"
2. "What languages should I translate to? (Press Enter for default: en, zh, fr, ko)"
3. "Should I download and process images? (yes/no, default: yes)"

### Step 2: Download Article Content

**Using Jina MCP** (Recommended - best integration with Claude):

1. **Fetch article content with images** (RECOMMENDED - enables smart image filtering):
   ```
   Tool: read_url
   Parameters:
     - url: {article_url}
     - withAllImages: true  ← ADD THIS

   Returns:
     - content: Markdown-formatted article content
     - images: Array of image objects with URLs and metadata
     - title, description, etc.
   ```
   **Why this matters**: Returns structured image data instead of parsing markdown. You can access `response.images` directly.

2. **Get publication date** (optional but recommended):
   ```
   Tool: guess_datetime_url
   Parameters:
     - url: {article_url}

   Returns: Detected publication and update dates
   ```

3. **Extract metadata from the fetched content**:
   - Title (from markdown H1 or metadata)
   - Author (if available in content)
   - Publication date (from guess_datetime_url or content)
   - Main content (body text)
   - All image URLs (from `response.images` array if withAllImages=true, else extract from markdown)
   - Detect YouTube videos (search for youtube.com/embed, youtu.be, youtube.com/watch URLs)

**Alternative: Using Jina API directly** (if MCP not available):

```bash
# Fetch article as markdown
curl "https://r.jina.ai/{article_url}"

# With custom options
curl "https://r.jina.ai/{article_url}" \
  -H "X-Return-Format: markdown" \
  -H "X-With-Generated-Alt: true"
```

**Fallback**: If neither Jina MCP nor API is available:
- Ask user to provide article content directly
- Or use web scraping with Claude's web browsing capability
- Manual copy-paste of article content

### Step 3: Generate Article Slug

Create a URL-friendly slug from the article title:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Keep only: a-z, 0-9, hyphens
- Maximum 60 characters

Example: "Building React Apps with TypeScript" → "building-react-apps-with-typescript"

### Step 3.5: Filter Content Images (HEURISTIC FILTERING)

**Critical improvement**: Most articles contain 15-20 images, but only 1-3 are actual content images (diagrams, charts, screenshots). The rest are decorative icons, logos, placeholders, or social preview images. We use heuristic rules to filter them.

**Input**: Array of image URLs (from Step 2)

**Heuristic Filtering Rules**:

```typescript
// Blacklist - IMMEDIATE REJECTION
const blacklist = [
  'placeholder.svg',      // Placeholder images
  'favicon',              // Website icons
  'logo',                 // Company logos
  'spinner',              // Loading animations
  'avatar',               // User avatars
  'decoration',           // Decorative elements
  'icon-',                // Icon files
  'social-share',         // Social media preview
  'og-image',             // OpenGraph preview
  'twitter-card'          // Twitter card images
];

// Whitelist - MUST KEEP
const whitelist = [
  'diagram',              // Architecture diagrams
  'chart',                // Data visualizations
  'screenshot',           // UI screenshots
  'visualization',        // Data viz
  'architecture',         // System architecture
  'flowchart',            // Process flows
  'graph',                // Charts/graphs
  'timeline'              // Timeline graphics
];

function heuristicFilter(images: ImageInfo[]): ImageInfo[] {
  return images.filter(img => {
    const url = img.url.toLowerCase();
    const filename = img.filename.toLowerCase();

    // 🚫 BLACKLIST: Immediate rejection
    if (blacklist.some(term => url.includes(term) || filename.includes(term))) {
      return false; // Skip decorative images
    }

    // ✅ WHITELIST: Must keep
    if (whitelist.some(term => url.includes(term) || filename.includes(term))) {
      return true; // Keep content images
    }

    // 📏 FILE TYPE & SIZE RULES
    if (url.endsWith('.png') && img.fileSize > 10000) return true; // PNG > 10KB likely content
    if (url.endsWith('.jpg') && img.fileSize > 15000) return true; // JPG > 15KB likely content
    if (url.endsWith('.svg') && !url.includes('placeholder')) return true; // SVG (except placeholder)

    // 🎯 CONTEXT RULES
    // If image appears near keywords like "diagram", "figure", "example"
    if (isNearContext(img, ['diagram', 'figure', 'example', 'illustration'])) {
      return true;
    }

    return false; // Default: exclude if uncertain
  }).slice(0, 5); // MAX 5 images to avoid clutter
}
```

**Example Filtering**:
- Input: 18 images from claude.com blog
- Detected: 1 placeholder.svg (11 variations), 1 og-image.jpg, 5 decorative SVG icons, 1 MCP diagram PNG
- Filtered: **Only 1 image kept** (MCP diagram)
- Result: 94% reduction in noise

**User Confirmation** (shows transparency):
```
📊 Image Analysis Complete:
✅ Found 18 images total
🎯 Identified 1 content image (MCP protocol diagram)
🚫 Filtered 17 decorative/placeholder images

Image to download:
[Preview: https://cdn.../mcp-diagram.png]
Description: MCP protocol architecture diagram

Download? (Enter=yes, no=skip):
```

### Step 4: Process Filtered Images

If user chose to download images (from Step 3.5):

**User Confirmation** (show transparency):
```
📊 Image Processing Summary:
✅ Found {total_images} total images on the page
🎯 Identified {filtered_images} content images (diagrams, charts, screenshots)
🚫 Filtered {skipped_images} decorative/placeholder images

Content images to download:
1. [Preview URL: https://.../mcp-diagram.png]
   → Description: MCP protocol architecture diagram
   → Size: 142KB PNG

2. [Preview URL: https://.../data-flow.png]
   → Description: Data flow visualization
   → Size: 89KB PNG

Download these images? (Enter=yes, no=no) [yes]:
```

If user confirms (default=yes):

1. Create image directory:
   ```bash
   mkdir -p "public/images/docs/{article-slug}"
   ```

2. For each **filtered** image URL:
   - Generate descriptive name from context (e.g., "mcp-architecture", "data-flow-diagram")
   - Add index only if multiple similar images: `{descriptive-name}-{index}.{ext}`
   - Download using curl with retry logic:
     ```bash
     curl -f -L -o "public/images/docs/{slug}/{image-name}" "{image_url}" || \
     curl -f -L -o "public/images/docs/{slug}/{image-name}" "{image_url}" || \
     echo "⚠️  Failed to download: {image_url}"
     ```

3. Update image references in content:
   - Original: `![MCP architecture](https://example.com/mcp-diagram.png)`
   - Updated: `![MCP architecture](/images/docs/{article-slug}/mcp-architecture.png)`

4. Handle failed downloads gracefully:
   - If download fails after 2 retries, keep original URL
   - Log failure but continue with other images
   - Report failures in final summary

**Important difference from v1.0**: Instead of downloading ALL images (15-20), we now:
- ✅ Filter intelligently (3-5 content images)
- ✅ Show preview to user
- ✅ Get confirmation before downloading
- ✅ Skip decorative images automatically
- ✅ Faster downloads, less storage waste

### Step 5: Classify Article

Load `references/classification-rules.md` and analyze the article to determine:

1. **Category** (one of 8):
   - development
   - data
   - ai-ml
   - design
   - content
   - business
   - devops
   - security

2. **Difficulty Level** (one of 3):
   - beginner: Introductory content, basic concepts
   - intermediate: Requires some background knowledge
   - advanced: Complex, requires expertise

3. **Tags** (3-7 tags):
   - Extract technology stack (e.g., react, python, docker)
   - Identify tools and frameworks
   - Add relevant keywords
   - Use lowercase with hyphens (e.g., machine-learning)

### Step 6: Translate Content

**Translation Strategy**: Use professional translation for each target language.

For each target language (en, zh, fr, ko):

1. **Prepare content for translation**:
   - Combine title, description, and main content
   - Ensure code blocks are clearly marked
   - Keep image references intact

2. **Request translation**:
   - Ask for professional translation to the target language
   - Specify that this is technical documentation
   - Emphasize the need to preserve Markdown formatting and code blocks

   Example request format:
   ```
   Please translate the following article to {language_name} ({language_code}).
   This is technical documentation - preserve all Markdown syntax, code blocks,
   and image references exactly as they appear.

   [Article content here]
   ```

3. **Translation will automatically apply**:
   - Professional translation quality (via translator skill)
   - Preservation of all Markdown syntax
   - Code blocks remain unchanged
   - Image references stay the same (paths unchanged)
   - Heading hierarchy maintained
   - Technical terms handled appropriately for target language
   - Natural, fluent target language text

4. **Language-specific handling**:
   - **Chinese (zh)**: Simplified Chinese, technical terms stay in English when appropriate
   - **French (fr)**: Standard French technical terminology, formal tone
   - **Korean (ko)**: Formal style (합니다), technical terms mixed with Korean
   - **English (en)**: Clear, professional US English

5. **Quality considerations**:
   - Translation preserves the original meaning and intent
   - Technical accuracy is maintained
   - Content reads naturally in the target language
   - Format and structure remain identical to source

6. **Save translations**:
   - Save original English version first
   - Then save each translated version
   - Maintain consistent file structure across all languages

### Step 7: Generate MDX Files

For each language, create the MDX file:

1. **File path**: `content/docs/{lang}/{category}/{article-slug}.mdx`

2. **Frontmatter** (use `assets/frontmatter-template.yaml` as reference):
   ```yaml
   ---
   title: "{translated_title}"
   description: "{translated_description}"
   lang: {language_code}
   category: {determined_category}
   difficulty: {determined_difficulty}
   tags:
     - {tag1}
     - {tag2}
     - {tag3}
   source_url: "{original_article_url}"
   published_date: "{YYYY-MM-DD}"
   author: "{original_author}"
   ---
   ```

3. **Content Conversion**:
   - Load `references/fumadocs-components.md` to understand available components
   - Convert appropriate sections to Fumadocs components:
     - Card layouts → `<Cards>` and `<Card>`
     - Important notes → `<Callout type="info|warn|error">`
     - Step-by-step guides → `<Steps>` and `<Step>`
     - Code with multiple package managers → `<Tabs>` and `<Tab>`
     - File structures → `<Files>`, `<Folder>`, `<File>`
   - **CRITICAL**: Never implement custom components. Only use built-in Fumadocs components
   - Keep standard Markdown for paragraphs, lists, headings, code blocks

4. **Validate and Fix MDX Syntax**:
   - Ensure all JSX components are properly closed
   - Check that code blocks use correct syntax (triple backticks)
   - Verify frontmatter YAML is valid
   - **CRITICAL - Escape special characters**:
     - Replace `<` with `&lt;` when used in text (not in JSX tags or code blocks)
     - Common cases: `<5`, `<10`, `<100`, `<script`, `<div` in plain text
     - Example: "less than 5k" → write as `&lt;5k` if written as `<5k`
     - Do NOT escape `<` inside code blocks (triple backticks) or valid JSX components
     - Replace `>` with `&gt;` when used in text comparisons
   - **Check for MDX parsing traps**:
     - Patterns like `<number`, `<word` in plain text will break MDX
     - Use HTML entities or rephrase: `<5k` → `&lt;5k` or "less than 5k"
   - **Ensure Markdown formatting has proper spacing**:
     - Bold/italic must have space after closing marker before next char
     - Pattern: `**粗体：** 文字` not `**粗体：**文字`
     - Run regex fix: replace `\*\*([^*]+)\*\*([^ \n*-])` with `**$1** $2`
     - This prevents MDX rendering issues especially in non-Latin languages
   - Confirm no syntax errors that would break rendering

5. Create the file:
   ```bash
   mkdir -p "content/docs/{lang}/{category}"
   # Write the MDX content to file
   ```

### Step 8: Create/Update meta.json for All Languages

**CRITICAL**: Create proper meta.json files for sidebar navigation with localized titles.

Load reference files:
- `references/category-translations.json` - Get translated category names
- `references/category-icons.json` - Get appropriate icons

For **each language** (en, zh, fr, ko):

1. **Create/Update category meta.json**: `content/docs/{lang}/{category}/meta.json`

   ```json
   {
     "title": "{translated_category_name}",
     "icon": "{category_icon}",
     "pages": ["{article-slug}", "..."],
     "defaultOpen": false
   }
   ```

   **Example for ai-ml category:**
   - **English** (`content/docs/en/ai-ml/meta.json`):
     ```json
     {
       "title": "AI & Machine Learning",
       "icon": "Brain",
       "pages": ["{article-slug}", "..."],
       "defaultOpen": false
     }
     ```

   - **Chinese** (`content/docs/zh/ai-ml/meta.json`):
     ```json
     {
       "title": "AI 与机器学习",
       "icon": "Brain",
       "pages": ["{article-slug}", "..."],
       "defaultOpen": false
     }
     ```

   - **French** (`content/docs/fr/ai-ml/meta.json`):
     ```json
     {
       "title": "IA et Apprentissage Automatique",
       "icon": "Brain",
       "pages": ["{article-slug}", "..."],
       "defaultOpen": false
     }
     ```

   - **Korean** (`content/docs/ko/ai-ml/meta.json`):
     ```json
     {
       "title": "AI 및 머신러닝",
       "icon": "Brain",
       "pages": ["{article-slug}", "..."],
       "defaultOpen": false
     }
     ```

2. **Handling existing meta.json:**
   - If file exists, read current `pages` array
   - Ask user: "Where to add new article? (1: top, 2: bottom, 3: alphabetical)"
   - Preserve other user customizations (icon, defaultOpen, etc.)
   - If `pages` array exists, insert article slug; if not, create with `["{slug}", "..."]`

3. **Update/Create root meta.json**: `content/docs/{lang}/meta.json`

   - Check if category is listed in root `pages` array
   - If not, ask user: "Add '{category}' to root navigation? (yes/no)"
   - If yes, ask: "Where to add? (1: top, 2: bottom, 3: after specific item)"

   **Example root meta.json:**
   ```json
   {
     "title": "Documentation",
     "pages": [
       "index",
       "getting-started",
       "---[Book]Categories---",
       "ai-ml",
       "development",
       "data",
       "..."
     ]
   }
   ```

4. **Translation mapping for all 8 categories:**

   | Category | English | Chinese | French | Korean |
   |----------|---------|---------|--------|--------|
   | ai-ml | AI & Machine Learning | AI 与机器学习 | IA et Apprentissage Automatique | AI 및 머신러닝 |
   | development | Development | 开发 | Développement | 개발 |
   | data | Data | 数据 | Données | 데이터 |
   | design | Design | 设计 | Design | 디자인 |
   | content | Content | 内容 | Contenu | 콘텐츠 |
   | business | Business | 商业 | Affaires | 비즈니스 |
   | devops | DevOps | DevOps | DevOps | DevOps |
   | security | Security | 安全 | Sécurité | 보안 |

5. **Icon mapping for categories:**

   | Category | Icon | Alternative Icons |
   |----------|------|-------------------|
   | ai-ml | Brain | Cpu, Zap, Sparkles |
   | development | Code | Terminal, Braces, FileCode |
   | data | Database | BarChart, PieChart, TrendingUp |
   | design | Palette | Paintbrush, Layers, Layout |
   | content | FileText | BookOpen, Book, FileEdit |
   | business | Briefcase | TrendingUp, DollarSign, Users |
   | devops | Server | Cloud, Container, GitBranch |
   | security | Shield | Lock, ShieldCheck, Key |

**Important Notes:**
- Always create meta.json for ALL 4 languages, not just English
- Use localized titles from the translation mapping
- Use the `...` syntax to auto-include other pages: `["featured-article", "..."]`
- Never hardcode English titles in non-English meta.json files
- Preserve user's existing customizations when updating

### Step 9: Archive Original Content

Create archive directory:
```bash
mkdir -p "archive/{YYYY-MM}/{article-slug}/images"
```

Save the following files:

1. **original.md**: Original article content in Markdown
2. **metadata.json**:
   ```json
   {
     "source_url": "{original_url}",
     "download_date": "{ISO_8601_timestamp}",
     "title": "{original_title}",
     "author": "{author}",
     "languages": ["en", "zh", "fr", "ko"],
     "category": "{category}",
     "difficulty": "{difficulty}",
     "tags": ["{tag1}", "{tag2}", "{tag3}"],
     "published_files": {
       "en": "content/docs/en/{category}/{slug}.mdx",
       "zh": "content/docs/zh/{category}/{slug}.mdx",
       "fr": "content/docs/fr/{category}/{slug}.mdx",
       "ko": "content/docs/ko/{category}/{slug}.mdx"
     },
     "images": [
       {
         "original_url": "{image_url}",
         "local_path": "/images/docs/{slug}/{image-name}",
         "status": "success|failed"
       }
     ]
   }
   ```
3. **images/**: Copy of downloaded images (as backup)

### Step 10: Summary Report

Provide a comprehensive summary to the user:

```
✅ Article Import Complete!

📄 Article: {title}
🔗 Source: {source_url}
📁 Category: {category}
📊 Difficulty: {difficulty}
🏷️  Tags: {tag1, tag2, tag3, ...}

📝 Files Created:
  ✅ en: content/docs/en/{category}/{slug}.mdx
  ✅ zh: content/docs/zh/{category}/{slug}.mdx
  ✅ fr: content/docs/fr/{category}/{slug}.mdx
  ✅ ko: content/docs/ko/{category}/{slug}.mdx

📂 Navigation (meta.json):
  ✅ en: content/docs/en/{category}/meta.json ("{English Category Name}")
  ✅ zh: content/docs/zh/{category}/meta.json ("{Chinese Category Name}")
  ✅ fr: content/docs/fr/{category}/meta.json ("{French Category Name}")
  ✅ ko: content/docs/ko/{category}/meta.json ("{Korean Category Name}")
  📌 Article added to sidebar navigation
  🎨 Icon: {category_icon}

🖼️  Images: {successful_count}/{total_count} downloaded
  📂 Location: public/images/docs/{slug}/

📦 Archive: archive/{YYYY-MM}/{slug}/
  - original.md
  - metadata.json
  - images/ ({count} files)

⚠️  Issues (if any):
  - Failed images: {list_of_failed_urls}
  - meta.json conflicts: {any_merge_issues}
  - Warnings: {any_warnings}

🎉 Next Steps:
  1. Review the generated MDX files for accuracy
  2. Check sidebar navigation shows correct category names in all languages
  3. Test the article in your local Fumadocs site (npm run dev)
  4. Adjust translations or meta.json ordering if needed
  5. Verify images display correctly
```

## Error Handling

### Image Download Failures
- Retry once with a 2-second delay
- If still fails, log the failure and continue
- Keep the original URL in the MDX file
- Include failed URLs in the final report

### Translation Errors
- If one language fails, continue with others
- Log the error and notify user in final report
- At minimum, ensure English version is created

### Classification Uncertainty
- If unable to determine category, default to "content"
- If unable to determine difficulty, default to "intermediate"
- Always provide at least 3 tags (use generic terms if needed)

### MDX Validation Errors
- **Check for common syntax errors before saving**:
  - Scan for unescaped `<` in plain text (e.g., `<5`, `<number`, `<word`)
  - Verify all JSX tags are properly closed
  - Ensure code blocks are properly fenced with triple backticks
  - Check that blockquotes (`>`) don't interfere with JSX
- **Auto-fix common issues**:
  - Replace `<` with `&lt;` in plain text contexts
  - Replace `>` with `&gt;` in comparison contexts
  - Wrap problematic expressions in backticks if appropriate
- If validation fails after fixes, save as .md instead and notify user
- Provide specific error messages for debugging
- **Common MDX pitfalls to avoid**:
  - `<5k tokens` → `&lt;5k tokens` or "less than 5k tokens"
  - `<script>` in text → `&lt;script&gt;` or use code formatting
  - Unclosed JSX tags (always use `<Tag>...</Tag>` or self-close `<Tag />`)

## Examples

### Example 1: Technical Tutorial

**Input URL**: `https://example.com/react-hooks-guide`

**Expected Output**:
- Slug: `react-hooks-guide`
- Category: `development`
- Difficulty: `intermediate`
- Tags: `react`, `hooks`, `javascript`, `frontend`
- 4 MDX files created (en, zh, fr, ko)
- Images downloaded to `public/images/docs/react-hooks-guide/`

### Example 2: Data Science Article

**Input URL**: `https://example.com/pandas-data-analysis`

**Expected Output**:
- Slug: `pandas-data-analysis`
- Category: `data`
- Difficulty: `beginner`
- Tags: `python`, `pandas`, `data-analysis`, `tutorial`
- 4 MDX files with code blocks preserved
- Archive created with metadata

### Example 3: AI/ML Deep Dive

**Input URL**: `https://example.com/transformer-architecture-explained`

**Expected Output**:
- Slug: `transformer-architecture-explained`
- Category: `ai-ml`
- Difficulty: `advanced`
- Tags: `ai`, `machine-learning`, `transformers`, `nlp`, `deep-learning`
- Complex diagrams downloaded and referenced
- Technical terms preserved in all languages

## Important Notes

### Fumadocs Components
**Always refer to `references/fumadocs-components.md` before adding components.**

**CRITICAL RULE**: ❌ Never implement custom components. Only use Fumadocs built-in components.

Available components include:
- `<Cards>` and `<Card>` for card layouts
- `<Callout>` for important notes
- `<Tabs>` and `<Tab>` for tabbed content
- `<Steps>` and `<Step>` for step-by-step guides
- `<Files>`, `<Folder>`, `<File>` for file trees
- `<Accordion>` for collapsible content
- `<ImageZoom>` for zoomable images

### Translation Quality
- Technical accuracy is paramount
- Preserve code examples exactly
- Adapt cultural references when necessary
- Use appropriate technical terminology for each language
- Chinese: 使用简体中文，技术术语保持英文或使用通用译法
- French: Maintain formal tone, use standard technical terms
- Korean: Use appropriate honorifics and technical terminology

### File Organization
Follow Fumadocs conventions:
- Language-specific directories: `content/docs/{lang}/`
- Category subdirectories: `content/docs/{lang}/{category}/`
- Images in public: `public/images/docs/{slug}/`
- Archive by month: `archive/{YYYY-MM}/{slug}/`

## Troubleshooting

### "Jina API not accessible"
- Check internet connection
- Verify Jina API key (if required)
- Try Jina MCP as alternative
- Fall back to manual content input

### "Images not downloading"
- Check public/images/docs/ directory permissions
- Verify curl is installed: `which curl`
- Check image URLs are accessible
- Review firewall/proxy settings

### "MDX syntax errors"
- Review `references/fumadocs-components.md` for correct syntax
- Validate YAML frontmatter formatting
- Check for unclosed JSX tags
- Ensure code blocks use triple backticks

### "Translation taking too long"
- Translate one language at a time
- Skip non-essential languages if needed
- Use simpler translation prompts for faster processing

## Version History

- v1.0.0 (2025-11-15): Initial release
  - Multi-language support (en, zh, fr, ko)
  - 8-category classification system
  - Automatic image processing
  - MDX conversion with Fumadocs components
  - Archive system with full traceability
