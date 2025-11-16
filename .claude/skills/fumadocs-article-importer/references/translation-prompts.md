# Translation Prompts for Multi-Language Article Import

This document contains the translation prompts used for converting articles into different languages while maintaining technical accuracy and proper formatting.

## General Translation Principles

### Core Rules (Apply to All Languages)
1. **Preserve all Markdown syntax exactly** - Do not modify formatting
2. **Keep code blocks unchanged** - Code should remain in original form
3. **Maintain image references** - Paths and alt text structure stay the same
4. **Preserve heading hierarchy** - H1, H2, H3 levels must match original
5. **Keep technical terms appropriate** - Some terms better left in English
6. **Adapt examples culturally** - When relevant, localize examples
7. **Maintain link structure** - Preserve all URLs and link formatting

### What to Translate
- ✅ Article title
- ✅ Article description/summary
- ✅ Body paragraphs and explanations
- ✅ Headings and subheadings
- ✅ List items
- ✅ Blockquote content
- ✅ Table content
- ✅ Image alt text (keep descriptive)
- ✅ Callout/alert messages

### What NOT to Translate
- ❌ Code blocks (code, commands, syntax)
- ❌ Code variable names
- ❌ File paths and URLs
- ❌ Package names and module names
- ❌ API endpoints
- ❌ Function/class names in inline code
- ❌ Fumadocs component syntax (e.g., `<Card>`, `<Callout>`)
- ❌ YAML frontmatter keys (only translate values when appropriate)

---

## English (en) - Original Language

**Prompt**: No translation needed. This is the base language.

**Process**:
1. Use the original article content as-is
2. Convert to MDX format
3. Apply Fumadocs components where appropriate
4. Ensure clean Markdown syntax

**Special Considerations**:
- Verify American English spelling (color, not colour)
- Use technical terminology standard in English-speaking communities
- Keep examples relevant to global audience

---

## Chinese (zh) - Simplified Chinese

**Translation Prompt**:

```
Translate the following technical article to Simplified Chinese (简体中文).

CRITICAL RULES:
1. Preserve ALL Markdown syntax exactly (**, *, `, ```, >, -, 1., etc.)
2. Do NOT translate code blocks - keep all code in original form
3. Do NOT modify image paths or URLs
4. Keep technical terms in English when standard practice (e.g., API, React, hook, component)
5. Use standard Chinese translations for common technical concepts where appropriate
6. Maintain the exact same heading structure (H1, H2, H3)
7. Keep Fumadocs component syntax unchanged (e.g., <Card>, <Callout>)

TRANSLATION GUIDELINES:
- Use clear, professional technical Chinese
- Keep sentences concise and readable
- Use standard technical terminology from major tech companies (阿里巴巴, 腾讯, 字节跳动)
- When in doubt, provide the English term in parentheses: 组件 (component)
- Adapt examples to be culturally relevant for Chinese readers when appropriate

PRESERVE EXACTLY:
- All code blocks (```javascript, ```python, etc.)
- File paths (/public/images/...)
- URLs (https://...)
- Package names (npm install react)
- Command line syntax (curl, npm, git commands)
- Fumadocs JSX components (<Cards>, <Card>, <Callout>, etc.)
- YAML frontmatter structure

EXAMPLE OF GOOD TRANSLATION:

Original:
> **Note**: This feature requires React 18 or higher.

Correct:
> **注意**: 此功能需要 React 18 或更高版本。

Original:
```bash
npm install react-query
```

Correct (unchanged):
```bash
npm install react-query
```

Now translate the following article:

---

{ARTICLE_CONTENT}

---

Provide the complete translated article with all Markdown formatting preserved.
```

**Special Considerations for Chinese**:

### Technical Terms to Keep in English
- Framework/library names: React, Vue, Next.js, Express
- Programming concepts commonly used in English: hook, state, props, component
- Tools: npm, yarn, git, docker, kubernetes
- File extensions: .js, .tsx, .md, .json

### Standard Chinese Translations
- function → 函数
- variable → 变量
- array → 数组
- object → 对象
- string → 字符串
- database → 数据库
- server → 服务器
- client → 客户端
- API → API (keep in English)
- endpoint → 端点 or 接口
- request → 请求
- response → 响应

### Common Phrases
- "Let's get started" → 让我们开始吧
- "For example" → 例如
- "Note that" → 请注意
- "In this tutorial" → 在本教程中
- "Best practices" → 最佳实践
- "Common mistakes" → 常见错误

---

## French (fr) - French

**Translation Prompt**:

