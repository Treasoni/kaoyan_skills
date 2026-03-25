"""
MemOS 集成模块

本模块处理822电子技术基础的MemOS集成，包括：
- 用户上下文加载
- 错误记录保存
- 个性化提醒生成
- 画像新鲜度检查

来源: code.md 第9-175行
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import json

CONVERSATION_ID = None  # 在运行时设置


def load_user_context_from_memory(user_id: str) -> Dict[str, Any]:
    """从MemOS加载电子技术学习上下文

    Args:
        user_id: 用户ID

    Returns:
        用户上下文字典，包含画像、错误历史、知识点卡片
    """
    try:
        # 搜索用户画像
        profile_results = search_memory(
            query=f"#user_profile #subject_electronics #user_{user_id}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=1
        )

        # 搜索错误历史
        mistake_results = search_memory(
            query=f"#mistake_record #subject_electronics #user_{user_id}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=50
        )

        # 搜索知识点卡片
        knowledge_results = search_memory(
            query=f"#knowledge_card #subject_electronics #user_{user_id}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=100
        )

        return {
            "profile": parse_profile(profile_results),
            "mistakes": parse_mistakes(mistake_results),
            "knowledge_cards": parse_knowledge_cards(knowledge_results),
            "loaded": True
        }
    except Exception as e:
        log_warning(f"MemOS不可用，降级为无状态模式: {e}")
        return {
            "profile": get_default_profile(),
            "mistakes": [],
            "knowledge_cards": {},
            "loaded": False
        }


def save_mistake_to_memory(user_id: str, knowledge_point: str, mistake_type: str,
                           original_understanding: str, correction: str) -> None:
    """保存错误记录到MemOS

    Args:
        user_id: 用户ID
        knowledge_point: 知识点名称（如"负反馈类型判断"）
        mistake_type: 错误类型
        original_understanding: 原始理解
        correction: 正确理解
    """
    from .cross_subject import find_math_refs

    mistake_data = {
        "knowledge_point": knowledge_point,
        "mistake_type": mistake_type,
        "original_understanding": original_understanding,
        "correction": correction,
        "timestamp": get_current_time(),
        "subject": "electronics"
    }

    # 查找数学关联
    cross_refs = find_math_refs(knowledge_point)
    if cross_refs:
        mistake_data["cross_subject_refs"] = cross_refs

    try:
        add_message(
            conversation_first_message=CONVERSATION_ID,
            messages=[{
                "role": "assistant",
                "content": json.dumps(mistake_data),
                "chat_time": get_current_time()
            }]
        )
    except Exception as e:
        log_warning(f"保存错误记录失败: {e}")


def generate_personalized_reminders(user_id: str, knowledge_point: str = None) -> List[Dict[str, Any]]:
    """基于历史错误生成个性化提醒

    Args:
        user_id: 用户ID
        knowledge_point: 可选，限定特定知识点

    Returns:
        个性化提醒列表
    """
    context = load_user_context_from_memory(user_id)
    if not context["loaded"]:
        return []

    reminders = []

    # 统计各知识点错误次数
    mistake_counts = {}
    for mistake in context["mistakes"]:
        kp = mistake.get("knowledge_point")
        if knowledge_point and kp != knowledge_point:
            continue
        mistake_counts[kp] = mistake_counts.get(kp, 0) + 1

    # 生成高频错误提醒
    for kp, count in mistake_counts.items():
        if count >= 3:
            # 获取该知识点的常见错误类型
            common_types = get_common_mistake_types(context["mistakes"], kp)
            reminders.append({
                "knowledge_point": kp,
                "mistake_count": count,
                "common_types": common_types,
                "reminder": f"⚠️ 你在「{kp}」方面已出错{count}次",
                "suggestion": generate_suggestion(kp, common_types)
            })

    return reminders


def check_context_freshness_electronics(user_id: str) -> tuple:
    """检查用户画像是否需要刷新

    Returns:
        (is_fresh, days_since_update, prompt_if_stale)
    """
    try:
        results = search_memory(
            query=f"#user_profile #subject_electronics #user_{user_id}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=1
        )

        if not results:
            return (False, None, "请确认你的822电子技术基础学习配置")

        last_update = parse_timestamp(results[0])
        days_since = (datetime.now() - last_update).days

        if days_since > 30:
            return (
                False,
                days_since,
                f"你的学习配置已{days_since}天未更新，请确认是否需要调整"
            )

        return (True, days_since, None)
    except Exception as e:
        return (False, None, "无法检查学习配置，请手动确认")


# ============ 辅助函数 ============

def parse_profile(results) -> Dict[str, Any]:
    """解析用户画像"""
    if not results:
        return get_default_profile()
    # 简化实现
    return get_default_profile()


def parse_mistakes(results) -> List[Dict[str, Any]]:
    """解析错误历史"""
    return []  # 简化实现


def parse_knowledge_cards(results) -> Dict[str, Any]:
    """解析知识点卡片"""
    return {}  # 简化实现


def parse_timestamp(memory_item) -> datetime:
    """从MemOS记录解析时间戳"""
    return datetime.now()  # 简化实现


def get_default_profile() -> Dict[str, Any]:
    """获取默认用户画像"""
    return {
        "exam_type": "822电子技术基础",
        "target_school": "湖南大学",
        "focus_modules": ["模电", "数电"]
    }


def get_current_time() -> str:
    """获取当前时间字符串"""
    return datetime.now().isoformat()


def log_warning(message: str) -> None:
    """记录警告日志"""
    print(f"[WARNING] {message}")


def get_common_mistake_types(mistakes: List[Dict], knowledge_point: str) -> List[str]:
    """获取某知识点的常见错误类型"""
    types = []
    for m in mistakes:
        if m.get("knowledge_point") == knowledge_point:
            types.append(m.get("mistake_type"))
    return list(set(types))


def generate_suggestion(knowledge_point: str, common_types: List[str]) -> List[str]:
    """根据错误类型生成建议"""
    suggestions = {
        "circuit_misread": "建议先识别电路拓扑，再进行分析",
        "calculation_error": "注意单位统一，检查公式是否正确",
        "concept_confusion": "建议画对比表格，区分易混淆概念",
        "forgot_condition": "使用检查清单，确保不遗漏条件"
    }
    return [suggestions.get(t, "多练习相关题目") for t in common_types]
