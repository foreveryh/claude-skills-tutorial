# Fumadocs UI 组件完整清单

> **重要提醒**: 永远不要自己实现组件！Fumadocs 提供了丰富的内置组件，务必先检查是否已有可用组件。

## 📚 组件分类概览

Fumadocs UI 提供了 **15+ 个内置组件**，分为以下几类：

1. **内容组织** - Cards, Accordion, Tabs, Steps
2. **代码展示** - Code Block, Code Block (Dynamic)
3. **提示信息** - Callout, Banner
4. **文件结构** - Files (File Tree)
5. **类型文档** - Type Table, Auto Type Table
6. **媒体增强** - Zoomable Image
7. **导航辅助** - Inline TOC
8. **外部集成** - GitHub Info, Graph View

---

## 🎯 默认 MDX 组件

这些组件通过 `defaultMdxComponents` 自动可用，无需显式导入。

### Cards & Card

**用途**: 创建卡片布局，展示链接、功能特性等

**自动可用**: ✅ 是（通过 `fumadocs-ui/mdx`）

**用法**:
```mdx
<Cards>
  <Card title="Learn React" href="/docs/react" />
  <Card title="Learn Vue" href="/docs/vue" />
</Cards>
```

**Props**:
- `Card`:
  - `title`: 卡片标题（必需）
  - `href`: 链接地址（必需）
  - `description`: 卡片描述（可选）
  - `icon`: 图标（可选）

**当前项目使用**: ✅ 已使用

---

### Callout

**用途**: 显示提示、警告、注意事项等

**导入**: `fumadocs-ui/components/callout`

**自动可用**: ✅ 是

**用法**:
```mdx
<Callout type="info">
  This is an informational message.
</Callout>

<Callout type="warn">
  Warning: Be careful with this!
</Callout>

<Callout type="error">
  Error: Something went wrong.
</Callout>
```

**Props**:
- `type`: "info" | "warn" | "error" | "tip"（可选，默认 "info"）
- `title`: 标题（可选）

**当前项目使用**: ❌ 未使用

---

### Headings

**用途**: 自动生成带锚点的标题

**自动可用**: ✅ 是

**用法**:
```mdx
## This is a Heading
```

**特性**:
- 自动生成 ID
- 自动添加锚点链接
- 支持 Table of Contents

---

### Code Blocks

**用途**: 语法高亮的代码块

**自动可用**: ✅ 是（使用 Rehype Code）

**用法**:
````mdx
```javascript
console.log('Hello World');
```

```python title="main.py"
def hello():
    print("Hello World")
```
````

**特性**:
- 语法高亮
- 文件名显示（通过 `title` 属性）
- 行号显示
- 行高亮

---

## 🔧 内容组织组件

### Tabs

**用途**: 创建选项卡式内容

**导入**: `fumadocs-ui/components/tabs`

**用法**:
```mdx
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';

<Tabs items={['npm', 'pnpm', 'yarn']}>
  <Tab value="npm">
    ```bash
    npm install fumadocs
    ```
  </Tab>
  <Tab value="pnpm">
    ```bash
    pnpm add fumadocs
    ```
  </Tab>
  <Tab value="yarn">
    ```bash
    yarn add fumadocs
    ```
  </Tab>
</Tabs>
```

**Props**:
- `Tabs`:
  - `items`: 选项卡标题数组
  - `defaultValue`: 默认激活的选项卡
  - `persist`: 是否持久化选择
- `Tab`:
  - `value`: 选项卡值（必需）

**特性**:
- 基于 Radix UI
- 持久化选择（跨页面）
- 共享值（同一页面多个 Tabs 同步）

**当前项目使用**: ❌ 未使用

---

### Accordion

**用途**: 创建可折叠的手风琴式内容（适合 FAQ）

**导入**: `fumadocs-ui/components/accordion`

**用法**:
```mdx
import { Accordions, Accordion } from 'fumadocs-ui/components/accordion';

<Accordions>
  <Accordion title="What is Fumadocs?">
    Fumadocs is a framework for building documentation sites.
  </Accordion>
  <Accordion title="How do I install it?">
    Run `npm install fumadocs` to install.
  </Accordion>
</Accordions>
```

**Props**:
- `Accordion`:
  - `title`: 标题（必需）
  - `defaultOpen`: 是否默认展开

