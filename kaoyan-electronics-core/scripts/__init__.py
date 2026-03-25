"""
822电子技术核心模块

本模块是 kaoyan-electronics-core 技能的Python实现，包含：
- MemOS 集成（用户上下文加载、错误保存）
- 数学前置知识检查
- 跨学科知识关联
- 调度信号处理
- 统一错误模型
- 考点权重计算

版本: v2.0.0 (模块化重构)
"""

from .memos_client import (
    load_user_context_from_memory,
    save_mistake_to_memory,
    generate_personalized_reminders,
    check_context_freshness_electronics,
    get_default_profile,
    get_common_mistake_types,
    generate_suggestion,
)

from .math_prerequisites import (
    MATH_PREREQUISITES,
    check_math_prerequisites,
    get_math_mastery_level,
)

from .cross_subject import (
    MATH_TO_ELECTRONICS_MAP,
    ELECTRONICS_TO_MATH_MAP,
    generate_cross_subject_reminders,
    find_math_refs,
    find_electronics_refs,
)

from .dispatch_signals import (
    check_dispatch_signals,
    process_dispatch_signal,
    mark_signal_processed,
)

from .unified_mistake import (
    save_mistake_with_subject_tag,
)

from .priority_calculator import (
    calculate_priority_score,
    get_study_time_recommendation,
    calculate_urgency_score,
)

__all__ = [
    # MemOS 集成
    "load_user_context_from_memory",
    "save_mistake_to_memory",
    "generate_personalized_reminders",
    "check_context_freshness_electronics",
    "get_default_profile",
    "get_common_mistake_types",
    "generate_suggestion",
    # 数学前置
    "MATH_PREREQUISITES",
    "check_math_prerequisites",
    "get_math_mastery_level",
    # 跨学科关联
    "MATH_TO_ELECTRONICS_MAP",
    "ELECTRONICS_TO_MATH_MAP",
    "generate_cross_subject_reminders",
    "find_math_refs",
    "find_electronics_refs",
    # 调度信号
    "check_dispatch_signals",
    "process_dispatch_signal",
    "mark_signal_processed",
    # 统一错误
    "save_mistake_with_subject_tag",
    # 优先级计算
    "calculate_priority_score",
    "get_study_time_recommendation",
    "calculate_urgency_score",
]

__version__ = "2.0.0"
