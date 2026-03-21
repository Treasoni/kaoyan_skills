---
name: kaoyan-electronics
description: This skill routes 822 electronics learning requests to specialized sub-skills for 湖南大学822电子技术基础考研 preparation, including circuit diagram analysis, SOP templates for 17 problem types, knowledge point structure, and MemOS integration for persistent tracking.
---

# 822电子技术基础技能路由器 (Kaoyan Electronics Router)

> 📁 详细代码实现见 [code.md](code.md)

## 技能概述

本技能是822电子技术基础学习的**路由入口**，负责识别用户意图并路由到对应的子技能：

```
kaoyan-electronics (路由器)
    ↓ 识别意图后调用
    ├─→ kaoyan-electronics-core     (核心协调层：MemOS集成、调度信号、跨学科关联)
    ├─→ kaoyan-electronics-sop      (SOP模板库：17个标准化解题流程)
    ├─→ kaoyan-electronics-circuit  (电路图解析：智能识别、静态+动态分析)
    └─→ kaoyan-electronics-structure (知识点结构：知识图谱、前置知识关联)
```

## v2.0.0 更新说明

原技能（v1.2.0，约1400行）已拆分为4个独立子技能：
- **kaoyan-electronics-core**: MemOS集成、调度信号处理、跨学科关联、数学前置检查、考点权重
- **kaoyan-electronics-sop**: 17个SOP模板、康华光符号体系、LaTeX标准、Mermaid波形图
- **kaoyan-electronics-circuit**: 电路图智能识别、静态分析+动态分析
- **kaoyan-electronics-structure**: 知识点图谱、前置知识关联、知识点卡片模板

**拆分优势**：
- 每个子技能功能专注，易于维护
- 触发条件更精准，减少冲突
- 用户可直接调用特定功能的子技能

---

## 子技能速查

| 子技能 | 功能描述 | 触发关键词 |
|--------|----------|------------|
| **kaoyan-electronics-circuit** | 电路图分析 | "电路图"、"分析电路"、"静态分析"、"动态分析" |
| **kaoyan-electronics-sop** | SOP模板/解题步骤 | "怎么做"、"解题步骤"、"反馈类型判断"、"计数器设计" |
| **kaoyan-electronics-structure** | 知识点结构 | "知识点结构"、"前置知识"、"复习XX"、"知识图谱" |
| **kaoyan-electronics-core** | 核心协调层 | "配置"、"状态"、"欠账检查"、"跨学科" |

---

## 路由逻辑

当用户请求涉及822电子技术基础学习时，本技能会：

1. **分析用户意图**：识别用户想要完成的具体任务
2. **选择子技能**：根据意图匹配最合适的子技能
3. **调用子技能**：将用户请求传递给对应的子技能处理
4. **返回结果**：将子技能的处理结果返回给用户

### 意图分类规则

> 📁 详细代码实现见 [code.md](code.md)

| 优先级 | 触发条件 | 路由目标 |
|--------|----------|----------|
| 1 | "电路图"、"分析电路"、"静态分析"、"动态分析" | kaoyan-electronics-circuit |
| 2 | "怎么做"、"解题步骤"、"SOP"、"反馈类型判断" | kaoyan-electronics-sop |
| 3 | "知识点结构"、"知识图谱"、"前置知识"、"复习XX" | kaoyan-electronics-structure |
| 4 | "配置"、"状态"、"欠账检查"、"跨学科" | kaoyan-electronics-core |
| 5 | 上传图片 | kaoyan-electronics-circuit |
| 6 | 通用电子技术请求 | 智能推断（默认sop） |

---

## 使用示例

### 示例1: 电路图分析

**用户输入**："帮我分析这个电路" [上传电路图]

**路由流程**:
1. 识别关键词："分析电路" + 图片上传
2. 匹配子技能：`kaoyan-electronics-circuit`
3. 调用子技能处理请求

### 示例2: 解题步骤

**用户输入**："负反馈类型判断怎么做？"

**路由流程**:
1. 识别关键词："怎么做"、"反馈类型判断"
2. 匹配子技能：`kaoyan-electronics-sop`
3. 调用子技能返回SOP步骤

