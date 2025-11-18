---
name: skill-article-writer
description: Generate comprehensive analysis articles from Claude skills. This skill should be used when you want to analyze a skill from the Anthropic skills repository and create a detailed tutorial article explaining its structure, design patterns, and usage. Perfect for creating documentation, tutorials, and educational content about existing skills.
license: Complete terms in LICENSE.txt
---

# skill-article-writer

Generate comprehensive analysis articles from Claude skills. This skill transforms any skill from the Anthropic repository into a detailed tutorial with explanations, best practices, and usage examples.

## What This Skill Does

**skill-article-writer** is a meta-skill that:
- Analyzes skill structure and bundled resources
- Generates detailed article outlines
- Creates comprehensive tutorials with code examples
- Produces multi-language versions (en, zh, fr)
- Follows proven documentation patterns

**Use cases**:
- Creating documentation for internal skills
- Writing tutorials for skill development
- Analyzing best practices from example skills
- Generating educational content for Claude users

### Skills vs. Articles

- **Skills**: Executable workflows that extend Claude's capabilities
- **Articles**: Educational content that explains how skills work
- **This Skill**: Bridges the gap by analyzing skills and creating articles

## Prerequisites

Before using this skill, you must have:

1. **Access to Anthropic skills repository**: `github.com/anthropics/skills`
2. **Local clone of target skill**: The skill must be available locally
3. **Python 3.x**: Required for analysis scripts
4. **Write access**: Ability to create article files in your project

## How The Skill Works

### Progressive Analysis

This skill uses a three-stage analysis process:

1. **Structure Analysis** (`analyze_skill.py`)
   - Examines directory structure
   - Parses SKILL.md metadata
   - Identifies bundled resources
   - Generates comprehensive metadata

2. **Outline Generation** (`generate_article_outline.py`)
   - Creates article structure
   - Plans section content
   - Identifies code examples
   - Generates markdown template

3. **Content Creation**
   - Fills in outline with detailed analysis
   - Adds practical examples
   - Creates multi-language versions
   - Validates MDX syntax

### Output Structure

Each generated article follows this structure:

```
1. Introduction (what is this skill?)
2. Skill Anatomy (directory structure)
3. Technical Deep Dive (how it works)
4. Usage Examples (practical demonstrations)
5. Best Practices (design principles)
6. Integration Patterns (with other skills)
7. Troubleshooting (common issues)
8. Conclusion and Next Steps
```

## Directory Structure

The skill-article-writer includes helper scripts for automation:

```
skill-article-writer/
├── SKILL.md                    # This file
├── scripts/
│   ├── analyze_skill.py        # Analyze skill structure
│   └── generate_article_outline.py  # Generate article template
├── references/
│   └── article-templates.md    # Template patterns for different skill types
└── examples/
    └── skill-creator-output.md # Example: analysis of skill-creator
```

## The 7-Step Article Creation Process

### Step 1: Understand the Source Skill

**Purpose**: Gain deep understanding of the skill's structure and purpose

**Actions**:
1. **Read the skill's SKILL.md**: Understand what problem it solves
2. **Examine bundled resources**: Scripts, references, and assets
3. **Identify key workflows**: How does the skill accomplish its goals?
4. **Note the target audience**: Who is this skill designed for?

**Output**: Comprehensive understanding of the skill's value proposition

**Example**: When analyzing `skill-creator`, we identified:
- **Problem solved**: Manual skill creation is error-prone
- **Key workflows**: 6-step creation process with validation
- **Target audience**: Developers creating Claude skills
- **Value proposition**: Systematic approach ensures quality and consistency

### Step 2: Analyze Structure and Extract Metadata

**Purpose**: Extract structured information for article generation

**Run analysis script**:
```bash
scripts/analyze_skill.py /path/to/skill-name > /tmp/skill-metadata.json
```

**What the script extracts**:
- Directory structure and file organization
- YAML frontmatter (name, description, etc.)
- Section headings and content structure
- Bundled resources inventory
- Commands and usage patterns
- Workflow steps

**Output**: JSON metadata file with structured skill information

