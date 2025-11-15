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
- Jina API access or Jina MCP is configured
- `curl` is installed for image downloads
- Write access to `content/docs/` and `public/images/` directories

## Workflow

### Step 1: Get Article Information

Ask the user for the following information:
1. "What is the URL of the article you want to import?"
2. "What languages should I translate to? (Press Enter for default: en, zh, fr, ko)"
3. "Should I download and process images? (yes/no, default: yes)"

### Step 2: Download Article Content

Use Jina API or Jina MCP to fetch the article:

**Using Jina API**:
```bash
curl "https://r.jina.ai/{article_url}"
```

**Using Jina MCP**:
Use the MCP tool to fetch the article content.

Extract the following from the fetched content:
- Title
- Author (if available)
- Publication date (if available)
- Main content (body text)
- All image URLs

### Step 3: Generate Article Slug

Create a URL-friendly slug from the article title:
- Convert to lowercase
- Replace spaces with hyphens
- Remove special characters
- Keep only: a-z, 0-9, hyphens
- Maximum 60 characters

Example: "Building React Apps with TypeScript" → "building-react-apps-with-typescript"

### Step 4: Process Images

If user chose to download images:

1. Create image directory:
   ```bash
   mkdir -p "public/images/docs/{article-slug}"
   ```

2. For each image URL in the article:
   - Generate descriptive name from context (e.g., "component-tree", "data-flow")
   - Add index number: `{descriptive-name}-{index}.{ext}`
   - Download using curl with retry logic:
     ```bash
     curl -f -L -o "public/images/docs/{slug}/{image-name}" "{image_url}" || \
     curl -f -L -o "public/images/docs/{slug}/{image-name}" "{image_url}" || \
     echo "Failed to download: {image_url}"
     ```

3. Update image references in content:
   - Original: `![alt](https://example.com/image.png)`
   - Updated: `![alt](/images/docs/{article-slug}/component-tree-1.png)`

4. Keep original URLs for failed downloads (do not block the process)

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

For each target language (en, zh, fr, ko):

1. Load the appropriate translation prompt from `references/translation-prompts.md`

2. Translate the following:
   - Article title
   - Article description (first 1-2 sentences)
   - Main content body

3. **Important Translation Rules**:
   - Preserve all Markdown syntax exactly
   - Keep code blocks unchanged
   - Preserve image references (paths stay the same)
   - Maintain heading hierarchy
   - Keep technical terms in English where appropriate
   - Adapt examples to be culturally relevant if needed

4. Save original English version first, then translations

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

4. **Validate MDX Syntax**:
   - Ensure all JSX components are properly closed
   - Check that code blocks use correct syntax (triple backticks)
   - Verify frontmatter YAML is valid
   - Confirm no syntax errors that would break rendering

5. Create the file:
   ```bash
   mkdir -p "content/docs/{lang}/{category}"
   # Write the MDX content to file
   ```

### Step 8: Update Navigation (Optional)

Check if `content/docs/{lang}/{category}/meta.json` exists:
- If yes: Ask user if they want to add the new article to navigation
- If no: Create a basic meta.json with the new article

Example meta.json:
```json
{
  "title": "{Category Name}",
  "pages": [
    "{article-slug}"
  ]
}
```

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

🖼️  Images: {successful_count}/{total_count} downloaded
  📂 Location: public/images/docs/{slug}/

📦 Archive: archive/{YYYY-MM}/{slug}/
  - original.md
  - metadata.json
  - images/ ({count} files)

⚠️  Issues (if any):
  - Failed images: {list_of_failed_urls}
  - Warnings: {any_warnings}

🎉 Next Steps:
  1. Review the generated MDX files for accuracy
  2. Test the article in your local Fumadocs site
  3. Adjust translations if needed
  4. Update meta.json for navigation (if not done automatically)
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
- Check for common syntax errors before saving
- If validation fails, save as .md instead and notify user
- Provide specific error messages for debugging

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
