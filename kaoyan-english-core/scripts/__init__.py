"""
kaoyan-english-core 技能代码模块

版本: 2.0.0 (模块化重构)
创建日期: 2026-03-24
最后更新: 2026-03-24

本模块提供考研英语核心基础设施功能，包括：
1. MemOS 集成（用户上下文、词汇卡片、复习会话）
2. 欠账与疲劳检查（熔断机制、疲劳干预）
3. 调度信号处理（跨科目协调）
4. 记忆压缩模式（时间转移）
5. 动态权重响应（阶段自适应）
6. 统一错误模型（错误记录与分析）
7. Day 编号计算（共享功能）
8. 数据模型定义（枚举、类、常量）

模块结构:
    - memos_client: MemOS 记忆加载与保存
    - debt_fatigue_checker: 欠账检查与疲劳干预
    - dispatch_signals: 调度信号处理
    - memory_compression: 记忆压缩模式
    - phase_targets: 阶段目标与权重
    - unified_mistake: 统一错误模型
    - day_calculator: Day 编号计算
    - data_models: 数据模型定义
"""

__version__ = "2.0.0"

# MemOS 客户端
from .memos_client import (
    load_user_context_from_memory,
    parse_memory_to_english_context,
    create_default_user_context,
    save_word_card_to_memory,
    record_review_session,
    check_context_freshness_english,
    extract_user_profile,
    extract_word_cards,
    extract_review_records,
    extract_mental_state,
)

# 欠账与疲劳检查
from .debt_fatigue_checker import (
    check_vocabulary_debt_with_memory,
    calculate_overdue_words,
    generate_vocabulary_recovery_plan,
    check_vocabulary_fatigue_intervention,
    calculate_vocabulary_fatigue_score,
    DEBT_LIMIT,
)

# 调度信号处理
from .dispatch_signals import (
    check_dispatch_signals,
    process_dispatch_signal,
    mark_signal_as_processed,
    create_dispatch_signal,
)

# 记忆压缩模式
from .memory_compression import (
    activate_memory_compression_mode,
    get_planned_english_hours,
    calculate_compression_ratio,
    adjust_vocabulary_target_for_compression,
    generate_compression_recovery_plan,
)

# 动态权重响应
from .phase_targets import (
    get_phase_vocabulary_target,
    calculate_polysemy_priority_score,
    adjust_review_list_by_phase,
    get_phase_specific_instructions,
    calculate_daily_review_time,
)

# 统一错误模型
from .unified_mistake import (
    save_unified_english_mistake,
    create_mistake_record,
    batch_save_mistakes,
    analyze_mistake_patterns,
    get_polysemy_critical_words,
)

# Day 编号计算
from .day_calculator import (
    calculate_day_number,
    get_max_day_number_from_files,
    get_validated_day_number,
    format_day_number,
    generate_day_filenames,
    parse_day_number_from_filename,
    get_day_range,
    START_DATE,
    START_DAY,
    DEFAULT_DIRECTORY,
)

# 数据模型
from .data_models import (
    # 枚举类型
    ExamType,
    CurrentLevel,
    ReviewFocus,
    LearningStyle,
    PolysemySensitivity,
    MentalStatus,
    WarningLevel,
    ExamFrequency,

    # 常量
    DEFAULT_DAILY_NEW_WORD_TARGET,
    DEFAULT_POLYSEMY_SENSITIVITY,
    DEFAULT_REVIEW_FOCUS,
    DEFAULT_LEARNING_STYLE,
    AUTO_REFRESH_INTERVAL_DAYS,
    POLYSEMY_CRITICAL_THRESHOLD,
    POLYSEMY_WARNING_THRESHOLD,
    SM2_DEFAULT_EASE_FACTOR,
    SM2_MIN_EASE_FACTOR,
    SM2_DEFAULT_INTERVAL,

    # 数据模型类
    UserProfile,
    WordCard,
    ReviewRecord,
    MentalStateRecord,
)

__all__ = [
    # MemOS 客户端
    "load_user_context_from_memory",
    "parse_memory_to_english_context",
    "create_default_user_context",
    "save_word_card_to_memory",
    "record_review_session",
    "check_context_freshness_english",
    "extract_user_profile",
    "extract_word_cards",
    "extract_review_records",
    "extract_mental_state",

    # 欠账与疲劳检查
    "check_vocabulary_debt_with_memory",
    "calculate_overdue_words",
    "generate_vocabulary_recovery_plan",
    "check_vocabulary_fatigue_intervention",
    "calculate_vocabulary_fatigue_score",
    "DEBT_LIMIT",

    # 调度信号处理
    "check_dispatch_signals",
    "process_dispatch_signal",
    "mark_signal_as_processed",
    "create_dispatch_signal",

    # 记忆压缩模式
    "activate_memory_compression_mode",
    "get_planned_english_hours",
    "calculate_compression_ratio",
    "adjust_vocabulary_target_for_compression",
    "generate_compression_recovery_plan",

    # 动态权重响应
    "get_phase_vocabulary_target",
    "calculate_polysemy_priority_score",
    "adjust_review_list_by_phase",
    "get_phase_specific_instructions",
    "calculate_daily_review_time",

    # 统一错误模型
    "save_unified_english_mistake",
    "create_mistake_record",
    "batch_save_mistakes",
    "analyze_mistake_patterns",
    "get_polysemy_critical_words",

    # Day 编号计算
    "calculate_day_number",
    "get_max_day_number_from_files",
    "get_validated_day_number",
    "format_day_number",
    "generate_day_filenames",
    "parse_day_number_from_filename",
    "get_day_range",
    "START_DATE",
    "START_DAY",
    "DEFAULT_DIRECTORY",

    # 数据模型 - 枚举
    "ExamType",
    "CurrentLevel",
    "ReviewFocus",
    "LearningStyle",
    "PolysemySensitivity",
    "MentalStatus",
    "WarningLevel",
    "ExamFrequency",

    # 数据模型 - 常量
    "DEFAULT_DAILY_NEW_WORD_TARGET",
    "DEFAULT_POLYSEMY_SENSITIVITY",
    "DEFAULT_REVIEW_FOCUS",
    "DEFAULT_LEARNING_STYLE",
    "AUTO_REFRESH_INTERVAL_DAYS",
    "POLYSEMY_CRITICAL_THRESHOLD",
    "POLYSEMY_WARNING_THRESHOLD",
    "SM2_DEFAULT_EASE_FACTOR",
    "SM2_MIN_EASE_FACTOR",
    "SM2_DEFAULT_INTERVAL",

    # 数据模型 - 类
    "UserProfile",
    "WordCard",
    "ReviewRecord",
    "MentalStateRecord",
]
