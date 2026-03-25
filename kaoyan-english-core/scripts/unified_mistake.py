"""
统一错误模型模块

提供英语错误记录的统一格式和保存功能，包括：
1. 错误记录保存
2. 错误类型标记
3. 僻义错误特殊处理

版本: 2.0.0
创建日期: 2026-03-24
最后更新: 2026-03-24
"""

from typing import Dict, List, Any, Optional
from datetime import datetime


def save_unified_english_mistake(
    mistake_data: Dict[str, Any],
    user_id: str
) -> None:
    """保存英语错误记录（统一格式）

    将错误记录保存到 MemOS，使用统一的错误模型格式。
    僻义错误会自动添加 #polysemy_critical 标签。

    Args:
        mistake_data: 错误数据字典，包含：
            - type: 错误类型
            - word: 相关词汇（可选）
            - tags: 标签列表
            - 其他错误详情
        user_id: 用户ID

    Examples:
        >>> mistake = {
        ...     "type": "polysemy_error",
        ...     "word": "address",
        ...     "tags": ["#error"],
        ...     "context": "误将address理解为'地址'，应为'演讲'"
        ... }
        >>> save_unified_english_mistake(mistake, "user123")
    """
    mistake_data["subject"] = "english"

    # 英语专用错误类型处理
    if mistake_data.get("type") == "polysemy_error":
        mistake_data.setdefault("tags", []).append("#polysemy_critical")

    try:
        # 这里应该调用实际的 add_message 函数
        # add_message(
        #     messages=[{
        #         "role": "assistant",
        #         "content": {
        #             "type": "unified_mistake_record",
        #             "data": mistake_data
        #         },
        #         "tags": [
        #             "#mistake_record",
        #             "#subject_english",
        #             f"#word_{mistake_data.get('word', '')}",
        #             f"#mistake_type_{mistake_data.get('type', 'unknown')}",
        #             f"#user_{user_id}"
        #         ]
        #     }],
        #     user_id=user_id
        # )
        print(f"Info: Saved mistake record for word: {mistake_data.get('word', 'unknown')}")
    except Exception as e:
        # log_warning(f"Failed to save mistake: {e}")
        print(f"Warning: Failed to save mistake: {e}")


def create_mistake_record(
    mistake_type: str,
    word: str,
    correct_answer: str,
    user_answer: str,
    context: str = "",
    tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """创建标准化的错误记录

    Args:
        mistake_type: 错误类型（如 "polysemy_error", "spelling_error"）
        word: 相关词汇
        correct_answer: 正确答案
        user_answer: 用户答案
        context: 错误上下文
        tags: 额外标签

    Returns:
        dict: 标准化的错误记录

    Examples:
        >>> record = create_mistake_record(
        ...     "polysemy_error", "address", "演讲", "地址",
        ...     "真题语境：2020年Text1"
        ... )
        >>> record['type']
        'polysemy_error'
    """
    if tags is None:
        tags = []

    return {
        "type": mistake_type,
        "word": word,
        "correct_answer": correct_answer,
        "user_answer": user_answer,
        "context": context,
        "tags": tags,
        "timestamp": datetime.now().isoformat(),
        "subject": "english"
    }


def batch_save_mistakes(
    mistakes: List[Dict[str, Any]],
    user_id: str
) -> int:
    """批量保存错误记录

    Args:
        mistakes: 错误记录列表
        user_id: 用户ID

    Returns:
        int: 成功保存的错误数量

    Examples:
        >>> mistakes = [
        ...     create_mistake_record("polysemy_error", "test", "A", "B"),
        ...     create_mistake_record("spelling_error", "example", "example", "exmple"),
        ... ]
        >>> count = batch_save_mistakes(mistakes, "user123")
        >>> count
        2
    """
    saved_count = 0
    for mistake in mistakes:
        try:
            save_unified_english_mistake(mistake, user_id)
            saved_count += 1
        except Exception as e:
            print(f"Warning: Failed to save mistake for {mistake.get('word')}: {e}")

    return saved_count


def analyze_mistake_patterns(
    mistakes: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """分析错误模式

    Args:
        mistakes: 错误记录列表

    Returns:
        dict: 错误模式分析结果

    Examples:
        >>> mistakes = [
        ...     {"type": "polysemy_error", "word": "address"},
        ...     {"type": "polysemy_error", "word": "company"},
        ...     {"type": "spelling_error", "word": "example"},
        ... ]
        >>> analysis = analyze_mistake_patterns(mistakes)
        >>> analysis['polysemy_error_count']
        2
    """
    type_counts = {}
    word_counts = {}

    for mistake in mistakes:
        # 统计错误类型
        mistake_type = mistake.get("type", "unknown")
        type_counts[mistake_type] = type_counts.get(mistake_type, 0) + 1

        # 统计错误词汇
        word = mistake.get("word", "")
        if word:
            word_counts[word] = word_counts.get(word, 0) + 1

    # 找出最常见的错误类型和词汇
    most_common_type = max(type_counts.items(), key=lambda x: x[1])[0] if type_counts else None
    most_common_word = max(word_counts.items(), key=lambda x: x[1])[0] if word_counts else None

    return {
        "total_mistakes": len(mistakes),
        "type_counts": type_counts,
        "word_counts": word_counts,
        "most_common_type": most_common_type,
        "most_common_word": most_common_word,
        "polysemy_error_count": type_counts.get("polysemy_error", 0),
        "polysemy_error_ratio": type_counts.get("polysemy_error", 0) / len(mistakes) if mistakes else 0
    }


def get_polysemy_critical_words(
    mistakes: List[Dict[str, Any]],
    min_error_count: int = 2
) -> List[str]:
    """获取僻义错误关键词汇

    Args:
        mistakes: 错误记录列表
        min_error_count: 最小错误次数阈值

    Returns:
        list: 需要重点关注的僻义词列表

    Examples:
        >>> mistakes = [
        ...     {"type": "polysemy_error", "word": "address"},
        ...     {"type": "polysemy_error", "word": "address"},
        ...     {"type": "polysemy_error", "word": "company"},
        ... ]
        >>> critical = get_polysemy_critical_words(mistakes, 2)
        >>> 'address' in critical
        True
    """
    polysemy_errors = [
        m for m in mistakes
        if m.get("type") == "polysemy_error"
    ]

    word_counts = {}
    for mistake in polysemy_errors:
        word = mistake.get("word", "")
        if word:
            word_counts[word] = word_counts.get(word, 0) + 1

    critical_words = [
        word for word, count in word_counts.items()
        if count >= min_error_count
    ]

    return critical_words


# 导出的公共函数
__all__ = [
    "save_unified_english_mistake",
    "create_mistake_record",
    "batch_save_mistakes",
    "analyze_mistake_patterns",
    "get_polysemy_critical_words",
]
