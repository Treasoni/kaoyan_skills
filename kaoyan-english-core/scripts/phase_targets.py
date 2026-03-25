"""
动态权重响应模块

根据考试倒计时阶段自动调整词汇学习策略，包括：
1. 阶段词汇目标计算
2. 僻义权重动态调整
3. 复习比例优化

版本: 2.0.0
创建日期: 2026-03-24
最后更新: 2026-03-24
"""

from typing import Dict, Any


def get_phase_vocabulary_target(days_to_exam: int) -> Dict[str, Any]:
    """根据阶段获取词汇学习目标

    基于距离考试的天数，自动调整每日新词量、
    复习比例、学习重点和僻义权重。

    Args:
        days_to_exam: 距离考试的天数

    Returns:
        dict: 词汇学习目标配置，包含：
            - daily_new_words: 每日新词数量
            - review_ratio: 复习比例（0.0-1.0）
            - focus: 学习重点描述
            - polysemy_weight: 僻义权重系数

    Examples:
        >>> # 基础期（>300天）
        >>> target = get_phase_vocabulary_target(350)
        >>> target['daily_new_words']
        50
        >>> # 冲刺期（30-90天）
        >>> target = get_phase_vocabulary_target(60)
        >>> target['focus']
        '高频词+僻义词'
    """
    if days_to_exam > 300:        # 基础期
        return {
            "daily_new_words": 50,
            "review_ratio": 0.3,
            "focus": "词汇积累",
            "polysemy_weight": 1.0,
            "phase": "foundation",
            "phase_name": "基础期"
        }

    elif days_to_exam > 180:      # 强化期
        return {
            "daily_new_words": 40,
            "review_ratio": 0.5,
            "focus": "僻义词+真题语境",
            "polysemy_weight": 1.2,
            "phase": "reinforcement",
            "phase_name": "强化期"
        }

    elif days_to_exam > 90:       # 十月强化期
        return {
            "daily_new_words": 30,
            "review_ratio": 0.6,
            "focus": "僻义词强化",
            "polysemy_weight": 1.5,
            "phase": "october_boost",
            "phase_name": "十月强化期"
        }

    elif days_to_exam > 30:       # 冲刺期
        return {
            "daily_new_words": 10,
            "review_ratio": 0.9,
            "focus": "高频词+僻义词",
            "polysemy_weight": 2.0,
            "phase": "sprint",
            "phase_name": "冲刺期"
        }

    else:                         # 极限冲刺
        return {
            "daily_new_words": 0,
            "review_ratio": 1.0,
            "focus": "全部复习",
            "polysemy_weight": 2.0,
            "phase": "final_sprint",
            "phase_name": "极限冲刺"
        }


def calculate_polysemy_priority_score(
    base_priority: float,
    polysemy_weight: float,
    exam_frequency: str
) -> float:
    """计算僻义词优先级分数

    Args:
        base_priority: 基础优先级（0.0-1.0）
        polysemy_weight: 僻义权重系数
        exam_frequency: 考试频率（"high", "medium", "low"）

    Returns:
        float: 调整后的优先级分数

    Examples:
        >>> score = calculate_polysemy_priority_score(0.5, 1.5, "high")
        >>> score > 0.5
        True
    """
    frequency_multiplier = {
        "high": 1.3,
        "medium": 1.0,
        "low": 0.7
    }

    multiplier = frequency_multiplier.get(exam_frequency, 1.0)
    return base_priority * polysemy_weight * multiplier


def adjust_review_list_by_phase(
    word_list: list,
    days_to_exam: int,
    max_words: int = 100
) -> list:
    """根据阶段调整复习列表

    Args:
        word_list: 待复习词汇列表
        days_to_exam: 距离考试天数
        max_words: 最大复习词汇数

    Returns:
        list: 调整后的复习词汇列表

    Examples:
        >>> words = [{"word": "test", "priority": 0.8}]
        >>> adjusted = adjust_review_list_by_phase(words, 60, 50)
        >>> len(adjusted) <= 50
        True
    """
    target = get_phase_vocabulary_target(days_to_exam)

    # 根据僻义权重重新排序
    sorted_words = sorted(
        word_list,
        key=lambda w: (
            -w.get("polysemy_alert", False) * target["polysemy_weight"],
            -w.get("priority", 0.5)
        )
    )

    # 返回前 max_words 个
    return sorted_words[:max_words]


def get_phase_specific_instructions(days_to_exam: int) -> list:
    """获取阶段特定的学习指导

    Args:
        days_to_exam: 距离考试天数

    Returns:
        list: 学习指导要点列表

    Examples:
        >>> instructions = get_phase_specific_instructions(60)
        >>> len(instructions) > 0
        True
    """
    target = get_phase_vocabulary_target(days_to_exam)
    phase = target["phase"]

    instructions_map = {
        "foundation": [
            "重点积累核心词汇",
            "建立词汇网络",
            "注重语境理解"
        ],
        "reinforcement": [
            "加强僻义词学习",
            "结合真题语境",
            "提高复习频率"
        ],
        "october_boost": [
            "僻义词专项训练",
            "高频词深度复习",
            "错题反复巩固"
        ],
        "sprint": [
            "高频词+僻义词并重",
            "快速复习模式",
            "减少新词学习"
        ],
        "final_sprint": [
            "全面复习不遗漏",
            "查漏补缺",
            "保持语感"
        ]
    }

    return instructions_map.get(phase, [])


def calculate_daily_review_time(
    days_to_exam: int,
    total_study_minutes: int
) -> Dict[str, Any]:
    """计算每日复习时间分配

    Args:
        days_to_exam: 距离考试天数
        total_study_minutes: 总学习时间（分钟）

    Returns:
        dict: 时间分配方案

    Examples:
        >>> allocation = calculate_daily_review_time(60, 120)
        >>> 'new_words_minutes' in allocation
        True
        >>> 'review_minutes' in allocation
        True
    """
    target = get_phase_vocabulary_target(days_to_exam)

    review_minutes = int(total_study_minutes * target["review_ratio"])
    new_words_minutes = total_study_minutes - review_minutes

    return {
        "new_words_minutes": new_words_minutes,
        "review_minutes": review_minutes,
        "review_ratio": target["review_ratio"],
        "focus": target["focus"]
    }


# 导出的公共函数
__all__ = [
    "get_phase_vocabulary_target",
    "calculate_polysemy_priority_score",
    "adjust_review_list_by_phase",
    "get_phase_specific_instructions",
    "calculate_daily_review_time",
]
