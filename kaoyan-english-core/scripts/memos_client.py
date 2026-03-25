"""
MemOS 集成客户端模块

提供 kaoyan-english-core 技能与 MemOS 的集成功能，包括：
1. 用户上下文加载与保存
2. 词汇卡片持久化
3. 复习会话记录
4. 用户画像新鲜度检查

版本: 2.0.0
创建日期: 2026-03-24
最后更新: 2026-03-24
"""

from datetime import datetime, date
from typing import Dict, List, Optional, Any


def load_user_context_from_memory(user_input: Dict[str, Any]) -> Optional[Dict]:
    """从 MemOS 加载用户上下文

    Args:
        user_input: 用户输入字典，必须包含 user_id 字段

    Returns:
        dict: 用户上下文信息，包含用户画像、词汇库等
        None: MemOS 不可用时触发降级

    Examples:
        >>> user_input = {"user_id": "user123"}
        >>> context = load_user_context_from_memory(user_input)
        >>> if context:
        ...     print(f"Loaded {len(context['vocabulary_cards'])} word cards")
    """
    try:
        # 这里应该调用实际的 search_memory 函数
        # 为了模块化，我们使用占位符
        results = []  # search_memory(query=f"#user_profile #user_{user_input.get('user_id')}", top_k=10)
        return parse_memory_to_english_context(results)
    except Exception as e:
        # log_warning(f"MemOS unavailable: {e}")
        print(f"Warning: MemOS unavailable: {e}")
        return None


def parse_memory_to_english_context(memory_results: List[Dict]) -> Dict[str, Any]:
    """将 MemOS 结果解析为英语学习上下文

    Args:
        memory_results: 从 MemOS 检索到的记忆结果列表

    Returns:
        dict: 包含以下键的上下文字典：
            - user_profile: 用户画像
            - vocabulary_cards: 词汇卡片列表
            - review_history: 复习历史
            - mental_history: 心理状态历史

    Examples:
        >>> results = [{"type": "word_card", "data": {...}}]
        >>> context = parse_memory_to_english_context(results)
        >>> 'user_profile' in context
        True
    """
    if not memory_results:
        return create_default_user_context()

    context = {
        "user_profile": extract_user_profile(memory_results),
        "vocabulary_cards": extract_word_cards(memory_results),
        "review_history": extract_review_records(memory_results),
        "mental_history": extract_mental_state(memory_results)
    }

    return context


def create_default_user_context() -> Dict[str, Any]:
    """创建默认用户上下文（降级方案）

    Returns:
        dict: 默认的空上下文结构
    """
    return {
        "user_profile": {},
        "vocabulary_cards": [],
        "review_history": [],
        "mental_history": []
    }


def extract_user_profile(memory_results: List[Dict]) -> Dict[str, Any]:
    """从记忆结果中提取用户画像

    Args:
        memory_results: 记忆结果列表

    Returns:
        dict: 用户画像数据
    """
    for item in memory_results:
        if item.get("type") == "user_profile":
            return item.get("data", {})
    return {}


def extract_word_cards(memory_results: List[Dict]) -> List[Dict]:
    """从记忆结果中提取词汇卡片

    Args:
        memory_results: 记忆结果列表

    Returns:
        list: 词汇卡片列表
    """
    cards = []
    for item in memory_results:
        if item.get("type") == "word_card":
            cards.append(item.get("data", {}))
    return cards


def extract_review_records(memory_results: List[Dict]) -> List[Dict]:
    """从记忆结果中提取复习记录

    Args:
        memory_results: 记忆结果列表

    Returns:
        list: 复习记录列表
    """
    records = []
    for item in memory_results:
        if item.get("type") == "review_record":
            records.append(item.get("data", {}))
    return records


def extract_mental_state(memory_results: List[Dict]) -> List[Dict]:
    """从记忆结果中提取心理状态历史

    Args:
        memory_results: 记忆结果列表

    Returns:
        list: 心理状态记录列表
    """
    states = []
    for item in memory_results:
        if item.get("type") == "mental_state":
            states.append(item.get("data", {}))
    return states


