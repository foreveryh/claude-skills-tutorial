# Fumadocs 项目结构分析

## 当前项目结构

```
claude-skills-tutorial/
├── app/                      # Next.js App Router
├── content/
│   └── docs/                 # 文档内容目录
│       ├── index.mdx         # 示例：首页
│       └── test.mdx          # 示例：测试页面
├── lib/                      # 工具函数库
├── mdx-components.tsx        # MDX 组件定义
├── next.config.mjs           # Next.js 配置
├── package.json              # 依赖管理
├── source.config.ts          # Fumadocs 配置
└── tsconfig.json             # TypeScript 配置
```

## Fumadocs 配置（source.config.ts）

```typescript
export const docs = defineDocs({
  dir: 'content/docs',        // 文档根目录
  docs: {
    schema: frontmatterSchema, // Frontmatter 验证模式
    postprocess: {
      includeProcessedMarkdown: true,
    },
  },
  meta: {
    schema: metaSchema,        // meta.json 验证模式
  },
});
```

## MDX 文件格式示例

### 基本格式

```mdx
---
title: Hello World
description: Your first document
---

# 正文内容

## 二级标题

普通文本...
```

### 支持的 MDX 组件

从示例文件中发现的组件：

1. **Cards 组件**
   ```mdx
   <Cards>
     <Card title="标题" href="链接" />
   </Cards>
   ```

2. **代码块**
   ```mdx
   ```js
   console.log('Hello World');
   ```
   ```

## 待探索的内容

- [ ] 是否有 `meta.json` 文件？
- [ ] 多语言支持的目录结构
- [ ] 图片资源的存放位置
- [ ] 其他可用的 MDX 组件
- [ ] Frontmatter 的完整 schema 定义

## 参考链接

- Fumadocs 官方文档: https://fumadocs.dev
- MDX Collections: https://fumadocs.dev/docs/mdx/collections
