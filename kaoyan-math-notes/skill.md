---
name: kaoyan-math-notes
description: This skill handles note generation and updates for 考研数学 (Chinese graduate entrance math exam) preparation. Use it when users want to generate exam-oriented study notes from existing materials, update notes based on feedback, or create structured learning content with LaTeX formatting.
version: 1.1.0
---

# 考研数学笔记生成更新技能

> 代码与模板：Python 逻辑见 [code.md](code.md)，笔记模板见 [templates/knowledge-point-template.md](templates/knowledge-point-template.md)

## 技能概述

本技能专注于考研数学笔记的生成和更新，帮助用户：
1. **基于现成笔记生成考研学习笔记**
2. **根据反馈更新笔记**
3. **LaTeX格式强制**
4. **已有笔记保护机制**

核心特色：个性化学习轨迹记录（"我的理解记录"）、错误模式追踪（"我的错误类型"）、与 kaoyan-math-core 集成支持 MemOS 持久化。

---

## 触发条件

**触发**：「生成考研数学笔记」「帮我整理成考研笔记」「更新/补充数学笔记」「这个知识点不太明白」

**不触发**：查询知识点结构 → `kaoyan-math-structure`；配置/欠账 → `kaoyan-math-core`

---

## 笔记生成规范

### 内容生成来源

1. 高数资料目录：`/Users/zhqznc/Documents/高数资料/`
2. 优先级：用户提供的 README.md 内容 → 高数资料 → AI 通用补充
3. 定义、定理、例题优先来自高数资料

### 已有笔记保护机制 ⚠️

1. 生成前检查目标路径是否已有笔记文件
2. 不下覆盖已有内容
3. 只为缺失知识点创建新文件
4. 告知用户哪些已存在、哪些将新建

```python
def check_existing_notes(target_path, knowledge_points):
    existing, to_create = [], []
    for kp in knowledge_points:
        file_path = f"{target_path}/{kp}.md"
        (existing if os.path.exists(file_path) and has_content(file_path) else to_create).append(kp)
    return {"existing": existing, "to_create": to_create}
```

---

## 数学公式格式标准 ⚠️

所有数学公式使用 LaTeX：行内 `$...$`，独立公式 `$$...$$`。常用符号映射见 [code.md](code.md)。

---

## 核心功能

### 功能1：基于现成笔记生成考研学习笔记

输入：用户笔记 + 模块信息（高数/线代 + 章节）→ 输出：结构化 Obsidian 笔记（含考试重点、题型、易错点、例题）

### 功能2：根据反馈更新笔记

输入：已有笔记路径 + 用户反馈（理解困难点、希望补充的内容）
→ 分析理解障碍 → 优化表达 → 添加辅助内容 → 标注易错点 → 记录思维过程

---

## 输出格式

笔记按 [templates/knowledge-point-template.md](templates/knowledge-point-template.md) 生成，包含：原始定义、直观理解、定理条件、考试重点、典型题型、解题方法、易错点、我的理解记录、错误类型、例题、相关知识点。

---

## 更新标记

```markdown
<!-- UPDATE: YYYY-MM-DD 用户反馈不理解XX -->
[补充内容]
<!-- END UPDATE -->
```

---

## 文件组织

```
考研数学/{模块}/
├── 📑 索引.md
├── 📊 学习进度.md
└── {章节}/  — 按知识点分文件
```

完整目录结构见 [kaoyan-math-structure](../../kaoyan-math-structure/SKILL.md)。

---

## 技能集成

| 技能 | 用途 |
|------|------|
| kaoyan-math-core | 错误记录、个性化提醒 |
| kaoyan-math-structure | 知识点结构、目录模板 |
| obsidian-markdown | 创建 Obsidian 笔记 |

---

*创建日期: 2026-03-10*
*版本: 1.1.0 (模板提取到 templates/, 2026-07-12)*
