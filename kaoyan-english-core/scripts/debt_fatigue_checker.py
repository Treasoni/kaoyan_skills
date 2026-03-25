"""
词汇欠账与疲劳检查模块

提供词汇学习中的欠账检测和疲劳度监控功能，包括：
1. 词汇欠账检查（含熔断机制）
2. 疲劳度干预建议
3. 复习恢复计划生成

版本: 2.0.0
创建日期: 2026-03-24
最后更新: 2026-03-24
"""

from datetime import date
from typing import Dict, List, Optional, Any


# 常量定义
DEBT_LIMIT = 200  # 词汇欠账熔断阈值


def check_vocabulary_debt_with_memory(user_context: Dict[str, Any]) -> Dict[str, Any]:
    """检查词汇欠账（含熔断机制）

    计算逾期未复习的词汇数量，超过阈值时触发熔断机制，
    建议暂停新词学习，专注复习。

    Args:
        user_context: 用户上下文，必须包含 vocabulary_cards

    Returns:
        dict: 欠账状态和处理策略，包含以下键：
            - type: "vocabulary_emergency" 或 "normal"
            - overdue_count: 逾期词汇数量
            - strategy: 处理策略（仅紧急时）
            - message: 提示信息（仅紧急时）
            - suggestion: 建议措施（仅紧急时）
            - recovery_plan: 恢复计划（仅紧急时）

    Examples:
        >>> context = {"vocabulary_cards": [{"next_review": date(2026, 3, 20)}]}
        >>> result = check_vocabulary_debt_with_memory(context)
        >>> result['type']
        'normal'
    """
    # 计算逾期未复习的词汇数量
    overdue_words = calculate_overdue_words(user_context)

    if overdue_words > DEBT_LIMIT:
        return {
            "type": "vocabulary_emergency",
            "overdue_count": overdue_words,
            "strategy": "recovery_only",
            "message": f"⚠️ 待复习词汇已达{overdue_words}个，超过安全阈值",
            "suggestion": "暂停新词学习，专注复习",
            "recovery_plan": generate_vocabulary_recovery_plan(overdue_words)
        }

    return {"type": "normal", "overdue_count": overdue_words}


def calculate_overdue_words(user_context: Dict[str, Any]) -> int:
    """计算逾期未复习的词汇数量

    Args:
        user_context: 用户上下文

    Returns:
        int: 逾期词汇数量

    Examples:
        >>> from datetime import date
        >>> context = {
        ...     "vocabulary_cards": [
        ...         {"next_review": date(2026, 3, 20)},  # 逾期
        ...         {"next_review": date(2026, 3, 25)},  # 未逾期
        ...     ]
        ... }
        >>> calculate_overdue_words(context)
        1
    """
    vocabulary_cards = user_context.get("vocabulary_cards", [])
    today = date.today()

    overdue_count = 0
    for card in vocabulary_cards:
        next_review = card.get("next_review")
        if next_review and next_review < today:
            overdue_count += 1

    return overdue_count


def generate_vocabulary_recovery_plan(overdue_count: int) -> Dict[str, Any]:
    """生成词汇恢复计划

    Args:
        overdue_count: 逾期词汇数量

    Returns:
        dict: 恢复计划，包含每日复习量分配和预计天数

    Examples:
        >>> plan = generate_vocabulary_recovery_plan(250)
        >>> plan['estimated_days']
        5
    """
    # 假设每天能复习50个词
    daily_capacity = 50
    estimated_days = (overdue_count + daily_capacity - 1) // daily_capacity

    return {
        "total_overdue": overdue_count,
        "daily_capacity": daily_capacity,
        "estimated_days": estimated_days,
        "stages": [
            {
                "day": i + 1,
                "words_to_review": min(daily_capacity, overdue_count - i * daily_capacity)
            }
            for i in range(estimated_days)
        ]
    }


def check_vocabulary_fatigue_intervention(
    user_context: Dict[str, Any]
) -> Optional[Dict[str, Any]]:
    """检查是否需要词汇疲劳干预

    分析最近3天的心理状态历史，如果连续3天疲劳度超过0.6，
    则触发疲劳干预建议。

    Args:
        user_context: 用户上下文，必须包含 mental_history

    Returns:
        dict: 干预方案，包含以下键（需要干预时）：
            - intervention_needed: True
            - mode: 干预模式（如 "vocabulary_relief"）
            - avg_fatigue: 平均疲劳度
            - actions: 建议的行动列表
        None: 无需干预

    Examples:
        >>> context = {
        ...     "mental_history": [
        ...         {"date": "2026-03-22", "vocabulary_fatigue": 0.7},
        ...         {"date": "2026-03-23", "vocabulary_fatigue": 0.8},
        ...         {"date": "2026-03-24", "vocabulary_fatigue": 0.65},
        ...     ]
        ... }
        >>> result = check_vocabulary_fatigue_intervention(context)
        >>> result['intervention_needed']
        True
    """
    mental_history = user_context.get("mental_history", [])

    if len(mental_history) < 3:
        return None

    recent_days = mental_history[-3:]
    tired_count = sum(
        1 for d in recent_days
        if d.get("vocabulary_fatigue", 0) > 0.6
    )

    if tired_count >= 3:
        avg_fatigue = sum(
            d.get("vocabulary_fatigue", 0.5) for d in recent_days
        ) / len(recent_days)

        return {
            "intervention_needed": True,
            "mode": "vocabulary_relief",
            "avg_fatigue": avg_fatigue,
            "actions": [
                "减少新词量50%",
                "增加真题语境阅读",
                "暂停僻义词训练",
                "增加写作应用练习"
            ]
        }

    return None


def calculate_vocabulary_fatigue_score(
    review_count: int,
    correct_rate: float,
    duration_minutes: int
) -> float:
    """计算词汇学习疲劳度分数

    基于复习量、正确率和学习时长计算疲劳度。

    Args:
        review_count: 复习词汇数量
        correct_rate: 正确率（0.0-1.0）
        duration_minutes: 学习时长（分钟）

    Returns:
        float: 疲劳度分数（0.0-1.0）

    Examples:
        >>> score = calculate_vocabulary_fatigue_score(100, 0.75, 60)
        >>> 0 <= score <= 1
        True
    """
    # 基础疲劳度：复习量/100
    volume_fatigue = min(review_count / 100.0, 0.5)

    # 正确率疲劳度：正确率越低，疲劳度越高
    accuracy_fatigue = (1.0 - correct_rate) * 0.3

    # 时长疲劳度：每30分钟增加0.1
    time_fatigue = min(duration_minutes / 30.0 * 0.1, 0.2)

    total_fatigue = volume_fatigue + accuracy_fatigue + time_fatigue
    return min(total_fatigue, 1.0)


# 导出的公共函数和常量
__all__ = [
    "check_vocabulary_debt_with_memory",
    "calculate_overdue_words",
    "generate_vocabulary_recovery_plan",
    "check_vocabulary_fatigue_intervention",
    "calculate_vocabulary_fatigue_score",
    "DEBT_LIMIT",
]
