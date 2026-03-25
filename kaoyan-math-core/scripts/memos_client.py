"""
kaoyan-math-core - MemOS客户端模块

本模块提供与MemOS记忆系统的集成功能，包括：
1. 用户上下文加载
2. 错误记录保存
3. 个性化提醒生成
4. 上下文新鲜度检查

版本: v2.0.0 (模块化重构)
来源: code.md 模块化拆分
"""

from typing import Dict, List, Optional, Any
from datetime import datetime


def load_user_context_from_memory(user_input: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """从MemOS加载用户上下文

    此函数尝试从MemOS系统中检索用户的数学学习上下文信息，
    包括用户画像、错题库和知识卡片。如果MemOS不可用，
    将返回None以触发降级处理。

    Args:
        user_input: 用户输入数据，必须包含user_id字段

    Returns:
        dict: 用户上下文信息，包含以下字段：
            - user_profile: 用户画像（数学基础、考试类型等）
            - mistake_records: 历史错题记录
            - knowledge_cards: 已掌握的知识卡片
        None: MemOS不可用时触发降级

    Examples:
        >>> user_input = {"user_id": "student_001"}
        >>> context = load_user_context_from_memory(user_input)
        >>> if context:
        ...     print(f"加载用户画像: {context['user_profile']}")
    """
    try:
        # TODO: 实际实现中需要调用search_memory函数
        # 这里提供接口定义，实际调用由技能框架完成
        results = []  # search_memory(query=f"#user_profile {user_input.get('user_id')}", top_k=10)
        return parse_memory_to_math_context(results)
    except Exception as e:
        # 降级处理：记录警告但不中断流程
        print(f"⚠️ MemOS不可用: {e}")
        return None


def parse_memory_to_math_context(memory_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """将MemOS结果解析为数学学习上下文

    从MemOS返回的原始记忆结果中提取和结构化数学学习相关信息。

    Args:
        memory_results: MemOS搜索结果列表

    Returns:
        dict: 解析后的数学学习上下文，包含：
            - user_profile: 用户画像
            - mistake_records: 错题记录
            - knowledge_cards: 知识卡片
    """
    if not memory_results:
        return create_default_user_context()

    context = {
        "user_profile": extract_user_profile(memory_results),
        "mistake_records": extract_mistake_records(memory_results),
        "knowledge_cards": extract_knowledge_cards(memory_results)
    }

    return context


def create_default_user_context() -> Dict[str, Any]:
    """创建默认用户上下文

    当MemOS不可用或无历史数据时，提供基础的默认上下文。

    Returns:
        dict: 默认用户上下文
    """
    return {
        "user_profile": {
            "math_level": "intermediate",
            "exam_type": "数学二",
            "exam_date": "2026-12-25",
            "weak_modules": []
        },
        "mistake_records": [],
        "knowledge_cards": []
    }


def extract_user_profile(memory_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """从记忆结果中提取用户画像

    Args:
        memory_results: MemOS搜索结果

    Returns:
        dict: 用户画像信息
    """
    # TODO: 实现具体的提取逻辑
    return {
        "math_level": "intermediate",
        "exam_type": "数学二",
        "updated_at": datetime.now()
    }


def extract_mistake_records(memory_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """从记忆结果中提取错题记录

    Args:
        memory_results: MemOS搜索结果

    Returns:
        list: 错题记录列表
    """
    # TODO: 实现具体的提取逻辑
    return []


def extract_knowledge_cards(memory_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """从记忆结果中提取知识卡片

    Args:
        memory_results: MemOS搜索结果

    Returns:
        list: 知识卡片列表
    """
    # TODO: 实现具体的提取逻辑
    return []


def save_mistake_to_memory(mistake_data: Dict[str, Any], user_id: str) -> bool:
    """保存错误记录到MemOS

    将数学学习中的错误记录保存到MemOS系统，便于后续复习和个性化提醒。

    Args:
        mistake_data: 错误记录数据，必须包含：
            - knowledge_point: 知识点名称
            - type: 错误类型（计算错误/概念错误/条件遗漏等）
            - content: 错误内容
            - correction: 正确解法
        user_id: 用户ID

    Returns:
        bool: 保存成功返回True，失败返回False

    Examples:
        >>> mistake = {
        ...     "knowledge_point": "洛必达法则",
        ...     "type": "条件遗漏",
        ...     "content": "未检查0/0型",
        ...     "correction": "必须先验证分子分母都趋于0"
        ... }
        >>> success = save_mistake_to_memory(mistake, "student_001")
    """
    try:
        # TODO: 实际实现中需要调用add_message函数
        # add_message(
        #     messages=[{
        #         "role": "assistant",
        #         "content": {
        #             "type": "mistake_record",
        #             "data": mistake_data
        #         },
        #         "tags": [
        #             "#mistake_record",
        #             f"#kp_{mistake_data['knowledge_point']}",
        #             f"#mistake_type_{mistake_data['type']}",
        #             f"#user_{user_id}"
        #         ]
        #     }],
        #     user_id=user_id
        # )
        print(f"✅ 已保存错题: {mistake_data['knowledge_point']}")
        return True
    except Exception as e:
        print(f"⚠️ 保存错题失败 {mistake_data['knowledge_point']}: {e}")
        # 降级：不影响主流程，仅不保存
        return False


def generate_personalized_reminders(user_id: str, current_kp: str) -> List[str]:
    """基于用户历史错误生成个性化提醒

    分析用户在特定知识点上的历史错误模式，生成针对性的学习提醒。

    Args:
        user_id: 用户ID
        current_kp: 当前知识点

    Returns:
        list: 个性化提醒列表，每个提醒为字符串

    Examples:
        >>> reminders = generate_personalized_reminders("student_001", "洛必达法则")
        >>> print(reminders)
        ['⚠️ 你在条件遗漏方面已出错 5 次，特别注意验证0/0型或∞/∞型']
    """
    try:
        # TODO: 实际实现中需要调用search_memory函数
        # mistake_history = search_memory(
        #     query=f"#mistake_record #user_{user_id} #kp_{current_kp}",
        #     top_k=50
        # )
        mistake_history = []

        if not mistake_history:
            return []

        # 分析错误模式
        error_patterns = aggregate_error_patterns(mistake_history)

        reminders = []
        for pattern in error_patterns:
            if pattern["frequency"] >= 3:  # 重复犯错3次以上
                reminders.append(
                    f"⚠️ 你在 {pattern['type']} 方面已出错 {pattern['frequency']} 次，"
                    f"特别注意 {pattern['trigger']}"
                )

        return reminders
    except Exception as e:
        print(f"⚠️ 生成个性化提醒失败: {e}")
        return []


def aggregate_error_patterns(mistake_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """聚合错误模式

    Args:
        mistake_history: 错误历史记录

    Returns:
        list: 错误模式列表
    """
    # TODO: 实现具体的错误模式聚合逻辑
    return []


def check_context_freshness_math(user_context: Dict[str, Any], current_date: datetime) -> Optional[Dict[str, Any]]:
    """检查数学学习画像是否需要刷新

    根据用户画像的最后更新时间判断是否需要更新用户信息。

    Args:
        user_context: 用户上下文
        current_date: 当前日期

    Returns:
        dict: 包含needs_refresh, reason, questions等字段
            - needs_refresh: bool, 是否需要刷新
            - reason: str, 刷新原因
            - questions: list, 需要询问用户的问题
        None: 不需要刷新

    Examples:
        >>> from datetime import datetime, timedelta
        >>> context = {"user_profile": {"updated_at": datetime.now() - timedelta(days=35)}}
        >>> result = check_context_freshness_math(context, datetime.now())
        >>> print(result['needs_refresh'])
        True
    """
    profile = user_context.get("user_profile")
    if not profile:
        return None

    updated_at = profile.get("updated_at")
    if isinstance(updated_at, str):
        updated_at = datetime.fromisoformat(updated_at)

    days_since_update = (current_date - updated_at).days

    # 超过30天自动触发刷新询问
    if days_since_update > 30:
        return {
            "needs_refresh": True,
            "reason": f"画像已{days_since_update}天未更新",
            "questions": [
                "你的数学水平有变化吗？(基础/中级/高级)",
                f"考试类型需要调整吗？(当前: {profile.get('exam_type', '数一')})",
                f"考试日期需要更新吗？(当前: {profile.get('exam_date', '未设置')})",
                "重点模块需要调整吗？(高数/线代/概率)"
            ]
        }

    return {"needs_refresh": False}


def safe_load_context(user_input: Dict[str, Any]) -> Dict[str, Any]:
    """安全加载用户上下文（含降级处理）

    尝试从MemOS加载用户上下文，如果失败则使用默认上下文。

    Args:
        user_input: 用户输入数据

    Returns:
        dict: 用户上下文（MemOS数据或默认数据）
    """
    context = load_user_context_from_memory(user_input)
    if context is None:
        print("ℹ️ MemOS不可用，使用默认上下文")
        return create_default_user_context()
    return context
