# Fumadocs 页面约定详解

> 基于官方文档：https://fumadocs.dev/docs/ui/page-conventions

## 📁 文件组织与 Slug 生成

### Slug 生成规则

文件路径自动生成页面 slug（相对于 content 文件夹）：

```
./dir/page.mdx      → ['dir', 'page']    → URL: /docs/dir/page
./dir/index.mdx     → ['dir']            → URL: /docs/dir
./index.mdx         → []                 → URL: /docs
```

### 文件夹分组（Folder Groups）

使用括号包裹文件夹名，可以在不影响子文件 slug 的情况下组织文件：

```
./(group-name)/page.mdx  → ['page']  → URL: /docs/page
```

**用途**：逻辑分组但不想增加 URL 层级

### 根文件夹（Root Folders）

通过在文件夹中创建 `meta.json` 并设置 `root: true`，将文件夹标记为独立导航区域：

```json
{
  "title": "API Reference",
  "root": true
}
```

**效果**：该文件夹在导航中独立显示，只展示其包含的内容

---

## 📝 Frontmatter Schema

### 必需字段

```yaml
---
title: 页面标题        # ✅ 必需
---
```

### 常用字段

```yaml
---
title: 页面标题
description: 页面描述
icon: HomeIcon        # 侧边栏图标名称
full: false           # 是否全宽显示
---
```

### 自定义 Frontmatter

在 `source.config.ts` 中可以自定义 schema：

```typescript
import { z } from 'zod';
import { frontmatterSchema } from 'fumadocs-mdx/config';

export const docs = defineDocs({
  docs: {
    schema: frontmatterSchema.extend({
      // 添加自定义字段
      category: z.string().optional(),
      difficulty: z.enum(['beginner', 'intermediate', 'advanced']).optional(),
      tags: z.array(z.string()).optional(),
      author: z.string().optional(),
      published_date: z.string().optional(),
      source_url: z.string().url().optional(),
      lang: z.string().optional(),
    }),
  },
});
```

---

## 🗂️ Meta 文件（meta.json）

### 基本用途

在任意文件夹创建 `meta.json` 来自定义外观和排序：

```json
{
  "title": "显示名称",
  "icon": "MyIcon",
  "pages": ["index", "getting-started", "advanced"],
  "defaultOpen": true
}
```

### Pages 数组控制

`pages` 数组用于控制项目的顺序和包含关系：

**基本用法**：
```json
{
  "pages": ["index", "getting-started", "configuration"]
}
```

**特殊操作符**：

1. **分隔符**：`---Label---`
   ```json
   {
     "pages": ["index", "---Basics---", "tutorial", "---Advanced---", "api"]
   }
   ```

2. **通配符**：`...`
   ```json
   {
     "pages": ["index", "..."]  // index 在前，其他按字母顺序
   }
   ```

3. **反向排序**：`z...a`
   ```json
   {
     "pages": ["z...a"]  // 所有项按字母逆序
   }
   ```

4. **排除项**：`!item`
   ```json
   {
     "pages": ["...", "!internal"]  // 包含所有，但排除 internal
   }
   ```

### Root 标记

```json
{
  "title": "Documentation",
  "root": true
}
```

---

## 🌐 国际化（i18n）路由

Fumadocs 支持两种 i18n 文件组织方式：

### 方式 1: 目录分离（推荐）

```
content/docs/
├── en/
│   ├── index.mdx
│   └── getting-started.mdx
├── zh/
│   ├── index.mdx
│   └── getting-started.mdx
└── fr/
    ├── index.mdx
    └── getting-started.mdx
```

**URL 结构**：
- `/docs/getting-started` (默认语言 en)
- `/zh/docs/getting-started`
- `/fr/docs/getting-started`

### 方式 2: 点号标记

```
content/docs/
├── index.mdx
├── index.zh.mdx
├── index.fr.mdx
├── getting-started.mdx
├── getting-started.zh.mdx
└── getting-started.fr.mdx
```

**我们的选择**：方式 1 - 目录分离（更清晰，易维护）

---

## 🎨 图标使用

### Frontmatter 中的图标

```yaml
---
icon: HomeIcon
---
```

### Meta.json 中的图标

```json
{
  "icon": "BookOpen"
}
```

**注意**：需要确保图标在项目中已注册（通常通过 lucide-icons 插件）

---

## 📂 推荐的文件结构

### 单语言项目

```
content/docs/
├── index.mdx
├── meta.json
├── getting-started/
│   ├── index.mdx
│   ├── installation.mdx
│   └── meta.json
├── guides/
│   ├── meta.json
│   ├── basic-usage.mdx
│   └── advanced-topics.mdx
└── api-reference/
    ├── meta.json (root: true)
    └── ...
```

### 多语言项目（我们的方案）

```
content/docs/
├── en/
│   ├── index.mdx
│   ├── meta.json
│   ├── frontend/
│   │   ├── meta.json
│   │   ├── react-basics.mdx
│   │   └── vue-intro.mdx
│   └── backend/
│       └── ...
├── zh/
│   ├── index.mdx
│   ├── meta.json
│   └── ... (相同结构)
├── fr/
│   └── ... (相同结构)
└── ko/
    └── ... (相同结构)
```

---

## 🖼️ 图片处理约定

### 图片存储位置

```
public/
└── images/
    └── docs/
        ├── react-basics/
        │   ├── component-tree-1.png
        │   └── hooks-flow-2.png
        └── vue-intro/
            └── reactivity-1.png
```

### MDX 中引用

```mdx
![Component Tree](/images/docs/react-basics/component-tree-1.png)
```

**注意**：`/public/` 目录在引用时不需要包含在路径中

---

## 📋 Skill 实现清单

基于以上约定，我们的 Skill 需要：

- [x] ✅ 理解 slug 生成规则
- [x] ✅ 使用目录分离的 i18n 方式
- [ ] ⏳ 生成符合规范的 frontmatter
- [ ] ⏳ 为每个分类创建 meta.json
- [ ] ⏳ 按照约定组织图片文件
- [ ] ⏳ 确保所有语言版本的目录结构一致
- [ ] ⏳ 使用合适的图标（可选）

---

## 🎯 关键要点总结

1. **Title 是必需的** - 每个 MDX 文件必须有 title frontmatter
2. **Index.mdx 简化 URL** - 使用 index.mdx 可以缩短 URL
3. **Meta.json 控制导航** - 用于自定义显示和排序
4. **i18n 目录分离** - 我们使用 `en/`, `zh/`, `fr/`, `ko/` 结构
5. **图片在 public** - 静态资源放在 `/public/images/docs/`
6. **Slug 自动生成** - 从文件路径自动生成，保持一致性很重要