**Key insight**: This metadata serves as the single source of truth for article generation

### Step 3: Generate Article Outline

**Purpose**: Create a structured outline that covers all important aspects

**Run outline generator**:
```bash
scripts/generate_article_outline.py /tmp/skill-metadata.json > /tmp/article-outline.md
```

**The outline includes**:
- Complete article structure with all sections
- Calls to action for expansion
- Component placeholders (Callouts, Cards, Steps)
- Source attribution blocks
- Appendix for detailed resource listings

**Design considerations**:
- Follows proven article structure from successful skill analyses
- Adapts section depth based on skill complexity
- Includes both overview and deep-dive sections
- Provides practical examples and use cases

**Output**: Comprehensive outline (150-200 lines) covering:
- Introduction and overview
- Technical deep dive
- Usage examples
- Best practices
- Troubleshooting
- Conclusion

### Step 4: Research and Expand Content

**Purpose**: Transform the outline into a detailed, informative article

**Content expansion process**:

1. **Fill in section details**:
   - Explain each concept thoroughly
   - Add code snippets and examples
   - Include practical demonstrations
   - Provide real-world use cases

2. **Add visual elements**:
   - Insert `<Callout type="info|warn|tip">` for important points
   - Use `<Cards>` and `<Card>` for related concepts
   - Add `<Steps>` and `<Step>` for procedural content
   - Include `<Files>`, `<Folder>`, `<File>` for directory structures

3. **Create practical examples**:
   - Walk through a complete example
   - Show before and after
   - Include expected output
   - Highlight key takeaways

4. **Add cross-references**:
   - Link to related skills
   - Reference external documentation
   - Connect to broader concepts

**Writing style**: Use imperative/infinitive form throughout

- ❌ **Wrong**: "You should run the script"
- ✅ **Right**: "Run the script"

**Output**: Complete article draft in English (3000-4000 words)

### Step 4.5: Generate Article Cover Illustration

**Purpose**: Automatically create a modern, theme-relevant SVG cover illustration for the skill analysis article.

**Why this matters**:
- Visual appeal increases engagement and readability
- Consistent illustration style across all skill documentation
- Saves time compared to manual design
- Automatically matches skill theme and technical domain

**Process**:

1. **Invoke the philosophical-illustrator skill**:
   - This skill generates modern, colorful SVG illustrations for technical content
   - Automatically selects color palette based on skill domain
   - Creates theme-relevant visual metaphors

2. **Prepare illustration context from skill analysis**:
   ```
   Skill Name: {skill-name}
   Article Title: {article-title}
   Main Topic: {skill's main purpose}
   Key Concepts: {extracted from Step 1 and Step 3}
   Technical Domain: {development/data/ai-ml/testing/etc.}
   ```

3. **Domain-to-Category Mapping** (for color palette selection):

   | Skill Domain | Category | Palette | Colors |
   |--------------|----------|---------|--------|
   | Code/Development | development | Pink-Purple | #C67B9B, #B8789E, #A97BA1 |
   | AI/ML/Agents | ai-ml | Pink-Purple | #C67B9B, #B8789E, #A97BA1 |
   | Data Processing | data | Beige-Neutral | #C9BFA8, #D4CAAF, #B8AD98 |
   | Testing/QA | development | Blue | #5B8FB9, #6B9BC4, #7AA5C8 |
   | DevOps/Infrastructure | devops | Green-Olive | #6B7F64, #758C6E, #607360 |
   | Security | security | Blue | #5B8FB9, #6B9BC4, #7AA5C8 |
   | Design/UI | design | Orange-Coral | #D17B5C, #C88860, #B87A5D |
   | General/Multi-purpose | content | Multi-topic | #CA8760, #D17B5C, #B87A5D |

4. **Generate SVG illustration**:
   - Use the Skill tool to invoke philosophical-illustrator
   - Pass skill name, domain, and key concepts
   - The skill will generate a 800x450px SVG with theme-relevant imagery
   - For skill analysis articles, focus on visual metaphors that represent:
     - Workflow automation (gears, connections, flow diagrams)
     - Code structure (brackets, files, hierarchies)
     - Problem-solving (lightbulbs, tools, transformations)

