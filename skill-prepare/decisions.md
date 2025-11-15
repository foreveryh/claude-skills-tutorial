# 关键决策记录

> 本文档记录在 Skill 开发过程中做出的所有重要决策

## 决策模板

```
## [决策编号] 决策标题
- **日期**: YYYY-MM-DD
- **状态**: 待定 | 已决策 | 已实施 | 已废弃
- **决策者**: 用户 | 团队讨论
- **背景**: 为什么需要做这个决策？
- **选项**:
  - 选项A: 描述
  - 选项B: 描述
- **决策**: 选择了哪个选项？
- **理由**: 为什么选择这个选项？
- **影响**: 这个决策会影响什么？
```

---

## [D001] 文章下载方案选择
- **日期**: 2025-11-15
- **状态**: 待定
- **背景**: 需要从外部 URL 下载文章内容
- **选项**:
  - 选项A: 使用 Jina API (HTTP 调用)
  - 选项B: 使用 Jina MCP (Model Context Protocol)
- **决策**: 待定
- **理由**: 待讨论
- **影响**: 影响 Skill 的实现方式和依赖关系

---

## [D002] 多语言目标语言
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 需要将文章翻译为4种语言
- **选项**: 英文、中文、法语、韩语
- **决策**: 支持以下4种语言
  - 英文 (en)
  - 中文 (zh)
  - 法语 (fr)
  - 韩语 (ko)
- **理由**: 用户确认
- **影响**: 影响文件组织结构和翻译工作流，需要为每种语言创建相应的目录和配置

---

## [D003] 文章分类策略
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 需要将文章归类到合适的 category
- **选项**:
  - 选项A: 完全自动分类（基于内容分析）
  - 选项B: 半自动（AI 建议 + 人工确认）
  - 选项C: 完全人工选择
- **决策**: 选项A - 完全自动分类
- **理由**:
  - 教程规模 50-200 篇，手动分类工作量大
  - AI 可以基于内容准确判断分类
  - 用户可在发布后手动调整（如有需要）
- **影响**:
  - Skill 需要包含智能分类逻辑
  - 需要为每个 category 提供清晰的定义和识别特征

---

## [D004] 图片存储位置
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 下载的图片需要存储在项目中
- **选项**:
  - 选项A: 正式发布图片在 `/public/`
  - 选项B: 临时源文件在 `source/` 或归档目录
- **决策**: 双重存储策略
  - **正式图片**: `/public/images/docs/{article-slug}/`
  - **源文件归档**: 在归档目录下保存原始图片
- **理由**:
  - public 目录是 Next.js 静态资源标准位置
  - 源文件归档便于追溯和备份
- **影响**:
  - MDX 中引用: `/images/docs/{article-slug}/image.png`
  - 归档目录同时保留原始图片

---

## [D005] 归档目录结构
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 需要确定原文和图片的归档组织方式
- **选项**:
  - 选项A: 按日期组织 `/archive/2025-11-15/`
  - 选项B: 按分类组织 `/archive/category-name/`
  - 选项C: 按域名组织 `/archive/example.com/`
  - 选项D: 按月份/slug 组织 `/archive/2025-11/article-slug/`
- **决策**: 选项D - 按月份/slug 组织
- **目录结构**:
  ```
  archive/
  └── 2025-11/
      └── article-slug/
          ├── original.md          # 原始 Markdown
          ├── metadata.json        # 元数据
          └── images/              # 原始图片
              ├── image1.png
              └── image2.jpg
  ```
