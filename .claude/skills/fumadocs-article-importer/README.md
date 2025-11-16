# Fumadocs Article Importer Skill

Automatically import external articles into your Fumadocs project with multi-language translation, AI-powered classification, and image processing.

## Features

- 📥 **Article Download**: Fetch articles using Jina API or Jina MCP
- 🌐 **Multi-Language Support**: Auto-translate to English, Chinese, French, and Korean
- 🏷️ **AI Classification**: Automatically categorize articles into 8 categories with difficulty levels and tags
- 🖼️ **Image Processing**: Download and organize images with smart naming
- 📝 **MDX Conversion**: Convert to Fumadocs-compatible MDX with built-in components
- 📦 **Archive System**: Full traceability with original content and metadata

## Quick Start

1. Ensure your Fumadocs project is initialized
2. Configure Jina API access or Jina MCP
3. Use the skill by providing an article URL

## Supported Languages

- **English (en)**: Original or translated
- **Chinese (zh)**: Simplified Chinese with proper technical terminology
- **French (fr)**: Professional technical French
- **Korean (ko)**: Formal technical Korean

## Category System

Articles are automatically classified into one of 8 categories:

1. **development**: Development & Code
2. **data**: Data & Analytics
3. **ai-ml**: AI & Machine Learning
4. **design**: Design & Creative
5. **content**: Content & Writing
6. **business**: Business & Marketing
7. **devops**: DevOps & Infrastructure
8. **security**: Security & Testing

## Difficulty Levels

- **beginner**: Introductory content, basic concepts
- **intermediate**: Requires some background knowledge
- **advanced**: Expert-level, complex topics

## File Structure

```
fumadocs-article-importer/
├── SKILL.md                           # Main skill instructions
├── README.md                          # This file
├── references/                        # Supporting documentation
│   ├── classification-rules.md        # Category and tag definitions
│   ├── translation-prompts.md         # Translation guidelines
│   └── fumadocs-components.md         # Fumadocs component reference
└── assets/                            # Templates and resources
    └── frontmatter-template.yaml      # Frontmatter structure
```

## Output Structure

After importing an article:

### Published Files
```
content/docs/
├── en/{category}/{slug}.mdx          # English version
├── zh/{category}/{slug}.mdx          # Chinese version
├── fr/{category}/{slug}.mdx          # French version
└── ko/{category}/{slug}.mdx          # Korean version

public/images/docs/{slug}/
├── image-1.png
├── diagram-2.jpg
└── ...
```

### Archive
```
archive/{YYYY-MM}/{slug}/
├── original.md                        # Original content
├── metadata.json                      # Full traceability data
└── images/                            # Image backups
```

## Example Usage

### Import a Technical Tutorial

**Input**:
- URL: `https://example.com/react-hooks-complete-guide`
- Languages: All (en, zh, fr, ko)
- Download images: Yes

**Output**:
- **Category**: development
- **Difficulty**: intermediate
- **Tags**: react, hooks, javascript, frontend, web
- **Files**: 4 MDX files (one per language)
- **Images**: Downloaded to `/public/images/docs/react-hooks-complete-guide/`
- **Archive**: Complete metadata and original content

### Import a Data Science Article

**Input**:
- URL: `https://example.com/pandas-data-cleaning-tutorial`
- Languages: en, zh (selected languages only)
- Download images: Yes

**Output**:
- **Category**: data
- **Difficulty**: beginner
- **Tags**: python, pandas, data-analysis, tutorial, data-cleaning
- **Files**: 2 MDX files (English and Chinese)
- **Images**: Organized with descriptive names
- **Archive**: Full traceability

## Requirements

### System Requirements
- Fumadocs project initialized
- Node.js environment
- `curl` installed (for image downloads)

### API/MCP Access

**For Article Fetching (Highly Recommended):**
- **Jina MCP Server**: https://github.com/jina-ai/MCP
  - Converts webpages to clean markdown
  - Extracts publication dates automatically
  - 15+ tools for content processing
  - **Quick Setup**:
    - Public server: `https://mcp.jina.ai/sse` (easiest, free tier available)
    - Self-hosted: Clone repo, `npm install`, `npm start`
  - See `references/jina-mcp-setup.md` for detailed setup
  - **Fallback**: Jina API via curl (if MCP not available)

**For Translation (Built-in):**
- **Translator Skill**: Built-in professional translation
  - Uses Claude's native translation capabilities
  - Preserves Markdown formatting and code blocks
  - Consistent technical terminology handling
  - Language-specific best practices (zh, fr, ko, en)
  - **No configuration required** - automatically activated when needed
  - Located in `.claude/skills/translator/`

**Performance:**
- Article fetching with Jina MCP: ~3-4 seconds (vs ~10+ seconds with curl)
- Translation (4 languages): Automatic via translator skill
- **Overall: Fast and efficient workflow with no external dependencies for translation**

### Directory Permissions
- Write access to `content/docs/`
- Write access to `public/images/`
- Write access to `archive/`

## Customization

### Modify Classification Rules
Edit `references/classification-rules.md` to:
- Add new categories
- Update keyword matching
- Adjust difficulty criteria
- Customize tag extraction

### Adjust Translation Prompts
Edit `references/translation-prompts.md` to:
- Fine-tune translation quality
- Add language-specific rules
- Update technical term handling

### Update Frontmatter Schema
Modify `assets/frontmatter-template.yaml` to:
- Add new custom fields
- Change required fields
- Adjust validation rules

## Best Practices

### For Best Results
1. **Verify Source Quality**: Choose well-structured articles with clean HTML
2. **Check Image Accessibility**: Ensure images are publicly accessible
3. **Review Translations**: Spot-check critical technical content
4. **Update Navigation**: Add new articles to meta.json for proper navigation
5. **Test Locally**: Preview articles in local Fumadocs before publishing

### Common Pitfalls to Avoid
- ❌ Don't import articles with paywalls or login requirements
- ❌ Don't skip image download step without reviewing image references
- ❌ Don't modify classification rules without testing
- ❌ Don't ignore MDX validation errors
- ❌ Don't forget to update navigation files

## Troubleshooting

### Images Not Downloading
- Check internet connectivity
- Verify image URLs are accessible
- Check `public/images/` write permissions
- Review firewall/proxy settings

### Translation Errors
- Verify language codes (en, zh, fr, ko)
- Check translation prompt formatting
- Test with shorter articles first
- Review API rate limits

### Classification Inconsistencies
- Review classification-rules.md
- Check article content quality
- Adjust keyword matching if needed
- Manually override if necessary

### MDX Syntax Errors
- Validate frontmatter YAML
- Check for unclosed JSX components
- Review code block syntax
- Consult fumadocs-components.md

## Version History

- **v1.0.0** (2025-11-15): Initial release
  - Multi-language translation (4 languages)
  - 8-category classification system
  - Automatic image processing
  - MDX conversion with Fumadocs components
  - Full archive system

## Contributing

This skill is part of the [Claude Skills Tutorial](https://github.com/user/claude-skills-tutorial) project. Contributions and feedback are welcome!

## Resources

- [Fumadocs Documentation](https://fumadocs.dev)
- [Jina AI Reader](https://jina.ai/reader)
- [Claude Skills Guide](https://github.com/anthropics/skills)
- [MDX Documentation](https://mdxjs.com)

## License

MIT License - See LICENSE.txt for details

---

**Created**: 2025-11-15
**Last Updated**: 2025-11-15
**Maintained by**: Claude Skills Tutorial Project
