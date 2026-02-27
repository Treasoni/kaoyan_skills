# Agent Skills Collection

一个为 Claude Code 设计的技能（Skills）集合，专注于考研学习和知识管理场景。

## 项目概述

本项目包含多个可复用的 Agent Skills，每个技能都是一个独立的功能模块，可以通过 Claude Code 的 Skill 工具调用。这些技能主要用于：

- **考研备考**：数学、英语、电子技术等学科的学习辅助
- **计划管理**：学习计划生成、进度追踪
- **知识管理**：笔记生成、知识库组织、文档处理

## 技能列表

| 技能 | 描述 | 版本 |
|------|------|------|
| [kaoyan-math](./kaoyan-math/) | 考研数学学习笔记生成，支持LaTeX格式、MemOS集成、跨学科关联 | v3.1.0 |
| [kaoyan-english](./kaoyan-english/) | 考研英语词汇管理、间隔重复、写作练习，集成MemOS | v2.0.0 |
| [kaoyan-plan](./kaoyan-plan/) | 考研学习计划生成，支持课表解析、任务分配、欠账管理 | v3.2.0 |
| [kaoyan-electronics](./kaoyan-electronics/) | 湖南大学822电子技术基础，支持电路图解析、SOP库 | v1.2.0 |
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
├── kaoyan-math/                 # 考研数学
├── kaoyan-english/              # 考研英语
├── kaoyan-plan/                 # 考研计划
├── kaoyan-electronics/          # 电子技术基础
├── kaoyan-info/                 # 考研信息
├── knowledge-learning/          # 知识学习
├── knowledge-base-organizer/    # 知识库组织
└── word-template-generator/     # Word模板生成
```

## 版本历史

- **2025-02**: 初始版本，包含8个核心技能
- **2025-02**: 添加 MemOS 集成支持
- **2025-02**: 添加跨学科关联功能

## 许可证

本项目技能仅供个人学习使用。

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这些技能。
