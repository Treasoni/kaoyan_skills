"""
kaoyan-math-core - 知识点图谱模块

本模块提供数学知识点之间的关联关系管理，包括：
1. 知识点关系图数据结构
2. 前置知识、组合应用、跨章节关联
3. 主动关联提示生成

版本: v2.0.0 (模块化重构)
来源: code.md 模块化拆分
"""

from typing import Dict, List, Optional, Any


# 知识点关系图数据结构
KNOWLEDGE_GRAPH: Dict[str, Dict[str, Any]] = {
    "洛必达法则": {
        "prerequisites": ["极限定义", "导数定义"],
        "combinations": ["等价无穷小", "泰勒公式"],
        "applications": ["定积分应用", "变限积分求导"],
        "cross_chapter_prompts": [
            "注意：当遇到变限积分求导时，通常会结合洛必达法则考查",
            "建议：同时复习 [[定积分应用]] 中的变限积分部分",
            "关联：洛必达法则常与泰勒公式结合考查极限问题"
        ]
    },
    "泰勒公式": {
        "prerequisites": ["导数定义", "高阶导数"],
        "combinations": ["洛必达法则", "等价无穷小"],
        "applications": ["级数展开", "近似计算"],
        "cross_chapter_prompts": [
            "注意：泰勒公式在处理复杂函数极限时比洛必达法则更简洁",
            "建议：掌握常见函数的泰勒展开式（sin x, cos x, e^x, ln(1+x)）",
            "关联：泰勒公式是级数展开的基础，参考 [[幂级数]]"
        ]
    },
    "变限积分求导": {
        "prerequisites": ["定积分定义", "导数定义"],
        "combinations": ["洛必达法则", "复合函数求导"],
        "applications": ["积分方程", "微分方程"],
        "cross_chapter_prompts": [
            "注意：变限积分求导常与洛必达法则结合考查极限",
            "建议：熟练掌握牛顿-莱布尼茨公式和链式法则",
            "关联：遇到积分方程时，常需先求导转化为微分方程"
        ]
    },
    "等价无穷小": {
        "prerequisites": ["极限定义", "无穷小概念"],
        "combinations": ["洛必达法则", "泰勒公式"],
        "applications": ["极限计算", "级数收敛性判断"],
        "cross_chapter_prompts": [
            "注意：等价无穷小替换在乘除法中可用，加减法中需谨慎",
            "建议：牢记常见等价无穷小（x→0时）",
            "关联：与泰勒公式结合可处理更复杂的极限问题"
        ]
    },
    "定积分定义": {
        "prerequisites": ["极限概念", "黎曼和"],
        "combinations": ["变限积分", "反常积分"],
        "applications": ["面积计算", "物理应用"],
        "cross_chapter_prompts": [
            "注意：定积分的几何意义是曲边梯形面积",
            "建议：理解积分定义的分割、近似、求和、取极限过程",
            "关联：定积分是变限积分求导的基础"
        ]
    },
    "导数定义": {
        "prerequisites": ["极限概念", "函数连续性"],
        "combinations": ["复合函数求导", "隐函数求导"],
        "applications": ["切线方程", "单调性判断"],
        "cross_chapter_prompts": [
            "注意：导数的几何意义是切线斜率",
            "建议：掌握导数的几种定义形式",
            "关联：导数定义是洛必达法则、泰勒公式的基础"
        ]
    }
}