**特性**:
- 基于 Radix UI Accordion
- 平滑动画
- 可嵌套

**当前项目使用**: ❌ 未使用

---

### Steps

**用途**: 显示步骤式教程

**导入**: `fumadocs-ui/components/steps`

**用法**:
```mdx
import { Steps, Step } from 'fumadocs-ui/components/steps';

<Steps>
  <Step>
    ## Install Dependencies

    Run `npm install` to install all dependencies.
  </Step>
  <Step>
    ## Configure Settings

    Update your `config.json` file.
  </Step>
  <Step>
    ## Run the App

    Execute `npm start` to launch.
  </Step>
</Steps>
```

**特性**:
- 自动编号
- 视觉引导线
- 支持嵌套内容

**当前项目使用**: ❌ 未使用

---

## 💻 代码展示组件

### Code Block (Static)

**用途**: 基础代码块（已默认可用）

**导入**: `fumadocs-ui/components/codeblock`

**自动可用**: ✅ 是

（见上文默认 MDX 组件）

---

### Code Block (Dynamic)

**用途**: 动态加载的代码块（适合大型代码文件）

**导入**: `fumadocs-ui/components/dynamic-codeblock`

**用法**:
```mdx
import { DynamicCodeBlock } from 'fumadocs-ui/components/dynamic-codeblock';

<DynamicCodeBlock
  lang="typescript"
  code={`
    // Your code here
    const hello = "world";
  `}
/>
```

**Props**:
- `lang`: 语言（必需）
- `code`: 代码字符串（必需）
- `title`: 文件名（可选）

**当前项目使用**: ❌ 未使用

---

## 📁 文件结构组件

### Files (File Tree)

**用途**: 显示文件/文件夹结构

**导入**: `fumadocs-ui/components/files`

**用法**:
```mdx
import { Files, Folder, File } from 'fumadocs-ui/components/files';

<Files>
  <Folder name="app" defaultOpen>
    <File name="layout.tsx" />
    <File name="page.tsx" />
    <Folder name="api">
      <File name="route.ts" />
    </Folder>
  </Folder>
  <Folder name="components">
    <File name="Button.tsx" />
    <File name="Card.tsx" />
  </Folder>
</Files>
```

**Props**:
- `Folder`:
  - `name`: 文件夹名称（必需）
  - `defaultOpen`: 是否默认展开
- `File`:
  - `name`: 文件名（必需）

**当前项目使用**: ❌ 未使用

---

## 🔔 提示信息组件

### Banner

**用途**: 在页面顶部显示公告/通知

**导入**: `fumadocs-ui/components/banner`

**用法**:
```mdx
import { Banner } from 'fumadocs-ui/components/banner';

<Banner variant="rainbow">
  🎉 New feature released! Check out our latest update.
</Banner>
```

**Props**:
- `variant`: "default" | "rainbow"
- `color`: 自定义颜色（用于 rainbow 变体）

**当前项目使用**: ❌ 未使用

---

## 📊 类型文档组件

### Type Table

**用途**: 显示 TypeScript 类型定义表格

**导入**: `fumadocs-ui/components/type-table`

**用法**:
```mdx
import { TypeTable } from 'fumadocs-ui/components/type-table';

<TypeTable
  type={{
    name: { type: 'string', description: 'User name' },
    age: { type: 'number', description: 'User age' },
    email: { type: 'string', description: 'User email', optional: true }
  }}
/>
```

**Props**:
- `type`: 类型对象（必需）

**当前项目使用**: ❌ 未使用

---

### Auto Type Table

**用途**: 从 TypeScript 文件自动生成类型表格

**导入**: `fumadocs-ui/components/auto-type-table`

**用法**:
```mdx
import { AutoTypeTable } from 'fumadocs-ui/components/auto-type-table';

<AutoTypeTable
  path="./types/user.ts"
  name="User"
/>
```

**Props**:
- `path`: TypeScript 文件路径（必需）
- `name`: 导出的类型名称（必需）

**特性**:
- 自动解析 TypeScript 定义
- 显示类型、描述、可选性
- 支持复杂类型

**当前项目使用**: ❌ 未使用

---

## 🖼️ 媒体增强组件

### Zoomable Image (ImageZoom)

**用途**: 可点击放大的图片

**导入**: `fumadocs-ui/components/image-zoom`

**用法**:

