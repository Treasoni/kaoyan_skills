# kaoyan-math-notes 代码模块

本文档提供 kaoyan-math-notes 技能的入口逻辑。具体算法实现已模块化至 `scripts/` 目录下。

> 📋 **返回主文档**: [skill.md](skill.md)

---

## 概述

kaoyan-math-notes 技能的核心算法已拆分为3个专业Python模块：

| 模块 | 文件 | 职责 |
|------|------|------|
| 保护机制 | [scripts/protection.py](scripts/protection.py) | 已有笔记检查、内容验证 |
| 生成函数 | [scripts/generation.py](scripts/generation.py) | 知识点提取、模板生成、LaTeX公式 |
| 更新函数 | [scripts/update.py](scripts/update.py) | 反馈更新、理解障碍分析 |

---

## 核心依赖导入

```python
import sys
import os

# 确保能正确导入 scripts 模块
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, "scripts")
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from scripts.protection import (
    check_existing_notes,
    has_content,
)

from scripts.generation import (
    extract_knowledge_points,
    generate_note_from_template,
    generate_latex_formula,
    generate_example_block,
)

from scripts.update import (
    update_note_with_feedback,
    analyze_understanding_barrier,
)
```

---

## 主入口 API

### 1. 保护机制

```python
# 检查已有笔记
result = check_existing_notes(target_path, knowledge_points)
# 返回: {"existing": [...], "to_create": [...]}

# 检查文件是否有内容
has_content = has_content(file_path)
```

### 2. 笔记生成

```python
# 从用户笔记中提取知识点
kps = extract_knowledge_points(notes_content, "高数")

# 基于模板生成笔记
note = generate_note_from_template("洛必达法则", "高数", user_notes, "数二")

# 生成LaTeX公式
formula = generate_latex_formula("\\lim_{x \\to 0}\\frac{f(x)}{g(x)}", "极限定义")

# 生成例题块
example = generate_example_block(question, analysis, solution, comment)
```

### 3. 笔记更新

```python
# 根据反馈更新笔记
success = update_note_with_feedback(note_path, "不理解为什么...", "理解困难")

# 分析理解障碍类型
analysis = analyze_understanding_barrier(feedback)
# 返回: {"type": "逻辑跳跃", "suggestions": [...]}
```

---

## 核心功能说明

### 1. 已有笔记保护

- **check_existing_notes**: 扫描目标目录，返回已有笔记和待创建列表
- **has_content**: 检查文件是否有实际内容（非空，非纯frontmatter）

### 2. 笔记模板结构

```yaml
---
知识点: {kp_name}
模块: {module}
考试类型: {exam_type}
考试频率: ⭐⭐⭐⭐⭐
学习状态: 待学习
tags: [{module}, {kp_name}]
---

# {kp_name}

## 原始定义
## 直观理解 💡
## 定理条件 ⚠️
## 考试重点 ⭐
## 典型题型
## 解题方法
## 易错点 ⚠️
## 我的理解记录 🧠
## 我的错误类型 📌
## 例题
## 相关知识点 📚
## 补充说明 📝
```

### 3. 理解障碍类型

| 类型 | 关键词 | 建议 |
|------|--------|------|
| 逻辑跳跃 | "不懂为什么"、"怎么来的" | 补充推导过程 |
| 概念抽象 | "太抽象"、"无法理解" | 添加直观解释 |
| 缺乏例题 | "不会做题"、"没有例子" | 添加典型例题 |
| 条件不清 | "什么时候用"、"什么条件" | 明确使用条件 |

---

## 版本兼容性

重构后保持功能完全不变：
- ✅ 已有笔记保护（不覆盖）
- ✅ 知识点提取
- ✅ 模板生成
- ✅ LaTeX公式
- ✅ 反馈更新
- ✅ 理解障碍分析

---

## 模块化说明

详细的模块文档请参考各模块源文件中的 docstring。

---

## 历史版本

原 `code.md` (348行) 已备份为 `code.md.backup`，包含所有历史实现细节。

---

> 📋 **返回主文档**: [skill.md](skill.md)
