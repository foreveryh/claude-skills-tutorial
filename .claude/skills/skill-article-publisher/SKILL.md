---
name: skill-article-publisher
license: Complete terms in LICENSE.txt
description: Automate article validation, semantic commit generation, and git publishing for MDX documentation. Validates syntax, runs build checks, creates semantic commits, and pushes to remote repositories.
---

# Article Publisher Automation Guide

This skill automates the complete article publishing workflow: MDX syntax validation, build verification, semantic commit generation, and git push. Use this to ensure documentation quality and maintain consistent git history.

---

# Process

## 🚀 6-Step Publishing Workflow

This is a comprehensive publishing skill that validates and publishes MDX articles with automated semantic commits and git push.

### Phase 1: Identify Target Files

#### 1.1 Determine Article Location

First, identify what needs to be published:

**For single article**: Provide path to specific `.mdx` file
```bash
content/docs/en/development/my-article.mdx
```

**For multiple articles**: Provide directory containing changes
```bash
content/docs/en/development/
```

The skill will automatically detect:
- New MDX files (added to git)
- Modified MDX files
- Multi-language versions (en, zh, fr)
- File types (skill analysis, tutorials, etc.)

#### 1.2 Review Current Git Status

Before publishing, understand the current state:

**Check git status**:
```bash
git status
```

**Review changes**:
```bash
git diff --staged
```

**Ensure all MDX files are saved** and ready for validation.

---

### Phase 2: Run Validation

#### 2.1 MDX Syntax Validation

**Run validation script**:

```bash
cd .claude/skills/skill-article-publisher
python scripts/validate_mdx.py /path/to/article.mdx
```

**Or validate directory**:
```bash
python scripts/validate_mdx.py content/docs/en/development/
```

**What it checks**:
- ✅ YAML frontmatter structure
- ✅ Required fields (title, description, lang)
- ✅ Unescaped comparison operators (>, <) in text
- ✅ Common unescaped characters
- ✅ MDX component tag balance
- ✅ HTML tag balance

**Critical checks for Claude skills**:
- **Comparison operators**: Always use `&gt;` and `&lt;` instead of `>` and `<` in text
  - ❌ Wrong: `>80% accuracy`
  - ✅ Correct: `&gt;80% accuracy`
- **Frontmatter**: Must have `title`, `description`, `lang` fields
- **Lang codes**: Should be `en`, `zh`, or `fr` for standard Claude skills

#### 2.2 Build Validation (Optional but Recommended)

**Run build to verify MDX compilation**:

```bash
npm run build
```

**Why this matters**:
- **Primary validation**: Build catches all MDX syntax errors
- Verifies MDX components render correctly
- Ensures imports and dependencies work
- Validates TypeScript types if applicable

**Important note on validation**:
The MDX validation script focuses on common issues (comparison operators, frontmatter), while complex MDX component syntax validation is best handled by the build process. Always run build validation for complete assurance.

**Or use validation script with build**:
```bash
python scripts/validate_mdx.py content/docs/en/development/article.mdx --build
```

**Build timeout**: 5 minutes (adjust in script if needed)

**Interpret results**:
- ✅ Build succeeds → MDX syntax is valid
- ❌ Build fails → Check error messages for issues
- ⚠️  Build timeout → May indicate large project or problem

---

### Phase 3: Review Validation Results

#### 3.1 Analyze Validation Output

**Validation report structure**:
```
MDX VALIDATION REPORT
================================================================================

❌ ERRORS (2):
  File: content/docs/en/development/article.mdx:730
  Error: Unescaped comparison operator found. Use &gt; instead of > in: Typical benchmarks: >80% accuracy

⚠️  WARNINGS (1):
  File: content/docs/en/development/article.mdx:1
  Warning: Lang code "ko" may not be supported.

📊 SUMMARY:
  Files checked: 1
  Files valid: 0
  Errors: 2
  Warnings: 1

❌ Validation failed due to errors
```

**Fix errors before proceeding**:
1. **Unescaped operators**: Replace `>` with `&gt;` and `<` with `&lt;`
2. **Missing fields**: Add required frontmatter fields
3. **Tag balance**: Close any unclosed MDX components
4. **Invalid lang**: Change to supported language code

**Warnings are acceptable** but should be reviewed.

#### 3.2 Run Validation Again

After fixing issues, re-run validation:

```bash
python scripts/validate_mdx.py content/docs/en/development/article.mdx
```

**Continue until**: "All files passed validation"

---

### Phase 4: Generate Commit Message

