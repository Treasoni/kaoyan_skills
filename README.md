# Agent Skills Collection

一个为 Claude Code 设计的技能（Skills）集合，遵循**三层架构**（L1 入口路由 → L2 领域模块 → L3 工具能力），专注考研学习和知识管理场景。

> 📖 **技能体系地图**：详见 [SKILL_SYSTEM.md](./SKILL_SYSTEM.md)，包含准入规则、维护清单和子模块边界定义。

## 项目概述

本项目包含 40+ 个可复用的 Agent Skills，每个技能都是一个独立的功能模块，可以通过 Claude Code 的 Skill 工具调用。这些技能主要用于：

- **考研备考**：数学、英语、电子技术等学科的学习辅助
- **计划管理**：学习计划生成、进度追踪、欠账管理
- **知识管理**：笔记生成、错题整理、知识库组织、理解验证
- **工具增强**：Obsidian 集成、图表生成、智能搜索、安全审计

## 三层架构

```
用户请求
  │
  ▼
L1 入口路由        ← 日常只暴露这些入口
  ├─ /kaoyan-plan      学习计划、进度、欠账
  ├─ /kaoyan-math      考研数学（路由器）
  ├─ /kaoyan-english   考研英语（路由器）
  ├─ /kaoyan-electronics  822 电子技术（路由器）
  ├─ /understanding    理解验证、推导检查
  ├─ /mistake-book     错题整理
  ├─ /digest           学习消化、经验记录
  │
  ▼
L2 领域模块         ← 按需调度，不直接暴露给用户
  ├─ 数学: core / notes / structure / summary
  ├─ 英语: core / vocab / review / quiz / writing
  ├─ 电子: core / sop / circuit / structure
  ├─ 错题: extract / restructure
  │
  ▼
L3 工具能力         ← 通用工具，跨领域复用
  ├─ 图示: excalidraw-diagram / math-graph / knowledge-mindmap
  ├─ Obsidian: cli / markdown / bases / sortspec-generator
  ├─ 搜索: smart-search / kaoyan-info
  ├─ 维护: skill-refactor / maintain-learnings / prompt-cache-optimizer / security-secret-audit / fix-table-pipe
  ├─ 文件: word-template-generator
  ├─ 词汇: parse-words
  └─ 章节: chapter-summary
```

## 技能列表

### L1 入口路由

| 技能 | 描述 | 版本 |
|------|------|------|
| [kaoyan-math](./kaoyan-math/) | 考研数学路由器，调度到子技能（笔记生成、知识点结构、核心协调） | v4.0.0 |
| [kaoyan-english](./kaoyan-english/) | 考研英语路由器，调度到子技能（词汇、复习、测试、写作） | v4.0.0 |
| [kaoyan-plan](./kaoyan-plan/) | 考研学习计划生成，支持课表解析、任务分配、欠账管理、MemOS集成 | v3.16.0 |
| [kaoyan-electronics](./kaoyan-electronics/) | 822电子技术基础路由器，调度到子技能（电路分析、SOP、知识点结构） | v2.0.0 |
| [understanding](./understanding/) | 理解验证：检查概念/推导/笔记是否正确，输出结构化 `[!personal]` 记录 | v1.0.0 |
| [mistake-book](./mistake-book/) | 错题整理：快速整理错题到学科错题本，自动格式化、更新索引 | v1.0.0 |
| [digest](./digest/) | 学习消化：回顾学习会话，记录心得和错误到 .learnings/，自动压缩去重 | - |

### L2 领域模块

#### 考研数学子技能

| 技能 | 描述 |
|------|------|
| [kaoyan-math-core](./kaoyan-math-core/) | 核心协调层：MemOS集成、调度信号、统一错误模型、跨学科关联 |
| [kaoyan-math-notes](./kaoyan-math-notes/) | 笔记生成更新：LaTeX格式强制、知识点模板、已有笔记保护 |
| [kaoyan-math-structure](./kaoyan-math-structure/) | 知识点结构模板：高数/线代/概率模块参考 |
| [kaoyan-math-summary](./kaoyan-math-summary/) | 章节笔记整理：提取定义定理公式、保留个人理解、生成结构化总结 |

#### 考研英语子技能

