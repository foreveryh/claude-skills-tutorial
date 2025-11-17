# skill-article-publisher

Automate article validation, semantic commit generation, and git publishing for MDX documentation.

## Quick Start

```bash
cd .claude/skills/skill-article-publisher

# Validate MDX file
python scripts/validate_mdx.py /path/to/article.mdx

# Publish article (dry run)
python scripts/publish_article.py /path/to/article.mdx

# Publish and push
python scripts/publish_article.py /path/to/article.mdx --push

# Publish directory of articles
python scripts/publish_article.py content/docs/en/development/ --push
```

## Features

- ✅ **MDX Validation**: Check syntax, frontmatter, and common errors
- ✅ **Build Validation**: Run `npm run build` to verify MDX compiles
- ✅ **Semantic Commits**: Auto-generate conventional commit messages
- ✅ **Multi-language Support**: Detect en, zh, fr translations
- ✅ **Git Integration**: Stage, commit, and push automatically
- ✅ **Dry Run Mode**: Preview changes before committing
- ✅ **Comprehensive Examples**: See `examples/` directory

## Installation

Install the dependencies:

```bash
# From project root
npm install  # For build validation
pip install -r requirements.txt  # If requirements.txt exists
```

## Usage

### Validate MDX Files

```bash
# Single file
python scripts/validate_mdx.py content/docs/en/development/article.mdx

# Directory (recursive)
python scripts/validate_mdx.py content/docs/en/development/

# With build validation
python scripts/validate_mdx.py content/docs/en/development/article.mdx --build
```

### Publish Articles

```bash
# Dry run (preview)
python scripts/publish_article.py content/docs/en/development/article.mdx

# Commit and push
python scripts/publish_article.py content/docs/en/development/article.mdx --push

# Force commit type
python scripts/publish_article.py content/docs/en/development/article.mdx --push --type feat

# Skip build validation (faster)
python scripts/publish_article.py content/docs/en/development/article.mdx --push --skip-build
```

## Directory Structure

```
skill-article-publisher/
├── SKILL.md (2500+ lines - comprehensive usage guide)
├── scripts/
│   ├── validate_mdx.py (250+ lines - MDX validation)
│   └── publish_article.py (350+ lines - publishing automation)
├── references/
│   └── semantic-commit-guide.md (semantic commit best practices)
└── examples/
    └── publish-mcp-builder-output.md (example workflow)
```

## Key Checks

The validator catches these common MDX errors:

- ❌ Unescaped comparison operators: `>80%` → `&gt;80%`
- ❌ Invalid frontmatter structure
- ❌ Missing required fields (title, description, lang)
- ❌ Invalid language codes
- ❌ Build compilation errors

## Commit Types

Generated commits follow conventional commits:

- `feat`: New skill analyses, significant features
- `docs`: Documentation, tutorials (default)
- `fix`: Bug fixes, corrections
- `chore`: Maintenance, refactoring

## Examples

### Publish Single Article

```bash
python scripts/publish_article.py \
  content/docs/en/development/analyzing-mcp-builder.mdx \
  --push \
  --type feat
```

**Generated commit**:
```
feat: publish analyzing-mcp-builder (en, zh, fr)

skill-analysis: analyzing-mcp-builder

Languages: en, zh, fr
```

### Publish Multiple Articles

```bash
python scripts/publish_article.py \
  content/docs/en/development/ \
  --push
```

**Generated commit**:
```
docs: publish multiple articles (2 skill-analysis, 1 tutorial)

skill-analysis: analyzing-mcp-builder, analyzing-webapp-testing
tutorial: tutorial-creating-first-skill

Languages: en, zh, fr
```

## Requirements

- Python 3.7+
- Git
- npm (for build validation)
- Working Node.js project (for build validation)

## Best Practices

1. **Always validate before publishing**: Catch errors early
2. **Use dry run first**: Preview changes with `--push`
3. **Fix validation errors**: Address warnings/errors before commit
4. **Group related changes**: Publish related articles together
5. **Use semantic types**: Match commit type to change nature

## Troubleshooting

**Validation errors**: Run validation script first to see specific issues

```bash
python scripts/validate_mdx.py path/to/file.mdx
```

**Build fails**: Check build output for MDX compilation errors

```bash
npm run build 2>&1 | grep -A 5 Error
```

**Git push fails**: Ensure credentials are configured

```bash
git config --global user.name"Your Name"
git config --global user.email"your.email@example.com"
```

## See Also

- **SKILL.md**: Complete 6-step usage guide with detailed examples
- **references/semantic-commit-guide.md**: Semantic commit best practices
- **examples/**: Example workflows and outputs

## License

See LICENSE.txt for complete terms.
