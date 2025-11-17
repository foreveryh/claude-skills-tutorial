# Example: Publishing analyzing-mcp-builder

This example demonstrates the complete publishing workflow for the analyzing-mcp-builder article.

## Initial Validation

**Run validation**:
```bash
cd .claude/skills/skill-article-publisher
python scripts/validate_mdx.py content/docs/en/development/analyzing-mcp-builder.mdx
```

**Validation output**:
```
Found 1 MDX files to validate

[1/1] Validating analyzing-mcp-builder.mdx...

MDX VALIDATION REPORT
================================================================================

❌ ERRORS (2):
  File: content/docs/en/development/analyzing-mcp-builder.mdx:730
  Error: Unescaped comparison operator found. Use &gt; instead of > in: Typical benchmarks: >80% accuracy

  File: content/docs/en/development/analyzing-mcp-builder.mdx:731
  Error: Unescaped comparison operator found. Use &gt; instead of > in: - **Good**: >80% accuracy

⚠️  WARNINGS (0):

📊 SUMMARY:
  Files checked: 1
  Files valid: 0
  Errors: 2
  Warnings: 0

❌ Validation failed due to errors
================================================================================
```

## Fix Errors

**Edit the file** and fix the unescaped operators:

**Before**:
```mdx
Typical benchmarks:
- **Good**: >80% accuracy
- **Excellent**: >90% accuracy
- **Outstanding**: >95% accuracy
```

**After**:
```mdx
Typical benchmarks:
- **Good**: &gt;80% accuracy
- **Excellent**: &gt;90% accuracy
- **Outstanding**: &gt;95% accuracy
```

**Re-run validation**:
```bash
python scripts/validate_mdx.py content/docs/en/development/analyzing-mcp-builder.mdx
```

**Output**:
```
================================================================================

❌ ERRORS (0):

⚠️  WARNINGS (0):

📊 SUMMARY:
  Files checked: 1
  Files valid: 1
  Errors: 0
  Warnings: 0

✅ All files passed validation with no issues!
================================================================================
```

## Dry Run

**Test publish without committing**:
```bash
python scripts/publish_article.py content/docs/en/development/analyzing-mcp-builder.mdx
```

**Output**:
```
📁 Project root: /Users/peng/Dev/AI_SKILLS/claude-skills

🔧 Running build validation (this may take a while)...
✅ Build validation passed

🔍 Running MDX validation...

MDX VALIDATION REPORT
================================================================================

⚠️  WARNINGS (3):
  File: content/docs/en/development/analyzing-mcp-builder.mdx:1
  Warning: Lang code "zh" may not be supported.

  File: content/docs/zh/development/analyzing-mcp-builder.mdx:1
  Warning: Lang code "zh" may not be supported.

  File: content/docs/fr/development/analyzing-mcp-builder.mdx:1
  Warning: Lang code "fr" may not be supported.

📊 SUMMARY:
  Files checked: 3
  Files valid: 3
  Errors: 0
  Warnings: 3

✅ All files passed validation (with warnings)

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

✅ Dry run complete!
```

## Review and Confirm

**Review the output**:
- ✅ Build passed
- ✅ MDX validation passed (warnings acceptable)
- ✅ Correct files detected (3 languages)
- ✅ Commit message looks good
- ✅ Dry run shows what would happen

**Ready to publish?** Rerun with `--push`:

```bash
python scripts/publish_article.py content/docs/en/development/analyzing-mcp-builder.mdx --push
```

## Actual Publish

**Confirmation prompt**:
```
================================================================================
Proceed with commit and push? [y/N]: y

🔧 Running build validation (this may take a while)...
✅ Build validation passed

🔍 Running MDX validation...
✅ MDX validation passed (with 3 warnings)

📁 Project root: /Users/peng/Dev/AI_SKILLS/claude-skills

📄 Changes detected (3 files):
  - content/docs/en/development/analyzing-mcp-builder.mdx [en]
  - content/docs/zh/development/analyzing-mcp-builder.mdx [zh]
  - content/docs/fr/development/analyzing-mcp-builder.mdx [fr]

📝 Generated commit message:

    feat: publish analyzing-mcp-builder (en, zh, fr)

    skill-analysis: analyzing-mcp-builder

    Languages: en, zh, fr

📝 Preparing commit...
✅ Commit created successfully

🚀 Pushing to remote...
✅ Changes pushed to origin/main

✅ Publish complete!
```

## Verify Result

**Check git log**:
```bash
git log -1 --pretty=format:"%h %s"
```

**Output**:
```
a1b2c3d feat: publish analyzing-mcp-builder (en, zh, fr)
```

**Check remote**:
```bash
git status
```

**Output**:
```
On branch main
Your branch is up to date with 'origin/main'.

nothing to commit, working tree clean
```

## View on GitHub

Visit repository on GitHub/GitLab:
- Go to repository page
- Check latest commit matches
- Verify files are published
- Verify CI/CD passes (if applicable)

## Summary of Workflow

1. ✅ **Identified files**: 3 MDX files (en, zh, fr)
2. ✅ **Validated MDX**: Fixed 2 syntax errors
3. ✅ **Built project**: Verified no build errors
4. ✅ **Generated commit**: feat type with proper message
5. ✅ **Created commit**: Staged and committed changes
6. ✅ **Pushed to remote**: Origin/main updated

## Common Variations

### Publishing Without Build Validation

```bash
python scripts/publish_article.py \
  content/docs/article.mdx \
  --push \
  --skip-build
```

**Use when**: Build already verified or need faster publishing

### Publishing Multiple Files

```bash
python scripts/publish_article.py \
  content/docs/en/development/ \
  --push
```

**Automatically detects**: All new/modified MDX files in directory

### Force Specific Commit Type

```bash
python scripts/publish_article.py \
  content/docs/article.mdx \
  --push \
  --type docs
```

**Overrides**: Auto-detection of commit type

### CI/CD Integration

```yaml
# In .github/workflows/publish.yml
- name: Publish articles
  run: |
    cd .claude/skills/skill-article-publisher
    python scripts/publish_article.py content/docs/ --push
```

**Benefits**:
- Automated validation
- Consistent commits
- No manual intervention
- Immediate publishing
