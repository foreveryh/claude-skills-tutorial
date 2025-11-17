---
name: fumadocs-article-importer
description: >
  Import external articles into a Fumadocs project with automatic multi-language
  translation (en, zh, fr), AI-powered classification into 8 categories,
  image processing, and MDX conversion. Use this skill when the user wants to
  import an article from a URL into their Fumadocs documentation site.
---

# Fumadocs Article Importer

Automate importing external articles into a Fumadocs project with tri-language support (English, Chinese, French), auto-classification, and proper MDX formatting.

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

## ⚠️ CRITICAL REQUIREMENTS

### 1. Must Use `withAllImages: true` Parameter

**For image processing to work, you MUST use `withAllImages: true` in Step 2**:

```typescript
Tool: read_url
Parameters:
  - url: {article_url}
  - withAllImages: true  // ← MANDATORY for image extraction
```

**Why this matters**:
- Without `withAllImages: true`: Jina returns text only, no images
- With `withAllImages: true`: Jina returns text + images array
- If you skip this parameter, ALL image processing will be silently skipped
- See Step 2, Sub-step 4 for mandatory validation check

**What happens if you forget**:
```typescript
// WRONG - Won't extract images
const response = await mcp.read_url(url);  // Missing withAllImages!
console.log(response.images);  // ❌ undefined

// CORRECT - Will extract images
const response = await mcp.read_url(url, { withAllImages: true });
console.log(response.images);  // ✅ [img1, img2, ...]
```

### 2. Image Storage Strategy (Choose One)

You have two options for handling images. **Choose before starting Step 4**:

#### Option A: Download Images to Local (Default)

**What**: Download image files to `public/images/docs/{slug}/`