def generate_proactive_links(knowledge_point: str, user_mistakes: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    """生成主动关联提示

    基于知识点关系图生成学习建议和关联提示，包括：
    - 前置知识提醒
    - 常见组合考查点
    - 跨章节关联提示
    - 基于用户历史错误的个性化提醒

    Args:
        knowledge_point: 当前知识点名称
        user_mistakes: 用户历史错误记录（可选），用于生成个性化提醒

    Returns:
        dict: 关联提示结构，包含以下字段：
            - prerequisites: list, 前置知识点列表
            - combinations: list, 常见组合考查点
            - cross_chapter_prompts: list, 跨章节提示
            - personalized: list, 个性化提醒（基于用户历史错误）

    Examples:
        >>> links = generate_proactive_links("洛必达法则")
        >>> print(links['prerequisites'])
        ['极限定义', '导数定义']
        >>> print(links['cross_chapter_prompts'][0])
        '注意：当遇到变限积分求导时，通常会结合洛必达法则考查'

        >>> # 带个性化提醒
        >>> mistakes = [{"type": "条件遗漏", "condition": "0/0型验证"}]
        >>> links = generate_proactive_links("洛必达法则", mistakes)
        >>> print(links['personalized'][0])
        '💡 你经常遗漏0/0型验证条件，复习时重点看 [[洛必达法则]] 的定理条件部分'
    """
    graph = KNOWLEDGE_GRAPH.get(knowledge_point, {})

    links = {
        "prerequisites": graph.get("prerequisites", []),
        "combinations": graph.get("combinations", []),
        "cross_chapter_prompts": graph.get("cross_chapter_prompts", []),
        "personalized": []
    }

    # 生成个性化提示（基于用户历史错误）
    if user_mistakes:
        for mistake in user_mistakes:
            if mistake.get("type") == "条件遗漏":
                condition = mistake.get("condition", "相关条件")
                links["personalized"].append(
                    f"💡 你经常遗漏{condition}条件，"
                    f"复习时重点看 [[{knowledge_point}]] 的定理条件部分"
                )
            elif mistake.get("type") == "计算错误":
                links["personalized"].append(
                    f"💡 你在 {mistake.get('content', '该知识点')} 上出现过计算错误，"
                    f"建议多练习相关计算题"
                )

    return links


def get_prerequisites(knowledge_point: str) -> List[str]:
    """获取知识点的前置知识

    Args:
        knowledge_point: 知识点名称

    Returns:
        list: 前置知识点列表，如果知识点不存在则返回空列表
    """
    return KNOWLEDGE_GRAPH.get(knowledge_point, {}).get("prerequisites", [])


def get_combinations(knowledge_point: str) -> List[str]:
    """获取知识点的常见组合考查点

    Args:
        knowledge_point: 知识点名称

    Returns:
        list: 常见组合考查点列表
    """
    return KNOWLEDGE_GRAPH.get(knowledge_point, {}).get("combinations", [])


def get_applications(knowledge_point: str) -> List[str]:
    """获取知识点的应用场景

    Args:
        knowledge_point: 知识点名称

    Returns:
        list: 应用场景列表
    """
    return KNOWLEDGE_GRAPH.get(knowledge_point, {}).get("applications", [])


def get_cross_chapter_prompts(knowledge_point: str) -> List[str]:
    """获取跨章节关联提示

    Args:
        knowledge_point: 知识点名称

    Returns:
        list: 跨章节提示列表
    """
    return KNOWLEDGE_GRAPH.get(knowledge_point, {}).get("cross_chapter_prompts", [])


def check_prerequisite_mastery(knowledge_point: str, mastered_kps: List[str]) -> Dict[str, Any]:
    """检查前置知识掌握情况

    Args:
        knowledge_point: 要学习的知识点
        mastered_kps: 用户已掌握的知识点列表

    Returns:
        dict: 包含以下字段：
            - ready: bool, 是否准备好学习该知识点
            - missing_prerequisites: list, 未掌握的前置知识点
            - suggestions: list, 学习建议
    """
    prerequisites = get_prerequisites(knowledge_point)
    missing = [kp for kp in prerequisites if kp not in mastered_kps]

    if missing:
        return {
            "ready": False,
            "missing_prerequisites": missing,
            "suggestions": [
                f"⚠️ 学习「{knowledge_point}」前需要先掌握：",
                f"  - {', '.join(missing)}",
                f"💡 建议按顺序学习：{' → '.join(missing + [knowledge_point])}"
            ]
        }

    return {
        "ready": True,
        "missing_prerequisites": [],
        "suggestions": [
            f"✅ 你已掌握学习「{knowledge_point}」所需的前置知识"
        ]
    }


def add_knowledge_point(
    name: str,
    prerequisites: List[str],
    combinations: List[str],
    applications: List[str],
    cross_chapter_prompts: List[str]
) -> None:
    """添加新知识点到关系图

    Args:
        name: 知识点名称
        prerequisites: 前置知识点列表
        combinations: 常见组合考查点列表
        applications: 应用场景列表
        cross_chapter_prompts: 跨章节提示列表
    """
    KNOWLEDGE_GRAPH[name] = {
        "prerequisites": prerequisites,
        "combinations": combinations,
        "applications": applications,
        "cross_chapter_prompts": cross_chapter_prompts
    }


def get_all_knowledge_points() -> List[str]:
    """获取所有知识点列表

    Returns:
        list: 所有知识点名称列表
    """
    return list(KNOWLEDGE_GRAPH.keys())
