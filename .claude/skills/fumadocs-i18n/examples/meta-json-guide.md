# meta.json 多语言最佳实践

## 核心概念

在 fumadocs 中，`meta.json` 的作用是**分离 URL 路径和显示名称**：

- **URL 路径**：固定的、SEO 友好的英文路径（如 `ai-ml`）
- **显示名称**：语义化的、多语言的文件夹标题（如 "AI & Machine Learning", "AI 与机器学习"）

## 为什么需要 meta.json？

### 问题场景

```
content/docs/
└── en/
    └── ai-ml/              ← URL 是 /en/docs/ai-ml
        └── page.mdx
```

**问题**：
- Sidebar 会显示 "ai-ml"（技术名称，不够友好）
- 无法为不同语言显示不同的标题
- 无法控制页面顺序

### 解决方案：使用 meta.json

```
content/docs/
├── en/
│   └── ai-ml/
│       ├── meta.json       ← 控制英文显示
│       └── page.mdx
└── zh/
    └── ai-ml/
        ├── meta.json       ← 控制中文显示
        └── page.mdx
```

**效果**：
- URL 仍然是 `/en/docs/ai-ml`（不变）
- 英文 Sidebar 显示："AI & Machine Learning"
- 中文 Sidebar 显示："AI 与机器学习"

## meta.json 结构

### 基本字段

```json
{
  "title": "Display Name",        // Sidebar 中显示的名称（必需）
  "icon": "IconName",             // 文件夹图标（可选）
  "pages": ["page1", "page2"],    // 页面顺序（可选）
  "defaultOpen": true,            // 是否默认展开（可选）
  "root": false                   // 是否为根文件夹（可选）
}
```

### 字段说明

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | Sidebar 中显示的文件夹名称 |
| `icon` | string | ❌ | 图标名称（需要配置 icon handler） |
| `pages` | array | ❌ | 控制页面显示顺序，未列出的页面不显示 |
| `defaultOpen` | boolean | ❌ | 是否默认展开文件夹（默认 false） |
| `root` | boolean | ❌ | 标记为根文件夹，创建 Sidebar Tabs |

## 完整示例

### 1. 基础多语言文件夹

#### 英文：`content/docs/en/ai-ml/meta.json`
```json
{
  "title": "AI & Machine Learning",
  "icon": "Brain",
  "pages": [
    "introduction",
    "skills-explained",
    "best-practices"
  ],
  "defaultOpen": true
}
```

#### 中文：`content/docs/zh/ai-ml/meta.json`
```json
{
  "title": "AI 与机器学习",
  "icon": "Brain",
  "pages": [
    "introduction",
    "skills-explained",
    "best-practices"
  ],
  "defaultOpen": true
}
```

#### 法语：`content/docs/fr/ai-ml/meta.json`
```json
{
  "title": "IA et Apprentissage Automatique",
  "icon": "Brain",
  "pages": [
    "introduction",
    "skills-explained",
    "best-practices"
  ],
  "defaultOpen": true
}
```

#### 韩语：`content/docs/ko/ai-ml/meta.json`
```json
{
  "title": "AI 및 머신러닝",
  "icon": "Brain",
  "pages": [
    "introduction",
    "skills-explained",
    "best-practices"
  ],
  "defaultOpen": true
}
```

### 2. 根目录 meta.json

控制顶级导航和顺序：

#### 英文：`content/docs/en/meta.json`
```json
{
  "title": "Documentation",
  "pages": [
    "index",
    "getting-started",
    "---Core Concepts---",
    "ai-ml",
    "development",
    "data",
    "---Advanced---",
    "configuration",
    "api"
  ]
}
```

#### 中文：`content/docs/zh/meta.json`
```json
{
  "title": "文档",
  "pages": [
    "index",
    "getting-started",
    "---核心概念---",
    "ai-ml",
    "development",
    "data",
    "---高级内容---",
    "configuration",
    "api"
  ]
}
```

**注意**：分隔符 `---Label---` 也支持多语言！

### 3. 复杂目录结构

```
content/docs/en/
├── meta.json                     # 顶级导航
├── index.mdx
├── getting-started/
│   ├── meta.json                 # "Getting Started" 类别
│   ├── installation.mdx
│   └── configuration.mdx
├── ai-ml/
│   ├── meta.json                 # "AI & Machine Learning" 类别
│   ├── introduction.mdx
│   └── advanced/
│       ├── meta.json             # "Advanced Topics" 子类别
│       ├── neural-networks.mdx
│       └── transformers.mdx
└── api/
    └── meta.json                 # "API Reference" 类别
```

#### `content/docs/en/getting-started/meta.json`
```json
{
  "title": "Getting Started",
  "icon": "Rocket",
  "pages": [
    "installation",
    "configuration",
    "first-project"
  ],
  "defaultOpen": true
}
```

#### `content/docs/en/ai-ml/meta.json`
```json
{
  "title": "AI & Machine Learning",
  "icon": "Brain",
  "pages": [
    "introduction",
    "advanced"
  ],
  "defaultOpen": false
}
```

