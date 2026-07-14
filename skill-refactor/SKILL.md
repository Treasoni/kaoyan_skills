---
name: skill-refactor
description: 技能自动化重构器 - 自动提取代码到code.md、拆分过长内容、优化技能结构。**自动触发**：每次修改.claude/skills目录下的SKILL.md或code.md后检测并提示用户确认。手动触发：当用户提到"重构技能"、"拆分技能"、"技能代码分离"、"优化技能结构"时使用此skill。
---

# 技能自动化重构器 (Skill Refactor)

> 📁 详细代码实现见 [code.md](code.md)

## 功能概述

本技能用于自动化维护和优化其他技能的文件结构：

1. **代码分离**：自动识别并���取 SKILL.md 中的代码块到 code.md
2. **内容拆分**：当文件过长时智能拆分为多个模块
3. **结构优化**：保持功能完整性，添加模块引用

---

## 触发条件

### 自动触发（混合模式）

当检测到以下情况时，**提示用户确认后执行**：
- 写入 `.claude/skills/**/SKILL.md` 后检测到：
  - 包含可提取的代码块
  - 文件行数 > 300行
- 写入 `.claude/skills/**/code.md` 后检测到：
  - 文件行数 > 400行

### 手动触发

- "重构技能"、"拆分技能"
- "技能代码分离"、"优化技能结构"
- "整理技能文件"、"技能模块化"

---

## 阈值配置

| 文件类型 | 行数阈值 | 触发操作 |
|----------|----------|----------|
| SKILL.md | > 300行 | 内容拆分 |
| code.md | > 400行 | 模块化拆分 |

### 用户确认机制

检测到需要重构时，显示预览并询问用户：

```
🔍 检测到 {skill_name} 需要重构：
- 包含 X 个代码块可提取
- 文件长度 Y 行（超过阈值）

是否执行重构？
[✅ 立即执行] [⏭️ 跳过] [📋 查看详情]
```

---

## 工作流程

### 1. 代码提取流程

```
SKILL.md (包含代码块)
    ↓ 分析
识别 ```python``` 等代码块
    ↓ 提取
创建/更新 code.md
    ↓ 引用
在 SKILL.md 添加 > 📁 详见 [code.md](code.md)
```

### 2. 内容拆分流程

```
SKILL.md (> 300行)
    ↓ 分析章节结构
按 ## 标题分组
    ↓ 拆分
├── SKILL.md (主文档，< 150行)
├── modules/overview.md (模块概览)
├── modules/module1.md (模块1详细)
└── modules/module2.md (模块2详细)
```

### 3. code.md 拆分流程

```
code.md (> 400行)
    ↓ 分析代码结构
按功能模块分组
    ↓ 拆分
├── code.md (主入口)
├── scripts/core.py (核心函数)
├── scripts/utils.py (工具函数)
└── scripts/constants.py (常量定义)
```

---

## 拆分原则

1. **按章节拆分**：以 `##` 标题为边界
2. **保持功能完整**：每个模块独立可用
3. **添加引用链接**：模块间双向引用
4. **更新文档索引**：在 SKILL.md 中维护模块列表

---

## 输出格式

### 变更报告

```markdown
# 🔧 技能重构报告

## 📊 变更统计
| 项目 | 原始 | 重构后 |
|------|------|--------|
| SKILL.md 行数 | 404 | 198 |
| code.md 行数 | 0 | 285 |
| 新增模块文件 | 0 | 2 |

## ✅ 执行操作
1. 提取 5 个代码块到 code.md
2. 拆分 "详细SOP模板" 章节到 modules/sop_details.md
3. 拆分 "符号体系" 章节到 modules/symbols.md
4. 更新 SKILL.md 模块引用表

## 📁 文件变更
- 修改: SKILL.md (-206行)
- 新增: code.md (+285行)
- 新增: modules/sop_details.md (+156行)
- 新增: modules/symbols.md (+89行)
```

---

## 验证标准

- [ ] 代码块已提取到 code.md
- [ ] SKILL.md 长度 < 300行
- [ ] code.md 长度 < 400行（如已拆分）
- [ ] 功能描述保持不变
- [ ] 模块引用链接正确
- [ ] 无内容丢失

---

## 使用示例

### 示例1：自动触发

```
用户修改了 kaoyan-electronics-sop/SKILL.md

AI 检测后提示：
🔍 检测到 kaoyan-electronics-sop/SKILL.md 需要重构：
- 包含 8 个代码块可提取
- 文件长度 404 行（超过 300 行阈值）

用户确认：[✅ 立即执行]

AI 执行重构并生成报告...
```

### 示例2：手动触发

```
用户：帮我重构 kaoyan-electronics-core 技能

AI 执行：
1. 分析 kaoyan-electronics-core 目录
2. 检测 SKILL.md 和 code.md
3. 执行必要的拆分操作
4. 生成变更报告
```

---

## 技能集成

### 与其他技能的协作

| 技能 | 协作场景 |
|------|----------|
| skill-creator | 创建新技能后自动优化结构 |
| simplify | 重构后简化代码 |
| fix-table-pipe | 确保表格格式正确 |

---

## 📁 模块文档

| 模块 | 文件 | 内容 |
|------|------|------|
| 代码实现 | [code.md](code.md) | 分析器、提取器、拆分器、报告生成器 |
| 检测逻辑 | [scripts/detector.py](scripts/detector.py) | 代码块检测、行数统计 |
| 重构逻辑 | [scripts/refactor.py](scripts/refactor.py) | 代码提取、内容拆分 |
| 拆分逻辑 | [scripts/splitter.py](scripts/splitter.py) | 章节拆分、模块生成 |

---

*创建日期: 2026-03-27*
*版本: 1.0.0*
