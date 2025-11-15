# 最终分类标准定义

> 基于用户确认和社区研究的最终决策

## 核心决策

- **分类方案**: 方案 B - 标准分类（8大类）
- **教程规模**: 50-200 篇（中型）
- **难度等级**: beginner / intermediate / advanced
- **标签体系**: 启用（Fumadocs 支持）
- **分类方式**: AI 自动分类

---

## 📁 Categories 定义（8大类）

### 1. development
**名称**: Development & Code (开发编程)

**描述**: 软件开发、编程语言、框架和工具

**包含内容**:
- 编程语言（JavaScript, Python, Go, Rust, etc.）
- 前端框架（React, Vue, Svelte, etc.）
- 后端框架（Node.js, Django, FastAPI, etc.）
- 开发工具（VS Code, Git, npm, etc.）
- 测试框架（Jest, Pytest, Playwright, etc.）
- API 开发与集成

**示例 Skills**: artifacts-builder, TDD, code-review, Git workflows

**识别关键词**: code, programming, framework, library, API, development, build

---

### 2. data
**名称**: Data & Analytics (数据分析)

**描述**: 数据处理、分析、可视化和数据库

**包含内容**:
- 数据处理（Pandas, NumPy, data cleaning）
- 数据可视化（D3.js, Matplotlib, charts）
- 数据库（SQL, NoSQL, PostgreSQL, MongoDB）
- 数据分析工具（Excel, Jupyter, analytics）
- 统计分析和报表

**示例 Skills**: CSV analyzer, D3 visualization, xlsx, database queries

**识别关键词**: data, analytics, visualization, database, SQL, charts, statistics

---

### 3. ai-ml
**名称**: AI & Machine Learning (AI 机器学习)

**描述**: 人工智能、机器学习和深度学习

**包含内容**:
- 机器学习（supervised, unsupervised learning）
- 深度学习（neural networks, TensorFlow, PyTorch）
- 自然语言处理（NLP, transformers, LLMs）
- 计算机视觉（image recognition, object detection）
- AI 应用开发（chatbots, AI agents）
- Model training and deployment

**示例 Skills**: LLM integration, model training, AI automation

**识别关键词**: AI, machine learning, ML, deep learning, neural network, NLP, GPT, model, training

---

### 4. design
**名称**: Design & Creative (设计创意)

**描述**: UI/UX 设计、视觉设计和创意工作

**包含内容**:
- UI/UX 设计（Figma, Sketch, prototyping）
- 视觉设计（graphics, layouts, typography）
- 生成艺术（algorithmic art, p5.js）
- 品牌设计（brand guidelines, themes）
- 图片处理和编辑

**示例 Skills**: algorithmic-art, canvas-design, theme-factory, brand-guidelines

**识别关键词**: design, UI, UX, visual, creative, art, graphics, Figma, branding

---

### 5. content
**名称**: Content & Writing (内容写作)

**描述**: 内容创作、写作、研究和文档

**包含内容**:
- 技术写作（documentation, technical writing）
- 内容创作（blog posts, articles, copywriting）
- 研究和引用（research, citations）
- 媒体处理（video, audio, transcripts）
- 文档生成（docx, pdf, markdown）

**示例 Skills**: article-extractor, youtube-transcript, docx, content-research

**识别关键词**: writing, content, documentation, article, blog, media, transcript, document

---

### 6. business
**名称**: Business & Marketing (商业营销)

**描述**: 商业策略、营销和管理

**包含内容**:
- 营销策略（marketing campaigns, demand generation）
- 竞品分析（competitive analysis, market research）
- 项目管理（project planning, collaboration）
- 商业分析（business intelligence, metrics）
- 客户沟通（CRM, customer engagement）

**示例 Skills**: competitive-analysis, lead-generation, internal-comms, meeting-analysis

**识别关键词**: business, marketing, strategy, management, sales, customer, campaign, analytics

---

### 7. devops
**名称**: DevOps & Infrastructure (运维基础设施)

**描述**: 运维、部署、基础设施和云服务

**包含内容**:
- CI/CD（continuous integration, deployment pipelines）
- 容器化（Docker, Kubernetes, containerization）
- 云服务（AWS, GCP, Azure, cloud infrastructure）
- 监控和日志（monitoring, logging, observability）
- 自动化运维（automation, infrastructure as code）

**示例 Skills**: AWS CDK, Docker workflows, deployment automation

**识别关键词**: DevOps, CI/CD, Docker, Kubernetes, cloud, AWS, deployment, infrastructure, monitoring

---

### 8. security
**名称**: Security & Testing (安全测试)

**描述**: 安全分析、测试和质量保证

**包含内容**:
- 安全分析（security analysis, vulnerability assessment）
- 渗透测试（penetration testing, ethical hacking）
- 自动化测试（automated testing, test automation）
- 调试和故障排除（debugging, troubleshooting）
- 质量保证（QA, quality assurance）