| 技能 | 描述 |
|------|------|
| [kaoyan-english-core](./kaoyan-english-core/) | 核心协调层：MemOS集成、调度信号处理、记忆压缩模式 |
| [kaoyan-english-vocab](./kaoyan-english-vocab/) | 词汇管理：PDF词汇提取、查词、熟词僻义检测、真题语境 |
| [kaoyan-english-review](./kaoyan-english-review/) | 复习计划：SM-2复习计划、统计追踪、分阶段策略 |
| [kaoyan-english-quiz](./kaoyan-english-quiz/) | 单词测试：词义测试、搭配测试、僻义测试 |
| [kaoyan-english-writing](./kaoyan-english-writing/) | 写作训练：写作替换、汉译英、词义辨析 |

#### 822电子技术子技能

| 技能 | 描述 |
|------|------|
| [kaoyan-electronics-core](./kaoyan-electronics-core/) | 核心协调层：MemOS集成、调度信号、跨学科关联、数学前置检查 |
| [kaoyan-electronics-sop](./kaoyan-electronics-sop/) | SOP模板库：17个标准化解题流程（模电8+数电9）、康华光符号体系 |
| [kaoyan-electronics-circuit](./kaoyan-electronics-circuit/) | 电路图解析：智能识别、静态分析+动态分析、电路图生成、MCP工具集成 |
| [kaoyan-electronics-structure](./kaoyan-electronics-structure/) | 知识点结构：知识图谱、前置知识关联、知识点卡片模板 |

#### 错题相关子技能

| 技能 | 描述 |
|------|------|
| [mistake-extract](./mistake-extract/) | 错题精华提炼：提取核心口诀、避坑要点、解题方法模板、检查清单 |
| [mistake-restructure](./mistake-restructure/) | 错题本结构优化：自动分析错题关联、按知识点分类索引、生成关联网络图 |

### L3 工具能力

#### 图示工具

| 技能 | 描述 | 版本 |
|------|------|------|
| [excalidraw-diagram](./excalidraw-diagram/) | Excalidraw图生成：流程图、思维导图、关系图等，支持Obsidian/标准/动画三种模式 | v1.2.1 |
| [math-graph](./math-graph/) | 数学函数绘图：Python+Matplotlib生成教科书级函数图像，多图对比 | v1.0.0 |
| [knowledge-mindmap](./knowledge-mindmap/) | 知识思维导图：自动分析知识点目录结构，生成 Excalidraw 格式思维导图 | v0.1.0 |

#### Obsidian 工具

| 技能 | 描述 |
|------|------|
| [obsidian-cli](./obsidian-cli/) | Obsidian CLI 交互：读/写/搜索/管理笔记与属性，支持插件开发和调试 |
| [obsidian-markdown](./obsidian-markdown/) | Obsidian 风味 Markdown：wikilinks、embeds、callouts、properties 等语法 |
| [obsidian-bases](./obsidian-bases/) | Obsidian Bases 文件管理：创建/编辑 .base 文件、视图、筛选器、公式 |
| [sortspec-generator](./sortspec-generator/) | 为 Obsidian 文件夹生成 sortspec.md 排序配置文件（Custom Sort 插件） |

#### 搜索与信息

| 技能 | 描述 |
|------|------|
| [smart-search](./smart-search/) | 智能搜索路由器：基于 opencli 的网站/社交媒体/技术资料/新闻搜索 |
| [kaoyan-info](./kaoyan-info/) | 考研信息收集、备考文档整理 |

#### 维护与优化

| 技能 | 描述 |
|------|------|
| [skill-refactor](./skill-refactor/) | 技能自动化重构器：自动提取代码到 code.md、拆分过长内容、优化技能结构 |
| [maintain-learnings](./maintain-learnings/) | .learnings/ 经验库维护：聚类诊断、规则修复、技能同步 |
| [prompt-cache-optimizer](./prompt-cache-optimizer/) | 审计并优化 LLM 提示缓存命中率、输入 token、延迟与调用成本 |
| [security-secret-audit](./security-secret-audit/) | Git 仓库安全审计：检测泄露的 API 密钥、令牌、密码等凭据 |
| [fix-table-pipe](./fix-table-pipe/) | 修复Markdown表格中LaTeX绝对值符号被误解析的问题 |

#### 其他工具

| 技能 | 描述 | 版本 |
|------|------|------|
| [parse-words](./parse-words/) | 英语阅读词汇解析：从 `==highlighted==` 词汇生成词义分析段 | v1.0.0 |
| [chapter-summary](./chapter-summary/) | 章节总结：整理数学/专业课章节笔记，生成结构化总结文件 | - |
| [word-template-generator](./word-template-generator/) | Word文档模板处理 | v1.0.0 |
| [knowledge-learning](./knowledge-learning/) | 通用知识学习辅助 | v1.0.0 |
| [knowledge-base-organizer](./knowledge-base-organizer/) | Obsidian知识库组织、MOC生成 | v1.1.0 |

