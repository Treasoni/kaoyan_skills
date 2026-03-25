# kaoyan-english-review 代码模块

本文档提供 kaoyan-english-review 技能的入口逻辑。具体算法实现已模块化至 `scripts/` 目录下。

> 📋 **返回主文档**: [skill.md](skill.md)

---

## 概述

kaoyan-english-review 技能的核心算法已拆分为5个专业Python模块：

| 模块 | 文件 | 职责 |
|------|------|------|
| SM-2算法 | [scripts/sm2_kaoyan.py](scripts/sm2_kaoyan.py) | 考研适配的SM-2间隔重复算法 |
| 复习清单 | [scripts/review_list.py](scripts/review_list.py) | 每日复习清单生成、优先级排序 |
| 分阶段策略 | [scripts/phase_strategy.py](scripts/phase_strategy.py) | 阶段学习目标、策略常量 |
| 学习统计 | [scripts/statistics.py](scripts/statistics.py) | Dashboard生成、进度图表 |
| 复习记录 | [scripts/review_recorder.py](scripts/review_recorder.py) | 复习结果保存、历史记录 |

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

from scripts.sm2_kaoyan import (
    calculate_next_review_kaoyan,
    calculate_sm2_interval,
)

from scripts.review_list import (
    generate_daily_review_list,
    format_card_list,
)

from scripts.phase_strategy import (
    get_phase_vocabulary_target,
    PHASE_STRATEGY_TABLE,
)

from scripts.statistics import (
    generate_statistics_dashboard,
    generate_progress_chart_data,
)

from scripts.review_recorder import (
    save_review_result,
)
```

---

## 主入口 API

### 1. SM-2 算法

```python
# 考研适配的SM-2算法
card = calculate_next_review_kaoyan(card, quality, exam_date)
# 返回更新后的卡片（含 next_review, current_phase, adjusted_interval 等）

# 标准SM-2间隔计算
interval = calculate_sm2_interval(card, quality)
# 返回复习间隔（天）
```

### 2. 每日复习清单

```python
# 生成每日复习清单
review_list = generate_daily_review_list(user_context, exam_date)
# 返回: {"date": ..., "phase": ..., "high_priority": [...], "normal_priority": [...], "stats": {...}}
```

### 3. 分阶段策略

```python
# 获取当前阶段的学习目标
target = get_phase_vocabulary_target(days_to_exam)
# 返回: {"phase": "强化期", "daily_new_words": 40, "review_ratio": 0.5, ...}
```

### 4. 学习统计

```python
# 生成学习统计Dashboard
dashboard = generate_statistics_dashboard(user_context)
# 返回: {"summary": {...}, "polysemy": {...}, "recent_7_days": {...}, "progress_chart": {...}}
```

### 5. 复习记录保存

```python
# 保存复习结果
success = save_review_result(user_id, word, quality, review_time)
```

---

## 核心数据结构

### SM-2 基础字段

| 字段 | 类型 | 说明 |
|------|------|------|
| ease_factor | float | 记忆难度因子，默认2.5 |
| interval | int | 复习间隔（天） |
| review_count | int | 复习次数 |
| next_review | date | 下次复习日期 |
| correct_count | int | 正确次数 |
| incorrect_count | int | 错误次数 |
| forgetting_rate | float | 遗忘率 = incorrect_count / review_count |

### 考研适配字段

| 字段 | 类型 | 说明 |
|------|------|------|
| current_phase | string | 当前阶段（基础期/强化期/冲刺期/极限冲刺期） |
| phase_factor | float | 阶段系数（0.5-1.0） |
| days_to_exam | int | 距离考试天数 |
| adjusted_interval | int | 调整后的复习间隔 |

### 阶段策略表

| 阶段 | 天数 | 每日新词 | 复习比例 | 僻义权重 |
|------|------|----------|----------|----------|
| 基础期 | >300 | 50 | 30% | 1.0x |
| 强化期 | 180-300 | 40 | 50% | 1.2x |
| 十月强化期 | 90-180 | 30 | 60% | 1.5x |
| 冲刺期 | 30-90 | 10 | 90% | 2.0x |
| 极限冲刺 | <30 | 0 | 100% | 2.0x |

---

## 版本兼容性

重构后保持功能完全不变：
- ✅ 考研适配的SM-2算法
- ✅ 每日复习清单生成
- ✅ 分阶段学习策略
- ✅ 学习统计Dashboard
- ✅ 复习记录保存

---

## 模块化说明

详细的模块文档请参考各模块源文件中的 docstring。

---

## 历史版本

原 `code.md` (459行) 已备份为 `code.md.backup`，包含所有历史实现细节。

---

> 📋 **返回主文档**: [skill.md](skill.md)
