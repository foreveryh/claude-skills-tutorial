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

## The 6-Step Article Creation Process

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

### Step 5: Create Multi-Language Versions

**Purpose**: Make the article accessible to international audiences

**Translation process**:

1. **Preserve technical terms**: Keep these in English
   - Claude, Skills, SKILL.md
   - Technical acronyms: API, SDK, MCP
   - Product names: GitHub, Fumadocs
   - Code blocks and identifiers

2. **Translate strategically**:
   - Maintain markdown formatting
   - Preserve code block content
   - Keep image paths unchanged
   - Follow language-specific best practices:
     - **Chinese (zh)**: No extra spaces around English terms
     - **French (fr)**: Formal tone, keep English terms as-is
     - **English (en)**: Clear, professional US English

3. **Content Safety Processing** (Step 2.5):
   - Fix `<5k` patterns → `&lt;5k`
   - Escape dangerous tags in text
   - Fix bold formatting spacing
   - Auto-inject component imports

**Output**: Three complete article versions (en, zh, fr)

### Step 6: Package and Validate

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

**Output**: Production-ready articles in three languages

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