## 核心特性

### MemOS 集成

多个考研相关技能集成了 MemOS 记忆系统，实现：

- 用户画像持久化存储
- 跨设备学习进度同步
- 个性化错误追踪
- 千人千面的学习建议

### 跨学科关联

技能之间支持知识关联，例如：

- 数学知识点与电子技术应用的关联
- 英语词汇与写作场景的结合
- 统一错误模型支持跨技能聚合

### 路由器架构

考研主技能采用路由器架构，按需调度子技能：

```
kaoyan-math (路由器) v4.0.0
    ├─→ kaoyan-math-core      (核心协调：MemOS、调度信号、错误模型)
    ├─→ kaoyan-math-notes     (笔记生成更新：LaTeX、知识点模板)
    └─→ kaoyan-math-structure (知识点结构：高数/线代/概率模块)

kaoyan-english (路由器) v4.0.0
    ├─→ kaoyan-english-core    (核心协调：MemOS、调度信号、记忆压缩)
    ├─→ kaoyan-english-vocab   (词汇管理：PDF提取、查词、熟词僻义)
    ├─→ kaoyan-english-review  (复习计划：SM-2算法、统计追踪)
    ├─→ kaoyan-english-quiz    (单词测试：词义、搭配、僻义测试)
    └─→ kaoyan-english-writing (写作训练：替换、汉译英、词义辨析)

kaoyan-electronics (路由器) v2.0.0
    ├─→ kaoyan-electronics-core     (核心协调：MemOS、跨学科关联、考点权重)
    ├─→ kaoyan-electronics-sop      (SOP模板：17个标准化解题流程)
    ├─→ kaoyan-electronics-circuit  (电路图解析：静态+动态分析)
    └─→ kaoyan-electronics-structure (知识点结构：知识图谱、前置知识)
```

## 安装使用

### 前置要求

