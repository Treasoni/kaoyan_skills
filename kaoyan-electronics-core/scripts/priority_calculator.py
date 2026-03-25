"""
考点权重计算模块

本模块处理822电子技术基础的考点权重计算，包括：
- 优先级分数计算
- 学习时间推荐

来源: code.md 第484-532行
"""

from typing import Tuple


def calculate_priority_score(exam_frequency: int, exam_importance: int,
                             mastery_level: int, days_to_exam: int) -> int:
    """计算知识点优先级分数

    Args:
        exam_frequency: 考试频率 (1-10)
        exam_importance: 考试重要性 (1-10)
        mastery_level: 掌握程度 (0-100)
        days_to_exam: 距离考试天数

    Returns:
        优先级分数
    """
    # 时间衰减因子
    if days_to_exam > 180:
        alpha = 0.8  # 基础阶段
    elif days_to_exam > 90:
        alpha = 1.0  # 强化阶段
    elif days_to_exam > 30:
        alpha = 1.5  # 冲刺阶段
    else:
        alpha = 2.0  # 押题阶段

    # 优先级公式
    priority = (exam_frequency * exam_importance) / (mastery_level + 1) * alpha

    return int(priority * 10)  # 放大10倍便于比较


def get_study_time_recommendation(priority_score: int) -> Tuple[str, str]:
    """根据优先级分数推荐学习时间

    Args:
        priority_score: 优先级分数

    Returns:
        (建议时间, 策略描述)
    """
    if priority_score > 50:
        return ("60-90分钟", "重点突破，每天必练")
    elif priority_score > 20:
        return ("30-45分钟", "强化训练，隔天练习")
    elif priority_score > 10:
        return ("15-20分钟", "保持手感，每周复习")
    else:
        return ("0-10分钟", "考前突击，考前一周")


def calculate_urgency_score(days_to_exam: int, mastery_level: int) -> str:
    """计算紧迫度等级

    Args:
        days_to_exam: 距离考试天数
        mastery_level: 掌握程度 (0-100)

    Returns:
        紧迫度等级 (critical/high/medium/low)
    """
    if days_to_exam < 30 and mastery_level < 60:
        return "critical"
    elif days_to_exam < 60 and mastery_level < 70:
        return "high"
    elif days_to_exam < 90 and mastery_level < 80:
        return "medium"
    else:
        return "low"
