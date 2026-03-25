"""
每日复习清单生成模块

本模块处理考研英语词汇的每日复习清单生成，包括：
- 每日复习清单生成
- 优先级排序
- 卡片格式化

来源: code.md 第127-206行
"""

from datetime import date
from typing import Dict, Any, List

from .phase_strategy import get_phase_vocabulary_target


def generate_daily_review_list(user_context: Dict[str, Any], exam_date: date) -> Dict[str, Any]:
    """生成每日复习清单

    Args:
        user_context: 用户上下文
        exam_date: 考试日期

    Returns:
        dict: 复习清单
    """
    vocabulary_cards = user_context.get("vocabulary_cards", [])
    today = date.today()

    # 1. 筛选今日待复习词
    due_cards = [
        card for card in vocabulary_cards
        if card.get("next_review") and card.get("next_review") <= today
    ]

    # 2. 按优先级排序
    # 优先级：僻义词 > 高频词 > 普通词
    sorted_cards = sorted(
        due_cards,
        key=lambda c: (
            -int(c.get("polysemy_alert", False)),  # 僻义词优先
            -c.get("frequency", 0),                 # 高频词次之
            c.get("next_review", today)             # 越早到期越优先
        )
    )

    # 3. 分组
    high_priority = []
    normal_priority = []

    for card in sorted_cards:
        if card.get("polysemy_alert") or card.get("frequency", 0) >= 4:
            high_priority.append(card)
        else:
            normal_priority.append(card)

    # 4. 获取阶段策略
    days_to_exam = (exam_date - today).days
    phase_target = get_phase_vocabulary_target(days_to_exam)

    return {
        "date": today.isoformat(),
        "phase": phase_target.get("focus"),
        "days_to_exam": days_to_exam,
        "high_priority": format_card_list(high_priority[:20]),  # 最多20个高优先级
        "normal_priority": format_card_list(normal_priority[:30]),  # 最多30个普通
        "stats": {
            "total_due": len(due_cards),
            "high_priority_count": len(high_priority),
            "normal_priority_count": len(normal_priority),
            "polysemy_count": sum(1 for c in due_cards if c.get("polysemy_alert"))
        }
    }


def format_card_list(cards: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """格式化卡片列表为输出格式"""
    result = []
    for card in cards:
        item = {
            "word": card.get("word"),
            "interval": card.get("interval"),
            "review_count": card.get("review_count"),
            "polysemy_alert": card.get("polysemy_alert"),
            "warning_level": card.get("warning_level"),
        }
        if card.get("next_review"):
            item["next_review"] = card["next_review"].isoformat()
        result.append(item)
    return result