```
Translate the following technical article to French.

CRITICAL RULES:
1. Preserve ALL Markdown syntax exactly (**, *, `, ```, >, -, 1., etc.)
2. Do NOT translate code blocks - keep all code in original form
3. Do NOT modify image paths or URLs
4. Keep technical terms in English when standard in French tech community
5. Use standard French technical terminology where appropriate
6. Maintain the exact same heading structure (H1, H2, H3)
7. Keep Fumadocs component syntax unchanged (e.g., <Card>, <Callout>)

TRANSLATION GUIDELINES:
- Use clear, professional technical French
- Follow standard French tech writing conventions
- Use formal "vous" form when addressing the reader
- Keep technical terms that are commonly used in English (e.g., framework, hook, component)
- Provide French translations for general programming concepts
- Adapt examples to be relevant for French-speaking audience when appropriate

PRESERVE EXACTLY:
- All code blocks (```javascript, ```python, etc.)
- File paths (/public/images/...)
- URLs (https://...)
- Package names (npm install react)
- Command line syntax (curl, npm, git commands)
- Fumadocs JSX components (<Cards>, <Card>, <Callout>, etc.)
- YAML frontmatter structure

EXAMPLE OF GOOD TRANSLATION:

Original:
> **Note**: This feature requires React 18 or higher.

Correct:
> **Remarque** : Cette fonctionnalité nécessite React 18 ou version ultérieure.

Original:
```bash
npm install react-query
```

Correct (unchanged):
```bash
npm install react-query
```

Now translate the following article:

---

{ARTICLE_CONTENT}

---

Provide the complete translated article with all Markdown formatting preserved.
```

**Special Considerations for French**:

### Technical Terms to Keep in English
- Framework/library names: React, Vue, Next.js, Express
- Modern programming terms: hook, state, component, props
- Tools: npm, yarn, git, docker, kubernetes
- Common abbreviations: API, REST, HTTP, JSON

### Standard French Translations
- function → fonction
- variable → variable
- array → tableau
- object → objet
- string → chaîne (de caractères)
- database → base de données
- server → serveur
- client → client
- request → requête
- response → réponse
- file → fichier
- folder → dossier

### Common Phrases
- "Let's get started" → Commençons
- "For example" → Par exemple
- "Note that" → Notez que
- "In this tutorial" → Dans ce tutoriel
- "Best practices" → Bonnes pratiques
- "Common mistakes" → Erreurs courantes

### French Typography Rules
- Space before: `:`, `;`, `!`, `?`
- Use guillemets français: « text »
- Use proper accents: é, è, ê, à, etc.

---

## Korean (ko) - Korean

**Translation Prompt**:

```
Translate the following technical article to Korean (한국어).

CRITICAL RULES:
1. Preserve ALL Markdown syntax exactly (**, *, `, ```, >, -, 1., etc.)
2. Do NOT translate code blocks - keep all code in original form
3. Do NOT modify image paths or URLs
4. Keep technical terms in English when standard in Korean tech community
5. Use standard Korean technical terminology where appropriate
6. Maintain the exact same heading structure (H1, H2, H3)
7. Keep Fumadocs component syntax unchanged (e.g., <Card>, <Callout>)

TRANSLATION GUIDELINES:
- Use clear, professional technical Korean (기술 문서 작성체)
- Use formal polite form (합니다/습니다 체)
- Keep technical terms that are commonly used in English in Korean tech community
- Use standard Korean translations from major tech companies (Naver, Kakao, Samsung)
- Provide Korean translations for general programming concepts
- Adapt examples to be relevant for Korean audience when appropriate

PRESERVE EXACTLY:
- All code blocks (```javascript, ```python, etc.)
- File paths (/public/images/...)
- URLs (https://...)
- Package names (npm install react)
- Command line syntax (curl, npm, git commands)
- Fumadocs JSX components (<Cards>, <Card>, <Callout>, etc.)
- YAML frontmatter structure

EXAMPLE OF GOOD TRANSLATION:

Original:
> **Note**: This feature requires React 18 or higher.

Correct:
> **참고**: 이 기능은 React 18 이상이 필요합니다.

Original:
```bash
npm install react-query
```

Correct (unchanged):
```bash
npm install react-query
```

Now translate the following article:

---

{ARTICLE_CONTENT}

---

Provide the complete translated article with all Markdown formatting preserved.
```

**Special Considerations for Korean**:

### Technical Terms to Keep in English
- Framework/library names: React, Vue, Next.js, Express
- Programming concepts commonly used in English: hook, state, props, component
- Tools: npm, yarn, git, docker, kubernetes
- Abbreviations: API, REST, HTTP, JSON, SDK

### Standard Korean Translations
- function → 함수
- variable → 변수
- array → 배열
- object → 객체
- string → 문자열
- database → 데이터베이스
- server → 서버
- client → 클라이언트
- request → 요청
- response → 응답
- file → 파일
- folder → 폴더
- API → API (keep in English)
- endpoint → 엔드포인트 or 종단점

