# kaoyan-plan 核心算法模块

本文档提供 kaoyan-plan 技能的入口逻辑。具体算法实现已模块化至 `scripts/` 目录下。

> 📋 **返回主文档**: [skill.md](skill.md)

---

## 概述

kaoyan-plan 技能的核心算法已拆分为5个专业Python模块：

| 模块 | 文件 | 职责 |
|------|------|------|
| 主规划器 | [scripts/main_planner.py](scripts/main_planner.py) | 主规划算法（v3.0/v2.1/自适应） |
| 记忆管理 | [scripts/memos_client.py](scripts/memos_client.py) | MemOS 记忆加载与保存 |
| 进度追踪 | [scripts/progress_tracker.py](scripts/progress_tracker.py) | 英语单词、专业课进度管理 |
| SM-2算法 | [scripts/sm2_algorithm.py](scripts/sm2_algorithm.py) | 单词复习间隔计算 |
| 规则引擎 | [scripts/rules_engine.py](scripts/rules_engine.py) | 疲劳度、作息、欠账、熔断机制 |

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

from scripts.main_planner import (
    generate_daily_plan_v3,
    generate_daily_plan,
    generate_daily_plan_adaptive
)
from scripts.progress_tracker import record_task_completion
from scripts.memos_client import load_weekly_data_for_review
from scripts.rules_engine import (
    calculate_mixed_fatigue,
    get_slot_preferences,
    check_task_debt_with_memory
)
```

---

## 工作流程架构

```
[用户输入]
      ↓
[MemOS: 加载画像/专业课进度]
      ↓
[识别输入模式]
      ↓
[欠账/熔断检测]
      ↓
[SM-2 单词验证]
      ↓
[生成计划]
      ↓
[MemOS: 保存]
```

---

## 主入口 API

### 1. 生成每日计划 (v3.0 MemOS集成版)

系统默认应调用此接口生成包含数学、英语、专业课等内容的日程：

```python
def generate_plan(user_input, mode="minimal", previous_plan=None):
    """
    包装函数：调用 v3.0 主规划器

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")
        previous_plan: 昨日计划（用于检测欠账）

    返回:
        每日计划
    """
    try:
        return generate_daily_plan_v3(user_input, mode, previous_plan)
    except Exception as e:
        print(f"v3.0 生成失败，降级到 v2.1: {e}")
        return generate_daily_plan(user_input, mode, previous_plan)
```

### 2. 记录任务完成度

当用户汇报 "Day 015 第1次复习" 或 "数电第一章" 完成时调用：

```python
def process_completion_report(user_id, completed_tasks_raw, planned_tasks):
    """
    包装函数：处理完成报告并更新英语/专业课进度表

    参数:
        user_id: 用户ID
        completed_tasks_raw: 用户原始完成报告
        planned_tasks: 计划中的任务列表

    返回:
        完成记录文件路径
    """
    from scripts.progress_tracker import parse_user_completion_report
    completed_tasks = parse_user_completion_report(completed_tasks_raw)
    return record_task_completion(user_id, completed_tasks, planned_tasks)
```

---

## 版本兼容性

重构后保持 **v3.11.0** 功能完全不变：
- ✅ MemOS集成（可降级）
- ✅ 欠账熔断保护（>10h）
- ✅ 心理状态追踪
- ✅ SM-2单词复习验证
- ✅ 英语进度自动更新
- ✅ 专业课进度检查
- ✅ 周日复盘数据汇总

---

## 快速参考

### 主规划器函数

| 函数 | 版本 | 说明 |
|------|------|------|
| `generate_daily_plan_v3()` | v3.0 | MemOS集成版，含完整功能 |
| `generate_daily_plan()` | v2.1 | 降级兼容版，无MemOS依赖 |
| `generate_daily_plan_adaptive()` | 自适应 | 极简版，基础功能 |

### 进度追踪函数

| 函数 | 说明 |
|------|------|
| `record_task_completion()` | 记录任务完成，更新进度文件 |
| `parse_user_completion_report()` | 解析用户完成报告 |
| `extract_english_tasks()` | 提取英语学习任务 |
| `update_english_progress_file()` | 更新英语学习进度 |
| `check_electronics_progress()` | 检查专业课进度 |

### 规则引擎函数

| 函数 | 说明 |
|------|------|
| `check_task_debt_with_memory()` | 检查任务欠账，含熔断机制 |
| `calculate_mixed_fatigue()` | 计算混合疲劳度 |
| `get_slot_preferences()` | 获取时段偏好 |
| `check_mental_health_intervention()` | 心理健康干预检查 |
| `check_context_freshness()` | 用户画像新鲜度检查 |

### SM-2 算法函数

| 函数 | 说明 |
|------|------|
| `calculate_sm2_next_review()` | 计算下次复习日期 |
| `validate_vocabulary_review_files()` | 验证单词表复习任务 |
| `consistency_check_after_plan_generation()` | 计划生成后一致性检查 |

---

## 模块化说明

详细的模块文档请参考各模块源文件中的 docstring：

- [scripts/main_planner.py](scripts/main_planner.py) - 主规划器实现
- [scripts/memos_client.py](scripts/memos_client.py) - MemOS 客户端实现
- [scripts/progress_tracker.py](scripts/progress_tracker.py) - 进度追踪实现
- [scripts/sm2_algorithm.py](scripts/sm2_algorithm.py) - SM-2 算法实现
- [scripts/rules_engine.py](scripts/rules_engine.py) - 规则引擎实现

---

## 历史版本

原 `code.md` (1926行) 已备份为 `code.md.backup`，包含所有历史实现细节。

---

> 📋 **返回主文档**: [skill.md](skill.md)
