"""
复习记录保存模块

本模块处理考研英语词汇的复习记录保存，包括：
- 复习结果保存
- 复习历史记录

来源: code.md 第387-428行
"""

from datetime import datetime, date
from typing import Dict, Any, Optional

from .sm2_kaoyan import calculate_next_review_kaoyan


def save_review_result(user_id: str, word: str, quality: int,
                       review_time: Optional[datetime] = None) -> bool:
    """保存复习结果

    Args:
        user_id: 用户ID
        word: 复习的单词
        quality: 回忆质量评分 (0-5)
        review_time: 复习时间（可选）

    Returns:
        bool: 是否保存成功
    """
    review_time = review_time or datetime.now()

    try:
        # 获取当前卡片
        card = get_word_card(user_id, word)

        # 计算下次复习时间
        exam_date = get_exam_date(user_id)
        updated_card = calculate_next_review_kaoyan(card, quality, exam_date)

        # 更新卡片
        update_word_card(user_id, updated_card)

        # 记录复习历史
        add_review_history(user_id, {
            "word": word,
            "quality": quality,
            "review_time": review_time,
            "interval": updated_card.get("interval"),
            "phase": updated_card.get("current_phase")
        })

        log_info(f"Saved review result for {word}: quality={quality}")
        return True
    except Exception as e:
        log_warning(f"Failed to save review result: {e}")
        return False


# ============ 辅助函数（需在运行时实现） ============

def get_word_card(user_id: str, word: str) -> Dict[str, Any]:
    """获取词汇卡片"""
    # 简化实现：实际应从存储中获取
    return {
        "word": word,
        "review_count": 0,
        "interval": 1,
        "ease_factor": 2.5,
        "correct_count": 0,
        "incorrect_count": 0,
    }


def update_word_card(user_id: str, card: Dict[str, Any]) -> None:
    """更新词汇卡片"""
    # 简化实现：实际应保存到存储
    pass


def get_exam_date(user_id: str) -> date:
    """获取考试日期"""
    # 简化实现：返回默认考试日期
    return date(2026, 12, 24)


def add_review_history(user_id: str, record: Dict[str, Any]) -> None:
    """添加复习历史记录"""
    # 简化实现：实际应保存到存储
    pass


def log_info(message: str) -> None:
    """记录信息日志"""
    print(f"[INFO] {message}")


def log_warning(message: str) -> None:
    """记录警告日志"""
    print(f"[WARNING] {message}")