#### 4.1 Detect Change Types

The publisher automatically detects:

**Change type from file path**:
- `analyzing-mcp-builder` → `feat` (new skill analysis)
- `analyzing-skill-name` → `feat` (skill analysis)
- `tutorial-*` → `docs` (documentation/tutorial)
- Other patterns → `docs` (default)

**Change type from branch**:
- `feature/*` → `feat`
- `fix/*` → `fix`
- `docs/*` → `docs`
- `main` → `docs` (default)

#### 4.2 Multi-Language Detection

**Languages detected from path**:
- `/en/` → English
- `/zh/` → Chinese
- `/fr/` → French

**Single file**:
```
feat: publish analyzing-mcp-builder (en, zh, fr)
```

**Multiple files**:
```
feat: publish multiple articles (3 skill-analysis, 2 tutorial)

skill-analysis: analyzing-mcp-builder, analyzing-webapp-testing
tutorial: tutorial-usage-patterns, tutorial-best-practices

Languages: en, zh, fr
```

---

### Phase 5: Commit Changes

#### 5.1 Dry Run (Default)

**Test without actual push**:

```bash
python scripts/publish_article.py content/docs/en/development/article.mdx
```

**What happens**:
1. ✅ Run MDX validation
2. ✅ Run build validation
3. ✅ Generate commit message (shows in output)
4. ⏭️  Commit (shows what would be committed)
5. ⏭️  Push (requires `--push` flag)

**Output includes**:
```
📄 Changes detected (3 files):
  - content/docs/en/development/analyzing-mcp-builder.mdx [en]
  - content/docs/zh/development/analyzing-mcp-builder.mdx [zh]
  - content/docs/fr/development/analyzing-mcp-builder.mdx [fr]

📝 Generated commit message:

    feat: publish analyzing-mcp-builder (en, zh, fr)

    skill-analysis: analyzing-mcp-builder

    Languages: en, zh, fr

📦 Actions:
  ✅ Validate MDX
  ✅ Create semantic commit (dry run)
  ⏭️  Push (use --push to enable)
```

#### 5.2 Create Commit

**With interactive confirmation**:

```bash
# Shows summary and asks for confirmation
python scripts/publish_article.py content/docs/en/development/article.mdx --push
```

**Automatically stage, commit, and push**:

```bash
python scripts/publish_article.py content/docs/en/development/article.mdx --push --type feat
```

**Available commit types**:
- `docs` → Documentation only (default)
- `feat` → New feature/skill analysis
- `fix` → Bug fix or correction
- `chore` → Maintenance, refactoring

---

### Phase 6: Push to Remote

#### 6.1 Automated Push

**With --push flag**:

```bash
python scripts/publish_article.py content/docs/en/development/article.mdx --push
```

**What happens**:
1. ✅ All validation passes
2. ✅ Commit created
3. ✅ Push to current branch
4. ✅ Shows success message

**Output**:
```
🚀 Pushing to remote...

✅ Changes pushed to origin/main

✅ Publish complete!
```

#### 6.2 Manual Push (Alternative)

**If not using --push, manually push later**:

```bash
git push origin $(git branch --show-current)
```

**Or create PR from GitHub/GitLab interface**.

---

## Publishing Options

### Option 1: Single Article (Interactive)

**For one article with confirmation**:

```bash
cd .claude/skills/skill-article-publisher
python scripts/publish_article.py content/docs/en/development/analyzing-mcp-builder.mdx
```

**Review output, then rerun with --push** if satisfied.

### Option 2: Directory Publishing

**For all articles in a directory**:

```bash
python scripts/publish_article.py content/docs/en/development/
```

**Automatically detects**:
- All new/modified `.mdx` files
- Multi-language versions
- Generates comprehensive commit

### Option 3: CI/CD Integration

**For automated pipelines**:

```bash
python scripts/publish_article.py content/docs/en/development/ \
  --push \
  --type docs \
  --skip-build  # If build already ran in CI
```

**GitHub Actions example**:
```yaml
- name: Publish articles
  run: |
    cd .claude/skills/skill-article-publisher
    python scripts/publish_article.py content/docs/ --push
```

### Option 4: Skip Validations (Fast Mode)

**When you know files are valid**:

```bash
python scripts/publish_article.py content/docs/en/development/article.mdx \
  --push \
  --skip-build \
  --skip-mdx
```

**Use with caution** - only when certain files are valid.

---

## Best Practices

### Validation Best Practices

