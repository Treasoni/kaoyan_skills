"""
考研规划Skill - Python脚本模块

本模块包含主规划算法、MemOS集成、进度追踪、SM-2算法、规则引擎。

版本: v2.0.0 (模块化重构)
来源: code.md 模块化拆分

模块结构:
    - main_planner: 主规划算法（v3.0/v2.1/自适应）
    - memos_client: MemOS 记忆加载与保存
    - progress_tracker: 英语单词、专业课进度管理
    - sm2_algorithm: SM-2 单词复习间隔计算
    - rules_engine: 疲劳度、作息、欠账、熔断机制
"""

__version__ = "2.0.0"

# 主规划器
from .main_planner import (
    generate_daily_plan_v3,
    generate_daily_plan,
    generate_daily_plan_adaptive,
    generate_sunday_review_plan_with_memory,
    generate_sunday_review_plan,
)

# 进度追踪
from .progress_tracker import (
    record_task_completion,
    parse_user_completion_report,
    generate_completion_record_file,
    extract_english_tasks,
    update_english_progress_file,
    check_electronics_progress,
)

# MemOS 客户端
from .memos_client import (
    safe_load_context,
    safe_save_plan,
    load_weekly_data_for_review,
    parse_memory_results_to_context,
    aggregate_weekly_stats,
    calculate_completion_stats,
)

# 规则引擎
from .rules_engine import (
    calculate_mixed_fatigue,
    get_slot_preferences,
    check_task_debt_with_memory,
    check_mental_health_intervention,
    check_context_freshness,
    split_large_time_block,
    is_sunday,
)

# SM-2 算法
from .sm2_algorithm import (
    calculate_sm2_next_review,
    validate_vocabulary_review_files,
    consistency_check_after_plan_generation,
    SM2_INTERVALS,
)

__all__ = [
    # 主规划器
    "generate_daily_plan_v3",
    "generate_daily_plan",
    "generate_daily_plan_adaptive",
    "generate_sunday_review_plan_with_memory",
    "generate_sunday_review_plan",
    # 进度追踪
    "record_task_completion",
    "parse_user_completion_report",
    "generate_completion_record_file",
    "extract_english_tasks",
    "update_english_progress_file",
    "check_electronics_progress",
    # MemOS 客户端
    "safe_load_context",
    "safe_save_plan",
    "load_weekly_data_for_review",
    "parse_memory_results_to_context",
    "aggregate_weekly_stats",
    "calculate_completion_stats",
    # 规则引擎
    "calculate_mixed_fatigue",
    "get_slot_preferences",
    "check_task_debt_with_memory",
    "check_mental_health_intervention",
    "check_context_freshness",
    "split_large_time_block",
    "is_sunday",
    # SM-2 算法
    "calculate_sm2_next_review",
    "validate_vocabulary_review_files",
    "consistency_check_after_plan_generation",
    "SM2_INTERVALS",
]
