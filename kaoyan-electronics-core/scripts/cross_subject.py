"""
跨学科知识关联模块

本模块处理数学与电子技术之间的跨学科知识关联，包括：
- 数学→电子技术知识图谱
- 电子技术→数学反向映射
- 跨学科提醒生成

来源: code.md 第299-351行
"""

from typing import Dict, Any, List, Optional


# 数学→电子技术知识图谱
MATH_TO_ELECTRONICS_MAP = {
    "复数运算": ["频率响应分析", "交流电路", "滤波器设计", "阻抗计算"],
    "微分方程": ["暂态响应", "RC/RL电路", "一阶电路分析"],
    "积分": ["RC充放电", "能量计算", "电容储能"],
    "拉普拉斯变换": ["s域分析", "传递函数", "频域分析"]
}

# 电子技术→数学反向映射
ELECTRONICS_TO_MATH_MAP = {
    "频率响应分析": ["复数运算", "对数运算"],
    "暂态响应": ["微分方程", "指数函数"],
    "滤波器设计": ["拉普拉斯变换", "复数运算"],
    "RC电路": ["积分", "微分方程"],
    "RL电路": ["微分方程", "指数函数"]
}


def generate_cross_subject_reminders(electronics_topic: str) -> Optional[Dict[str, Any]]:
    """生成跨学科提醒（数学→电子技术）

    Args:
        electronics_topic: 当前学习的电子技术主题

    Returns:
        跨学科提醒
    """
    math_topics = ELECTRONICS_TO_MATH_MAP.get(electronics_topic, [])
    if not math_topics:
        return None

    return {
        "electronics_topic": electronics_topic,
        "required_math": math_topics,
        "reminder": f"⚠️ 「{electronics_topic}」需要以下数学基础：{', '.join(math_topics)}",
        "suggestion": f"💡 建议先复习数学「{math_topics[0]}」再深入学习{electronics_topic}"
    }


def find_math_refs(electronics_topic: str) -> List[str]:
    """查找与电子技术知识点相关的数学知识点

    Args:
        electronics_topic: 电子技术知识点

    Returns:
        相关数学知识点列表
    """
    return ELECTRONICS_TO_MATH_MAP.get(electronics_topic, [])


def find_electronics_refs(math_topic: str) -> List[str]:
    """查找与数学知识点相关的电子技术知识点

    Args:
        math_topic: 数学知识点

    Returns:
        相关电子技术知识点列表
    """
    return MATH_TO_ELECTRONICS_MAP.get(math_topic, [])