### Common Phrases
- "Let's get started" → 시작하겠습니다
- "For example" → 예를 들어
- "Note that" → 주의하세요 or 참고하세요
- "In this tutorial" → 이 튜토리얼에서는
- "Best practices" → 모범 사례
- "Common mistakes" → 일반적인 실수

### Korean Typography
- Use Korean punctuation: 。(optional, can use .)
- Spacing between Korean and English: React를 사용합니다 (space after English word)
- Use proper honorifics in formal tone

---

## Quality Assurance Checklist

After translating to any language, verify:

### Syntax Preservation
- [ ] All Markdown formatting is intact (`**bold**`, `*italic*`, `` `code` ``)
- [ ] Code blocks are completely unchanged
- [ ] Heading levels match original (H1, H2, H3)
- [ ] Lists are properly formatted (ordered and unordered)
- [ ] Links are functional and unchanged
- [ ] Image references are intact
- [ ] Fumadocs components are unchanged (`<Card>`, `<Callout>`, etc.)

### Content Quality
- [ ] Translation is technically accurate
- [ ] Technical terminology is appropriate for the language
- [ ] Examples make sense in cultural context
- [ ] Tone is professional and consistent
- [ ] Grammar and spelling are correct
- [ ] Formatting matches language conventions (e.g., French spacing)

### Technical Accuracy
- [ ] Code snippets are unchanged
- [ ] Package names are unchanged
- [ ] Commands are unchanged
- [ ] File paths are unchanged
- [ ] URLs are unchanged
- [ ] API names are unchanged

### Consistency
- [ ] Technical terms are translated consistently throughout
- [ ] Tone is consistent (formal/informal)
- [ ] Terminology matches industry standards for that language
- [ ] Formatting style is consistent

---

## Post-Translation Process

### Step 1: Automated Validation
Run basic checks:
```javascript
// Pseudo-code for validation
function validateTranslation(original, translated) {
  // Count code blocks - should be identical
  const originalCodeBlocks = countCodeBlocks(original);
  const translatedCodeBlocks = countCodeBlocks(translated);
  assert(originalCodeBlocks === translatedCodeBlocks);

  // Verify heading count
  const originalHeadings = countHeadings(original);
  const translatedHeadings = countHeadings(translated);
  assert(originalHeadings === translatedHeadings);

  // Check for broken Markdown
  assertNoMarkdownErrors(translated);

  // Verify Fumadocs components are unchanged
  assertComponentsUnchanged(original, translated);
}
```

### Step 2: Manual Review (Optional)
If time permits:
- Read the first 2-3 paragraphs for flow and accuracy
- Verify code examples make sense in context
- Check that technical terms are appropriately handled

### Step 3: User Feedback Loop
After publishing:
- Monitor user feedback on translations
- Track which languages have issues
- Update translation prompts based on common errors

---

## Common Translation Errors to Avoid

### ❌ Error 1: Translating Code
**Wrong**:
```python
# Chinese translation - WRONG
définir hello_world():
    print("你好世界")
```

**Correct**:
```python
def hello_world():
    print("Hello World")
```

### ❌ Error 2: Breaking Markdown Syntax
**Wrong**:
```markdown
**Remarque** :Cette fonctionnalité... (missing space after colon)
```

**Correct**:
```markdown
**Remarque** : Cette fonctionnalité... (proper French spacing)
```

### ❌ Error 3: Translating Component Names
**Wrong**:
```markdown
<Carte title="En savoir plus" href="/docs" />
```

**Correct**:
```markdown
<Card title="En savoir plus" href="/docs" />
```

### ❌ Error 4: Modifying Image Paths
**Wrong**:
```markdown
![Diagramme](/images/docs/react-guide/component-tree-1-zh.png)
```

**Correct**:
```markdown
![组件树示意图](/images/docs/react-guide/component-tree-1.png)
```

---

## Language-Specific Resources

### Chinese (zh)
- [Microsoft Language Portal](https://www.microsoft.com/en-us/language) - Technical term glossaries
- [Alibaba Translation Guide](https://www.alibabagroup.com) - Industry standards
- Common tech blogs: InfoQ China, CSDN

### French (fr)
- [Termium Plus](https://www.btb.termiumplus.gc.ca/) - Official terminology
- [Wikipédia Informatique](https://fr.wikipedia.org) - Technical terms
- Common tech blogs: Journal du Net, Développez.com

### Korean (ko)
- [Naver Dictionary](https://dict.naver.com) - Technical terms
- [Korean IT Terminology](http://word.tta.or.kr) - Official IT dictionary
- Common tech blogs: Naver D2, Kakao Tech

---

## Version History

- v1.0.0 (2025-11-15): Initial translation prompts
  - English (base language)
  - Chinese (Simplified)
  - French
  - Korean

**Last Updated**: 2025-11-15