5. **Save illustration**:
   ```bash
   mkdir -p "public/images/docs/{article-slug}"
   # Save SVG output to:
   # public/images/docs/{article-slug}/cover.svg
   ```

6. **Update frontmatter reference**:
   - Add to frontmatter: `image: /images/docs/{article-slug}/cover.svg`
   - This field will be used by Fumadocs for article preview cards
   - Image appears in:
     - Article header
     - Card previews in navigation
     - Social media sharing (og:image)

**Example invocation**:
```
Use the philosophical-illustrator skill to generate a cover illustration:

Skill: skill-creator
Article Title: "Skill Creator Deep Dive: Systematic Approach to Building Claude Skills"
Domain: development
Key Concepts: Progressive disclosure, validation, bundled resources, 6-step process
Description: Analysis of skill-creator, a meta-skill for creating high-quality Claude skills

Please create a modern SVG illustration with:
- Pink-Purple color palette (development domain)
- Visual elements: code brackets, file structure icons, workflow connections, gears
- Metaphors: building blocks, systematic process, quality validation
- Modern, friendly aesthetic
- 800x450px dimensions
```

**Output**:
- SVG file saved to `public/images/docs/{slug}/cover.svg`
- Frontmatter updated with `image` field
- Illustration ready for all language versions (reused across en, zh, fr)

**Fallback**:
- If illustration generation fails, continue without image
- Log warning in summary report
- Article still functions normally (image is optional)

**Note**: The same cover image is used for all language versions of the article, as visual metaphors are language-agnostic.

### Step 5: Create Multi-Language Versions

**Purpose**: Make the article accessible to international audiences

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

#### Translation Process

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

**Output**: Three complete article versions (en, zh, fr)

### Step 6: Create/Update meta.json for All Languages

**Purpose**: Ensure proper sidebar navigation with localized titles for all languages

**CRITICAL**: Create proper meta.json files for sidebar navigation with localized titles.

Load reference files:
- `references/category-translations.json` - Get translated category names
- `references/category-icons.json` - Get appropriate icons

For **each language** (en, zh, fr):

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

**Output**: meta.json files created/updated for all languages with proper navigation structure

### Step 7: Package and Validate

**Purpose**: Ensure articles are ready for publication

**Validation checklist**:

✅ **Content validation**:
- [ ] MDX syntax is correct
- [ ] All components are properly imported
- [ ] Frontmatter is valid YAML
- [ ] SourceAttribution component is present
- [ ] Links are working
- [ ] Code blocks are syntax-highlighted

✅ **Build validation**:
- [ ] `npm run build` completes without errors
- [ ] All language versions render correctly
- [ ] No missing imports or undefined components
- [ ] Responsive design works (mobile, tablet, desktop)

✅ **Quality checks**:
- [ ] Article is comprehensive (2000+ words)
- [ ] Examples are practical and clear
- [ ] Best practices are highlighted
- [ ] Related articles are cross-referenced
- [ ] Summary provides actionable next steps

✅ **Multi-language verification**:
- [ ] All 3 language versions created (en, zh, fr)
- [ ] Technical terms preserved in all languages (Claude, Skills, MCP, etc.)
- [ ] meta.json files created/updated for all languages
- [ ] Category titles properly localized
- [ ] Navigation structure consistent across languages

**Output**: Production-ready articles in three languages

**Expected file structure**:
```
content/docs/
├── en/{category}/
│   ├── meta.json (English category title)
│   └── {article-slug}.mdx
├── zh/{category}/
│   ├── meta.json (Chinese category title)
│   └── {article-slug}.mdx
└── fr/{category}/
    ├── meta.json (French category title)
    └── {article-slug}.mdx
```

