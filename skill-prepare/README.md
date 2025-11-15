# Fumadocs 文章导入 Skill 准备文档

## 项目概述

创建一个 Claude Skill，用于自动化将外部文章导入到 Fumadocs 项目中，包括：
- 下载原文内容和图片
- 多语言翻译（4种语言：en, zh, fr, ko）
- 文章分类和归档
- MDX 格式转换和验证

## 目录结构

```
skill-prepare/
├── README.md                 # 本文件 - 项目概述
├── requirements.md           # 详细需求说明
├── questions.md              # 待解决的问题列表 (77% 已完成)
├── decisions.md              # 关键决策记录 (12/14 已决策)
├── workflow.md               # 工作流程设计
├── i18n-implementation.md    # 国际化实现方案
├── fumadocs-structure.md     # Fumadocs 项目结构分析
├── fumadocs-conventions.md   # Fumadocs 页面约定详解
├── fumadocs-components.md    # 🆕 Fumadocs 组件完整清单
├── category-research.md      # 分类标准研究（基于社区）
├── categories-final.md       # 最终分类标准定义
├── technical-notes.md        # 技术参考信息
└── summary.md                # 阶段性总结 (实时更新)
```

## 当前状态

- ✅ 项目初始化
- ✅ 需求收集（90% 完成）
- ✅ 技术设计（85% 完成）
- ⏸️ 待开始：Skill 开发

### 最新进展
- ✅ 完成图片处理策略（存储、命名、失败处理）
- ✅ 完成 Fumadocs 页面约定分析
- ✅ 完成 Frontmatter 字段定义
- ✅ 完成文章分类标准定义（8大类）
- ✅ 完成 Fumadocs 组件清单（15+ 组件）

## 进度概览

| 类别 | 进度 | 状态 |
|------|------|------|
| 多语言翻译 | ████████████████ 100% | ✅ 完成 |
| 图片处理 | ████████████████ 100% | ✅ 完成 |
| Frontmatter 定义 | ████████████████ 100% | ✅ 完成 |
| 文章分类 | ████████████████ 100% | ✅ 完成 |
| MDX 组件规范 | ████████████████ 100% | ✅ 完成 |
| 归档策略 | ░░░░░░░░░░░░░░░░ 0% | ⏸️ 待开始 |
| 工作流设计 | ██████████████░░ 90% | ⏳ 进行中 |

## 快速链接

### 📋 规划文档
- [详细需求](./requirements.md) - 功能需求和技术方案
- [待解决问题](./questions.md) - 22个问题，77%已回答
- [关键决策](./decisions.md) - 14个决策点，12个已完成

### 🔧 技术文档
- [工作流程设计](./workflow.md) - 7步处理流程
- [国际化方案](./i18n-implementation.md) - Fumadocs i18n 实现
- [页面约定](./fumadocs-conventions.md) - Fumadocs 官方规范
- [组件清单](./fumadocs-components.md) - **🆕 15+ 组件完整文档**
- [分类标准](./categories-final.md) - 8大类最终定义
- [技术笔记](./technical-notes.md) - 技术参考资料

### 📊 总结报告
- [阶段性总结](./summary.md) - 实时更新的进度总结

## 当前焦点

### 🎯 需要决定的关键问题

1. ~~**文章分类标准**~~（高优先级）✅ 已完成
   - ✅ 方案 B - 8大类标准分类
   - ✅ 8 个 categories 定义完成
   - 📄 详见：`categories-final.md`

2. **归档目录结构**（中优先级）⏳ 待定
   - 归档文件的组织方式
   - 元数据记录格式

3. ~~**MDX 组件规范**~~（中优先级）✅ 已完成
   - ✅ 15+ 个 Fumadocs 组件完整清单
   - ⚠️ 关键规则：永远不要自己实现组件
   - 📄 详见：`fumadocs-components.md`

## 已完成的重要决策

✅ **多语言**: en, zh, fr, ko 四种语言
✅ **i18n 方式**: 目录分离 (`content/docs/{lang}/`)
✅ **图片存储**: `/public/images/docs/{article-slug}/`
✅ **图片命名**: `{descriptive-name}-{index}.{ext}`
✅ **翻译流程**: 自动翻译，无需人工审核
✅ **Frontmatter**: title 必需，description/lang 推荐
✅ **分类体系**: 8大类 (development, data, ai-ml, design, content, business, devops, security)
✅ **MDX 组件**: 15+ 内置组件，禁止自定义实现

## 下一步行动

1. 确定文章分类标准和 categories 列表
2. 定义归档目录结构
3. 确认 MDX 组件使用规范
4. 开始编写 Skill

---

**维护者**: Claude
**创建日期**: 2025-11-15
**最后更新**: 2025-11-15
