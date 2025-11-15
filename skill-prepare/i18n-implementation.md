# Fumadocs 国际化实现方案

## 基本信息

- **目标语言**: 英文 (en), 中文 (zh), 法语 (fr), 韩语 (ko)
- **参考文档**: https://fumadocs.dev/docs/ui/internationalization/next

## Fumadocs i18n 工作原理

根据官方文档和社区最佳实践：

### 1. 配置定义

使用 `fumadocs-core/i18n` 的 `defineI18n` 函数定义配置：

```typescript
// lib/i18n.ts
import { defineI18n } from 'fumadocs-core/i18n';

export const i18n = defineI18n({
  defaultLanguage: 'en',
  languages: ['en', 'zh', 'fr', 'ko'],
});
```

### 2. Source Loader 集成

在 `lib/source.ts` 中传入 i18n 配置：

```typescript
import { loader } from 'fumadocs-core/source';
import { i18n } from '@/lib/i18n';
import { docs } from '@/.source';

export const source = loader({
  baseUrl: '/docs',
  source: docs.toFumadocsSource(),
  i18n, // 添加 i18n 配置
  plugins: [lucideIconsPlugin()],
});
```

### 3. RootProvider 配置

在 root layout 中使用 i18n 配置：

```typescript
// app/layout.tsx
import { RootProvider } from 'fumadocs-ui/provider';
import { i18n } from '@/lib/i18n';

export default function RootLayout({ children }) {
  return (
    <RootProvider i18n={i18n}>
      {children}
    </RootProvider>
  );
}
```

### 4. 创建 Middleware

重定向用户到合适的语言版本：

```typescript
// middleware.ts
import { createI18nMiddleware } from 'fumadocs-core/middleware';
import { i18n } from '@/lib/i18n';

export default createI18nMiddleware(i18n);

export const config = {
  matcher: ['/((?!api|_next/static|_next/image|favicon.ico).*)'],
};
```

## 目录结构方案

### 推荐方案：语言目录分离

```
content/
└── docs/
    ├── en/                      # 英文文档
    │   ├── index.mdx
    │   ├── frontend/
    │   │   └── react-basics.mdx
    │   └── backend/
    │       └── nodejs-intro.mdx
    ├── zh/                      # 中文文档
    │   ├── index.mdx
    │   ├── frontend/
    │   │   └── react-basics.mdx
    │   └── backend/
    │       └── nodejs-intro.mdx
    ├── fr/                      # 法语文档
    │   └── ...
    └── ko/                      # 韩语文档
        └── ...
```

### URL 结构

- 英文: `/docs/frontend/react-basics`
- 中文: `/zh/docs/frontend/react-basics`
- 法语: `/fr/docs/frontend/react-basics`
- 韩语: `/ko/docs/frontend/react-basics`

## 图片资源共享

**策略**: 所有语言共享同一套图片资源

```
public/
└── images/
    └── docs/
        └── react-basics/
            ├── component-tree.png
            └── hooks-flow.png
```

**引用方式**（所有语言版本使用相同路径）:
```mdx
![Component Tree](/images/docs/react-basics/component-tree.png)
```

## Frontmatter 扩展

需要添加 `lang` 字段来标识语言：

```yaml
---
title: React Basics
description: Learn React fundamentals
lang: en
source_url: https://example.com/react-basics
category: frontend
difficulty: beginner
---
```

## 导航和语言切换

Fumadocs UI 会自动处理：
- 语言切换器组件
- 同一文章的不同语言版本链接
- 面包屑导航

## Meta 文件组织

每个语言目录可能需要自己的 `meta.json`：

```
content/docs/en/meta.json
content/docs/zh/meta.json
content/docs/fr/meta.json
content/docs/ko/meta.json
```

## Skill 实现要点

1. **文件创建**: 为每种语言在对应目录下创建 MDX 文件
2. **路径映射**: 保持所有语言的目录结构一致
3. **图片引用**: 使用统一的图片路径（不区分语言）
4. **Slug 一致性**: 确保同一文章在不同语言下使用相同的 slug

## 待验证事项

- [ ] 当前项目是否已配置 i18n？（目前看起来没有）
- [ ] 是否需要在 Skill 中初始化 i18n 配置？
- [ ] meta.json 的具体结构和要求
- [ ] 语言切换的 UI 组件是否自动启用

## 实现步骤

1. ✅ 确定目标语言：en, zh, fr, ko
2. ⏳ 创建 i18n 配置文件
3. ⏳ 更新 source loader
4. ⏳ 创建语言目录结构
5. ⏳ 配置 middleware（如果需要）
6. ⏳ 在 Skill 中实现多语言文件生成逻辑

## 参考资源

- Fumadocs i18n 文档: https://fumadocs.dev/docs/ui/internationalization
- next-intl (可选集成): https://next-intl.dev
