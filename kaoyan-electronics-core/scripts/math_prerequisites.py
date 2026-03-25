"""
数学前置检查模块

本模块处理822电子技术基础的数学前置知识检查，包括：
- 数学前置知识常量定义
- 前置知识检查算法
- 数学掌握程度评估

来源: code.md 第179-295行
"""

from typing import Dict, Any, List, Optional


# 数学前置知识常量
MATH_PREREQUISITES = {
    "频率响应分析": {
        "required_math": [
            {
                "topic": "复数运算",
                "level": "basic",
                "check": "能正确进行复数加减乘除运算",
                "refresher": "复数运算回顾：j²=-1, Z=R+jX"
            },
            {
                "topic": "对数运算",
                "level": "basic",
                "check": "能理解对数坐标（波特图）",
                "refresher": "对数坐标：20log|H(jω)|"
            }
        ],
        "warning": "⚠️ 开始「频率响应」前，建议先确认数学基础是否扎实"
    },
    "暂态响应": {
        "required_math": [
            {
                "topic": "微分方程",
                "level": "intermediate",
                "check": "能求解一阶线性微分方程",
                "refresher": "一阶RC方程：τ·du/dt + u = U"
            },
            {
                "topic": "指数函数",
                "level": "basic",
                "check": "理解指数函数的图像和性质",
                "refresher": "指数衰减：e^(-t/τ)"
            }
        ],
        "warning": "⚠️ 「暂态响应」需要微分方程基础"
    },
    "滤波器设计": {
        "required_math": [
            {
                "topic": "拉普拉斯变换",
                "level": "intermediate",
                "check": "理解s域分析",
                "refresher": "传递函数：H(s)=Uo(s)/Ui(s)"
            }
        ],
        "warning": "⚠️ 「滤波器设计」需要拉普拉斯变换基础"
    }
}


def check_math_prerequisites(topic: str, user_context: Dict[str, Any]) -> Dict[str, Any]:
    """检查数学前置知识

    Args:
        topic: 要学习的电子技术主题
        user_context: 用户上下文（含数学学习记录）

    Returns:
        前置检查结果和建议
    """
    prereqs = MATH_PREREQUISITES.get(topic)

    if not prereqs:
        return {"needed": False}

    results = []
    for req in prereqs["required_math"]:
        math_topic = req["topic"]
        # 检查用户数学掌握程度
        mastery = get_math_mastery_level(user_context, math_topic)

        results.append({
            "topic": math_topic,
            "required_level": req["level"],
            "current_level": mastery,
            "passed": mastery >= req["level"],
            "refresher": req["refresher"]
        })

    all_passed = all(r["passed"] for r in results)

    return {
        "needed": True,
        "topic": topic,
        "warning": prereqs["warning"] if not all_passed else None,
        "results": results,
        "all_passed": all_passed
    }


def get_math_mastery_level(user_context: Dict[str, Any], math_topic: str) -> int:
    """获取用户对某数学知识点的掌握程度

    Args:
        user_context: 用户上下文
        math_topic: 数学知识点名称

    Returns:
        掌握程度 (0-100)
    """
    # 尝试从MemOS获取数学学习记录
    try:
        results = search_memory(
            query=f"#knowledge_card #subject_math #kp_{math_topic}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=1
        )
        if results:
            return parse_mastery_level(results[0])
    except:
        pass

    # 默认返回基础水平
    return 30


def parse_mastery_level(memory_item) -> int:
    """从MemOS记录解析掌握程度"""
    return 30  # 简化实现


# 运行时设置的变量
CONVERSATION_ID = None