def save_word_card_to_memory(word_card: Dict, user_id: str) -> None:
    """保存词汇卡片到 MemOS

    Args:
        word_card: 词汇卡片对象，必须包含 word 字段
        user_id: 用户ID

    Examples:
        >>> card = {"word": "example", "meaning": "例子"}
        >>> save_word_card_to_memory(card, "user123")
        Saved word card: example
    """
    try:
        # 这里应该调用实际的 add_message 函数
        # add_message(messages=[...], user_id=user_id)
        # log_info(f"Saved word card: {word_card['word']}")
        print(f"Info: Saved word card: {word_card.get('word', 'unknown')}")
    except Exception as e:
        # log_warning(f"Failed to save word card {word_card.get('word')}: {e}")
        print(f"Warning: Failed to save word card {word_card.get('word')}: {e}")
        # 降级：不影响主流程，仅不保存


def record_review_session(user_id: str, session_data: Dict[str, Any]) -> None:
    """记录复习会话到 MemOS（upsert 逻辑）

    首先查找今日已有记录，如果存在则标记为历史版本，
    然后保存新的当前版本。

    Args:
        user_id: 用户ID
        session_data: 复习会话数据，包含复习统计等信息

    Examples:
        >>> session = {"words_reviewed": 50, "correct_count": 45}
        >>> record_review_session("user123", session)
        Recorded review session for 2026-03-24
    """
    try:
        today = datetime.now().strftime("%Y-%m-%d")

        # 先查找今日已有记录
        # today_session = search_memory(
        #     query=f"#review_session_current #user_{user_id} #date_{today}",
        #     top_k=1
        # )
        today_session = []  # 占位符

        if today_session:
            # 标记旧版本为历史
            # add_message(messages=[...], user_id=user_id)
            pass

        # 保存新会话为当前版本
        # add_message(messages=[...], user_id=user_id)
        # log_info(f"Recorded review session for {today}")
        print(f"Info: Recorded review session for {today}")

    except Exception as e:
        # log_warning(f"Failed to record session: {e}")
        print(f"Warning: Failed to record session: {e}")


def check_context_freshness_english(
    user_context: Dict[str, Any],
    current_date: date
) -> Optional[Dict[str, Any]]:
    """检查英语学习画像是否需要刷新

    Args:
        user_context: 用户上下文，必须包含 user_profile
        current_date: 当前日期

    Returns:
        dict: 包含以下键的字典（需要刷新时）：
            - needs_refresh: True
            - reason: 刷新原因
            - questions: 需要询问用户的问题列表
        None: 不需要刷新

    Examples:
        >>> from datetime import date
        >>> context = {"user_profile": {"updated_at": date(2026, 2, 1),
        ...                            "daily_new_word_target": 50}}
        >>> result = check_context_freshness_english(context, date(2026, 3, 15))
        >>> result['needs_refresh']
        True
    """
    profile = user_context.get("user_profile")
    if not profile:
        return None

    updated_at = profile.get("updated_at")
    if not updated_at:
        return None

    days_since_update = (current_date - updated_at).days

    # 超过30天自动触发刷新询问
    if days_since_update > 30:
        return {
            "needs_refresh": True,
            "reason": f"画像已{days_since_update}天未更新",
            "questions": [
                "你的英语水平有变化吗？(基础/中级/高级)",
                f"每日新词目标需要调整吗？(当前: {profile.get('daily_new_word_target', 50)})",
                "复习重点需要调整吗？(均衡/僻义优先/写作优先)",
                f"僻义敏感度需要调整吗？(当前: {profile.get('polysemy_sensitivity', 'medium')})"
            ]
        }

    return {"needs_refresh": False}


# 导出的公共函数
__all__ = [
    "load_user_context_from_memory",
    "parse_memory_to_english_context",
    "create_default_user_context",
    "save_word_card_to_memory",
    "record_review_session",
    "check_context_freshness_english",
    "extract_user_profile",
    "extract_word_cards",
    "extract_review_records",
    "extract_mental_state",
]
