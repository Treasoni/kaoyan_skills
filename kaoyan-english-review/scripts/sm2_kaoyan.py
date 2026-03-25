"""
考研适配的SM-2算法模块

本模块处理考研英语词汇的SM-2间隔重复算法，包括：
- 考研适配的SM-2算法（根据考试倒计时调整间隔）
- 标准SM-2算法实现
- 词汇卡片更新

来源: code.md 第7-123行
"""

from datetime import date, timedelta
from typing import Dict, Any


def calculate_next_review_kaoyan(card: Dict[str, Any], quality: int, exam_date: date) -> Dict[str, Any]:
    """考研适配的SM-2算法

    Args:
        card: 词汇卡片对象
        quality: 回忆质量评分 (0-5)
        exam_date: 考试日期

    Returns:
        Card: 更新后的卡片对象
    """
    days_to_exam = (exam_date - date.today()).days
    standard_interval = calculate_sm2_interval(card, quality)

    # 倒计时权重计算
    if days_to_exam > 100:
        # 正常阶段：标准SM-2
        current_phase = "基础期"
        phase_factor = 1.0
        adjusted_interval = standard_interval

    elif days_to_exam > 30:
        # 强化阶段（考前30-100天）：
        # - 高频词：缩短20%间隔
        # - 僻义词：缩短30%间隔
        current_phase = "强化期"
        if card.get("frequency", 0) >= 5 or card.get("polysemy_alert"):
            phase_factor = 0.7 if card.get("polysemy_alert") else 0.8
        else:
            phase_factor = 0.9
        adjusted_interval = max(1, int(standard_interval * phase_factor))

    else:
        # 冲刺阶段（考前30天内）：
        # - 所有词间隔强制缩短
        # - 高频词/僻义词：最高优先级
        current_phase = "冲刺期" if days_to_exam > 7 else "极限冲刺期"
        if card.get("frequency", 0) >= 5 or card.get("polysemy_alert"):
            phase_factor = 0.5
            adjusted_interval = min(int(standard_interval * phase_factor), 3)  # 最多3天
        else:
            phase_factor = 0.7
            adjusted_interval = min(int(standard_interval * phase_factor), 7)  # 最多7天

    # 更新卡片数据
    card["current_phase"] = current_phase
    card["phase_factor"] = phase_factor
    card["adjusted_interval"] = adjusted_interval
    card["days_to_exam"] = days_to_exam
    card["next_review"] = date.today() + timedelta(days=adjusted_interval)

    return card


def calculate_sm2_interval(card: Dict[str, Any], quality: int) -> int:
    """标准SM-2算法计算复习间隔

    Args:
        card: 词汇卡片对象
        quality: 回忆质量评分 (0-5)
            5: 完美记忆
            4: 正确但有犹豫
            3: 回忆困难但正确
            2: 错误但有印象
            1: 错误无印象
            0: 完全忘记

    Returns:
        int: 复习间隔（天）

    标准SM-2间隔规则：
        - 第1次复习：学习后1天
        - 第2次复习：第1次复习后3天（累计4天）
        - 第3次复习：第2次复习后7天（累计11天）
        - 后续复习：interval × ease_factor
    """
    if quality >= 3:
        # 回答正确，增加间隔
        review_count = card.get("review_count", 0)
        if review_count == 0:
            # 第1次复习：学习后1天
            interval = 1
        elif review_count == 1:
            # 第2次复习：第1次复习后3天（累计4天）
            interval = 3
        elif review_count == 2:
            # 第3次复习：第2次复习后7天（累计11天）
            interval = 7
        else:
            # 后续复习：interval × ease_factor
            interval = int(card.get("interval", 7) * card.get("ease_factor", 2.5))

        # 更新ease factor
        # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        ease_factor = card.get("ease_factor", 2.5)
        ease_factor = max(1.3,
            ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        )

        card["ease_factor"] = ease_factor
        card["interval"] = interval
        card["correct_count"] = card.get("correct_count", 0) + 1
    else:
        # 回答错误，重新开始
        card["review_count"] = 0
        card["interval"] = 1
        card["incorrect_count"] = card.get("incorrect_count", 0) + 1

    card["review_count"] = card.get("review_count", 0) + 1
    total_reviews = card["review_count"]
    card["forgetting_rate"] = card.get("incorrect_count", 0) / max(1, total_reviews)

    return card.get("interval", 1)