- [Claude Code](https://claude.com/claude-code) CLI 工具
- 将技能目录放置在 Claude Code 的技能加载路径中

### 技能结构

每个技能目录包含：

```
skill-name/
├── SKILL.md          # 技能定义文件（必需）
├── README.md         # 技能说明文档
├── scripts/          # Python脚本（可选）
├── templates/        # 模板文件（可选）
└── references/       # 参考资源（可选）
```

### 触发技能

在 Claude Code 中，根据描述自动触发相应的技能。

例如：
- "帮我生成考研数学笔记" → 触发 `kaoyan-math`
- "制定今天的考研学习计划" → 触发 `kaoyan-plan`
- "整理这个英语词汇表" → 触发 `kaoyan-english`
- "画一个流程图" → 触发 `excalidraw-diagram`
- "整理这道错题" → 触发 `mistake-book`
- "我这样理解对不对" → 触发 `understanding`
- "帮我查一下这个信息" → 触发 `smart-search`

### 日常任务入口

| 用户意图 | 首选入口 |
|----------|----------|
| 今天怎么安排、补课、复盘、完成汇报 | `/kaoyan-plan` |
| 数学概念、笔记、题目、结构 | `/kaoyan-math` |
| 英语单词、阅读词汇、复习、测试、写作 | `/kaoyan-english` |
| 822 专业课、电路图、SOP、知识结构 | `/kaoyan-electronics` |
| 我这样理解对不对、推导检查 | `/understanding` |
| 记录错题、提炼错题、优化错题索引 | `/mistake-book` |
| 同步上下文 | `/sync` |

## 开发指南

### 创建新技能

新技能须满足[准入规则](./SKILL_SYSTEM.md#5-新技能准入规则)至少两条：

1. 创建技能目录和 `SKILL.md` 文件
2. 在 `SKILL.md` 中定义技能元数据（name, description, version）
3. 编写技能逻辑和处理流程
4. 添加 `README.md` 说明文档

### SKILL.md 格式

```yaml
---
name: skill-name
description: 技能描述
version: 1.0.0
author: 作者名
dependencies: []
tags: []
---

# 技能名称

技能详细说明...
```

### 维护检查清单

每次修改技能体系后检查：

- `SKILL.md` 不超过 300 行；长模板和代码已拆分到外部文件
- Obsidian 表格、LaTeX 管道符、证明折叠块符合项目规则
- `.claude/skills` 与 `SKILL.md` 能力等价
- 新增学习规则没有直接写进 `CLAUDE.md`，而是进入 `.learnings/RULES.md`

## 项目结构

```
skill/
├── README.md                    # 本文件
├── SKILL_SYSTEM.md              # 技能体系地图（架构总纲）
│
├── # L1 入口路由
├── kaoyan-plan/                 # 考研学习计划
├── kaoyan-math/                 # 考研数学路由器
├── kaoyan-english/              # 考研英语路由器
├── kaoyan-electronics/          # 电子技术基础路由器
├── understanding/               # 理解验证
├── mistake-book/                # 错题整理
├── digest/                      # 学习消化
│
├── # L2 考研数学子技能
├── kaoyan-math-core/            # 数学核心协调层
├── kaoyan-math-notes/           # 数学笔记生成
├── kaoyan-math-structure/       # 数学知识点结构
├── kaoyan-math-summary/         # 数学章节总结
│
├── # L2 考研英语子技能
├── kaoyan-english-core/         # 英语核心协调层
├── kaoyan-english-vocab/        # 英语词汇管理
├── kaoyan-english-review/       # 英语复习计划
├── kaoyan-english-quiz/         # 英语单词测试
├── kaoyan-english-writing/      # 英语写作训练
│
├── # L2 822电子技术子技能
├── kaoyan-electronics-core/     # 电子技术核心协调层
├── kaoyan-electronics-sop/      # 电子技术SOP模板库
├── kaoyan-electronics-circuit/  # 电路图解析
├── kaoyan-electronics-structure/ # 电子技术知识点结构
│
├── # L2 错题子技能
├── mistake-extract/             # 错题精华提炼
├── mistake-restructure/         # 错题本结构优化
│
├── # L3 图示工具
├── excalidraw-diagram/          # Excalidraw图生成
├── math-graph/                  # 数学函数绘图
├── knowledge-mindmap/           # 知识思维导图
│
├── # L3 Obsidian 工具
├── obsidian-cli/                # Obsidian CLI交互
├── obsidian-markdown/           # Obsidian Markdown格式
├── obsidian-bases/              # Obsidian Bases
├── sortspec-generator/          # 排序配置生成
│
├── # L3 搜索与信息
├── smart-search/                # 智能搜索
├── kaoyan-info/                 # 考研信息
│
├── # L3 维护与优化
├── skill-refactor/              # 技能重构器
├── maintain-learnings/          # 经验库维护
├── prompt-cache-optimizer/      # 提示缓存优化
├── security-secret-audit/       # 安全审计
├── fix-table-pipe/              # 表格管道符修复
│
├── # L3 其他工具
├── parse-words/                 # 词汇解析
├── chapter-summary/             # 章节总结
├── word-template-generator/     # Word模板生成
├── knowledge-learning/          # 知识学习
└── knowledge-base-organizer/    # 知识库组织
```

## 版本历史

- **2026-07**: 技能体系重构，引入三层架构（L1/L2/L3），技能数量扩展至 40+
  - 新增 L1 入口：`understanding`、`digest`
  - 新增 L2 子技能：`mistake-extract`、`mistake-restructure`
  - 新增 L3 工具：Obsidian 系列（`cli`/`markdown`/`bases`/`sortspec`）、`smart-search`、`skill-refactor`、`maintain-learnings`、`parse-words`、`chapter-summary`、`prompt-cache-optimizer`、`security-secret-audit`
  - 确立新技能准入规则和维护检查清单（见 `SKILL_SYSTEM.md`）
- **2026-03-25**: 路由器架构完成
  - kaoyan-math v4.0.0: 拆分为3个子技能（core/notes/structure）
  - kaoyan-english v4.0.0: 拆分为5个子技能（core/vocab/review/quiz/writing）
  - kaoyan-electronics v2.0.0: 拆分为4个子技能（core/sop/circuit/structure）
  - kaoyan-plan v3.13.0: 修复完成记录和学习日志问题
- **2026-03**: 新增 excalidraw-diagram v1.2.1、math-graph、mistake-book 等通用工具技能
- **2026-02**: 添加 MemOS 集成支持、跨学科关联功能
- **2026-02**: 初始版本，包含8个核心技能

## 许可证

本项目技能仅供个人学习使用。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这些技能。
