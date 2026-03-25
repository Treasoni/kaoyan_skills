"""
记忆压缩模式模块

当 kaoyan-plan 检测到其他科目欠账时，触发英语记忆压缩模式，
包括：
1. 压缩模式激活
2. 学习策略调整
3. 时间转移计算

版本: 2.0.0
创建日期: 2026-03-24
最后更新: 2026-03-24
"""

from typing import Dict, Any


def activate_memory_compression_mode(context: Dict[str, Any]) -> Dict[str, Any]:
    """激活记忆压缩模式

    当其他科目（如数学、专业课）出现欠账时，
    压缩英语学习时间，将时间转移至紧急科目。

    Args:
        context: 压缩上下文，包含：
            - compress_hours: 压缩后的学习小时数
            - transfer_to: 转移到的科目

    Returns:
        dict: 压缩后的学习计划，包含：
            - mode: "memory_compression"
            - original_hours: 原计划英语学习小时数
            - compressed_hours: 压缩后小时数
            - transfer_to: 转移目标科目
            - strategy: 压缩策略（减少新词、专注僻义等）
            - message: 提示信息

    Examples:
        >>> context = {"compress_hours": 1, "transfer_to": "math"}
        >>> plan = activate_memory_compression_mode(context)
        >>> plan['mode']
        'memory_compression'
        >>> plan['strategy']['reduce_new_words']
        True
    """
    compress_hours = context.get("compress_hours", 1)
    transfer_to = context.get("transfer_to", "math")

    return {
        "mode": "memory_compression",
        "original_hours": get_planned_english_hours(),
        "compressed_hours": compress_hours,
        "transfer_to": transfer_to,
        "strategy": {
            "reduce_new_words": True,           # 减少新词量
            "focus_polysemy_only": True,        # 只复习僻义词
            "skip_context_article": True,       # 跳过语境文章生成
            "use_quick_review": True            # 使用快速复习模式
        },
        "message": f"⚠️ 英语时间压缩{compress_hours}小时，转移至{transfer_to}"
    }


def get_planned_english_hours() -> float:
    """获取原计划的英语学习小时数

    Returns:
        float: 计划的英语学习小时数

    Examples:
        >>> hours = get_planned_english_hours()
        >>> hours > 0
        True
    """
    # 这里应该从用户画像或计划中获取
    # 暂时返回默认值
    return 3.0


def calculate_compression_ratio(
    original_hours: float,
    compressed_hours: float
) -> float:
    """计算压缩比例

    Args:
        original_hours: 原计划小时数
        compressed_hours: 压缩后小时数

    Returns:
        float: 压缩比例（0.0-1.0）

    Examples:
        >>> ratio = calculate_compression_ratio(3.0, 1.0)
        >>> round(ratio, 2)
        0.33
    """
    if original_hours == 0:
        return 0.0
    return compressed_hours / original_hours


def adjust_vocabulary_target_for_compression(
    daily_target: int,
    compression_ratio: float
) -> int:
    """根据压缩比例调整词汇学习目标

    Args:
        daily_target: 原每日新词目标
        compression_ratio: 压缩比例

    Returns:
        int: 调整后的每日新词目标

    Examples:
        >>> target = adjust_vocabulary_target_for_compression(50, 0.5)
        >>> target
        25
    """
    adjusted = int(daily_target * compression_ratio)
    # 至少保留10个新词
    return max(adjusted, 10)


def generate_compression_recovery_plan(
    compressed_hours: float,
    original_hours: float
) -> Dict[str, Any]:
    """生成压缩恢复计划

    当压缩模式结束后，如何恢复到正常学习状态。

    Args:
        compressed_hours: 压缩期间的小时数
        original_hours: 原计划的小时数

    Returns:
        dict: 恢复计划，包含每日增量恢复策略

    Examples:
        >>> plan = generate_compression_recovery_plan(1.0, 3.0)
        >>> 'recovery_schedule' in plan
        True
    """
    deficit = original_hours - compressed_hours
    recovery_days = 3  # 用3天时间恢复

    daily_increase = deficit / recovery_days

    return {
        "total_deficit_hours": deficit,
        "recovery_days": recovery_days,
        "daily_increase_hours": daily_increase,
        "recovery_schedule": [
            {
                "day": i + 1,
                "hours": compressed_hours + daily_increase * (i + 1),
                "focus": "gradual_increase" if i < recovery_days - 1 else "full_recovery"
            }
            for i in range(recovery_days)
        ]
    }


# 导出的公共函数
__all__ = [
    "activate_memory_compression_mode",
    "get_planned_english_hours",
    "calculate_compression_ratio",
    "adjust_vocabulary_target_for_compression",
    "generate_compression_recovery_plan",
]
