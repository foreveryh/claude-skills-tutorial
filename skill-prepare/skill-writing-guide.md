# Skill 编写指南（基于官方最佳实践）

> 基于 Anthropic 官方 skill-creator 和 template-skill 的分析总结

## 核心原则

### 1. 渐进式披露（Progressive Disclosure）

**三层信息加载机制**：
- **第1层 - 元数据**：~100 词（name + description），始终可用
- **第2层 - SKILL.md 主体**：<5k 词，技能触发时加载
- **第3层 - 捆绑资源**：按需加载（scripts, references, assets）

**目的**：保持上下文高效的同时维持可发现性

### 2. 自包含结构（Self-Contained）

每个 Skill 是一个独立目录，包含：
```
skill-name/
├── SKILL.md              # 必需 - 主要指令文件
├── scripts/              # 可选 - 可执行脚本
├── references/           # 可选 - 详细文档
└── assets/               # 可选 - 模板、素材
```

### 3. 内容策略

**黄金规则**：*"Information should live in either SKILL.md or reference files, not both."*

- **SKILL.md**：简洁的指令和工作流程（<5k 词）
- **references/**：详细信息、API 文档、schema 定义
- **避免重复**：详细内容放 references/，SKILL.md 保持精简

---

## 文件结构详解

### SKILL.md 结构

```markdown
---
name: skill-name
description: What the skill does and when Claude should use it
---

# Skill Instructions

[核心指令内容]

## Examples

[具体使用示例]

## Guidelines

[最佳实践和约束]
```

#### YAML Frontmatter（必需）

**必需字段**：
- `name`: 唯一标识符（小写，用连字符分隔）
- `description`: 技能功能和使用时机

**关键引用**：*"The name and description in YAML frontmatter determine when Claude will use the skill."*

#### Markdown 内容

包含指令、示例和指南，Claude 在技能激活时遵循这些内容。

### scripts/ 目录（可选）

**用途**：确定性或重复性任务的可执行代码

**示例场景**：
- PDF 旋转
- 图片批量处理
- 文件格式转换
- 自动化工作流脚本

### references/ 目录（可选）

**用途**：详细文档，按需加载到上下文

**适用内容**：
- API 文档和 schema
- 公司政策和规范
- 技术参考手册
- 复杂的配置说明

**优势**：避免 SKILL.md 过于臃肿，按需加载减少 token 消耗

### assets/ 目录（可选）

**用途**：输出中使用的文件

**示例内容**：
- 模板文件
- 样板代码
- 品牌素材（logo, 图标）
- 字体文件

---

## 编写风格指南

### 1. 语言模式

**✅ 推荐：使用祈使句/不定式**
```markdown
To accomplish X, do Y.
Create a new file using the following template.
Extract the main content from the article.
```

**❌ 避免：使用第二人称**
```markdown
❌ You should create a new file.
❌ You need to extract the main content.
```

**原因**：保持 AI 消费的清晰度，建立一致的程序性语言

### 2. 行为锚定（Behavioral Anchoring）

在 description 中明确说明何时应该激活技能：

```yaml
description: >
  This skill should be used when the user wants to import external articles
  into a Fumadocs project with multi-language translation and auto-classification.
```

使用第三人称框架描述触发条件。

### 3. 诊断式提问

在程序步骤中使用问题引导用户提供必要信息：

```markdown
1. Ask the user: "What is the URL of the article you want to import?"
2. Ask: "Which languages should I translate to? (default: en, zh, fr, ko)"
3. Confirm: "Should I download all images? (yes/no)"
```

这些问题帮助在设计开始前提取具体用例。

---

## 创建流程（6步）

### Step 1: 理解用例（Understand Use Cases）

通过示例提取具体需求：
- 用户想要完成什么？
- 有哪些具体示例？
- 边界条件是什么？

### Step 2: 规划可复用内容（Plan Reusable Contents）

确定需要哪些资源类型：
- **Scripts**：重复性任务？
- **References**：复杂文档？
- **Assets**：模板素材？

### Step 3: 初始化（Initialize）

使用模板创建基础结构：
```bash
# 官方使用 init_skill.py
python init_skill.py --name my-skill
```

### Step 4: 编辑内容（Edit SKILL.md）

- 使用祈使语言
- 保持简洁（<5k 词）
- 避免重复信息
- 明确工作流程

### Step 5: 打包和验证（Package & Validate）

```bash
# 官方使用 package_skill.py
python package_skill.py --skill my-skill
```

验证：
- YAML frontmatter 格式正确
- 文件结构完整
- references/ 可被正确引用

### Step 6: 迭代（Iterate）

基于实际使用反馈改进：
- 指令是否清晰？
- 是否需要更多示例？
- 是否需要额外的 references？

---

## 资源类型详解

### Scripts（脚本）

**特征**：
- 确定性任务
- 可重复执行
- 减少 AI 幻觉风险

**命名约定**：
- `init.sh` - 初始化脚本
- `process.py` - 主处理脚本
- `validate.js` - 验证脚本

### References（参考文档）

**特征**：
- 详细信息
- 按需加载
- 避免 SKILL.md 膨胀

**组织方式**：
```
references/
├── api-schema.json
├── translation-prompts.md
├── classification-rules.md
└── fumadocs-guide.md
```

### Assets（素材）

**特征**：
- 直接用于输出
- 模板化内容
- 品牌一致性

**示例**：
```
assets/
├── templates/
│   └── article-template.mdx
├── images/
│   └── placeholder.png
└── configs/
    └── default-frontmatter.yaml
```

---

## 最佳实践总结

### ✅ DO（推荐做法）

1. **保持 SKILL.md 简洁**：<5k 词，核心指令为主
2. **使用 references/**：详细信息放到单独文件
3. **清晰的 description**：明确说明何时使用该技能
4. **提供示例**：具体的使用场景和预期输出
5. **充分测试**：在真实环境中测试后再发布
6. **学习现有技能**：研究官方示例，理解模式

### ❌ DON'T（避免做法）

1. **重复信息**：SKILL.md 和 references/ 不要重复内容
2. **使用第二人称**：避免 "You should..." 模式
3. **过于冗长**：不要把所有细节都放 SKILL.md
4. **模糊的 description**：不要写泛泛的描述
5. **缺少示例**：不要只有抽象指令，没有具体示例
6. **未经测试**：不要发布未测试的技能

---

## 命名约定

### Skill Name

**格式**：小写，用连字符分隔空格

**✅ 好示例**：
- `article-importer`
- `fumadocs-translator`
- `multi-language-publisher`

**❌ 差示例**：
- `ArticleImporter`（驼峰命名）
- `article_importer`（下划线）
- `Article Importer`（空格）

### 目录结构

```
article-importer/
├── SKILL.md
├── scripts/
│   ├── download-article.sh
│   ├── process-images.py
│   └── generate-mdx.js
├── references/
│   ├── translation-prompts.md
│   ├── category-keywords.json
│   └── fumadocs-components.md
└── assets/
    └── frontmatter-template.yaml
```

---

## 技能分类

根据官方示例，技能可以分为：

1. **Creative**（创意）- 设计、艺术、生成
2. **Development**（开发）- 编程、测试、构建
3. **Enterprise**（企业）- 商业、管理、协作
4. **Data**（数据）- 分析、可视化、处理
5. **Content**（内容）- 写作、研究、文档

---

## 实战示例框架

### 简单 Skill（无额外资源）

```markdown
---
name: simple-formatter
description: Format text according to specific style guidelines
---

# Simple Formatter

## Instructions

1. Ask user for the text to format
2. Apply the following rules:
   - Capitalize first letter of each sentence
   - Remove extra whitespace
   - Add proper punctuation
3. Return formatted text

## Examples

**Input**: "hello world  this is a test"
**Output**: "Hello world. This is a test."
```

### 复杂 Skill（带资源）

```markdown
---
name: article-importer
description: >
  Import external articles into Fumadocs with multi-language translation,
  auto-classification, and image processing. Use when user provides an article
  URL and wants to publish it in multiple languages.
---

# Article Importer

## Overview

This skill automates importing external articles into a Fumadocs project.

## Prerequisites

- Fumadocs project initialized
- Jina API access (or Jina MCP configured)
- curl installed for image downloads

## Workflow

1. **Download Article**
   - Use Jina API to fetch article content
   - Extract title, author, publish date, main content

2. **Process Images**
   - Run `scripts/download-images.sh`
   - Save to `/public/images/docs/{article-slug}/`
   - Apply naming convention: `{descriptive-name}-{index}.{ext}`

3. **Classify Article**
   - Load `references/classification-rules.md`
   - Determine category (8 categories)
   - Assign difficulty level (beginner/intermediate/advanced)
   - Extract 3-7 tags

4. **Translate Content**
   - Load `references/translation-prompts.md`
   - Translate to en, zh, fr, ko
   - Generate MDX files for each language

5. **Generate MDX Files**
   - Use `assets/frontmatter-template.yaml`
   - Apply Fumadocs components (see `references/fumadocs-components.md`)
   - Save to `content/docs/{lang}/{category}/{slug}.mdx`

6. **Archive Original**
   - Save to `archive/{YYYY-MM}/{slug}/`
   - Generate `metadata.json` with full traceability

## Error Handling

- Image download failures: Retry once, then skip
- Translation errors: Log and continue with available languages
- Classification uncertainty: Default to "content" category

## Examples

[Include specific examples of article imports]
```

---

## 参考资源

### 官方文档
- [Anthropic Skills Repository](https://github.com/anthropics/skills)
- [skill-creator](https://github.com/anthropics/skills/tree/main/skill-creator)
- [template-skill](https://github.com/anthropics/skills/tree/main/template-skill)

### 社区示例
- [awesome-claude-skills (travisvn)](https://github.com/travisvn/awesome-claude-skills)
- [awesome-claude-skills (ComposioHQ)](https://github.com/ComposioHQ/awesome-claude-skills)

---

## 检查清单

创建 Skill 前，确认：

- [ ] ✅ YAML frontmatter 包含 name 和 description
- [ ] ✅ description 明确说明何时使用该技能
- [ ] ✅ SKILL.md 保持简洁（<5k 词）
- [ ] ✅ 详细信息放在 references/ 中
- [ ] ✅ 使用祈使句，避免第二人称
- [ ] ✅ 提供具体示例
- [ ] ✅ 包含错误处理说明
- [ ] ✅ 文件结构清晰（scripts/, references/, assets/ 按需使用）
- [ ] ✅ 在真实环境中充分测试

---

**创建日期**: 2025-11-15
**基于**: Anthropic skill-creator, template-skill, README.md
**维护者**: Claude