**方法 1**: 替换所有 img（推荐）
```tsx
// mdx-components.tsx
import { ImageZoom } from 'fumadocs-ui/components/image-zoom';

export function useMDXComponents() {
  return {
    img: ImageZoom,
    ...defaultMdxComponents
  };
}
```

**方法 2**: 单独使用
```mdx
import { ImageZoom } from 'fumadocs-ui/components/image-zoom';

<ImageZoom
  src="/images/diagram.png"
  alt="System Architecture"
  width={800}
  height={600}
/>
```

**Props**:
- 所有标准 `<img>` 属性
- 自动启用点击放大

**当前项目使用**: ❌ 未使用

---

## 🧭 导航辅助组件

### Inline TOC

**用途**: 在页面内嵌入目录

**导入**: `fumadocs-ui/components/inline-toc`

**用法**:
```mdx
import { InlineTOC } from 'fumadocs-ui/components/inline-toc';

<InlineTOC items={toc} />
```

**Props**:
- `items`: TOC 项数组（从页面数据获取）

**特性**:
- 自动高亮当前章节
- 平滑滚动

**当前项目使用**: ❌ 未使用

---

## 🔗 外部集成组件

### GitHub Info

**用途**: 显示 GitHub 仓库信息（stars, forks 等）

**导入**: `fumadocs-ui/components/github-info`

**用法**:
```mdx
import { GitHubInfo } from 'fumadocs-ui/components/github-info';

<GitHubInfo owner="fuma-nama" repo="fumadocs" />
```

**Props**:
- `owner`: GitHub 用户名/组织（必需）
- `repo`: 仓库名称（必需）

**当前项目使用**: ❌ 未使用

---

### Graph View

**用途**: 显示文档依赖关系图

**导入**: `fumadocs-ui/components/graph-view`

**用法**: （通常在布局中配置）

**当前项目使用**: ❌ 未使用

---

## 📋 组件使用统计

### 当前项目已使用（2/15+）
- ✅ Cards / Card
- ✅ Code Blocks（默认）

### 推荐添加到 Skill 中（高优先级）
1. **Callout** - 用于重要提示、警告
2. **Tabs** - 用于多种安装/配置方式
3. **Steps** - 用于教程步骤
4. **Files** - 用于显示项目结构
5. **ImageZoom** - 用于技术图表

### 可选组件（按需使用）
- Accordion - FAQ 或可折叠内容
- Banner - 重要公告
- Type Table - TypeScript 类型文档
- Auto Type Table - 自动生成类型文档
- Inline TOC - 长文档内部导航
- GitHub Info - 显示项目统计

---

## 🎨 组件导入最佳实践

### 全局配置（推荐）

在 `mdx-components.tsx` 中配置：

```tsx
import defaultMdxComponents from 'fumadocs-ui/mdx';
import { ImageZoom } from 'fumadocs-ui/components/image-zoom';

export function useMDXComponents(components: MDXComponents): MDXComponents {
  return {
    ...defaultMdxComponents,
    img: ImageZoom, // 替换默认 img
    ...components,
  };
}
```

### 按需导入

在 MDX 文件中：

```mdx
import { Tabs, Tab } from 'fumadocs-ui/components/tabs';
import { Callout } from 'fumadocs-ui/components/callout';
import { Steps, Step } from 'fumadocs-ui/components/steps';
```

---

## ⚠️ 重要规则

### ❌ 永远不要自己实现这些组件：
- 卡片布局 → 使用 `Cards/Card`
- 选项卡 → 使用 `Tabs/Tab`
- 手风琴 → 使用 `Accordion`
- 代码块 → 使用内置 Code Block
- 提示框 → 使用 `Callout`
- 文件树 → 使用 `Files/Folder/File`
- 步骤指南 → 使用 `Steps/Step`

### ✅ 使用前检查清单：
1. 查看本文档是否有现成组件
2. 检查 [Fumadocs 官方文档](https://fumadocs.dev/docs/ui/components)
3. 确认无可用组件后再考虑自定义

---

## 📖 参考资源

- [Fumadocs UI Components 文档](https://fumadocs.dev/docs/ui/components)
- [Fumadocs Markdown 指南](https://fumadocs.dev/docs/ui/markdown)
- [Fumadocs GitHub 仓库](https://github.com/fuma-nama/fumadocs)

---

**最后更新**: 2025-11-15
**文档维护**: Claude