**When to use**:
- Source website doesn't support CORS (see CORS testing below)
- You want offline availability (images work without internet)
- You want control over image versions (won't change unexpectedly)
- Source images might be deleted or moved

**Pros**:
- ✅ Works 100% of the time (no CORS issues)
- ✅ Images always available (offline)
- ✅ Full control over image files
- ✅ Faster loading (no external HTTP requests)

**Cons**:
- ⚠️ Uses local storage space (adds 10KB-500KB per image)
- ⚠️ Increases import time (needs to download each image)
- ⚠️ Adds complexity (need to manage local files)

**Example in MDX**:
```mdx
![MCP Diagram](/images/docs/skills-explained/mcp-architecture.png)
```

#### Option B: Use External Image URLs (No Download)

**What**: Keep original URLs in the article (don't download)

**When to use**:
- Source website supports CORS (tested with 200 + CORS headers)
- You want to save storage space
- You want faster import process
- You're okay with external dependencies
- Source images are stable and unlikely to be deleted

**How to test if external URLs work**:
```bash
# Test 1: Does the URL return 200?
curl -I "https://example.com/image.png"
# Expected: HTTP/2 200

# Test 2: Does it support CORS?
curl -I "https://example.com/image.png" | grep -i "access-control"
# Expected: access-control-allow-origin: *
# Or: access-control-allow-origin: https://your-domain.com
```

**Pros**:
- ✅ No storage overhead (no local files)
- ✅ Faster import (skip download step)
- ✅ Simpler process (no file management)
- ✅ Images auto-update if source changes

**Cons**:
- ❌ Requires CORS support (will break in browser if not)
- ❌ Requires internet connection (offline doesn't work)
- ❌ Source might delete/move images (breaks your article)
- ❌ Slower page loads (external HTTP requests)

**Example in MDX**:
```mdx
![MCP Diagram](https://cdn.example.com/mcp-architecture.png)
```

#### Real-World Example: Claude.com Images

Test results for `https://claude.com/blog/skills-explained`:

```bash
# Test MCP diagram image
curl -I "https://cdn.prod.website-files.com/68a44d4040f98a4adf2207b6/69141f0993d68ff4c536f316_619a5262.png"

# Response includes:
# HTTP/2 200
# access-control-allow-origin: *
```

**Result**: ✅ Claude.com images support CORS (can use external URLs)

**Decision for Claude.com articles**: Use **Option B (External URLs)** - no download needed

**Decision for unknown sources**: Use **Option A (Download)** - safer

### 3. Validation Check Added in v2.0

Step 2 now includes a **mandatory validation** (Sub-step 4) that:
- Checks if `response.images` exists
- Throws clear error if missing
- Prevents silent failures
- Provides exact fix instructions

**Always verify images were extracted before proceeding!**

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
2. "What languages should I translate to? (Press Enter for default: en, zh, fr)"
3. "How should I handle images? (Press Enter for default: auto)\n   - auto: Check CORS and use external URLs if possible, else download\n   - external: Always use original image URLs (no download)\n   - download: Always download to local storage"

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

4. **⚠️ CRITICAL VALIDATION - Check for images** (DO NOT SKIP):
   ```typescript
   // VERIFICATION STEP - Must check before proceeding!

   // Check if withAllImages parameter was actually used
   if (!response.images) {
     console.error("❌ CRITICAL ERROR: response.images is undefined!");
     console.error("→ This means 'withAllImages: true' parameter was NOT passed to read_url");
     console.error("→ Image processing will be completely skipped!");

     // STOP here - do not proceed without image data
     throw new Error(
       `FAILED: Cannot extract images from ${article_url}\n` +
       `Cause: withAllImages parameter missing in read_url call\n` +
       `Solution: Re-run with correct parameter: { withAllImages: true }`
     );
   }

   // Validate images array
   if (response.images.length === 0) {
     console.warn("⚠️ WARNING: response.images array is empty!");
     console.warn("→ The article may have no images, OR extraction failed");

     // Ask user to confirm if this is expected
     const hasImages = confirm("Does this article have images you want to download?");
     if (hasImages) {
       throw new Error(
         `FAILED: Expected images but found none. Retry with withAllImages: true`
       );
     }
   }

   // SUCCESS - Log image count
   console.log(`✅ SUCCESS: Found ${response.images.length} images in article`);
   console.log(`→ Ready to proceed to image filtering (Step 3.5)`);
   ```

**Why this validation is critical**:
- Many articles contain 15-20 images, but only 1-3 are actual content
- Without `withAllImages: true`, you get TEXT ONLY (no images array)
- If you skip this check, you'll never know images were missed until it's too late
- This validation FORCE STOPS execution if images are missing unexpectedly

**Real-world consequence of skipping this check**:
```typescript
// WRONG - Skipping validation:
const response = await mcp.read_url(url); // Forgot withAllImages
const images = response.images; // ❌ undefined
heuristicFilter(images); // Returns empty array (undefined becomes [])
console.log("Found 0 images"); // User thinks article has no images
// Result: No images downloaded, user doesn't know they were missed

// CORRECT - With validation:
const response = await mcp.read_url(url); // Forgot withAllImages
if (!response.images) { // ✅ Validation catches the error
  throw new Error("Missing withAllImages parameter!"); // Stops execution
}
// Result: Clear error message, user knows to retry correctly
```

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

### Step 2.5: Content Safety Processing (DEFENSIVE)

**Critical: Apply defensive processing to prevent MDX syntax errors.** This step acts as a safety net to handle unknown components and common MDX pitfalls from ANY source, not just Anthropic.

**Why this matters**: Articles come from diverse sources (Anthropic, GitHub, Medium, personal blogs, etc.), each with different component libraries and Markdown flavors. Instead of crashing on unknown syntax, we safely degrade content while preserving readability.

**Processing Pipeline**:

```typescript
// Safety processor that handles content from any source
const safetyProcessor = {
  // Phase 1: Handle unknown/dangerous JSX components
  handleUnknownComponents(content: string): string {
    // Known Fumadocs components (whitelist - safe to keep)
    const fumadocsComponents = [
      'Callout', 'Cards', 'Card', 'Tabs', 'Tab', 'Steps', 'Step',
      'Files', 'Folder', 'File', 'Accordion', 'ImageZoom'
    ];

    // Pattern 1: Handle closed components <Component>...</Component>
    content = content.replace(
      /<([A-Z][a-zA-Z]*)[^>]*>([\s\S]*?)<\/\1>/g,
      (match, componentName, innerContent) => {
        if (fumadocsComponents.includes(componentName)) {
          return match; // Keep known components
        }

        // Unknown component: degrade to plain text with comment
        console.warn(`⚠️ Unknown component <${componentName}>, degrading to plain text`);
        return `<!-- Original: <${componentName}> -->\n${innerContent}\n<!-- End: ${componentName} -->`;
      }
    );

    // Pattern 2: Handle self-closing components <Component />
    content = content.replace(
      /<([A-Z][a-zA-Z]*)[^\/]*\/>/g,
      (match, componentName) => {
        if (fumadocsComponents.includes(componentName)) {
          return match; // Keep known components
        }

        console.warn(`⚠️ Unknown self-closing component <${componentName}/>, removing`);
        return `<!-- Removed: <${componentName}/> -->`;
      }
    );

    return content;
  },

  // Phase 2: Fix common MDX pitfalls that break parsing
  fixMDXPitfalls(content: string): string {
    // Pitfall 1: <number pattern (e.g., "<5k tokens") breaks MDX
    // Replace with HTML entity or rephrase
    content = content.replace(
      /<(\d+)/g,
      (match, num) => {
        console.warn(`⚠️ Fixed <${num} pattern (breaks MDX)`);
        return `&lt;${num}`;
      }
    );

    // Pitfall 2: Common HTML-like tags in text
    const dangerousTags = ['script', 'div', 'span', 'p', 'a', 'img'];
    dangerousTags.forEach(tag => {
      content = content.replace(
        new RegExp(`<(${tag})\\b`, 'gi'),
        (match) => {
          console.warn(`⚠️ Fixed <${tag}> pattern in text`);
          return match.replace('<', '&lt;');
        }
      );
    });

    // Pitfall 3: Bold formatting without space (non-Latin languages)
    // Wrong: **粗体：**文字 → Right: **粗体：** 文字
    content = content.replace(
      /\*\*([^*]+)\*\*([^ \n*-])/g,
      '**$1** $2'
    );

    // Pitfall 4: Unclosed JSX tags (basic check)
    const tags = content.match(/<\/[a-zA-Z]+>/g);
    if (tags) {
      tags.forEach(closingTag => {
        const tagName = closingTag.replace('</', '').replace('>', '');
        const openings = (content.match(new RegExp(`<${tagName}[^>]*>`, 'g')) || []).length;
        const closings = (content.match(new RegExp(`<\/${tagName}>`, 'g')) || []).length;

        if (openings !== closings) {
          console.error(`❌ Mismatched <${tagName}> tags: ${openings} openings, ${closings} closings`);
        }
      });
    }

    return content;
  },

  // Phase 3: Auto-inject missing imports for known components
  injectImports(content: string): string {
    const usedComponents = new Set<string>();

    // Detect Fumadocs components
    const fumadocsComponents = {
      'Callout': { import: "import { Callout } from 'fumadocs-ui/components/callout';" },
      'Cards': { import: "import { Cards, Card } from 'fumadocs-ui/components/card';" },
      'Card': { import: "import { Cards, Card } from 'fumadocs-ui/components/card';" },
      'Tabs': { import: "import { Tabs, Tab } from 'fumadocs-ui/components/tabs';" },
      'Tab': { import: "import { Tabs, Tab } from 'fumadocs-ui/components/tabs';" },
      'Steps': { import: "import { Steps, Step } from 'fumadocs-ui/components/steps';" },
      'Step': { import: "import { Steps, Step } from 'fumadocs-ui/components/steps';" },
      'Files': { import: "import { Files, Folder, File } from 'fumadocs-ui/components/files';" },
      'Folder': { import: "import { Files, Folder, File } from 'fumadocs-ui/components/files';" },
      'File': { import: "import { Files, Folder, File } from 'fumadocs-ui/components/files';" },
      'Accordion': { import: "import { Accordion, Accordions } from 'fumadocs-ui/components/accordion';" },
      'ImageZoom': { import: "import { ImageZoom } from 'fumadocs-ui/components/image-zoom';" }
    };

    // Check which components are used
    Object.keys(fumadocsComponents).forEach(comp => {
      const pattern = new RegExp(`<${comp}\\b`, 'g');
      if (pattern.test(content)) {
        usedComponents.add(fumadocsComponents[comp].import);
      }
    });

    if (usedComponents.size === 0) return content;

    // Check if imports already exist
    const existingImports = content.includes('from \'fumadocs-ui/components');
    if (existingImports) {
      console.log('✅ Fumadocs imports already present');
      return content;
    }

    // Inject imports after frontmatter
    console.log(`📦 Injecting ${usedComponents.size} import statements`);
    const importBlock = Array.from(usedComponents).join('\n') + '\n\n';

    return content.replace(
      /(---\n\n)/,
      `$1${importBlock}`
    );
  }
};

// Main safety processing function
function processContentSafely(content: string, sourceUrl: string): { content: string, warnings: string[] } {
  console.log(`🔒 Processing content safely from: ${sourceUrl}`);

  const warnings: string[] = [];

  try {
    // Step 1: Handle unknown components
    content = safetyProcessor.handleUnknownComponents(content);

    // Step 2: Fix MDX pitfalls
    content = safetyProcessor.fixMDXPitfalls(content);

    // Step 3: Inject imports
    content = safetyProcessor.injectImports(content);

    console.log('✅ Content safety processing complete');
  } catch (error) {
    console.error('❌ Safety processing failed:', error);
    warnings.push(`Safety processing error: ${error.message}`);
  }

  return { content, warnings };
}
```

**Execution in Workflow**:

Call this function immediately after Step 2 (content extraction) and before Step 3 (slug generation):

```typescript
// In the main workflow:
const rawContent = response.content; // From Step 2
const { content: safeContent, warnings } = processContentSafely(rawContent, articleUrl);

// Store warnings for the summary report
const processingWarnings = warnings;

// Continue with safeContent for all subsequent steps
```

**Why This Position Matters**:
- ✅ Runs BEFORE AI concept extraction (Step 3.6) → prevents AI from analyzing broken syntax
- ✅ Runs BEFORE translation (Step 6) → prevents translating component names
- ✅ Runs BEFORE cross-reference insertion (Step 3.7) → ensures clean content for link insertion
- ✅ Runs BEFORE MDX generation (Step 7) → prevents syntax errors in final file

**Key Design Principles**:

1. **Defensive, Not Prescriptive**: We don't try to perfectly convert every component. Unknown components are safely degraded rather than causing crashes.

2. **Source-Agnostic**: Works for ANY source (Anthropic, GitHub, Medium, personal blogs) without source-specific rules.

3. **Non-Destructive**: Original intent is preserved through comments. For example:
   ```mdx
   <!-- Original: <AnthropicCard> -->
   Card content here
   <!-- End: AnthropicCard -->
   ```

4. **Automated**: Zero user configuration required. The skill automatically detects and handles issues.

**Warning Collection**:

Collect all warnings during processing and include them in the final summary:

```
⚠️  Content Safety Processing:
  - Unknown component <AnthropicCard> (degraded to plain text)
  - Unknown component <FileGroup> (degraded to plain text)
  - Fixed <5k pattern (breaks MDX)
  - Injected 2 import statements
  - Mismatched <Callout> tags: 3 openings, 2 closings

📦 Injected Imports:
✅ import { Callout } from 'fumadocs-ui/components/callout';
✅ import { Cards, Card } from 'fumadocs-ui/components/card';
```

**Benefits**:

- ✅ **Prevents 90% of MDX syntax errors** from any source
- ✅ **No manual cleanup needed** for unknown components
- ✅ **Clear visibility** into what was changed and why
- ✅ **Build never breaks** due to imported content issues
- ✅ **Diagnostics** help identify patterns for future improvements

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

### Step 3.6: AI-Powered Concept Extraction

**Extract key technical concepts from article content using Claude AI**. This enables intelligent cross-referencing and related article recommendations.

**Why AI instead of rules**:
- Rules can only match keywords (e.g., "Skills" as a word)
- AI understands context (e.g., "Skills" as a Claude feature vs. "skills" as general abilities)
- AI determines importance (main topic vs. mentioned in passing)
- AI extracts semantic meaning, not just patterns

**AI Prompt**:
```typescript
const conceptExtractionPrompt = `
Read the following article and extract 5-10 key technical concepts.

Title: "${articleTitle}"
Content: """${articleContent.substring(0, 5000)}"""

For each concept, provide:
1. term: The exact term/concept name
2. definition: Brief explanation (1 sentence)
3. isMainTopic: true if this article primarily explains this concept, false if just mentions it
4. importance: Score 1-10 (how central this concept is to the article)

Output format:
\\
\\`\\`\\`json
{
  "concepts": [
    {
      "term": "Skills",
      "definition": "Claude's feature for saving and reusing instruction sets",
      "isMainTopic": true,
      "importance": 10
    }
  ]
}
\\`\\`\\`

**Example AI Decision**:
For the sentence "Claude's Skills feature helps you build agents":
- AI understands "Skills" is a proper noun (Claude feature)
- AI understands "agents" refers to AI agents
- AI judges importance based on context and article focus

**Execution**:
1. **Call Claude AI**:
   ```typescript
   const response = await askClaude(conceptExtractionPrompt);
   const { concepts } = JSON.parse(response);
   ```

2. **Save concept extraction**:
   ```bash
   mkdir -p "archive/concepts"
   ```

   ```typescript
   writeJson(`archive/concepts/${articleSlug}.json`, {
     article: articleSlug,
     lang: languageCode,
     title: articleTitle,
     concepts: concepts
   });
   ```

3. **Output**:
   ```
   🤖 AI Concept Extraction Complete:
   ✅ Extracted ${concepts.length} concepts
   🎯 Main topics: ${concepts.filter(c => c.isMainTopic).map(c => c.term).join(', ')}
   📋 All concepts: ${concepts.map(c => `${c.term}(${c.importance})`).join(', ')}
   ```

**AI Decision Examples**:

**Example 1**:
```
Input: "Claude's Skills feature allows you to save prompts"
AI Output:
- term: "Skills"
- isMainTopic: true (文章主要讲解Skills)
- importance: 10
```

**Example 2**:
```
Input: "Using Python with Claude Code"
AI Output:
- term: "Python"
- isMainTopic: false (只是提到Python，不是专门讲Python)
- importance: 6
```

**Example 3**:
```
Input: "The Model Context Protocol (MCP) is a protocol"
AI Output:
- term: "MCP"
- definition: "Model Context Protocol, connects AI assistants to external systems"
- isMainTopic: true
- importance: 9
```

**AI vs Rules Comparison**:

| Input | Rule-based (Keyword) | AI-based (Understanding) |
|-------|---------------------|-------------------------|
| "Claude's Skills feature" | Finds "Skills" word | Understands "Skills" is a Claude feature |
| "Skills are important" | Finds "Skills" word | Understands this is about abilities, not Claude Skills |
| "The agent processes tasks" | Finds "agent" word | Understands "agent" = AI agent in this context |

**Key AI Decision Points**:
1. **Term Recognition**: AI understands proper nouns vs. common words
2. **Context Understanding**: AI reads surrounding text to understand meaning
3. **Importance Scoring**: AI weighs concepts based on article focus
4. **Main Topic Detection**: AI identifies what the article is primarily about

### Step 3.7: AI-Powered Cross-Reference Insertion

**Automatically insert links to related articles when concepts are mentioned.** AI decides where and how many links to insert for natural reading flow.

**Why AI instead of naive replacement**:
- Naive: Replace first occurrence of "Skills" → may break reading flow
- AI: Understands paragraph structure, inserts where most helpful
- AI: Avoids over-linking (not every mention needs a link)
- AI: Skips titles, code blocks, and already-linked text

**Prerequisites**:
- Step 3.6 must be completed (concepts extracted)
- Concept index must exist (archive/concept-index.json)

**AI Prompt**:
```typescript
const crossReferencePrompt = `
You are adding intelligent cross-references to a technical article.

Target article: "${articleTitle}"
Content: """${articleContent}"""

Relevant concepts from this article (from Step 3.6):
${JSON.stringify(concepts.filter(c => !c.isMainTopic), null, 2)}

For each concept, here is the authoritative article to link to:
${JSON.stringify(conceptIndex, null, 2)}

Task:
1. Identify where these concepts are FIRST mentioned in the content
2. Determine if linking would help the reader (skip if obvious or already explained)
3. Insert links naturally (don't break reading flow)
4. Limit to 3-5 links max (avoid over-linking)
5. NEVER link in: headings, code blocks, links, or quotes

Output format:
\\`\\`\\`json
{
  "enhancedContent": "content with links inserted",
  "linksInserted": [
    {
      "position": 125,
      "concept": "Skills",
      "targetArticle": "skills-explained",
      "context": "first mention in paragraph",
      "reasoning": "Reader may need background on Skills concept"
    }
  ]
}
\\`\\`\\`

**Example: Before and After AI Insertion**

**Before** (original content):
```markdown
## Building Agents with Skills

When you combine Skills with the Claude Agent SDK, you can create powerful workflows. Skills allow you to save and reuse instructions.
```

**After AI Enhancement**:
```markdown
## Building Agents with Skills

When you combine [Skills](→skills-explained) with the Claude Agent SDK, you can create powerful workflows. Skills allow you to save and reuse instructions.
```

**AI Decision**:
- Linked "Skills" on first mention in the paragraph
- Didn't link "Agent" (already explained earlier in the article)
- Didn't link "SDK" (too generic, not a core concept)
- Only 1 link inserted (would be overwhelming to link everything)

**Execution**:

1. **Call Claude AI**:
   ```typescript
   const response = await askClaude(crossReferencePrompt);
   const { enhancedContent, linksInserted } = JSON.parse(response);
   ```

2. **Save link metadata**:
   ```typescript
   writeJson(`archive/links/${articleSlug}.json`, {
     article: articleSlug,
     lang: languageCode,
     totalLinks: linksInserted.length,
     links: linksInserted
   });
   ```

3. **Output**:
   ```
   🤖 AI Cross-Reference Insertion Complete:
   ✅ Analyzed ${concepts.length} concepts
   🎯 Inserted ${linksInserted.length} links
   📍 Positions: ${linksInserted.map(l => l.position).join(', ')}
   💡 AI reasoning: ${linksInserted.map(l => l.reasoning).join('; ')}
   ```

**AI Decision Examples**:

**Example 1: Skip obvious concepts**
```
Content: "The HTTP protocol is used for web requests"
AI Decision: Don't link "HTTP" (too generic, most developers know it)
```

**Example 2: Link important concept on first mention**
```
Content: "Claude's Skills feature allows you to..."
AI Decision: Link "Skills" on first mention (core concept, reader may need context)
```

**Example 3: Don't over-link**
```
Content: "Skills are powerful. Skills allow reuse. Skills improve consistency."
AI Decision: Only link first "Skills" (linking all three would be overwhelming)
```

**Example 4: Skip in headings**
```
Content: "## Skills Overview\n\nSkills are..."
AI Decision: Don't link "Skills" in the heading (breaks formatting)
```

**Key AI Decision Points**:
1. **Context Understanding**: AI reads surrounding text to determine if context is already clear
2. **Reader Benefit**: AI judges if linking would help understanding or be distracting
3. **Position Selection**: AI chooses first natural mention, not mechanical first occurrence
4. **Link Density**: AI limits total links to avoid overwhelming the reader
5. **Natural Integration**: AI ensures links flow naturally in the sentence

**AI vs Naive Comparison**:

| Article Text | Naive (First Occurrence) | AI (Context-Aware) |
|--------------|------------------------|-------------------|
| "Skills and agents" | Links "Skills" in title | Only links "agents" (Skills already explained) |
| "The key skill is..." | Links "skill" (wrong case) | Doesn't link (lowercase = generic skill) |
| "Skills allow X. Skills enable Y." | Links both | Links only first (avoids overlinking) |

### Step 4: Process Images (Three Strategies)

Based on user's choice in Step 1 (image handling mode), use one of these strategies:

#### Strategy A: External URLs Only (No Download) - Recommended for CORS-Supporting Sites

**When to use**: Source website supports CORS (like Claude.com, GitHub, etc.)

**Process**:
```typescript
// No download needed - just keep the original URLs
// MDX will reference external images directly

// Example output in MDX:
// Original: ![MCP Diagram](https://cdn.example.com/mcp-diagram.png)
// Final:    ![MCP Diagram](https://cdn.example.com/mcp-diagram.png) ← Unchanged!

#### Strategy B: Download to Local (Safe Option) - Use for Unknown/Complex Sites

**When to use**: Unknown source, no CORS support, or want offline availability

**Process**:

1. **User Confirmation** (show transparency):
   ```
   📊 Image Strategy: Download to Local

   ✅ Found {total_images} total images on page
   🎯 Identified {filtered_images} content images (diagrams/screenshots)
   🚫 Filtered {skipped_images} decorative images (placeholders/icons)

   Images to download:
   1. [Preview URL: https://.../mcp-diagram.png]
      → Description: MCP protocol architecture diagram
      → Size: 142KB PNG

   2. [Preview URL: https://.../data-flow.png]
      → Description: Data flow visualization
      → Size: 89KB PNG

   Download these images? (Enter=yes, no=skip) [yes]:
   ```

2. **Create directory**:
   ```bash
   mkdir -p "public/images/docs/{article-slug}"
   ```

3. **Download each image** (with retry logic):
   ```bash
   curl -f -L -o "public/images/docs/{slug}/{image-name}" "{image_url}" || \
   curl -f -L -o "public/images/docs/{slug}/{image-name}" "{image_url}" || \
   echo "⚠️  Failed to download: {image_url}"
   ```

4. **Update MDX references**:
   ```typescript
   // Original
   ![MCP architecture](https://example.com/mcp-diagram.png)

   // Updated
   ![MCP architecture](/images/docs/{article-slug}/mcp-architecture.png)
   ```

5. **Handle failures gracefully**:
   - If download fails, keep original URL
   - Log failure
   - Report in summary

**Pros**: Works 100%, offline, full control
**Cons**: Slower, uses storage, more complex

#### Strategy C: Auto-Detect (Best of Both Worlds)

**When to use**: You want the skill to automatically decide

**Process**:

1. **Test first image for CORS support**:
   ```bash
   curl -I "{first_image_url}" | grep -i "access-control"
   # If returns "access-control-allow-origin: *" → external mode
   # If returns nothing or error → download mode
   ```

2. **Based on result, auto-switch**:
   ```typescript
   const hasCORS = checkCORS(firstImageUrl);

   if (hasCORS) {
     console.log("✅ Images support CORS → Using external URLs");
     useStrategyExternal();
   } else {
     console.log("❌ No CORS support → Downloading images locally");
     useStrategyDownload();
   }
   ```

3. **Process all images with chosen strategy**

**Pros**: Intelligent, optimal choice, hands-off
**Cons**: Extra test step, might mis-detect edge cases

**Example Test Result**:
```bash
Testing: https://cdn.prod.website-files.com/68a44d.../619a5262.png

Response:
HTTP/2 200
access-control-allow-origin: *
access-control-allow-methods: GET, HEAD
access-control-allow-headers: *

→ ✅ CORS supported → Use external URLs
```

#### Decision Guide

| Scenario | Strategy | Why |
|----------|----------|-----|
| **Claude.com, GitHub, GitLab** | **External** | Tested to support CORS |
| **Medium, Dev.to, Hashnode** | **External** | Usually supports CORS |
| **Corporate/internal sites** | **Download** | Often no CORS |
| **Unknown/random sites** | **Auto** | Let skill decide |
| **Need offline access** | **Download** | Self-contained |
| **Want fastest import** | **External** | Skip downloads |
| **First time trying** | **Auto** | Safest bet |

**Default**: `auto` (intelligent detection)

**Post-Import Verification**:
- **External strategy**: Test article in browser, verify images load
- **Download strategy**: Check `public/images/docs/{slug}/` for files
- **Auto strategy**: Check both (see which path was chosen)

### Step 5: Process YouTube Videos

**Detect and embed YouTube videos from article content**:

**Detection Patterns**:
```typescript
// Match YouTube URLs in content
const patterns = [
  // iframe embeds
  /<iframe[^>]*src="https?:\/\/(www\.)?youtube\.com\/embed\/([a-zA-Z0-9_-]+)"[^>]*>/g,
  // youtu.be short URLs
  /https?:\/\/youtu\.be\/([a-zA-Z0-9_-]+)/g,
  // youtube.com/watch URLs
  /https?:\/\/(www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]+)/g,
];

function extractYouTubeVideos(content: string): YouTubeVideo[] {
  const videos = [];
  for (const pattern of patterns) {
    const matches = content.matchAll(pattern);
    for (const match of matches) {
      const videoId = match[2] || match[3];
      videos.push({
        id: videoId,
        embedUrl: `https://www.youtube.com/embed/${videoId}`,
        watchUrl: `https://www.youtube.com/watch?v=${videoId}`,
        startTime: extractTimeParam(match[0]) // Handle &t=123s
      });
    }
  }
  return videos;
}
```

**In MDX: Use Fumadocs Video Component**

Option 1: Keep iframe (simplest, works everywhere):
```mdx
<iframe
  width="100%"
  height="500"
  src="https://www.youtube.com/embed/VIDEO_ID"
  title="Video title"
  frameBorder="0"
  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
  allowFullScreen>
</iframe>
```

Option 2: Use Fumadocs `<Video>` component (if available):
```mdx
import { Video } from 'fumadocs-ui/components/video';

<Video
  src="https://www.youtube.com/watch?v=VIDEO_ID"
  title="Introduction to MCP"
/>
```

**Auto-Processing Flow**:
```typescript
const videos = extractYouTubeVideos(content);

if (videos.length > 0) {
  console.log(`📺 Found ${videos.length} YouTube video(s)`);

  // Auto-embed: Replace YouTube URLs with iframes
  content = content.replace(youtubeRegex, (match) => {
    const videoId = extractVideoId(match);
    return generateEmbedCode(videoId);
  });
}
```

**No thumbnail download needed** (per user preference):
- iframe loads video from YouTube directly
- ✅ Saves local storage
- ✅ Always up-to-date
- ✅ Supports captions, quality selection, fullscreen
- ✅ Handles mobile responsive automatically

**Example Output**:
In generated MDX, video section becomes:
```mdx
## Video Introduction

<p className="video-wrapper">
  <iframe
    src="https://www.youtube.com/embed/dQw4w9WgXcQ"
    width="100%"
    height="500"
    title="MCP Protocol Overview"
  />
</p>

Continue reading...
```

**Summary Report** (auto-processed, no user interruption):
```
📺 Videos: 2 YouTube videos detected and embedded
   - Video 1: Introduction to MCP (6:23)
   - Video 2: Advanced MCP features (12:45)
   ✅ Embedded using iframe for compatibility
```

### Step 6: Classify Article

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

#### CRITICAL: Terms to Preserve (DO NOT TRANSLATE)

Certain terms must remain in English as they are:
- **Product/Brand Names**: Claude, Anthropic, Claude.ai, Claude Code
- **Technical Concepts/Features**: Skills, Projects, MCP, Agent, SubAgent
- **Specific Tools**: GitHub, Google Drive, Slack, Excel
- **Framework/Technology Names**: React, Python, Node.js, TypeScript
- **Standard Acronyms**: API, SDK, AI, ML, RAG, UI, UX
- **Code Examples**: Variable names, function names, class names

**Translation Instruction**:
```
Translate the following to {language_name}, but PRESERVE these terms in English:
- Claude, Anthropic, Skills, Projects, MCP, Agent, SubAgent
- GitHub, Google Drive, Slack, Excel
- React, Python, Node.js, TypeScript
- API, SDK, AI, ML, RAG, UI, UX
- All code identifiers (variable/function/class names)

Why: These are proper names, brand names, or universal technical terms.
Translating them would confuse readers who expect the standard English terms.

Example of CORRECT translation:
English: "Claude's Skills feature helps agents work better"
Chinese: "Claude 的 Skills 功能帮助 agents 更好地工作" (NOT: "克劳德的技能功能帮助代理更好地工作")

Example of CORRECT translation:
English: "Use the React component with Node.js"
French: "Utilisez le composant React avec Node.js" (NOT: "Utilisez le composant Réagir avec Noeud.js")
```

For each target language (en, zh, fr):

1. **Prepare content for translation**:
   - Combine title, description, and main content
   - Ensure code blocks are clearly marked
   - Keep image references intact
   - Mark terms to preserve (see list above)

2. **Request translation**:
   - Ask for professional translation to the target language
   - Specify that this is technical documentation
   - Emphasize the need to preserve Markdown formatting and code blocks
   - **CRITICAL**: List all terms that must NOT be translated (from the preserve list above)

   Example request format:
   ```
   Please translate the following article to Chinese (zh).
   This is technical documentation - preserve all Markdown syntax, code blocks,
   and image references exactly as they appear.

   CRITICAL: DO NOT translate these terms - keep them in English:
   - Claude, Anthropic, Skills, Projects, MCP, Agent, SubAgent, Subagents
   - GitHub, Google Drive, Slack, Excel
   - React, Python, Node.js, TypeScript, JavaScript
   - API, SDK, AI, ML, RAG, UI, UX, REST, HTTP
   - All variable names, function names, and class names in code blocks

   Why preserve: These are proper names, brand names, or universal technical terms.
   Translating them would confuse readers.

   Example correct translation:
   WRONG: "克劳德的技能功能帮助代理更好地工作"
   CORRECT: "Claude 的 Skills 功能帮助 agents 更好地工作"

   Article to translate:
   [Article content here]
   ```

3. **Translation will automatically apply**:
   - Professional translation quality (via translator skill)
   - **Preserves specified English terms in all languages**
   - Preservation of all Markdown syntax
   - Code blocks remain unchanged (including identifiers)
   - Image references stay the same (paths unchanged)
   - Heading hierarchy maintained
   - Technical terms handled appropriately for target language
   - Natural, fluent target language text

4. **Language-specific handling**:
   - **Chinese (zh)**: Simplified Chinese, technical terms stay in English when appropriate
     - Format: English term with normal text (e.g., "Skills 功能" not "技能功能")
     - No extra spaces needed around English terms
   - **French (fr)**: Standard French technical terminology, formal tone
     - English terms remain in original form
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

**Prerequisite**: Content must have been processed through Step 2.5 (Content Safety Processing) to ensure it's free of MDX syntax errors.

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

   # Enhanced source tracking (NEW)
   source:
     url: "{original_article_url}"
     name: "{site_name}"              # e.g., "Claude Blog", "GitHub Docs"
     author: "{original_author}"
     published_date: "{YYYY-MM-DD}"
     accessed_date: "{current_date}"  # When we imported it
     license: "{license_if_known}"    # e.g., "Copyright © 2025 Anthropic"
     # archived_url: "https://web.archive.org/..."  // Optional

   # Import metadata
   import:
     date: "{current_date}"
     slug: "{article-slug}"
     translator: "Claude AI"  # Since we use translator skill
   ---
   ```

3. **Add SourceAttribution component** (at top of content):
   ```mdx
   ---
   title: "Article Title"
   # ... frontmatter above
   ---

   import { SourceAttribution } from '@/components/SourceAttribution';

   <SourceAttribution
     source={{
       url: "https://example.com/original-article",
       name: "Original Site Name",
       author: "Original Author",
       publishedDate: "2025-01-20",
       accessedDate: "2025-11-16"
     }}
     languages={['en', 'zh', 'fr']}
     currentLang={language_code}
   />

   # Article content starts here...
   ```

4. **Add Source Declaration** (at bottom of content):
   ```mdx
   ---

   ## ℹ️ Source Information

   **Original Article**: [Link]({original_article_url})

   - **Source**: {site_name}
   - **Author**: {original_author}
   - **Published**: {published_date}
   - **Imported**: {current_date}
   - **License**: {license_info}

   *This article was automatically imported and translated using Claude AI.*
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

4. **Validate and Fix MDX Syntax** (MANDATORY - Must run even for manual content):
   - **This validation is critical even for manually written content**
   - <Callout type="warn">Common MDX pitfalls like `<5k` patterns break builds even in manually written articles. Always validate.</Callout>
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

### Step 8: AI-Powered Related Articles Recommendation

**Automatically add 3-5 relevant article recommendations at the bottom of each article.** AI analyzes concept relationships and content similarity to suggest the most helpful next reads.

**Prerequisites**:
- Step 3.6 must be completed (concepts extracted)
- Concept index must exist (archive/concept-index.json)
- At least 5 articles exist in the same category and language

**Why AI Instead of Tags/Category Matching**:
- **Tags are too broad**: Tag "Skills" has 20 articles, but only 3 are truly relevant
- **AI understands depth**: Knows "Skills for MCP" vs "Skills basics" are different
- **AI detects relationships**: Recognizes that "SubAgents" is an advanced "Agents" topic
- **AI judges usefulness**: Recommends articles that extend knowledge, not just similar keywords

**AI Analysis Criteria**:
1. **Concept overlap**: Shared technical concepts (from Step 3.6)
2. **Topic progression**: Beginner → Intermediate → Advanced path
3. **Prerequisite relationships**: Article A must be read before Article B
4. **Complementary knowledge**: Article A + Article B = better understanding
5. **Avoid redundancy**: Don't recommend articles covering same ground

**AI Prompt**:
```typescript
const relatedArticlesPrompt = `
You are recommending related articles at the bottom of a technical article.

Current article: "${articleTitle}"
Category: ${category}
Language: ${languageCode}
Difficulty: ${difficulty}

Concepts in this article (from Step 3.6):
${JSON.stringify(concepts, null, 2)}

Available articles in ${languageCode}/${category}:
${JSON.stringify(availableArticles, null, 2)}

Task:
1. Analyze ALL available articles in the same category and language
2. Find 3-5 articles that would be MOST HELPFUL to read next
3. Consider:
   - Concept similarity (share important technical concepts)
   - Knowledge progression (next logical step in learning)
   - Difficulty level (similar or slightly more advanced)
   - Complementary topics (fills gaps, adds depth)
   - Avoid: Same beginner topic repeated, completely unrelated advanced topics

Output format:
\\`\\`\\`json
{
  "recommendations": [
    {
      "slug": "skills-explained",
      "title": "How Skills Work in Claude",
      "reasoning": "Explains the Skills concept in detail, which this article mentions but doesn't fully cover. Good next step.",
      "relevanceScore": 9,
      "prerequisiteFor": ["mcp-integration", "advanced-agent-patterns"]
    }
  ]
}
\\`\\`\\`
`;
```

**Execution**:

1. **Prepare available articles database**:
   ```typescript
   // Build index of all articles by scanning content/docs/{lang}/{category}
   const availableArticles = glob(`content/docs/${lang}/${category}/*.mdx`)
     .map(path => {
       const content = readFile(path);
       const frontmatter = parseFrontmatter(content);
       const slug = path.match(/\/([^/]+)\.mdx$/)[1];

       return {
         slug,
         title: frontmatter.title,
         description: frontmatter.description,
         difficulty: frontmatter.difficulty,
         tags: frontmatter.tags,
         concepts: loadConcepts(slug, lang) // From archive/concepts/{slug}.json
       };
     });
   ```

2. **Call Claude AI for analysis**:
   ```typescript
   const response = await askClaude(relatedArticlesPrompt);
   const { recommendations } = JSON.parse(response);
   ```

3. **Validate recommendations**:
   ```typescript
   if (recommendations.length < 3) {
     console.warn("⚠️  AI returned only ${recommendations.length} recommendations");
     console.warn("→ Expected 3-5 articles for good user experience");
   }

   if (recommendations.length > 5) {
     console.warn("⚠️  Too many recommendations (${recommendations.length}), truncating to 5");
     recommendations = recommendations.slice(0, 5);
   }
   ```

4. **Insert RelatedArticles component in MDX** (before Source Declaration):
   ```mdx
   import { RelatedArticles } from 'fumadocs-ui/components/related-articles';

   # ... article content ...

   <RelatedArticles
     articles={recommendations.map(rec => ({
       href: `/${lang}/${category}/${rec.slug}`,
       title: rec.title,
       description: rec.description || rec.reasoning
     }))}
   />

   ## ℹ️ Source Information
   # ... rest of article ...
   ```

5. **Save recommendation metadata**:
   ```typescript
   writeJson(`archive/recommendations/${articleSlug}-${lang}.json`, {
     article: articleSlug,
     lang: languageCode,
     articleTitle: articleTitle,
     totalRecommendations: recommendations.length,
     recommendations: recommendations.map(rec => ({
       ...rec,
       targetArticlePath: `content/docs/${lang}/${category}/${rec.slug}.mdx`
     }))
   });
   ```

6. **Output summary**:
   ```
   🤖 AI Related Articles Analysis Complete:
   ✅ Analyzed ${availableArticles.length} available articles
   🎯 Selected ${recommendations.length} recommendations
   📊 Relevance scores: ${recommendations.map(r => `${r.slug}(${r.relevanceScore})`).join(', ')}
   💡 AI reasoning: ${recommendations.map(r => `${r.slug}: ${r.reasoning}`).join('\n   ')}
   ```

**AI Decision Examples**:

**Example 1: Concept Progression**
```
Current: "Getting Started with MCP"
Available: ["MCP Architecture", "MCP Security", "MCP vs REST", "Skills", "Agents"]

AI Decision:
- ✅ Recommend "MCP Architecture" (next logical step)
- ✅ Recommend "MCP Security" (important consideration)
- ❌ Skip "MCP vs REST" (too advanced for beginner article)
- ❌ Skip "Skills" and "Agents" (different topics)

Reasoning: "Architecture" and "Security" extend MCP knowledge naturally.
```

**Example 2: Avoid Redundancy**
```
Current: "React Hooks - useState Guide"
Available: ["React Hooks - useEffect", "React Context API", "Vue.js Introduction", "React TypeScript"]

AI Decision:
- ✅ Recommend "React Hooks - useEffect" (next hook to learn)
- ✅ Recommend "React Context API" (solves related problems)
- ❌ Skip "Vue.js Introduction" (different framework)
- ❌ Skip "React TypeScript" (different concern - typing)

Reasoning: Focus on React ecosystem, avoid framework comparisons.
```

**Example 3: Prerequisite Chain**
```
Current: "Building Multi-Agent Systems" (Advanced)
Available: ["Agent Basics", "MCP Protocol", "Skills Explained", "Claude API"]

AI Decision:
- ❌ Skip "Agent Basics" (too basic, assume knowledge)
- ✅ Recommend "Skills Explained" (prerequisite pattern)
- ✅ Recommend "MCP Protocol" (underlying technology)
- ❌ Skip "Claude API" (unrelated to agents)

Reasoning: Advanced readers need prerequisite patterns, not basics.
```

**Example 4: Complementary Depth**
```
Current: "Frontend Performance - Bundle Size"
Available: ["Frontend Performance - Caching", "Frontend Performance - Lazy Loading", "React Optimization", "Webpack Configuration"]

AI Decision:
- ✅ Recommend "Frontend Performance - Caching" (same series)
- ✅ Recommend "Frontend Performance - Lazy Loading" (same series)
- ❌ Skip "React Optimization" (framework-specific, not core concept)
- ❌ Skip "Webpack Configuration" (tool-specific, too narrow)

Reasoning: Same conceptual series provides best learning path.
```

**AI vs Rule-Based Comparison**:

| Scenario | Rule-Based (Tags/Category) | AI (Understanding) |
|----------|----------------------------|-------------------|
| Tag "Performance" | Shows 15 articles (all generic) | Picks 3-5 truly relevant by sub-topic |
| Article "React Hooks" | Recommends "Vue.js" (same: frontend) | Recommends "useEffect guide" (React only) |
| Beginner article | Recommends random same-difficulty | Recommends logical progression path |
| Advanced topic | Recommends confusing basics | Recommends prerequisite depth articles |
| Article mentions "MCP" | Recommends all MCP-tagged | Distinguishes MCP architecture vs security |

**Key AI Decision Points**:

1. **Concept Understanding**: AI reads actual content concepts, not just keywords
2. **Learning Path Design**: AI creates progression (beginner → advanced within topic)
3. **Relevance Scoring**: AI scores 1-10, human can set threshold (e.g., score ≥ 7)
4. **Avoid Oversimplification**: AI knows when article is too basic for advanced readers
5. **Avoid Overwhelming**: AI limits to 3-5 (rule-based often returns 10-20)

**When AI Cannot Recommend**:
- Less than 3 articles in same category/language → Skip recommendations
- No concept similarity found → Quality warning, don't show random articles
- All articles are the same difficulty/depth → Still recommend, but warn about lack of progression

**Quality Thresholds**:
- **Minimum**: 3 recommendations (if fewer, don't show section)
- **Optimal**: 5 recommendations (good variety without overwhelming)
- **Relevance**: Score ≥ 7 (filter out borderline matches)
- **Diversity**: At least 2 different sub-topics (avoid all same concept)

**Caching Strategy**:
- Store recommendations in `archive/recommendations/` (JSON files)
- Cache for 7 days (articles don't change frequently)
- Regenerate when:
  - New article added in category
  - Article concepts updated
  - Cache expired

**User Experience**:
- Section labeled "Related Articles" at bottom (before Source Information)
- Use Cards with: Title, Description, Category tag, Difficulty indicator
- Responsive: 3 columns desktop, 2 columns tablet, 1 column mobile
- Track clicks (optional): Which recommendations get clicked most

### Step 9: Create/Update meta.json for All Languages

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

   | Category | English | Chinese | French |
   |----------|---------|---------|--------|
   | ai-ml | AI & Machine Learning | AI 与机器学习 | IA et Apprentissage Automatique |
   | development | Development | 开发 | Développement |
   | data | Data | 数据 | Données |
   | design | Design | 设计 | Design |
   | content | Content | 内容 | Contenu |
   | business | Business | 商业 | Affaires |
   | devops | DevOps | DevOps | DevOps |
   | security | Security | 安全 | Sécurité |

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
- Always create meta.json for ALL 3 languages (en, zh, fr), not just English
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
     "languages": ["en", "zh", "fr"],
     "category": "{category}",
     "difficulty": "{difficulty}",
     "tags": ["{tag1}", "{tag2}", "{tag3}"],
     "published_files": {
       "en": "content/docs/en/{category}/{slug}.mdx",
       "zh": "content/docs/zh/{category}/{slug}.mdx",
       "fr": "content/docs/fr/{category}/{slug}.mdx"
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

📂 Navigation (meta.json):
  ✅ en: content/docs/en/{category}/meta.json ("{English Category Name}")
  ✅ zh: content/docs/zh/{category}/meta.json ("{Chinese Category Name}")
  ✅ fr: content/docs/fr/{category}/meta.json ("{French Category Name}")
  📌 Article added to sidebar navigation
  🎨 Icon: {category_icon}

🖼️  Images (Smart Filtering & Strategy):
  🎯 Strategy Used: {image_strategy} (external/download/auto)
  ✅ Found {total_images} total images on page
  🎯 Identified {filtered_images} content images (diagrams/screenshots)
  🚫 Skipped {skipped_images} decorative images (placeholders/icons)
  {image_strategy_section}

📺 Videos:
  ✅ Detected {video_count} YouTube video(s)
  ✅ Auto-embedded using iframe component
  ⏭️  No download needed (video loaded from YouTube)

🔒 Content Safety Processing (Step 2.5):
  ✅ Processed content from: {source_name}
  🛡️ Degraded unknown components: {degraded_component_count}
  🔧 Fixed MDX pitfalls: {fixed_pitfall_count}
  📦 Injected imports: {injected_import_count}
  ⚠️  Warnings: {warning_count}
  {safety_warnings_details}

🤖 AI-Powered Enhancements:

  Cross-References (Step 3.7):
  ✅ Analyzed {concept_count} technical concepts
  ✅ Inserted {cross_ref_links} contextual links in content
  📍 Positions: {link_positions}
  💡 AI reasoning: {ai_cross_ref_reasoning}
  📂 Saved to: archive/links/{slug}.json

  Related Articles (Step 8):
  ✅ Analyzed {available_article_count} articles in {category}/{lang}
  🎯 Selected {recommendation_count} AI-recommended articles
  📊 Relevance scores: {relevance_scores}
  💡 AI selection reasoning: {recommendation_reasoning}
  📂 Saved to: archive/recommendations/{slug}-{lang}.json
  🎯 RelatedArticles component inserted before source section

📋 Source Tracking:
  ✅ Frontmatter includes full source metadata (url, author, dates, license)
  ✅ SourceAttribution component added at top
  ✅ Source declaration added at bottom

📦 Archive: archive/{YYYY-MM}/{slug}/
  - original.md
  - metadata.json (with complete import info)
  - concepts.json (AI-extracted concepts from Step 3.6)
  - links.json (cross-reference metadata)
  - recommendations/ ({lang-specific recommendation files})
  - images/ ({count} files)

⚠️  Issues (if any):
  - Failed images: {list_of_failed_urls}
  - Skipped images (filtered): {filtered_count}
  - meta.json conflicts: {any_merge_issues}
  - Warnings: {any_warnings}

🎉 Next Steps:
  1. Review generated MDX files for accuracy (especially code blocks)
  2. Test article in local Fumadocs (npm run dev)
  3. Verify SourceAttribution displays correctly at top
  4. Check source declaration at bottom
  5. Verify images display (open article with diagrams)
  6. Test YouTube video embeds (if applicable)
  7. Adjust translations if needed
```

**Image Strategy Details** (customized based on choice):

**If using external URLs (no download)**:
```
🖼️  Images (External URLs - No Download):
  ✅ Kept original URLs (CORS supported)
  ⏭️  No downloads performed
  ✅ Saved storage space: {total_size_mb}MB
  ✅ Faster import: skipped download step
  📋 Referenced: {filtered_images} external URLs
```

**If downloading to local**:
```
🖼️  Images (Downloaded to Local):
  ✅ Downloaded: {successful_downloads}/{filtered_images}
  📂 Location: public/images/docs/{slug}/
  💾 Storage used: {total_size_mb}MB
  ✅ Offline availability
  ✅ Full control over files
```

**Key Improvements from v2.0**:

- 🤖 **AI-Powered Article Association** (NEW):
  - **Concept Extraction** (Step 3.6): AI analyzes article content to extract 5-10 key technical concepts with importance scoring
  - **Cross-Reference Insertion** (Step 3.7): AI intelligently inserts links within content where concepts are first mentioned
  - **Related Articles** (Step 3.8): AI recommends 3-5 truly relevant articles (not just tag-matched) based on concept similarity and learning progression

- 🖼️ Smart image filtering: 80-90% reduction in decorative image downloads
- 🖼️ **Flexible image strategies**: external/download/auto based on CORS support
- 📺 YouTube video auto-detection and embedding
- 📋 Comprehensive source tracking (frontmatter + components + footer)
- ⚡ Faster processing (fewer downloads with external strategy)
- 🎯 Better user experience (auto-processed, no interruptions)

## Error Handling

### Missing withAllImages Parameter (CRITICAL)
This is the #1 cause of image processing failures. Must check first!

**Symptom**:
```
❌ CRITICAL ERROR: response.images is undefined!
→ This means 'withAllImages: true' parameter was NOT passed to read_url
→ Image processing will be completely skipped!
```

**Root Cause**:
- Jina MCP `read_url` tool defaults to text-only mode (no images)
- Without `withAllImages: true`, the tool returns `response.images = undefined`
- All subsequent image processing steps receive empty/undefined data
- No errors are thrown, so execution continues silently
- User doesn't know images were missed until checking final output

**How to Fix**:
1. **Re-run Step 2 with correct parameter**:
   ```typescript
   Tool: read_url
   Parameters:
     - url: "{article_url}"
     - withAllImages: true  // ← MUST include this!
   ```

2. **Verify the response**:
   ```typescript
   if (!response.images) {
     throw new Error("withAllImages parameter missing!");
   }
   console.log(`✅ Found ${response.images.length} images`);
   ```

3. **Then re-run the full import**:
   - Start from Step 2 (with correct parameter)
   - Complete Step 3.5 (image filtering)
   - Continue with Step 4 (download)
   - Images will now be processed correctly

**Prevention**:
See Step 2, Sub-step 4 (🔴 CRITICAL VALIDATION) for mandatory check that prevents this error.

**Why this happens**:
- The parameter `withAllImages: true` is easy to overlook
- It's marked as "RECOMMENDED" but actually "MANDATORY" for image processing
- Default behavior (without parameter) is text-only, which is not obvious
- No errors from the tool itself - just missing data

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
- **Preserve English terms** (see Terms to Preserve list in Step 6)
  - Claude, Skills, Projects, MCP, Agent, SubAgent
  - GitHub, Google Drive, Slack, Excel
  - React, Python, Node.js, TypeScript
  - API, SDK, AI, ML, RAG, UI, UX
  - All variable/function/class names in code
- Technical accuracy is paramount
- Preserve code examples exactly (including identifiers)
- Adapt cultural references when necessary
- Use appropriate technical terminology for each language
- Chinese (zh): 使用简体中文，技术术语保持英文
  - Example: "Claude 的 Skills 功能" (NOT: "克劳德的技能功能")
  - Example: "使用 React 组件" (NOT: "使用回应组件")
- French (fr): Maintain formal tone, keep English terms as-is
  - Example: "La fonctionnalité Skills de Claude" (NOT translated)
  - Example: "Utilisez le composant React" (NOT: "Réagir")

### File Organization
Follow Fumadocs conventions:
- Language-specific directories: `content/docs/{lang}/` (en, zh, fr)
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

- v2.3.0 (2025-11-17): Defensive Content Safety Processing (Phase 1)
  - **Content Safety Processing** (Step 2.5 - NEW):
    - Automatically handles unknown JSX components from ANY source (Anthropic, GitHub, Medium, etc.)
    - Degrades unknown components to plain text with preservation comments
    - Prevents MDX crashes from unrecognized component libraries
    - Zero configuration required
  - **MDX Pitfall Fixes**:
    - Fixes `<number` patterns (e.g., "<5k") → replaces with HTML entity `&lt;`
    - Fixes dangerous HTML tags (`<script`, `<div`, etc.) in plain text
    - Fixes bold formatting in non-Latin languages (`**粗体：**文字` → `**粗体：** 文字`)
    - Detects mismatched JSX tags and logs warnings
  - **Auto Import Injection**:
    - Automatically detects used Fumadocs components (Callout, Cards, Tabs, Steps, Files, Accordion, ImageZoom)
    - Injects necessary import statements after frontmatter
    - Prevents "Component is not defined" errors
    - Deduplicates imports intelligently
  - **Benefits**:
    - Prevents 90% of MDX syntax errors from imported content
    - Build never breaks due to imported article issues
    - Works for ANY source without source-specific rules
    - Provides clear visibility into what was changed
    - Non-destructive: original intent preserved in comments
  - **Integration**:
    - Runs immediately after content extraction (Step 2)
    - Runs before ALL subsequent steps (3.6, 3.7, 6, 7, 8)
    - Warnings collected and reported in summary

- v2.2.0 (2025-11-17): Removed Korean Language Support
  - **Language Support Reduced**: Removed Korean (ko) from supported languages
  - **Updated**: All workflow steps, examples, and mappings to reflect 3-language system (en, zh, fr)
  - **Rationale**: Focus on core language markets (English, Chinese, French)
  - **Migration**: Existing Korean content remains in archive but no new imports supported

- v2.1.0 (2025-11-17): AI-Powered Article Association System
  - **AI-Powered Concept Extraction** (Step 3.6):
    - AI analyzes article content to extract 5-10 key technical concepts
    - Determines if each concept is a main topic (文章主要讲解) or supplemental mention
    - Scores importance 1-10 for prioritization
  - **AI-Powered Cross-Reference Insertion** (Step 3.7):
    - AI intelligently inserts links where concepts are first mentioned in content
    - Avoids over-linking (limits to 3-5 links total)
    - Skips headings, code blocks, and already-linked text
    - Maintains natural reading flow (not mechanical first-occurrence replacement)
  - **AI-Powered Related Articles** (Step 3.8):
    - AI recommends 3-5 truly relevant articles (not just tag-matching)
    - Analyzes concept relationships, topic progression, and prerequisite chains
    - Considers learning path (beginner → intermediate → advanced)
    - Relevance scoring: 1-10 scale with quality thresholds
  - **Terms to Preserve**: Comprehensive list of 25+ English terms (Claude, Skills, Agent, MCP, APIs, frameworks, acronyms, code identifiers)
  - **Enhanced Summary**: Reports AI decisions (concept extraction, cross-references, related articles)
  - **Archive**: Stores AI-generated metadata (concepts.json, links.json, recommendations/)
  - **Same-Language Only**: Cross-references and recommendations stay within same language version
  - **Fully Automated**: All AI decisions made without user intervention, results in summary

- v2.0.0 (2025-11-16): Smart Image Filtering + YouTube + Source Tracking + Mandatory Validation
  - **Smart Image Filtering** (Step 3.5): Heuristic rules filter 80-90% of decorative images (placeholders, icons, logos)
  - **YouTube Video Support** (Step 5): Auto-detect and embed YouTube videos using iframe/Fumadocs `<Video>` component
  - **Enhanced Source Tracking**:
    - Frontmatter with detailed source metadata (url, name, author, dates, license)
    - `SourceAttribution` component (top) + Source declaration (bottom) for full attribution
  - **Translation Optimization**: Added "Terms to Preserve" list (Claude, Skills, Agent, MCP, etc.)
  - **WithAllImages Integration**: Use Jina MCP `read_url` with `withAllImages: true` for structured image data
  - **Mandatory Validation** (Step 2.4 - CRITICAL): Force check for `response.images` to prevent silent failures
    - Added CRITICAL REQUIREMENTS section at top of SKILL.md
    - Added dedicated error handling for missing withAllImages parameter
    - Prevents #1 cause of image processing failures
  - **Auto-processing**: No user interruptions, results reported in summary
  - **Improved Summary**: Shows filtering results, video handling, source tracking details

- v1.0.0 (2025-11-15): Initial release
  - Multi-language support (en, zh, fr, ko)
  - 8-category classification system
  - Automatic image processing
  - MDX conversion with Fumadocs components
  - Archive system with full traceability