### 示例3: 知识点复习

**用户输入**："帮我复习负反馈"

**路由流程**:
1. 识别关键词："复习"、"负反馈"
2. 匹配子技能：`kaoyan-electronics-structure`
3. 调用子技能返回知识点卡片

### 示例4: 状态检查

**用户输入**："检查我的电子技术学习进度"

**路由流程**:
1. 识别关键词："检查"、"学习进度"
2. 匹配子技能：`kaoyan-electronics-core`
3. 调用子技能从MemOS读取进度

---

## 直接调用子技能

用户也可以直接调用子技能，跳过路由器：

```markdown
# 直接调用示例
- 使用 kaoyan-electronics-circuit 分析电路图
- 使用 kaoyan-electronics-sop 查询反馈类型判断SOP
- 使用 kaoyan-electronics-structure 复习计数器知识点
- 使用 kaoyan-electronics-core 检查学习状态
```

---

## 技能集成

### 子技能依赖关系

```
kaoyan-electronics (路由器)
    ↓
    ├─→ kaoyan-electronics-core (MemOS集成，被其他技能调用)
    │        ↓
    │        ├─→ kaoyan-electronics-sop (调用core保存错误记录)
    │        ├─→ kaoyan-electronics-circuit (调用core记录电路分析错误)
    │        └─→ kaoyan-electronics-structure (调用core获取知识点关系)
```

### 协同技能

| 技能 | 协同场景 |
|------|----------|
| kaoyan-plan | 提供每日计划时间分配，发送调度信号 |
| kaoyan-math | 跨学科知识关联（数学→电子技术） |
| obsidian-markdown | 创建Obsidian笔记 |

---

## 迁移说明

### 从 v1.2.0 迁移到 v2.0.0

**功能对等**：所有v1.2.0的功能在v2.0.0的子技能中都保留。

| v1.2.0 功能 | v2.0.0 子技能 |
|-------------|---------------|
| 电路图智能解析 | kaoyan-electronics-circuit |
| 17个SOP模板 | kaoyan-electronics-sop |
| 知识图谱主动关联 | kaoyan-electronics-structure |
| MemOS记忆追踪 | kaoyan-electronics-core |
| 康华光符号体系 | kaoyan-electronics-sop + circuit |
| Mermaid波形图 | kaoyan-electronics-sop |
| 考点权重动态记忆 | kaoyan-electronics-core |
| 数学前置检查 | kaoyan-electronics-core |
| 跨学科提醒 | kaoyan-electronics-core |
| 统一错误模型 | kaoyan-electronics-core |
| 调度信号处理 | kaoyan-electronics-core |

---

## 验证标准

1. ✅ 能够正确识别用户意图
2. ✅ 能够路由到正确的子技能
3. ✅ 子技能功能完整（不丢失原功能）
4. ✅ 用户使用体验不变
5. ✅ 支持直接调用子技能

---

## 文件路径

### 本技能文件

- `/kaoyan-electronics/SKILL.md` - 路由器技能
- `/kaoyan-electronics/code.md` - 路由逻辑代码实现

### 子技能文件

- `/kaoyan-electronics-core/SKILL.md`
- `/kaoyan-electronics-sop/SKILL.md`
- `/kaoyan-electronics-circuit/SKILL.md`
- `/kaoyan-electronics-structure/SKILL.md`

### 数据文件（被子技能引用）

- `/kaoyan-electronics/scripts/templates/sop_library.md`
- `/kaoyan-electronics/scripts/data/knowledge_graph_electronics.yaml`
- `/kaoyan-electronics/scripts/data/exam_weights.yaml`
- `/kaoyan-electronics/scripts/templates/knowledge_card_electronics.md`
- `/kaoyan-electronics/scripts/templates/latex_guide_electronics.md`
- `/kaoyan-electronics/scripts/templates/mermaid_guide_electronics.md`
- `/kaoyan-electronics/scripts/templates/mistake_record_electronics.md`

---

*创建日期: 2026-02-26*
*最后更新: 2026-03-12 (v2.0.0 拆分版)*
*维护者: Claude Code + 用户协作*
