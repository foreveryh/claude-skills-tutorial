# 工作流程设计

## 整体流程概览

```
用户输入 URL
    ↓
1. 下载文章内容
    ↓
2. 提取并下载图片
    ↓
3. 分析文章并归类
    ↓
4. 多语言翻译
    ↓
5. 生成 MDX 文件
    ↓
6. 验证 MDX 语法
    ↓
7. 归档原始文件
    ↓
完成
```

## 详细步骤设计

### Step 1: 下载文章内容

**输入**: URL
**工具**: Jina API / Jina MCP
**输出**: Markdown 格式的文章内容

**处理逻辑**:
```
1. 调用 Jina API 获取文章
2. 检查返回状态
3. 提取文章元数据（标题、作者等）
4. 保存原始 Markdown
```

**错误处理**:
- URL 无效 → 提示用户
- 网络错误 → 重试 3 次
- 内容为空 → 提示用户检查 URL

---

### Step 2: 提取并下载图片

**输入**: Markdown 内容
**工具**: curl / wget / fetch
**输出**: 本地图片文件 + 更新的图片引用

**处理逻辑**:
```
1. 正则匹配所有图片 URL
   - ![alt](url)
   - <img src="url">
2. 遍历每个图片 URL
3. 下载图片到指定目录
4. 生成本地路径
5. 替换原文中的图片 URL
```

**图片命名规则** (待决策):
```
格式: {article-slug}-{index}.{ext}
示例: hello-world-1.png
```

**错误处理**:
- 图片下载失败 → 记录日志，保留原 URL
- 格式不支持 → 记录警告
- 文件名冲突 → 添加时间戳

---

### Step 3: 分析文章并归类

**输入**: 文章内容
**工具**: Claude 内容分析
**输出**: Category, Difficulty, Tags

**处理逻辑**:
```
1. 分析文章主题
2. 识别技术栈
3. 评估难度等级
4. 提取关键词作为 tags
5. (可选) 请求用户确认
```

**分类维度** (待确认):
- **Category**: frontend, backend, devops, database, etc.
- **Difficulty**: beginner, intermediate, advanced
- **Tags**: react, typescript, docker, etc.

---

### Step 4: 多语言翻译

**输入**: 处理后的文章内容
**工具**: Claude 翻译
**输出**: 多个语言版本的文章

**翻译语言** (待确认):
- [ ] 英文 (en)
- [ ] 中文 (zh)
- [ ] 日文 (ja)
- [ ] 其他?

**处理逻辑**:
```
FOR EACH 目标语言:
  1. 使用专业翻译 prompt
  2. 翻译文章内容
  3. 保持代码块不变
  4. 保持链接不变
  5. 保持 MDX 组件语法
  6. (可选) 人工审核
  7. 保存翻译版本
```

**质量控制**:
- MDX 语法验证
- 图片引用检查
- 链接有效性检查

---

### Step 5: 生成 MDX 文件

**输入**: 翻译后的内容 + 元数据
**工具**: 文件系统操作
**输出**: 多个 MDX 文件

**文件路径结构** (待确认):
```
选项A: 语言目录分离
content/docs/en/category/article-slug.mdx
content/docs/zh/category/article-slug.mdx

选项B: 文件名后缀
content/docs/category/article-slug.en.mdx
content/docs/category/article-slug.zh.mdx

选项C: 单目录 + frontmatter 标识
content/docs/category/article-slug.mdx (lang: en)
```

**Frontmatter 模板**:
```yaml
---
title: 文章标题
description: 文章描述
category: frontend
difficulty: intermediate
tags: [react, typescript]
lang: en
source_url: https://example.com/article
published_date: 2025-11-15
author: 原作者
---
```

---

### Step 6: 验证 MDX 语法

**输入**: 生成的 MDX 文件
**工具**: MDX 解析器 / Next.js build
**输出**: 验证报告

**验证项**:
- [ ] Frontmatter 格式正确
- [ ] MDX 语法无错误
- [ ] 组件引用正确
- [ ] 图片路径有效
- [ ] 链接格式正确

**失败处理**:
- 记录错误详情
- 提示用户手动修复
- (可选) 自动重试翻译

---

### Step 7: 归档原始文件

**输入**: 原始内容 + 图片
**工具**: 文件系统操作
**输出**: 归档目录 + 元数据索引

**归档结构** (待确认):
```
archive/
└── {article-slug}/
    ├── original.md          # 原始文章
    ├── metadata.json        # 元数据
    └── images/              # 原始图片
        ├── image1.png
        └── image2.jpg
```

**metadata.json 内容**:
```json
{
  "source_url": "https://example.com/article",
  "download_date": "2025-11-15T10:30:00Z",
  "title": "Article Title",
  "author": "Author Name",
  "languages": ["en", "zh", "ja"],
  "category": "frontend",
  "processed_files": [
    "content/docs/en/frontend/article-slug.mdx",
    "content/docs/zh/frontend/article-slug.mdx"
  ]
}
```

---

## 人工介入点 (待确认)

可能需要人工确认的步骤：

1. **文章归类** → AI 建议，用户确认
2. **翻译审核** → 翻译完成后，用户检查
3. **MDX 修复** → 验证失败时，用户手动修复

---

## 幂等性设计

**重复处理同一 URL 的策略**:

- 选项A: 检查是否已存在，存在则跳过
- 选项B: 提示用户选择：覆盖 / 跳过 / 创建新版本
- 选项C: 始终覆盖（最新优先）

**检查机制**:
```
1. 根据 source_url 查询 metadata.json
2. 如果找到记录：
   - 显示已存在的文件
   - 询问用户操作
3. 如果未找到：
   - 继续正常流程
```

---

## 进度追踪

**显示进度的方式**:

```
正在处理: https://example.com/article

✓ 1/7 下载文章内容
✓ 2/7 下载图片 (3/5 张)
→ 3/7 分析并归类...
  4/7 翻译为多语言 (0/4)
  5/7 生成 MDX 文件
  6/7 验证语法
  7/7 归档原始文件
```

---

## 批处理支持 (可选)

如果支持批量处理：

```
输入:
  - url1
  - url2
  - url3

处理策略:
  - 串行处理（避免并发冲突）
  - 记录每篇文章的处理结果
  - 失败不影响其他文章
  - 最后生成汇总报告
```

---

## 待办事项

- [ ] 确认多语言组织方式
- [ ] 确定图片存储路径
- [ ] 确定归档目录结构
- [ ] 设计 frontmatter 完整 schema
- [ ] 确认人工介入点
- [ ] 确定幂等性策略