<Cards>
  <Card title="Always Validate First" icon="CheckCircle">
    Never commit without running validation first. Build failures are harder to debug after commit.
  </Card>

  <Card title="Escape Comparison Operators" icon="Code">
    Always use &gt; and &lt; in text content. Never use raw > or < outside code blocks.
  </Card>

  <Card title="Validate Single File First" icon="FileText">
    When publishing many files, validate one first to catch systematic errors.
  </Card>

  <Card title="Use Dry Run Mode" icon="Eye">
    Review commit message and changes with dry run before actually pushing.
  </Card>
</Cards>

### Commit Best Practices

<Steps>
  <Step>
    **Use Semantic Types**: Match commit type to change nature
    - `feat`: New skill analysis, significant features
    - `docs`: Documentation, tutorials
    - `fix`: Corrections, bug fixes
    - `chore`: Maintenance, refactoring
  </Step>

  <Step>
    **Group Related Changes**: Publish related articles together for cohesive commits
  </Step>

  <Step>
    **Write Descriptive Messages**: Generated messages should clearly describe what's published
  </Step>

  <Step>
    **Include All Languages**: Multi-language articles ensure international accessibility
  </Step>
</Steps>

### Common Pitfalls

<Callout type="warn">
  **Critical**: Never use raw > or < in MDX text content - always escape as &gt; and &lt;
</Callout>

❌ **Wrong**:
```mdx
Typical benchmarks:
- **Good**: >80% accuracy
- **Excellent**: >90% accuracy
```

✅ **Correct**:
```mdx
Typical benchmarks:
- **Good**: &gt;80% accuracy
- **Excellent**: &gt;90% accuracy
```

❌ **Don't commit without validation**:
```bash
git add . && git commit -m "add article" && git push
# May fail if MDX has syntax errors
```

✅ **Do use skill-article-publisher**:
```bash
python scripts/publish_article.py content/docs/ --push
# Validates, builds, commits, and pushes safely
```

---

## Examples

### Example 1: Single Skill Analysis

**Publishing one skill analysis**:

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

### Example 2: Multiple Articles

**Publishing directory of changes**:

```bash
python scripts/publish_article.py \
  content/docs/en/development/ \
  --push \
  --type docs
```

**Generated commit**:
```
docs: publish multiple articles (2 skill-analysis, 1 tutorial)

skill-analysis: analyzing-mcp-builder, analyzing-webapp-testing
tutorial: creating-first-skill

Languages: en, zh, fr
```

### Example 3: CI/CD Integration

**GitHub Actions workflow**:

```yaml
name: Publish Articles

on:
  push:
    branches: [main]
    paths: ['content/docs/**/*.mdx']

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          npm ci
          pip install -r requirements.txt

      - name: Publish articles
        run: |
          cd .claude/skills/skill-article-publisher
          python scripts/publish_article.py content/docs/ --push --type docs
```

---

## Troubleshooting

### Validation Errors

**Problem**: Build succeeds but validation shows errors

```
Error: Unescaped comparison operator found. Use &gt; instead of >
```

**Solution**:
```bash
# Find and replace all > with &gt; in text
# Find and replace all < with &lt; in text
# Rerun validation
python scripts/validate_mdx.py path/to/file.mdx
```

**Problem**: Frontmatter validation warnings

```
Warning: Missing recommended field in frontmatter: description
```

**Solution**: Add missing field to YAML frontmatter at top of file.

### Git Errors

**Problem**: "No changes to commit"

**Cause**: Files not staged or already committed

**Solution**:
```bash
git status  # Check current state
git add content/docs/  # Stage changes
python scripts/publish_article.py content/docs/ --push
```

**Problem**: Push fails with "rejected"

**Cause**: Remote has changes you don't have locally

**Solution**:
```bash
git pull --rebase origin $(git branch --show-current)
python scripts/publish_article.py content/docs/ --push
```

**Problem**: Authentication fails during push

**Cause**: Git credentials not configured

**Solution**:
```bash
# Configure git credentials
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# For HTTPS: use credential helper
git config --global credential.helper store

# For SSH: ensure SSH key is set up
ssh-keygen -t ed25519 -C "your.email@example.com"
```

### Build Failures

**Problem**: Build timeout (5 minutes)

**Cause**: Large project or slow machine

**Solution**:
```bash
# Skip build validation for faster publishing
python scripts/publish_article.py content/docs/ --push --skip-build
```

**Problem**: Build fails with MDX errors

**Cause**: Invalid MDX syntax

