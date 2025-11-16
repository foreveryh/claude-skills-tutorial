---
name: translator
description: Professional translation using Claude's native capabilities. Use this skill when the user needs to translate text between languages with high quality, or when content needs to be localized for different language audiences.
version: 1.0.0
---

# Professional Translation Skill

Provide professional, high-quality translation using Claude's native language understanding and generation capabilities.

## Overview

This skill enables accurate, context-aware translation between languages while preserving:
- Technical terminology
- Code blocks and syntax
- Markdown formatting
- Cultural appropriateness
- Original tone and intent

## Translation Workflow

### Step 1: Analyze Source Content

Before translating:
1. Identify the source language (if not explicitly provided)
2. Understand the content type (technical documentation, article, UI text, etc.)
3. Note any technical terms, code blocks, or special formatting
4. Determine the appropriate tone and style

### Step 2: Perform Translation

Apply professional translation principles:

**Accuracy:**
- Preserve the exact meaning of the original text
- Maintain technical accuracy, especially for domain-specific content
- Keep numerical values, dates, and proper nouns appropriate for the target locale

**Fluency:**
- Produce natural, idiomatic text in the target language
- Avoid literal word-for-word translation
- Use appropriate sentence structure for the target language

**Format Preservation:**
- Keep all Markdown syntax exactly as-is (headings, lists, links, etc.)
- Preserve code blocks completely unchanged
- Maintain image references and paths
- Keep HTML/JSX tags and attributes unchanged
- **CRITICAL for MDX - Bold/Italic spacing**:
  - Always add a space after `**bold**` or `*italic*` before the next character
  - Example: `**Text:** word` → Ensure space after the second `**`
  - Correct: `**粗体：** 文字` (space after `**`)
  - Wrong: `**粗体：**文字` (no space, will break MDX rendering)
  - This is especially important for non-Latin languages (Chinese, Korean, Japanese)
  - Apply to all bold/italic patterns: `**...**`, `*...*`, `__...__`, `_..._`

**Technical Terms:**
- For widely recognized technical terms (API, HTTP, Git), keep in English or use standard translations
- For product names and brand names, keep original
- Use target language conventions for technical documentation

### Step 3: Language-Specific Guidelines

**Chinese (Simplified - zh):**
- Use simplified Chinese characters (简体中文)
- Technical terms: Keep English when widely used (e.g., API, SDK) or use standard Chinese translations
- Punctuation: Use Chinese punctuation (。、，！？) for text, but keep English punctuation in code
- Tone: Professional and clear, use 您 for formal contexts

**French (fr):**
- Use proper French accents (é, è, à, ô, etc.)
- Technical terms: Use standard French translations when they exist (e.g., "ordinateur" not "computer")
- Tone: Maintain formal "vous" unless context clearly indicates informal tone
- Numbers: Use French formatting (space for thousands: 1 000 not 1,000)

**Korean (ko):**
- Use appropriate honorific level (formal 합니다 style for documentation)
- Technical terms: Common terms stay in English, but use Korean for general concepts
- Tone: Professional and respectful
- Mixed script: Acceptable to mix Korean with English technical terms

**English (en):**
- Use clear, professional English
- Follow US spelling conventions unless specified otherwise
- Technical terms: Use industry-standard terminology
- Tone: Professional but accessible

### Step 4: Quality Check

Before delivering translation:
1. Verify all code blocks remain unchanged
2. Check that Markdown formatting is preserved
3. Ensure technical terms are handled consistently
4. Confirm the translation reads naturally in the target language
5. Validate that links, images, and references still work

## Output Format

Present translations clearly:

**For single translations:**
Provide the translated text directly, maintaining all original formatting.

**For multiple languages:**
Use clear section headers to separate each language:

```markdown
## English (en)
[Translated content]

## 中文 (zh)
[Translated content]

## Français (fr)
[Translated content]

## 한국어 (ko)
[Translated content]
```

## Special Cases

### Code Comments
- Translate comments inside code blocks only if explicitly requested
- Default: Keep code (including comments) unchanged

### Mixed Content
- For content mixing multiple languages, preserve the intentional multilingual parts
- Only translate what should be translated

### Cultural References
- Adapt idioms and cultural references to equivalent concepts in target language
- When no equivalent exists, provide a culturally neutral translation that preserves meaning

### Acronyms and Abbreviations
- Keep widely-known acronyms in original form (HTML, CSS, API, REST, etc.)
- Spell out and translate acronyms specific to the source language

## Examples

### Example 1: Technical Documentation

**Source (en):**
```markdown
# Getting Started

Install the package using npm:

\`\`\`bash
npm install my-package
\`\`\`

The API provides three endpoints for data retrieval.
```

**Target (zh):**
```markdown
# 快速开始

使用 npm 安装该包：

\`\`\`bash
npm install my-package
\`\`\`

该 API 提供三个数据检索端点。
```

### Example 2: Preserving Technical Terms

**Source (en):**
"The React component uses hooks for state management."

**Target (zh):**
"该 React 组件使用 hooks 进行状态管理。"

**Target (fr):**
"Le composant React utilise des hooks pour la gestion d'état."

**Target (ko):**
"React 컴포넌트는 상태 관리를 위해 hooks를 사용합니다."

### Example 3: Markdown Preservation

**Source:**
```markdown
> **Note:** This is important.

See [documentation](https://example.com) for details.
```

**Translation maintains exact same structure:**
```markdown
> **注意：** 这很重要。

详情请参阅[文档](https://example.com)。
```

## Best Practices

1. **Context is key:** Understanding the content type and audience improves translation quality
2. **Consistency:** Use the same translation for recurring terms throughout a document
3. **Natural flow:** Prioritize readability in the target language over literal translation
4. **Preserve intent:** Maintain the original purpose and tone of the content
5. **Ask when uncertain:** If target language or specific terminology is unclear, ask for clarification

## Notes

- This skill uses Claude's native multilingual capabilities, no external translation APIs required
- Translation quality benefits from understanding the full context of the content
- For very large documents, consider translating section by section to maintain quality
- Always preserve code, links, and formatting exactly as they appear in the source
