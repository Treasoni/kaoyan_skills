"""
学习统计Dashboard模块

本模块处理考研英语词汇的学习统计，包括：
- 学习统计Dashboard生成
- 进度图表数据生成
- 近7天复习统计

来源: code.md 第289-383行
"""

from datetime import date
from typing import Dict, Any, List


def generate_statistics_dashboard(user_context: Dict[str, Any]) -> Dict[str, Any]:
    """生成学习统计Dashboard

    Args:
        user_context: 用户上下文

    Returns:
        dict: 统计数据
    """
    vocabulary_cards = user_context.get("vocabulary_cards", [])
    review_history = user_context.get("review_history", [])

    # 基础统计
    total_words = len(vocabulary_cards)
    mastered_count = sum(
        1 for c in vocabulary_cards
        if c.get("review_count", 0) >= 5 and c.get("forgetting_rate", 1) < 0.2
    )
    reviewing_count = sum(
        1 for c in vocabulary_cards
        if c.get("review_count", 0) > 0 and c.get("forgetting_rate", 1) >= 0.2
    )
    new_count = sum(
        1 for c in vocabulary_cards
        if c.get("review_count", 0) == 0
    )

    # 僻义统计
    polysemy_words = [c for c in vocabulary_cards if c.get("polysemy_alert")]
    polysemy_mastered = sum(
        1 for c in polysemy_words
        if c.get("review_count", 0) >= 5 and c.get("forgetting_rate", 1) < 0.2
    )
    polysemy_need_review = len(polysemy_words) - polysemy_mastered

    # 近7天复习统计
    recent_reviews = [
        r for r in review_history
        if (date.today() - r.get("date", date.today())).days <= 7
    ]
    total_reviewed = sum(r.get("words_reviewed", 0) for r in recent_reviews)

    total_correct = sum(r.get("results", {}).get("correct_count", 0) for r in recent_reviews)
    total_incorrect = sum(r.get("results", {}).get("incorrect_count", 0) for r in recent_reviews)
    total_attempts = total_correct + total_incorrect
    avg_accuracy = total_correct / max(1, total_attempts)

    return {
        "summary": {
            "total_words": total_words,
            "mastered_count": mastered_count,
            "mastered_percentage": f"{mastered_count / max(1, total_words) * 100:.1f}%",
            "reviewing_count": reviewing_count,
            "new_count": new_count
        },
        "polysemy": {
            "total": len(polysemy_words),
            "mastered": polysemy_mastered,
            "need_review": polysemy_need_review
        },
        "recent_7_days": {
            "total_reviewed": total_reviewed,
            "avg_accuracy": f"{avg_accuracy * 100:.1f}%",
            "daily_avg": total_reviewed / 7
        },
        "progress_chart": generate_progress_chart_data(review_history)
    }


def generate_progress_chart_data(review_history: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    """生成进度图表数据"""
    # 按日期聚合
    daily_data = {}
    for record in review_history:
        record_date = record.get("date")
        if record_date:
            date_str = record_date.isoformat()
            if date_str not in daily_data:
                daily_data[date_str] = {
                    "reviewed": 0,
                    "correct": 0,
                    "incorrect": 0
                }
            daily_data[date_str]["reviewed"] += record.get("session_info", {}).get("words_reviewed", 0)
            daily_data[date_str]["correct"] += record.get("results", {}).get("correct_count", 0)
            daily_data[date_str]["incorrect"] += record.get("results", {}).get("incorrect_count", 0)

    return daily_data
