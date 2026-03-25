# kaoyan-electronics-core 代码模块

本文档提供 kaoyan-electronics-core 技能的入口逻辑。具体算法实现已模块化至 `scripts/` 目录下。

> 📋 **返回主文档**: [skill.md](skill.md)

---

## 概述

kaoyan-electronics-core 技能的核心算法已拆分为6个专业Python模块：

| 模块 | 文件 | 职责 |
|------|------|------|
| MemOS集成 | [scripts/memos_client.py](scripts/memos_client.py) | 用户上下文加载、错题保存、个性化提醒 |
| 数学前置 | [scripts/math_prerequisites.py](scripts/math_prerequisites.py) | 数学前置知识检查、MATH_PREREQUISITES常量 |
| 跨学科关联 | [scripts/cross_subject.py](scripts/cross_subject.py) | 数学↔电子技术知识图谱、跨学科提醒 |
| 调度信号 | [scripts/dispatch_signals.py](scripts/dispatch_signals.py) | kaoyan-plan调度信号处理 |
| 统一错误 | [scripts/unified_mistake.py](scripts/unified_mistake.py) | 错误记录保存（含学科标签） |
| 优先级计算 | [scripts/priority_calculator.py](scripts/priority_calculator.py) | 考点权重计算、学习时间推荐 |

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

from scripts.memos_client import (
    load_user_context_from_memory,
    save_mistake_to_memory,
    generate_personalized_reminders,
    check_context_freshness_electronics,
)

from scripts.math_prerequisites import (
    MATH_PREREQUISITES,
    check_math_prerequisites,
    get_math_mastery_level,
)

from scripts.cross_subject import (
    MATH_TO_ELECTRONICS_MAP,
    ELECTRONICS_TO_MATH_MAP,
    generate_cross_subject_reminders,
    find_math_refs,
)

from scripts.dispatch_signals import (
    check_dispatch_signals,
    process_dispatch_signal,
    mark_signal_processed,
)

from scripts.unified_mistake import (
    save_mistake_with_subject_tag,
)

from scripts.priority_calculator import (
    calculate_priority_score,
    get_study_time_recommendation,
    calculate_urgency_score,
)
```

---

## 主入口 API

### 1. MemOS 集成

```python
# 加载用户上下文
context = load_user_context_from_memory(user_id)

# 保存错题记录
save_mistake_to_memory(user_id, knowledge_point, mistake_type,
                       original_understanding, correction)

# 生成个性化提醒
reminders = generate_personalized_reminders(user_id, knowledge_point)

# 检查画像新鲜度
is_fresh, days, prompt = check_context_freshness_electronics(user_id)
```

### 2. 数学前置检查

```python
# 检查数学前置知识
result = check_math_prerequisites("频率响应分析", user_context)
# 返回: {"needed": True, "all_passed": False, "warning": "...", "results": [...]}

# 获取数学掌握程度
mastery = get_math_mastery_level(user_context, "复数运算")
```

### 3. 跨学科关联

```python
# 生成跨学科提醒
reminder = generate_cross_subject_reminders("暂态响应")
# 返回: {"electronics_topic": "...", "required_math": [...], "reminder": "..."}

# 查找数学关联
math_refs = find_math_refs("滤波器设计")
# 返回: ["拉普拉斯变换", "复数运算"]
```

### 4. 调度信号处理

```python
# 检查调度信号
signals = check_dispatch_signals(user_id)

# 处理信号
for signal in signals:
    result = process_dispatch_signal(signal)
    if result:
        # 执行对应操作
        pass
    mark_signal_processed(signal["id"], user_id)
```

### 5. 优先级计算

```python
# 计算知识点优先级
priority = calculate_priority_score(
    exam_frequency=8,      # 考试频率 (1-10)
    exam_importance=9,     # 考试重要性 (1-10)
    mastery_level=40,      # 掌握程度 (0-100)
    days_to_exam=150       # 距离考试天数
)

# 获取学习时间推荐
time, strategy = get_study_time_recommendation(priority)
```

---

## 核心数据结构

### MATH_PREREQUISITES (数学前置知识)

```python
MATH_PREREQUISITES = {
    "频率响应分析": {
        "required_math": [
            {"topic": "复数运算", "level": "basic", "check": "...", "refresher": "..."},
            {"topic": "对数运算", "level": "basic", "check": "...", "refresher": "..."}
        ],
        "warning": "⚠️ 开始「频率响应」前，建议先确认数学基础是否扎实"
    },
    # ...
}
```

### MATH_TO_ELECTRONICS_MAP (数学→电子技术)

```python
MATH_TO_ELECTRONICS_MAP = {
    "复数运算": ["频率响应分析", "交流电路", "滤波器设计", "阻抗计算"],
    "微分方程": ["暂态响应", "RC/RL电路", "一阶电路分析"],
    # ...
}
```

### ELECTRONICS_TO_MATH_MAP (电子技术→数学)

```python
ELECTRONICS_TO_MATH_MAP = {
    "频率响应分析": ["复数运算", "对数运算"],
    "暂态响应": ["微分方程", "指数函数"],
    # ...
}
```

---

## 版本兼容性

重构后保持功能完全不变：
- ✅ MemOS集成（可降级）
- ✅ 数学前置知识检查
- ✅ 跨学科知识关联
- ✅ 调度信号处理
- ✅ 统一错误模型
- ✅ 考点权重计算

---

## 模块化说明

详细的模块文档请参考各模块源文件中的 docstring。

---

## 历史版本

原 `code.md` (588行) 已备份为 `code.md.backup`，包含所有历史实现细节。

---

> 📋 **返回主文档**: [skill.md](skill.md)