#### `content/docs/en/ai-ml/advanced/meta.json`
```json
{
  "title": "Advanced Topics",
  "icon": "Zap",
  "pages": [
    "neural-networks",
    "transformers",
    "fine-tuning"
  ]
}
```

## pages 字段高级用法

### 基础用法

```json
{
  "pages": [
    "index",           // 显示 index.mdx
    "getting-started", // 显示 getting-started.mdx
    "advanced"         // 显示 advanced/ 文件夹
  ]
}
```

### 高级语法

```json
{
  "pages": [
    "index",
    "---Getting Started---",              // 分隔符
    "installation",
    "configuration",
    "---[Rocket]Advanced Topics---",      // 带图标的分隔符
    "...",                                 // 包含所有剩余页面（按字母排序）
    "!excluded-page",                      // 从 ... 中排除
    "[External Link](https://example.com)", // 外部链接
    "[Github][GitHub](https://github.com)"  // 带图标的外部链接
  ]
}
```

### 实际示例

```json
{
  "title": "Documentation",
  "pages": [
    "index",
    "---[Book]Tutorials---",
    "getting-started",
    "basic-concepts",
    "---[Code]Reference---",
    "api",
    "components",
    "---[Link]External---",
    "[GitHub](https://github.com/yourproject)",
    "[npm][Package](https://npmjs.com/package/yourproject)",
    "---[Folder]More---",
    "...",                    // 包含所有其他页面
    "!draft",                 // 排除 draft.mdx
    "!internal"               // 排除 internal/ 文件夹
  ]
}
```

## 多语言组织策略

### 策略 1: 相同结构，不同标题

**适用场景**：所有语言的文档内容相同，只是翻译不同

```
content/docs/
├── en/
│   ├── meta.json          {"title": "Documentation"}
│   └── ai-ml/
│       ├── meta.json      {"title": "AI & Machine Learning"}
│       └── page.mdx
└── zh/
    ├── meta.json          {"title": "文档"}
    └── ai-ml/
        ├── meta.json      {"title": "AI 与机器学习"}
        └── page.mdx       (翻译版本)
```

### 策略 2: 不同结构

**适用场景**：不同语言有不同的内容组织

```
content/docs/
├── en/
│   ├── meta.json
│   ├── getting-started/
│   ├── api-reference/
│   └── tutorials/
└── zh/
    ├── meta.json
    ├── kuai-su-kai-shi/    # 快速开始（可能顺序不同）
    └── jiao-cheng/         # 教程（可能内容不同）
```

## 常见目录名称翻译参考

| 英文 | 中文 | 法语 | 韩语 |
|------|------|------|------|
| Getting Started | 快速开始 | Démarrage | 시작하기 |
| Tutorials | 教程 | Tutoriels | 튜토리얼 |
| API Reference | API 参考 | Référence API | API 참조 |
| Components | 组件 | Composants | 컴포넌트 |
| Configuration | 配置 | Configuration | 구성 |
| Advanced | 高级 | Avancé | 고급 |
| Examples | 示例 | Exemples | 예제 |
| FAQ | 常见问题 | FAQ | 자주 묻는 질문 |

## 图标配置

### 1. 在 meta.json 中指定图标名称

```json
{
  "title": "AI & Machine Learning",
  "icon": "Brain"
}
```

### 2. 配置图标处理器

在 `lib/source.ts` 中：

```typescript
import { loader } from 'fumadocs-core/source';
import { lucideIconsPlugin } from 'fumadocs-core/source/lucide-icons';

export const source = loader({
  baseUrl: '/docs',
  source: docs.toFumadocsSource(),
  plugins: [
    lucideIconsPlugin(), // 启用 Lucide 图标支持
  ],
  i18n,
});
```

### 3. 可用的图标

使用 Lucide React 图标库：https://lucide.dev/icons/

常用图标：
- `Book` - 书籍/文档
- `Rocket` - 快速开始
- `Code` - 代码/开发
- `Brain` - AI/智能
- `Database` - 数据
- `Settings` - 配置
- `Zap` - 快速/高级
- `Package` - 组件/包
- `Shield` - 安全
- `Cloud` - 云服务

## 实战示例：完整的多语言文档

### 目录结构

```
content/docs/
├── en/
│   ├── meta.json
│   ├── index.mdx
│   ├── getting-started/
│   │   ├── meta.json
│   │   ├── installation.mdx
│   │   └── quick-start.mdx
│   └── ai-ml/
│       ├── meta.json
│       ├── introduction.mdx
│       └── skills-explained.mdx
├── zh/
│   ├── meta.json
│   ├── index.mdx
│   ├── getting-started/
│   │   ├── meta.json
│   │   ├── installation.mdx
│   │   └── quick-start.mdx
│   └── ai-ml/
│       ├── meta.json
│       ├── introduction.mdx
│       └── skills-explained.mdx
└── (fr, ko similar structure...)
```

