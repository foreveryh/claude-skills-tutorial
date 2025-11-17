# Semantic Commit Guide for Article Publishing

This guide provides templates and best practices for semantic commits when publishing MDX articles.

## Commit Type Selection

### Type: `feat` (Feature)

**When to use**:
- New skill analysis articles
- New significant features or sections
- Major additions to documentation
- Breaking changes or new capabilities

**Examples**:
```
feat: publish analyzing-mcp-builder (en, zh, fr)

skill-analysis: mcp-builder completes the MCP server development guide
```

```
feat: add comprehensive Claude skills tutorial series

Add 5-part tutorial covering skill fundamentals to advanced patterns
Languages: en, zh
```

### Type: `docs` (Documentation)

**When to use** (default for most articles):
- Documentation improvements
- Tutorial articles
- Explanation guides
- Best practices articles

**Examples**:
```
docs: publish webapp-testing guide (en, zh, fr)

Complete Playwright testing guide with examples and best practices
```

```
docs: update skill-creator with new best practices

Incorporate lessons from skill-article-writer development
```

### Type: `fix` (Bug Fix)

**When to use**:
- Corrections to existing articles
- Bug fixes in examples
- Error corrections
- Broken link fixes

**Examples**:
```
fix: correct mdx syntax in analyzing-mcp-builder

Escape comparison operators causing build failures
```

```
fix: resolve broken links in tutorial-usage-patterns

Update outdated references to Anthropic skills repository
```

### Type: `chore` (Maintenance)

**When to use**:
- Refactoring without functional changes
- Dependency updates
- Template updates
- File organization

**Examples**:
```
chore: reorganize development section navigation

Reorder articles for better learning progression
```

```
chore: update all article frontmatter with new tags

Add missing tags for better discoverability
```

## Commit Message Structure

### Single Article

**Format**:
```
<type>: publish <article-slug> (<languages>)

<change-type>: <brief-description>

Languages: <lang-codes>
```

**Example**:
```
feat: publish analyzing-mcp-builder (en, zh, fr)

skill-analysis: comprehensive guide to MCP server development

Languages: en, zh, fr
```

### Multiple Articles

**Format**:
```
<type>: publish multiple articles (<count> <type1>, <count> <type2>)

<type1>: <file1>, <file2>, ...
<type2>: <file3>, <file4>, ...

Languages: <all-languages>
```

**Example**:
```
feat: publish multiple articles (2 skill-analysis, 1 tutorial)

skill-analysis: analyzing-mcp-builder, analyzing-webapp-testing
tutorial: tutorial-creating-first-skill

Languages: en, zh, fr
```

### Update Existing Article

**Format**:
```
<type>: update <article-slug> (<languages>)

<change-type>: <brief-description-of-changes>

Changes: <specific-updates>
```

**Example**:
```
fix: update analyzing-mcp-builder with new evaluation section

skill-analysis: add evaluation methodology details

Changes:
- Add evaluation.py script analysis
- Update best practices section
- Fix typos in examples
```

## Message Generation Logic

### Auto-Detection Algorithm

```python
# Change type detection
def detect_change_type(file_path):
    if 'analyzing-' in file_path:
        return 'skill-analysis'
    if 'mcp-' in file_path or 'playwright' in file_path:
        return 'testing'
    if 'tutorial-' in file_path:
        return 'tutorial'
    return 'article'

# Language detection
def detect_languages(file_path):
    languages = []
    if '/en/' in file_path:
        languages.append('en')
    if '/zh/' in file_path:
        languages.append('zh')
    if '/fr/' in file_path:
        languages.append('fr')
    return languages or ['en']

# Commit type selection
if skill_analysis_in_changes:
    commit_type = 'feat'
elif len(changes) > 3:
    commit_type = 'feat'
else:
    commit_type = 'docs'  # default
```

## Best Practices

### 1. Be Specific

❌ **Too vague**:
```
feat: add new article
```

✅ **Specific**:
```
feat: publish analyzing-mcp-builder guide (en, zh, fr)

skill-analysis: complete MCP server development guide with 4-phase workflow
```

