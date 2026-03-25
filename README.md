# Agent Skills Collection

一个为 Claude Code 设计的技能（Skills）集合，专注于考研学习和知识管理场景。

## 项目概述

本项目包含多个可复用的 Agent Skills，每个技能都是一个独立的功能模块，可以通过 Claude Code 的 Skill 工具调用。这些技能主要用于：

- **考研备考**：数学、英语、电子技术等学科的学习辅助
- **计划管理**：学习计划生成、进度追踪
- **知识管理**：笔记生成、知识库组织、文档处理

## 技能列表

### 考研主技能（路由器）

| 技能 | 描述 | 版本 |
|------|------|------|
| [kaoyan-math](./kaoyan-math/) | 考研数学路由器，调度到子技能（笔记生成、知识点结构、核心协调） | v4.0.0 |
| [kaoyan-english](./kaoyan-english/) | 考研英语路由器，调度到子技能（词汇、复习、测试、写作） | v4.0.0 |
| [kaoyan-plan](./kaoyan-plan/) | 考研学习计划生成，支持课表解析、任务分配、欠账管理、MemOS集成 | v3.13.0 |
| [kaoyan-electronics](./kaoyan-electronics/) | 822电子技术基础路由器，调度到子技能（电路分析、SOP、知识点结构） | v2.0.0 |

### 考研数学子技能

| 技能 | 描述 |
|------|------|
| [kaoyan-math-core](./kaoyan-math-core/) | 核心协调层：MemOS集成、调度信号、统一错误模型、跨学科关联 |
| [kaoyan-math-notes](./kaoyan-math-notes/) | 笔记生成更新：LaTeX格式强制、知识点模板、已有笔记保护 |
| [kaoyan-math-structure](./kaoyan-math-structure/) | 知识点结构模板：高数/线代/概率模块参考 |
| [kaoyan-math-summary](./kaoyan-math-summary/) | 章节笔记整理：提取定义定理公式、保留个人理解、生成结构化总结 |

### 考研英语子技能

| 技能 | 描述 |
|------|------|
| [kaoyan-english-core](./kaoyan-english-core/) | 核心协调层：MemOS集成、调度信号处理、记忆压缩模式 |
| [kaoyan-english-vocab](./kaoyan-english-vocab/) | 词汇管理：PDF词汇提取、查词、熟词僻义检测、真题语境 |
| [kaoyan-english-review](./kaoyan-english-review/) | 复习计划：SM-2复习计划、统计追踪、分阶段策略 |
| [kaoyan-english-quiz](./kaoyan-english-quiz/) | 单词测试：词义测试、搭配测试、僻义测试 |
| [kaoyan-english-writing](./kaoyan-english-writing/) | 写作训练：写作替换、汉译英、词义辨析 |

### 822电子技术子技能

| 技能 | 描述 |
|------|------|
| [kaoyan-electronics-core](./kaoyan-electronics-core/) | 核心协调层：MemOS集成、调度信号、跨学科关联、数学前置检查 |
| [kaoyan-electronics-sop](./kaoyan-electronics-sop/) | SOP模板库：17个标准化解题流程（模电8+数电9）、康华光符号体系 |
| [kaoyan-electronics-circuit](./kaoyan-electronics-circuit/) | 电路图解析：智能识别、静态分析+动态分析、MCP工具集成 |
| [kaoyan-electronics-structure](./kaoyan-electronics-structure/) | 知识点结构：知识图谱、前置知识关联、知识点卡片模板 |

### 通用工具技能

| 技能 | 描述 | 版本 |
|------|------|------|
| [excalidraw-diagram](./excalidraw-diagram/) | Excalidraw图生成：流程图、思维导图、关系图等，支持Obsidian/标准/动画三种模式 | v1.2.1 |
| [math-graph](./math-graph/) | 数学函数绘图：Python+Matplotlib生成教科书级函数图像，多图对比 | v1.0.0 |
| [mistake-book](./mistake-book/) | 错题整理：快速整理错题到学科错题本，自动格式化、更新索引 | v1.0.0 |
| [fix-table-pipe](./fix-table-pipe/) | 修复Markdown表格中LaTeX绝对值符号被误解析的问题 | - |
| [knowledge-mindmap](./knowledge-mindmap/) | 知识思维导图：生成知识点关联图 | - |

