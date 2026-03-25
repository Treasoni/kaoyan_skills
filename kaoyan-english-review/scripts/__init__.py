"""
考研英语复习模块

本模块是 kaoyan-english-review 技能的Python实现，包含：
- 考研适配的SM-2算法
- 每日复习清单生成
- 分阶段学习策略
- 学习统计Dashboard
- 复习记录保存

版本: v2.0.0 (模块化重构)
"""

from .sm2_kaoyan import (
    calculate_next_review_kaoyan,
    calculate_sm2_interval,
)

from .review_list import (
    generate_daily_review_list,
    format_card_list,
)

from .phase_strategy import (
    get_phase_vocabulary_target,
    PHASE_STRATEGY_TABLE,
)

from .statistics import (
    generate_statistics_dashboard,
    generate_progress_chart_data,
)

from .review_recorder import (
    save_review_result,
)

__all__ = [
    # SM-2算法
    "calculate_next_review_kaoyan",
    "calculate_sm2_interval",
    # 复习清单
    "generate_daily_review_list",
    "format_card_list",
    # 分阶段策略
    "get_phase_vocabulary_target",
    "PHASE_STRATEGY_TABLE",
    # 学习统计
    "generate_statistics_dashboard",
    "generate_progress_chart_data",
    # 复习记录
    "save_review_result",
]

__version__ = "2.0.0"
