# Claude Skills 分类标准研究

> 基于社区主流 awesome-claude-skills 仓库的分析

## 研究来源

分析了以下三个主要仓库：
1. **travisvn/awesome-claude-skills** - 专注 Claude Code
2. **ComposioHQ/awesome-claude-skills** - 9 大类
3. **abubakarsiddik31/claude-skills-collection** - 10 大类

---

## 社区主流分类体系

### 综合分类（10大类）

| 分类 | 英文 | 说明 | 典型 Skills 示例 |
|------|------|------|------------------|
| **文档处理** | Document Processing | Office 文档、PDF、表格操作 | docx, pdf, pptx, xlsx |
| **开发工具** | Development & Code | 编程、测试、Git、API 集成 | artifacts-builder, mcp-builder, webapp-testing, TDD |
| **创意设计** | Creative & Design | 视觉艺术、生成艺术、品牌设计 | algorithmic-art, canvas-design, theme-factory |
| **数据分析** | Data & Analysis | 数据处理、可视化、统计分析 | CSV analyzer, D3 visualization, root-cause-analysis |
| **写作研究** | Writing & Research | 内容创作、研究、文章提取 | article-extractor, content-research, citation-assistant |
| **商业营销** | Business & Marketing | 营销策略、竞品分析、需求生成 | competitive-analysis, lead-generation, ad-library |
| **生产力** | Productivity & Organization | 文件管理、发票整理、自动化 | file-organizer, invoice-manager, raffle-selector |
| **协作管理** | Collaboration & PM | 项目管理、代码审查、会议分析 | code-review, meeting-analysis, Notion-integration |
| **安全测试** | Security & Testing | 安全分析、模糊测试、调试 | digital-forensics, fuzz-testing, systematic-debugging |
| **媒体处理** | Media & Content | 视频、音频、图片处理 | youtube-transcript, image-enhancement, GIF-creator |

---

## 各仓库分类对比

### travisvn (官方风格，5大类)
1. Document Skills (docx, pdf, pptx, xlsx)
2. Design & Creative (art, canvas, GIF)
3. Development (artifacts, MCP, testing)
4. Communication (brand, internal-comms)
5. Meta (skill-creator)

### ComposioHQ (9大类)
1. Document Processing
2. Development & Code Tools
3. Data & Analysis
4. Business & Marketing
5. Communication & Writing
6. Creative & Media
7. Productivity & Organization
8. Collaboration & Project Management
9. Security & Systems

### abubakarsiddik31 (10大类 - 最完整)
1. Document Skills
2. Creative & Design
3. Development & Code Tools
4. Data & Analysis
5. Writing & Research
6. **Learning & Knowledge** (新增)
7. Media & Content
8. Collaboration & Project Management
9. Security & Testing
10. Utility & Automation

---

## 难度等级划分

虽然仓库中没有明确的难度分级，但可以根据 skill 复杂度推断：

### Beginner (初级)
- 单一功能，步骤简单
- 示例：file-organizer, article-extractor, youtube-transcript

### Intermediate (中级)
- 多步骤工作流，需要一定技术知识
- 示例：docx, csv-analyzer, code-review

### Advanced (高级)
- 复杂逻辑，需要专业知识或多工具集成
- 示例：mcp-builder, digital-forensics, systematic-debugging, TDD

---

## 🎯 推荐分类方案

### 方案 A: 精简分类（6大类）
**适用场景**: 教程内容相对聚焦

1. **Development** (开发)
   - 编程、测试、工具链、API

2. **AI & Data** (AI 与数据)
   - 机器学习、数据分析、可视化

3. **Content & Writing** (内容创作)
   - 写作、研究、文档、媒体

4. **Design & Creative** (设计创意)
   - UI/UX、视觉设计、生成艺术

5. **Business & Productivity** (商业效率)
   - 营销、管理、自动化

6. **Security & DevOps** (安全运维)
   - 安全、测试、CI/CD

### 方案 B: 标准分类（8大类）
**适用场景**: 内容丰富，覆盖面广

1. **Development & Code** (开发编程)
2. **Data & Analytics** (数据分析)
3. **AI & Machine Learning** (AI 机器学习)
4. **Design & Creative** (设计创意)
5. **Content & Writing** (内容写作)
6. **Business & Marketing** (商业营销)
7. **DevOps & Infrastructure** (运维基础设施)
8. **Security & Testing** (安全测试)

### 方案 C: 完整分类（10大类）
**适用场景**: 大型教程库，分类精细

采用 abubakarsiddik31 的 10 大类体系（见上表）

---

## 🏷️ 标签 (Tags) 建议

除了主分类，还可以用标签进行更细粒度的标记：

**技术栈标签**:
- `react`, `typescript`, `python`, `nodejs`, `docker`, `kubernetes`

**应用场景标签**:
- `automation`, `testing`, `monitoring`, `documentation`, `api-integration`

**技能类型标签**:
- `hands-on`, `conceptual`, `best-practices`, `troubleshooting`

**工具平台标签**:
- `claude-code`, `claude-api`, `mcp`, `playwright`, `git`

---

## 💡 分类决策建议

### 问题清单

1. **你的教程主要覆盖哪些领域？**
   - 纯技术开发？
   - AI/数据科学？
   - 全栈+商业+设计？

2. **预计教程数量级别？**
   - < 50 篇：精简分类（方案 A）
   - 50-200 篇：标准分类（方案 B）
   - > 200 篇：完整分类（方案 C）

3. **目标受众？**
   - 开发者：侧重技术分类
   - 产品/商业：增加商业分类
   - 综合：使用完整分类

### 推荐决策流程

```
Step 1: 确定主要内容方向
   ↓
Step 2: 选择分类方案（A/B/C）
   ↓
Step 3: 定义 3-5 个核心 categories
   ↓
Step 4: 可选：设置标签体系
   ↓
Step 5: 定义难度等级规则
```

---

## 📋 待用户确认

请根据你的教程内容特点，确认以下信息：

1. **主要内容领域**（可多选）：
   - [ ] 软件开发 (Development)
   - [ ] AI/机器学习 (AI/ML)
   - [ ] 数据分析 (Data)
   - [ ] 设计创意 (Design)
   - [ ] 商业营销 (Business)
   - [ ] DevOps/安全 (DevOps/Security)
   - [ ] 其他：___________

2. **预计教程规模**：
   - [ ] 小型 (< 50 篇)
   - [ ] 中型 (50-200 篇)
   - [ ] 大型 (> 200 篇)

3. **偏好分类方案**：
   - [ ] 方案 A (6 大类 - 精简)
   - [ ] 方案 B (8 大类 - 标准)
   - [ ] 方案 C (10 大类 - 完整)
   - [ ] 自定义

4. **难度等级**：
   - [ ] 使用 beginner/intermediate/advanced
   - [ ] 使用 1-5 星级
   - [ ] 不设置难度等级

5. **是否使用标签系统**：
   - [ ] 是，使用技术栈标签
   - [ ] 否，只用主分类

---

## 参考资源

- [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills)
- [ComposioHQ/awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills)
- [abubakarsiddik31/claude-skills-collection](https://github.com/abubakarsiddik31/claude-skills-collection)
- [Anthropic Official Skills](https://github.com/anthropics/skills)
