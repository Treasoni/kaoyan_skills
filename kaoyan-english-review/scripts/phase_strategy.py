"""
分阶段策略模块

本模块处理考研英语词汇的分阶段学习策略，包括：
- 根据阶段获取词汇学习目标
- 阶段策略常量定义

来源: code.md 第210-275行
"""

from typing import Dict, Any


def get_phase_vocabulary_target(days_to_exam: int) -> Dict[str, Any]:
    """根据阶段获取词汇学习目标

    Args:
        days_to_exam: 距离考试天数

    Returns:
        dict: 阶段学习目标
    """
    if days_to_exam > 300:        # 基础期
        return {
            "phase": "基础期",
            "daily_new_words": 50,
            "review_ratio": 0.3,
            "focus": "词汇积累",
            "polysemy_weight": 1.0,
            "strategy": "注重新词积累，标准SM-2间隔"
        }

    elif days_to_exam > 180:      # 强化期
        return {
            "phase": "强化期",
            "daily_new_words": 40,
            "review_ratio": 0.5,
            "focus": "僻义词+真题语境",
            "polysemy_weight": 1.2,
            "strategy": "启用熟词僻义预警，强化真题语境"
        }

    elif days_to_exam > 90:       # 十月强化期
        return {
            "phase": "十月强化期",
            "daily_new_words": 30,
            "review_ratio": 0.6,
            "focus": "僻义词强化",
            "polysemy_weight": 1.5,
            "strategy": "僻义词间隔缩短，增加真题语境"
        }

    elif days_to_exam > 30:       # 冲刺期
        return {
            "phase": "冲刺期",
            "daily_new_words": 10,
            "review_ratio": 0.9,
            "focus": "高频词+僻义词",
            "polysemy_weight": 2.0,
            "strategy": "缩短高频词间隔20%，重点复习僻义词"
        }

    else:                         # 极限冲刺
        return {
            "phase": "极限冲刺期",
            "daily_new_words": 0,
            "review_ratio": 1.0,
            "focus": "全部复习",
            "polysemy_weight": 2.0,
            "strategy": "强制缩短所有间隔，高频词最多3天一复习"
        }


# 阶段策略表常量
PHASE_STRATEGY_TABLE = [
    {"phase": "基础期", "days": ">300", "daily_new_words": 50, "review_ratio": "30%", "polysemy_weight": "1.0x"},
    {"phase": "强化期", "days": "180-300", "daily_new_words": 40, "review_ratio": "50%", "polysemy_weight": "1.2x"},
    {"phase": "十月强化期", "days": "90-180", "daily_new_words": 30, "review_ratio": "60%", "polysemy_weight": "1.5x"},
    {"phase": "冲刺期", "days": "30-90", "daily_new_words": 10, "review_ratio": "90%", "polysemy_weight": "2.0x"},
    {"phase": "极限冲刺", "days": "<30", "daily_new_words": 0, "review_ratio": "100%", "polysemy_weight": "2.0x"},
]