### 其他技能

| 技能 | 描述 | 版本 |
|------|------|------|
| [kaoyan-info](./kaoyan-info/) | 考研信息收集、备考文档整理 | - |
| [knowledge-learning](./knowledge-learning/) | 通用知识学习辅助 | - |
| [knowledge-base-organizer](./knowledge-base-organizer/) | Obsidian知识库组织、MOC生成 | - |
| [word-template-generator](./word-template-generator/) | Word文档模板处理 | - |

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
└── templates/        # 模板文件（可选）
```

### 触发技能

在 Claude Code 中，根据技能描述自动触发相应的技能。

例如：
- "帮我生成考研数学笔记" → 触发 `kaoyan-math`
- "制定今天的考研学习计划" → 触发 `kaoyan-plan`
- "整理这个英语词汇表" → 触发 `kaoyan-english`
- "画一个流程图" → 触发 `excalidraw-diagram`
- "整理这道错题" → 触发 `mistake-book`

## 开发指南

### 创建新技能

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

## 项目结构

```
skill/
├── README.md                    # 本文件
│
│  # 考研主技能（路由器）
├── kaoyan-math/                 # 考研数学路由器
├── kaoyan-english/              # 考研英语路由器
├── kaoyan-plan/                 # 考研计划
├── kaoyan-electronics/          # 电子技术基础路由器
│
│  # 考研数学子技能
├── kaoyan-math-core/            # 数学核心协调层
├── kaoyan-math-notes/           # 数学笔记生成
├── kaoyan-math-structure/       # 数学知识点结构
├── kaoyan-math-summary/         # 数学章节总结
│
│  # 考研英语子技能
├── kaoyan-english-core/         # 英语核心协调层
├── kaoyan-english-vocab/        # 英语词汇管理
├── kaoyan-english-review/       # 英语复习计划
├── kaoyan-english-quiz/         # 英语单词测试
├── kaoyan-english-writing/      # 英语写作训练
│
│  # 822电子技术子技能
├── kaoyan-electronics-core/     # 电子技术核心协调层
├── kaoyan-electronics-sop/      # 电子技术SOP模板库
├── kaoyan-electronics-circuit/  # 电路图解析
├── kaoyan-electronics-structure/ # 电子技术知识点结构
│
│  # 通用工具技能
├── excalidraw-diagram/          # Excalidraw图生成
├── math-graph/                  # 数学函数绘图
├── mistake-book/                # 错题整理
├── fix-table-pipe/              # 表格管道符修复
├── knowledge-mindmap/           # 知识思维导图
│
│  # 其他技能
├── kaoyan-info/                 # 考研信息
├── knowledge-learning/          # 知识学习
├── knowledge-base-organizer/    # 知识库组织
└── word-template-generator/     # Word模板生成
```

## 版本历史

- **2026-03-25**: 路由器架构完成
  - kaoyan-math v4.0.0: 拆分为3个子技能（core/notes/structure）
  - kaoyan-english v4.0.0: 拆分为5个子技能（core/vocab/review/quiz/writing）
  - kaoyan-electronics v2.0.0: 拆分为4个子技能（core/sop/circuit/structure）
  - kaoyan-plan v3.13.0: 修复完成记录和学习日志问题
- **2026-03**: 新增 excalidraw-diagram v1.2.1、math-graph、mistake-book 等通用工具技能
- **2026-02**: 添加 MemOS 集成支持
- **2026-02**: 添加跨学科关联功能
- **2026-02**: 初始版本，包含8个核心技能

## 许可证

本项目技能仅供个人学习使用。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这些技能。
