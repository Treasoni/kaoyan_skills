---
name: kaoyan-math
description: This skill routes mathematics learning requests to specialized sub-skills for 考研数学 (Chinese graduate entrance math exam) preparation, including note generation with LaTeX formatting, knowledge point structure templates, and core infrastructure with MemOS integration for persistent mistake tracking and cross-device synchronization.
version: 4.0.0
---

# 考研数学技能路由器 (Kaoyan Math Router)

## 技能概述

本技能是考研数学学习的**路由入口**，负责识别用户意图并路由到对应的子技能：

```
kaoyan-math (路由器)
    ↓ 识别意图后调用
    ├─→ kaoyan-math-core      (核心协调层：MemOS集成、调度信号、错误模型)
    ├─→ kaoyan-math-notes     (笔记生成更新：LaTeX格式、知识点模板)
    └─→ kaoyan-math-structure (知识点结构：高数/线代/概率模块)
```

## v4.0.0 更新说明

原技能（v3.2.0，约1760行）已拆分为4个独立文件：
- **kaoyan-math-core**: MemOS集成、调度信号、统一错误模型、跨学科关联、知识点联动
- **kaoyan-math-notes**: 笔记生成更新、LaTeX格式强制、知识点模板、已有笔记保护
- **kaoyan-math-structure**: 知识点结构模板、高数/线代/概率模块参考
- **kaoyan-math**: 路由器（本文件）

**拆分优势**：
- 每个子技能功能专注，易于维护
- 触发条件更精准，减少冲突
- 用户可直接调用特定功能的子技能

---

## 子技能速查

| 子技能 | 功能描述 | 触发关键词 |
|--------|----------|------------|
| **kaoyan-math-notes** | 笔记生成+更新 | "生成考研数学笔记"、"更新数学笔记"、"我对XX不理解"、"听课时不理解" |
| **kaoyan-math-structure** | 知识点结构 | "数学知识点结构"、"高数目录"、"极限章节结构"、"知识点关系图" |
| **kaoyan-math-core** | 核心协调层 | "数学学习配置"、"数学状态"、"数学欠账检查"、"跨学科关联" |

---

## 路由逻辑

当用户请求涉及考研数学学习时，本技能会：

1. **分析用户意图**：识别用户想要完成的具体任务
2. **选择子技能**：根据意图匹配最合适的子技能
3. **调用子技能**：将用户请求传递给对应的子技能处理
4. **返回结果**：将子技能的处理结果返回给用户

### 意图分类规则

```python
# 伪代码
def route_math_request(user_input):
    """路由数学学习请求"""

    # 1. 笔记生成/更新相关
    if any(keyword in user_input for keyword in [
        "生成考研数学笔记", "整理成考研笔记", "更新数学笔记",
        "我对XX不理解", "听课时不理解", "补充数学笔记"
    ]):
        return invoke_skill("kaoyan-math-notes", user_input)

    # 2. 知识点结构相关
    elif any(keyword in user_input for keyword in [
        "数学知识点结构", "高数目录", "极限章节结构",
        "线代知识点", "概率知识点", "知识点关系图"
    ]):
        return invoke_skill("kaoyan-math-structure", user_input)

    # 3. 核心配置相关
    elif any(keyword in user_input for keyword in [
        "数学学习配置", "数学状态", "数学欠账检查",
        "数学疲劳检查", "跨学科关联"
    ]):
        return invoke_skill("kaoyan-math-core", user_input)

    # 4. 通用数学学习请求 - 智能推断
    elif "数学" in user_input or "考研" in user_input:
        # 根据上下文推断用户意图
        context = analyze_context(user_input)
        if context.has_notes:
            return invoke_skill("kaoyan-math-notes", user_input)
        elif context.needs_structure:
            return invoke_skill("kaoyan-math-structure", user_input)
        else:
            return invoke_skill("kaoyan-math-core", user_input)

    # 5. 默认：笔记生成（最常见场景）
    else:
        return invoke_skill("kaoyan-math-notes", user_input)
```

---

## 使用示例

### 示例1: 笔记生成

**用户输入**："这是我的极限笔记，帮我生成考研学习笔记"

**路由流程**:
1. 识别关键词："极限笔记"、"生成考研学习笔记"
2. 匹配子技能：`kaoyan-math-notes`
3. 调用子技能处理请求

### 示例2: 笔记更新

**用户输入**："我对洛必达法则的条件不太理解"

**路由流程**:
1. 识别关键词："不理解"
2. 匹配子技能：`kaoyan-math-notes`
3. 调用子技能更新笔记

### 示例3: 知识点结构

**用户输入**："高数极限章节的知识点结构是什么？"

**路由流程**:
1. 识别关键词："知识点结构"、"极限章节"
2. 匹配子技能：`kaoyan-math-structure`
3. 调用子技能返回结构信息

### 示例4: 状态检查

**用户输入**："检查我的数学学习进度"

**路由流程**:
1. 识别关键词："检查"、"学习进度"
2. 匹配子技能：`kaoyan-math-core`
3. 调用子技能从MemOS读取进度

---

## 直接调用子技能

用户也可以直接调用子技能，跳过路由器：

```markdown
# 直接调用示例
- 使用 kaoyan-math-notes 生成极限笔记
- 使用 kaoyan-math-structure 查看高数目录
- 使用 kaoyan-math-core 检查学习状态
```

---

## 技能集成

### 子技能依赖关系

```
kaoyan-math (路由器)
    ↓
    ├─→ kaoyan-math-core (MemOS集成，被其他技能调用)
    │        ↓
    │        ├─→ kaoyan-math-notes (调用core保存错误记录)
    │        └─→ kaoyan-math-structure (调用core获取知识点关系)
```

### 协同技能

| 技能 | 协同场景 |
|------|----------|
| kaoyan-plan | 提供每日计划时间分配，发送调度信号 |
| kaoyan-electronics | 跨学科知识关联（数学→电子技术） |
| obsidian-markdown | 创建Obsidian笔记 |

---

## 迁移说明

### 从 v3.2.0 迁移到 v4.0.0

**功能对等**：所有v3.2.0的功能在v4.0.0的子技能中都保留。

| v3.2.0 功能 | v4.0.0 子技能 |
|-------------|---------------|
| 笔记生成规范 | kaoyan-math-notes |
| MemOS集成 | kaoyan-math-core |
| 笔记生成 | kaoyan-math-notes |
| 笔记更新 | kaoyan-math-notes |
| LaTeX格式 | kaoyan-math-notes |
| 知识点模板 | kaoyan-math-notes |
| 知识点联动 | kaoyan-math-core |
| 跨学科关联 | kaoyan-math-core |
| 调度信号处理 | kaoyan-math-core |
| 统一错误模型 | kaoyan-math-core |
| 知识点结构模板 | kaoyan-math-structure |
| 高数/线代/概率结构 | kaoyan-math-structure |

---

## 验证标准

1. ✅ 能够正确识别用户意图
2. ✅ 能够路由到正确的子技能
3. ✅ 子技能功能完整（不丢失原功能）
4. ✅ 用户使用体验不变
5. ✅ 支持直接调用子技能

---

## 文件路径

### 子技能文件

- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-math-core/skill.md`
- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-math-notes/skill.md`
- `/Users/zhqznc/Documents/考研复习/.claude/skills/kaoyan-math-structure/skill.md`

---

*创建日期: 2026-02-26*
*最后更新: 2026-03-10 (v4.0.0 拆分版)*
*维护者: Claude Code + 用户协作*