### 2. Include Languages

❌ **Missing languages**:
```
docs: publish analyzing-webapp-testing
```

✅ **With languages**:
```
docs: publish analyzing-webapp-testing (en, zh, fr)

skill-analysis: comprehensive Playwright testing guide
Languages: en, zh, fr
```

### 3. Group Related Changes

❌ **Separate commits for related articles**:
```bash
git commit -m "docs: publish analyzing-mcp-builder"
git commit -m "docs: publish analyzing-webapp-testing"
```

✅ **Single commit for related work**:
```bash
# Make changes to both files
git add content/docs/en/development/
# Single commit for both
feat: publish multiple skill analyses (2 files)

skill-analysis: analyzing-mcp-builder, analyzing-webapp-testing
```

### 4. Describe What and Why

❌ **Only what**:
```
feat: add evaluating section to mcp-builder
```

✅ **What and why**:
```
feat: expand analyzing-mcp-builder with evaluation framework

skill-analysis: add comprehensive evaluation methodology

Adds evaluation.py script analysis, testing procedures, and
quality metrics to help developers validate their MCP servers.
```

### 5. Use Present Tense

❌ **Past tense**:
```
feat: published analyzing-mcp-builder
```

✅ **Present tense**:
```
feat: publish analyzing-mcp-builder
```

## Common Patterns

### Skill Analysis Series

When publishing multiple skill analyses:

```
feat: publish skill analysis series (4 articles)

New skill analyses covering MCP, Playwright testing,
article writing, and skill creation patterns.

skill-analysis:
- analyzing-mcp-builder
- analyzing-webapp-testing
- analyzing-skill-article-writer
- analyzing-skill-creator

Languages: en, zh, fr
```

### Documentation Update Batch

When updating multiple documents:

```
docs: update development guides with new best practices

Incorporate lessons learned from recent skill development

Updates:
- skill-creator-deep-dive: add 6-step process
- agent-skills-overview: update architecture diagram
- tutorial-creating-first-skill: add validation section
```

### Translation Addition

When adding new language translations:

```
docs: add French translations for skill analyses

Complete French versions of recent analyses

Translations:
- analyzing-mcp-builder (fr)
- analyzing-webapp-testing (fr)
- analyzing-skill-article-writer (fr)

Languages: fr (added to existing en, zh)
```

## Special Cases

### Emergency Hotfix

When fixing critical issues:

```
fix: resolve mdx syntax error in main branch

Escaped comparison operators causing deployment failures

Files: analyzing-mcp-builder.mdx, analyzing-webapp-testing.mdx
Urgency: High - fixing broken build
```

### Revert Previous Change

When reverting:

```
revert: revert "feat: publish analyzing-experimental-skill"

Reverting experimental skill analysis pending further review

Reason: Need additional validation and review
Refs: a1b2c3d (commit being reverted)
```

### Initial Release

When publishing first set of articles:

```
feat: initial documentation release (5 articles)

Complete foundational content for Claude skills platform

Includes:
- 3 skill analyses (mcp-builder, webapp-testing, article-writer)
- 2 tutorials (getting-started, creating-first-skill)
- Full i18n support (en, zh, fr)

Languages: en, zh, fr
```

## Tools and Automation

### Using skill-article-publisher

```bash
# Auto-generates semantic commit based on changes
python scripts/publish_article.py content/docs/development/ --push
```

### Manual Commit with Template

```bash
# Use --type to specify commit type
python scripts/publish_article.py content/docs/article.mdx --push --type feat
```

### Pre-commit Hook

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/bash
# Validate MDX before commit
python .claude/skills/skill-article-publisher/scripts/validate_mdx.py \
  content/docs/ --no-build
```

---

## References

- **Conventional Commits**: conventionalcommits.org
- **Semantic Versioning**: semver.org
- **Git Best Practices**: git-scm.com/doc
- **skill-article-publisher**: /development/analyzing-skill-article-publisher
