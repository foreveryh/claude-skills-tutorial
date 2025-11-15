# 技术参考信息

## Jina AI Reader API

### 简介
Jina AI 提供了一个简单的 API 来将任何 URL 转换为 LLM 友好的格式。

### 使用方法

#### 方法 1: Jina API (HTTP)
```bash
curl https://r.jina.ai/https://example.com
```

#### 方法 2: Jina MCP
- 需要安装 Jina MCP 服务器
- 通过 MCP 协议访问 Jina 功能
- **待确认**: 是否已安装 Jina MCP？

### 输出格式
- Markdown 格式
- 包含文本内容
- 可能包含图片 URL

---

## Fumadocs MDX 语法

### Frontmatter Schema

从 `source.config.ts` 可以看到使用了 `frontmatterSchema`，具体定义待查。

可能的字段：
```yaml
---
title: 文章标题
description: 文章描述
# 待确认其他字段
---
```

### MDX 组件

#### 已知组件：

1. **Cards** - 卡片容器
   ```mdx
   <Cards>
     <Card title="标题" href="链接" />
   </Cards>
   ```

#### 待探索的组件：
- Callout / Alert
- Tabs
- CodeBlock
- 其他自定义组件

### MDX 导入规则

待确认：
- 组件是否需要显式导入？
- 哪些组件是全局可用的？

---

## 图片处理

### 下载图片
```bash
curl -o image.png https://example.com/image.png
```

### 图片命名策略（待决策）
- 选项A: 保持原文件名
- 选项B: 使用哈希值 (SHA256)
- 选项C: 使用递增编号
- 选项D: 结合文章标题的 slug

### 图片格式转换（可选）
- 使用 ImageMagick / Sharp
- 转换为 WebP 格式以优化性能

---

## 翻译提示词

### 基本结构

```
你是一个专业的技术文档翻译专家。

任务：将以下技术文章翻译为 [目标语言]

要求：
1. 保持技术术语的准确性
2. 保留原文的 Markdown/MDX 格式
3. 代码块不翻译，保持原样
4. 链接保持原样
5. 保持自然流畅的表达

原文：
[文章内容]

翻译：
```

### 待优化点
- 针对不同语言定制 prompt
- 术语表管理
- 上下文一致性检查

---

## MDX 语法验证

### 方法 1: 使用 Fumadocs CLI
```bash
# 待确认是否有验证命令
```

### 方法 2: Next.js 构建验证
```bash
npm run build
# 如果 MDX 有语法错误，构建会失败
```

### 方法 3: MDX 解析器
```javascript
// 使用 @mdx-js/mdx 验证语法
```

---

## 错误处理策略

### 网络错误
- 下载失败：重试 3 次，指数退避
- 超时设置：30 秒

### 文件系统错误
- 权限问题：提示用户
- 磁盘空间不足：提前检查

### 翻译错误
- API 失败：记录错误，跳过该语言
- 格式破坏：使用原文作为备份

---

## 性能优化

### 并发控制
- 图片下载：最多 5 个并发
- 翻译请求：串行处理（避免 API 限流）

### 缓存策略
- 已翻译内容缓存
- 图片下载缓存（避免重复下载）

---

## 参考资源

- Fumadocs 文档: https://fumadocs.dev
- Jina AI Reader: https://jina.ai/reader
- MDX 文档: https://mdxjs.com
- Claude Skills 规范: https://github.com/anthropics/skills