**Summary report template**:
```
✅ Article Creation Complete!

📄 Article: {title}
🔗 Source Skill: {skill-name}
📁 Category: {category}
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

🎨 Article Cover (Step 4.5):
  ✅ Generated SVG illustration using philosophical-illustrator
  📁 Saved to: public/images/docs/{slug}/cover.svg
  🎨 Color palette: {palette_name} ({domain} domain)
  📏 Dimensions: 800x450px
  🔗 Referenced in frontmatter: image: /images/docs/{slug}/cover.svg
  ✨ Visual theme: {theme_description}
  🌐 Shared across all language versions (language-agnostic)
  (Or: ⚠️  Cover generation skipped/failed - article continues without image)

🌐 Multi-Language Processing:
  ✅ Technical terms preserved: Claude, Skills, MCP, Agent, API, SDK
  ✅ Code blocks unchanged across all languages
  ✅ Frontmatter properly localized
  ✅ All language versions validated

🎉 Next Steps:
  1. Review generated MDX files for accuracy
  2. Test article in local Fumadocs (npm run dev)
  3. Verify all language versions render correctly
  4. Check navigation in all languages
  5. Run build to ensure no errors (npm run build)
```

## Article Structure Template

Generated articles follow this proven structure:

```
1. Introduction (what is this skill?)
2. Skill Anatomy (directory structure)
3. Bundled Resources (scripts, references, assets)
4. Technical Deep Dive (how it works)
5. Usage Examples (practical demonstrations)
6. Best Practices (design principles)
7. Integration Patterns (with other skills)
8. Real-World Use Cases
9. Troubleshooting Guide
10. Conclusion and Next Steps
```

### Component Usage Guide

**Recommended Fumadocs components**:

- **`<Callout type="info|warn|tip|error">`**: Highlight important points
- **`<Cards>` + `<Card>`**: Group related concepts
- **`<Steps>` + `<Step>`**: Show procedural workflows
- **`<Files>` + `<Folder>` + `<File>`**: Display directory structures
- **`<Tabs>` + `<Tab>`**: Show alternative approaches

**Writing pattern example**:

```mdx
<Callout type="info">
  This is a production-ready skill from the Anthropic repository.
</Callout>

<CodeBlock title="Example Usage">
```bash
python script.py --help
```
</CodeBlock>

<Steps>
  <Step>
    **Step 1**: Do this first...
  </Step>
  <Step>
    **Step 2**: Then do this...
  </Step>
</Steps>
```

## Examples

### Example 1: Analyzing skill-creator

**Source**: `github.com/anthropics/skills/tree/main/skill-creator`

**Analysis output**:
```json
{
  "name": "skill-creator",
  "complexity": "moderate",
  "resource_types": ["scripts"],
  "key_features": [
    "6-step creation process",
    "Progressive disclosure pattern",
    "Validation and packaging"
  ]
}
```

**Generated article**: See `examples/skill-creator-output.md`

### Example 2: Analyzing mcp-builder

**Source**: `github.com/anthropics/skills/tree/main/mcp-builder`

**Analysis output**:
```json
{
  "name": "mcp-builder",
  "complexity": "complex",
  "resource_types": ["scripts", "references"],
  "key_features": [
    "MCP specification analysis",
    "Server implementation guidance",
    "Tool definition workflows"
  ]
}
```

## Best Practices

### When to Use This Skill

✅ **DO use skill-article-writer when**:
- You need to document an existing skill
- Creating tutorials for internal skill development
- Analyzing best practices from example skills
- Generating educational content for the Claude community
- Creating multi-language documentation

❌ **DON'T use skill-article-writer when**:
- Writing about non-skill topics (use direct writing instead)
- Creating quick notes or brief summaries
- Documenting one-off workflows
- The source skill is not from Anthropic skills repository

### Article Quality Standards

Each generated article should:

1. **Be comprehensive**: Cover all aspects of the skill (2000-4000 words)
2. **Include practical examples**: Show real usage with code snippets
3. **Follow proven structure**: Use the template sections consistently
4. **Be accessible**: Provide context for readers unfamiliar with the domain
5. **Be actionable**: Include clear next steps and related resources

### Multi-Language Quality Standards

**Translation Quality**:
- **Preserve English terms** (see Terms to Preserve list in Step 5)
  - Claude, Skills, Projects, MCP, Agent, SubAgent
  - GitHub, Google Drive, Slack, Excel
  - React, Python, Node.js, TypeScript
  - API, SDK, AI, ML, RAG, UI, UX
  - All variable/function/class names in code