- **metadata.json 格式**:
  ```json
  {
    "source_url": "https://example.com/article",
    "download_date": "2025-11-15T10:30:00Z",
    "title": "Article Title",
    "author": "Author Name",
    "languages": ["en", "zh", "fr", "ko"],
    "category": "development",
    "difficulty": "intermediate",
    "tags": ["react", "typescript"],
    "published_files": {
      "en": "content/docs/en/development/article-slug.mdx",
      "zh": "content/docs/zh/development/article-slug.mdx",
      "fr": "content/docs/fr/development/article-slug.mdx",
      "ko": "content/docs/ko/development/article-slug.mdx"
    },
    "images": [
      {
        "original_url": "https://example.com/img1.png",
        "local_path": "public/images/docs/article-slug/component-tree-1.png",
        "archived_path": "archive/2025-11/article-slug/images/image1.png"
      }
    ]
  }
  ```
- **理由**:
  - 按月份归档方便管理和清理
  - Slug 唯一标识文章，便于查找
  - 同月文章聚合，易于浏览
  - 元数据 JSON 记录完整追溯信息
- **影响**:
  - Skill 需要获取当前年月（YYYY-MM 格式）
  - 创建归档目录时需要确保月份目录存在
  - 元数据需要记录完整的文件路径映射

---

## [D006] 翻译质量控制流程
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 需要确定翻译后的质量控制流程
- **选项**:
  - 选项A: 翻译后人工审核
  - 选项B: 自动翻译自动发布
- **决策**: 选项B - 自动翻译自动发布
- **理由**: 用户确认不需要人工审核，提高效率
- **影响**: 简化工作流，但需要高质量的翻译 prompt 和充分的测试

---

## [D007] 翻译提示词管理
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 翻译提示词如何管理和存储
- **选项**:
  - 选项A: 每次翻译时动态生成
  - 选项B: 提前写入 skill 作为参考材料
- **决策**: 选项B - 提前写入 skill
- **理由**: 用户确认，提示词会提前写入 skill，不需要保存版本记录
- **影响**: Skill 需要包含针对每种语言优化的翻译 prompt

---

## [D008] 图片命名规则
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 需要确定下载图片的命名规则
- **选项**:
  - 选项A: 保持原文件名
  - 选项B: 使用递增序号
  - 选项C: 使用内容哈希
- **决策**: 使用描述性名称 + 递增序号
  - 格式: `{descriptive-name}-{index}.{ext}`
  - 示例: `component-tree-1.png`, `data-flow-2.jpg`
- **理由**:
  - 描述性名称提高可读性和可维护性
  - 递增序号避免冲突
  - 便于人工查看和管理
- **影响**: 需要从原文件名或上下文提取描述性名称

---

## [D009] 图片下载失败处理
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 图片下载可能失败（403、404、网络错误等）
- **选项**:
  - 选项A: 重试多次直到成功
  - 选项B: 重试一次后放弃
  - 选项C: 立即放弃
- **决策**: 选项B - 重试一次，再失败就放弃
- **理由**: 平衡可靠性和效率，避免长时间阻塞
- **影响**:
  - 失败的图片保留原始 URL
  - 在日志中记录失败信息
  - 不阻止整体流程继续

---

## [D010] 分类方案选择
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 需要确定教程的分类体系
- **选项**:
  - 方案A: 精简分类（6大类）
  - 方案B: 标准分类（8大类）
  - 方案C: 完整分类（10大类）
- **决策**: 方案B - 标准分类（8大类）
- **理由**:
  - 教程规模 50-200 篇，适合标准分类
  - 平衡覆盖面和精细度
  - 包含技术和非技术类别（Skills 面向所有用户）
- **影响**:
  - 确定了 8 个主要 categories
  - 需要为每个 category 编写识别规则

---

## [D011] Categories 定义
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 基于方案 B，定义具体的分类类别
- **决策**: 确定以下 8 个 categories
  1. **development** - Development & Code (开发编程)
     - 编程语言、框架、工具、测试、Git
  2. **data** - Data & Analytics (数据分析)
     - 数据处理、可视化、统计分析、数据库
  3. **ai-ml** - AI & Machine Learning (AI 机器学习)
     - 机器学习、深度学习、NLP、计算机视觉
  4. **design** - Design & Creative (设计创意)
     - UI/UX、视觉设计、生成艺术、品牌
  5. **content** - Content & Writing (内容写作)
     - 写作、研究、文档、媒体处理
  6. **business** - Business & Marketing (商业营销)
     - 营销策略、竞品分析、需求生成、管理
  7. **devops** - DevOps & Infrastructure (运维基础设施)
     - CI/CD、容器、云服务、监控
  8. **security** - Security & Testing (安全测试)
     - 安全分析、渗透测试、调试、质量保证