### 英文配置

**`content/docs/en/meta.json`**
```json
{
  "title": "Documentation",
  "pages": [
    "index",
    "---[Rocket]Getting Started---",
    "getting-started",
    "---[Book]Guides---",
    "ai-ml",
    "---[Link]Resources---",
    "[GitHub](https://github.com/yourproject)"
  ]
}
```

**`content/docs/en/getting-started/meta.json`**
```json
{
  "title": "Getting Started",
  "icon": "Rocket",
  "pages": [
    "installation",
    "quick-start",
    "configuration"
  ],
  "defaultOpen": true
}
```

**`content/docs/en/ai-ml/meta.json`**
```json
{
  "title": "AI & Machine Learning",
  "icon": "Brain",
  "pages": [
    "introduction",
    "skills-explained",
    "best-practices"
  ],
  "defaultOpen": false
}
```

### 中文配置

**`content/docs/zh/meta.json`**
```json
{
  "title": "文档",
  "pages": [
    "index",
    "---[Rocket]快速开始---",
    "getting-started",
    "---[Book]指南---",
    "ai-ml",
    "---[Link]资源---",
    "[GitHub](https://github.com/yourproject)"
  ]
}
```

**`content/docs/zh/getting-started/meta.json`**
```json
{
  "title": "快速开始",
  "icon": "Rocket",
  "pages": [
    "installation",
    "quick-start",
    "configuration"
  ],
  "defaultOpen": true
}
```

**`content/docs/zh/ai-ml/meta.json`**
```json
{
  "title": "AI 与机器学习",
  "icon": "Brain",
  "pages": [
    "introduction",
    "skills-explained",
    "best-practices"
  ],
  "defaultOpen": false
}
```

## 最佳实践

### ✅ 推荐做法

1. **保持 URL 一致**
   - 所有语言使用相同的文件夹名称（如 `ai-ml`）
   - 便于语言切换时保持相同的路径结构

2. **为每个语言创建独立的 meta.json**
   - 每个语言目录下的文件夹都有自己的 meta.json
   - 可以有不同的标题、顺序、甚至结构

3. **使用语义化的显示名称**
   - 不要在 `title` 中使用技术名称（如 "ai-ml"）
   - 使用友好的、本地化的名称（如 "AI & Machine Learning"）

4. **合理使用分隔符**
   - 使用 `---Label---` 组织大型文档
   - 分隔符标签也应该本地化

5. **控制默认展开状态**
   - 重要的类别设置 `"defaultOpen": true`
   - 避免过多的默认展开，影响导航体验

### ❌ 避免的做法

1. ❌ 不要在所有语言中硬编码英文标题
```json
// 错误：中文 meta.json 使用英文标题
{
  "title": "Getting Started"  // 应该是 "快速开始"
}
```

2. ❌ 不要省略 meta.json
```
content/docs/zh/ai-ml/
└── page.mdx
// 缺少 meta.json，sidebar 会显示 "ai-ml"
```

3. ❌ 不要在 URL 中使用非英文字符
```
content/docs/zh/快速开始/  // ❌ URL 不友好
content/docs/zh/getting-started/  // ✅ 正确
```

4. ❌ 不要在 pages 数组中硬编码所有页面
```json
{
  "pages": ["page1", "page2", "page3", ...]  // 维护困难
}
// 更好的做法：
{
  "pages": ["important-page", "..."]  // 列出重要的，其余用 ...
}
```

## 调试技巧

### 1. 检查 meta.json 是否生效

```bash
# 清理缓存
rm -rf .next .source

# 重新构建
npm run build

# 检查生成的页面树
# 在浏览器控制台：
console.log(window.__NEXT_DATA__)
```

### 2. 验证文件结构

```bash
# 检查每个语言目录是否都有 meta.json
find content/docs -name "meta.json"

# 应该看到：
# content/docs/en/meta.json
# content/docs/en/ai-ml/meta.json
# content/docs/zh/meta.json
# content/docs/zh/ai-ml/meta.json
# ...
```

### 3. 常见问题

**问题**：meta.json 不生效，sidebar 仍显示文件夹名
**解决**：清理缓存重新构建

**问题**：某些页面不显示在 sidebar
**解决**：检查 `pages` 数组是否包含该页面，或使用 `...` 包含所有页面

**问题**：图标不显示
**解决**：确保配置了 `lucideIconsPlugin()`，使用正确的图标名称

## 总结

- **meta.json** 是控制 fumadocs sidebar 的核心配置文件
- 实现了 **URL 路径和显示名称的分离**
- 支持 **完全独立的多语言配置**
- 提供了 **丰富的页面组织选项**

通过合理使用 meta.json，你可以为每种语言提供最佳的导航体验！

---

**参考资料**：
- [Fumadocs Page Conventions](https://fumadocs.dev/docs/headless/page-conventions)
- [Fumadocs Sidebar Links](https://fumadocs.dev/docs/ui/navigation/sidebar)