**Solution**:
```bash
# Run validation to see specific errors
python scripts/validate_mdx.py content/docs/

# Or check build output directly
npm run build 2>&1 | grep -A 5 -B 5 Error
```

---

## Integration with Other Skills

skill-article-publisher works well with:

1. **skill-article-writer** - Validate and publish articles generated by article-writer
2. **skill-creator** - Validate and commit new skills
3. **translator** - After translation, validate all language versions
4. **fumadocs-article-importer** - Validate imported external articles

---

## Next Steps

To use skill-article-publisher:

1. **Clone the repository**: `git clone https://github.com/anthropics/skills`
2. **Locate the skill**: `cd .claude/skills/skill-article-publisher`
3. **Run validation**: `python scripts/validate_mdx.py path/to/article.mdx`
4. **Fix any errors**: Update MDX files based on validation output
5. **Test dry run**: `python scripts/publish_article.py path/to/article.mdx`
6. **Review commit message**: Ensure it accurately describes changes
7. **Publish**: `python scripts/publish_article.py path/to/article.mdx --push`

### Related Resources

- **skill-article-writer**: /development/analyzing-skill-article-writer
- **Claude Skills Repository**: github.com/anthropics/skills
- **Semantic Commits**: semantic-release.gitbook.io/semantic-release/
- **MDX Documentation**: mdxjs.com

---

## Conclusion

skill-article-publisher demonstrates exceptional Claude skill design by:

✅ **Automating Quality Assurance**: Systematic MDX validation prevents syntax errors
✅ **Enforcing Best Practices**: Built-in rules for comparison operators and structure
✅ **Semantic Commit Generation**: Intelligent detection of change types and languages
✅ **Git Workflow Integration**: Seamless staging, committing, and pushing
✅ **Safety Features**: Dry run mode, confirmation prompts, comprehensive validation
✅ **Error Prevention**: Catches issues before they reach production

The key insights from this skill ensure that every article is validated, properly committed, and safely published with minimal manual intervention.

---

## Summary

This comprehensive guide covered:

- ✅ 6-step publishing workflow from identification to push
- ✅ MDX syntax validation and common error prevention
- ✅ Build validation integration
- ✅ Change detection and categorization
- ✅ Automatic semantic commit generation
- ✅ Git staging, committing, and pushing
- ✅ Troubleshooting common issues
- ✅ CI/CD integration patterns

## Next Steps

Ready to automate your publishing workflow?

1. **Study the validation script**: Understand what it checks and why
2. **Test validation**: Run validate_mdx.py on existing articles
3. **Fix any issues**: Update articles based on validation output
4. **Try dry run**: Use publish_article.py without --push first
5. **Review commit message**: Ensure it accurately describes changes
6. **Publish with confidence**: Add --push when ready
7. **Integrate into workflow**: Use for all future article publishing

## ℹ️ Source Information

**Created**: 2025-01-17
**Skill**: skill-article-publisher
**Author**: Anthropic

This skill provides production-ready automation for MDX article publishing with comprehensive validation and semantic commit generation.

---

## Appendix

### Complete Script Features

**validate_mdx.py** (250+ lines):
- ✅ YAML frontmatter validation
- ✅ Comparison operator detection
- ✅ Unescaped character detection
- ✅ MDX component tag balance
- ✅ HTML tag balance
- ✅ Build validation integration
- ✅ Recursive directory validation
- ✅ Detailed error/warning reporting

**publish_article.py** (350+ lines):
- ✅ Git change detection
- ✅ Change type classification
- ✅ Multi-language detection
- ✅ Semantic commit generation
- ✅ Build validation
- ✅ MDX validation integration
- ✅ Automatic staging and committing
- ✅ Push to remote
- ✅ Dry run mode
- ✅ Interactive confirmation

### Validation Checklist

Before publishing, ensure:

- [ ] All MDX files pass validation
- [ ] No unescaped > or < in text content
- [ ] Build completes successfully
- [ ] Commit message accurately describes changes
- [ ] Changes staged and ready
- [ ] (Optional) Dry run reviewed
- [ ] Remote branch exists
- [ ] Git credentials configured

### Common Escape Patterns

| Raw | Escaped | Context |
|-----|---------|---------|
| `>` | `&gt;` | Text, comparisons, arrows |
| `<` | `&lt;` | Text, comparisons, arrows |
| `&` | `&amp;` | Text (not in entities) |
| `"` | `&quot;` | In HTML attributes |

**Note**: Always use escapes in text content, never in code blocks or YAML frontmatter.