- Technical accuracy is paramount
- Preserve code examples exactly (including identifiers)
- Adapt cultural references when necessary
- Use appropriate technical terminology for each language
- **Chinese (zh)**: 使用简体中文，技术术语保持英文
  - Example: "Claude 的 Skills 功能" (NOT: "克劳德的技能功能")
  - Example: "使用 React 组件" (NOT: "使用回应组件")
- **French (fr)**: Maintain formal tone, keep English terms as-is
  - Example: "La fonctionnalité Skills de Claude" (NOT translated)
  - Example: "Utilisez le composant React" (NOT: "Réagir")

**File Organization**:
Follow Fumadocs conventions:
- Language-specific directories: `content/docs/{lang}/` (en, zh, fr)
- Category subdirectories: `content/docs/{lang}/{category}/`
- meta.json files: Localized category titles for each language
- Navigation: Consistent structure across all languages

### Writing Style Guidelines

**Critical: Always use imperative/infinitive form**

❌ **Wrong**: "You should run the analysis script"
✅ **Right**: "Run the analysis script to extract metadata"

❌ **Wrong**: "If you want to create an article..."
✅ **Right**: "To create a comprehensive article..."

**Maintain consistency**:
- Verb-first sentences in all instructions
- Clear section headings
- Logical flow from overview to details
- Balanced use of components (not too many, not too few)

## Integration with Other Skills

skill-article-writer works well with:

1. **skill-creator**: Document new skills you create
2. **skill-builder**: Analyze complex skill architectures
3. **translator**: Generate multi-language versions
4. **fumadocs-article-importer**: Import external skill documentation

## Troubleshooting

### Analysis Script Errors

**Symptom**: `analyze_skill.py` reports parsing errors

**Causes**:
- SKILL.md has invalid YAML frontmatter
- File encoding issues
- Missing files or directories

**Solutions**:
1. Verify SKILL.md starts with `---` and has valid YAML
2. Check file encoding is UTF-8
3. Ensure skill directory structure is complete

### Missing Components

**Symptom**: Generated articles don't include expected Fumadocs components

**Cause**: Outline generator creates component placeholders, but they need to be manually expanded

**Solution**: Review the outline and expand component sections with actual content:
- Replace `<Callout>` placeholders with real callouts
- Add examples to `<Steps>` sections
- Fill in `<Cards>` with relevant information

### Translation Issues

**Symptom**: Technical terms like "Skills" or "Agent" are translated

**Cause**: Not following "Terms to Preserve" guidelines

**Solutions**:
1. Maintain the list of English terms that should not be translated:
   - Claude, Skills, SKILL.md, Agent, SubAgent, MCP
   - GitHub, Google Drive, Slack, Excel
   - React, Python, Node.js, TypeScript
   - API, SDK, AI, ML, RAG, UI, UX

2. Check each translation for accidentally translated terms

## Conclusion

**skill-article-writer** provides a systematic way to:

- ✅ Analyze skill structure and extract insights
- ✅ Generate comprehensive tutorial articles
- ✅ Create multi-language documentation efficiently
- ✅ Follow proven patterns for skill explanations
- ✅ Scale documentation creation across many skills

By using this skill, you can create high-quality educational content that helps others understand and use Claude skills effectively.

---

## Appendix

### Related Resources

- **Anthropic Skills Repository**: github.com/anthropics/skills
- **Claude Code Documentation**: claude.ai/docs
- **Fumadocs Documentation**: fumadocs.com
- **Example Skill Articles**: See `examples/` directory

### Article Templates

For different skill types, see:
- `references/article-templates.md` - Template variations
- `examples/skill-creator-output.md` - Full example analysis
- `references/writing-style-guide.md` - Writing conventions

## ℹ️ Source Information

**Base Skill Analysis**: skill-creator
- **Source**: Anthropic Skills Repository
- **Author**: Anthropic
- **License**: See LICENSE.txt

*This skill was created by analyzing best practices from skill-creator and applying them to the domain of skill documentation.*