**示例 Skills**: digital-forensics, fuzz-testing, systematic-debugging, webapp-testing

**识别关键词**: security, testing, QA, debugging, vulnerability, penetration, audit, test automation

---

## 🏷️ 标签体系（Tags）

### 标签类型

#### 技术栈标签
- **前端**: `react`, `vue`, `svelte`, `angular`, `nextjs`, `tailwind`
- **后端**: `nodejs`, `python`, `go`, `rust`, `django`, `fastapi`
- **数据库**: `postgresql`, `mongodb`, `redis`, `mysql`, `sqlite`
- **工具**: `git`, `docker`, `kubernetes`, `vscode`, `webpack`
- **AI/ML**: `tensorflow`, `pytorch`, `openai`, `llm`, `transformers`
- **云服务**: `aws`, `gcp`, `azure`, `vercel`, `netlify`

#### 应用场景标签
- `api`, `cli`, `web`, `mobile`, `desktop`
- `automation`, `monitoring`, `documentation`
- `real-time`, `serverless`, `microservices`

#### Skills 特定标签
- `claude-code`, `claude-api`, `mcp`, `skills`

### 标签使用规则

1. **数量**: 每篇文章 3-7 个标签
2. **优先级**:
   - 主要技术栈（必需）
   - 相关工具/框架
   - 应用场景
3. **命名**: 全小写，使用连字符（如 `machine-learning`）

---

## 📊 难度等级定义

### beginner (初级)
**特征**:
- 介绍性内容，概念解释
- 基础教程，入门指南
- 步骤简单，无需深厚背景知识
- 示例代码简洁明了

**示例**: "Getting Started with React", "Python Basics", "Git for Beginners"

### intermediate (中级)
**特征**:
- 需要一定基础知识
- 涉及多步骤工作流
- 包含最佳实践和常见模式
- 有一定技术深度

**示例**: "Building REST APIs with FastAPI", "React State Management", "Docker Compose Guide"

### advanced (高级)
**特征**:
- 需要专业知识
- 复杂架构或系统设计
- 性能优化、安全强化
- 多工具/技术集成

**示例**: "Microservices Architecture", "ML Model Optimization", "Advanced Security Patterns"

---

## 🤖 自动分类逻辑

### 分类判断流程

```
1. 提取文章关键信息
   - 标题
   - 描述/摘要
   - 主要关键词
   - 代码示例（如有）

2. 匹配 category
   - 基于识别关键词
   - 分析内容主题
   - 确定主要领域
   - 输出最匹配的 category

3. 判断 difficulty
   - 分析内容深度
   - 评估技术复杂度
   - 检查前置知识要求
   - 输出 beginner/intermediate/advanced

4. 提取 tags
   - 识别技术栈（框架、语言、工具）
   - 提取应用场景
   - 选择 3-7 个最相关标签
```

### 边界情况处理

**跨类别内容**:
- 选择最主要的类别
- 通过 tags 补充其他相关领域

**难以分类**:
- 默认归入 `content` 或 `business`
- 使用 tags 提供更多上下文

---

## 📋 Frontmatter 完整 Schema

```yaml
---
title: "文章标题"                    # 必需
description: "文章描述"              # 推荐
lang: en                             # 语言标识 (en/zh/fr/ko)
category: development                # 8 个 categories 之一
difficulty: intermediate             # beginner/intermediate/advanced
tags:                                # 3-7 个标签
  - react
  - typescript
  - api
source_url: "https://example.com"   # 原文链接
published_date: "2025-11-15"        # 发布日期
author: "Author Name"                # 原作者（可选）
---
```

---

## 🗂️ 目录结构示例

```
content/docs/
├── en/
│   ├── index.mdx
│   ├── meta.json
│   ├── development/
│   │   ├── meta.json
│   │   ├── react-hooks-guide.mdx
│   │   └── building-rest-apis.mdx
│   ├── data/
│   │   ├── meta.json
│   │   └── data-visualization-d3.mdx
│   ├── ai-ml/
│   │   └── intro-to-llms.mdx
│   ├── design/
│   ├── content/
│   ├── business/
│   ├── devops/
│   └── security/
├── zh/
│   └── ... (相同结构)
├── fr/
└── ko/
```

---

## ✅ 实施清单

- [x] 定义 8 个 categories
- [x] 为每个 category 提供识别关键词
- [x] 定义 3 个难度等级
- [x] 设计标签体系
- [x] 制定自动分类逻辑
- [x] 完善 Frontmatter schema
- [ ] 在 source.config.ts 中实现 schema 扩展
- [ ] 为每个 category 创建目录和 meta.json
- [ ] 在 Skill 中实现分类算法

---

**维护者**: Claude
**创建日期**: 2025-11-15
**基于**: 用户确认 + 社区研究 (category-research.md)