- **理由**:
  - 基于社区主流分类标准
  - 覆盖技术和非技术领域
  - 符合 Claude Skills 的多元化应用场景
- **影响**:
  - Frontmatter 的 category 字段使用这 8 个值
  - 需要在 meta.json 中创建对应分类目录

---

## [D012] 难度等级定义
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 需要为教程定义难度等级
- **选项**:
  - 选项A: beginner/intermediate/advanced
  - 选项B: 1-5 星级
  - 选项C: 不设置难度
- **决策**: 选项A - beginner/intermediate/advanced
- **理由**:
  - 三级分类简单清晰
  - 符合行业标准
  - AI 容易判断
- **影响**:
  - Frontmatter 增加 difficulty 字段
  - Skill 需要包含难度判断逻辑

---

## [D013] 标签体系
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 是否实现标签系统进行更细粒度分类
- **选项**:
  - 选项A: 实现标签体系
  - 选项B: 不使用标签
- **决策**: 选项A - 实现标签体系
- **理由**:
  - Fumadocs 支持通过 frontmatter schema 扩展添加 tags
  - 标签提供更灵活的分类和搜索
  - 技术栈标签帮助用户快速定位
- **影响**:
  - Frontmatter 增加 tags 字段（字符串数组）
  - Skill 需要从文章中提取相关技术栈标签
  - 示例标签：react, typescript, python, docker, api

---

## [D014] MDX 组件使用规范
- **日期**: 2025-11-15
- **状态**: ✅ 已决策
- **背景**: 需要确定 Skill 生成的 MDX 文件中可以使用哪些组件
- **决策**: 使用 Fumadocs 内置组件，禁止自定义实现
- **可用组件清单**:
  - **内容组织**: Cards, Callout, Tabs, Steps, Accordion
  - **代码展示**: Code Block (默认), Dynamic Code Block
  - **文件结构**: Files (File Tree)
  - **媒体增强**: ImageZoom
  - **其他**: Banner, Type Table, Auto Type Table, Inline TOC, GitHub Info
- **核心规则**:
  1. ❌ 永远不要自己实现组件
  2. ✅ 优先使用默认组件（Cards, Callout, Code Block）
  3. ✅ 复杂内容使用 Tabs, Steps, Files
  4. ✅ 所有图片使用 ImageZoom（替换默认 img）
- **理由**:
  - Fumadocs 提供 15+ 个专业组件
  - 避免重复造轮子和样式不一致
  - 组件经过优化，性能和可访问性有保证
- **影响**:
  - Skill 需要了解所有可用组件
  - 转换原文时智能选择合适组件
  - 详见: `fumadocs-components.md`

---

## 决策待办清单

- [ ] D001: 文章下载方案选择（低优先级，可在实现时决定）
- [x] D002: 多语言目标语言 ✅
- [x] D003: 文章分类策略 ✅
- [x] D004: 图片存储位置 ✅
- [x] D005: 归档目录结构 ✅
- [x] D006: 翻译质量控制流程 ✅
- [x] D007: 翻译提示词管理 ✅
- [x] D008: 图片命名规则 ✅
- [x] D009: 图片下载失败处理 ✅
- [x] D010: 分类方案选择 ✅
- [x] D011: Categories 定义 ✅
- [x] D012: 难度等级定义 ✅
- [x] D013: 标签体系 ✅
- [x] D014: MDX 组件使用规范 ✅

**完成度**: 13/14 (93%) ✅ 核心决策全部完成！
