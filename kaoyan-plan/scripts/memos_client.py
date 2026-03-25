"""
MemOS 记忆管理模块

本模块处理与 MemOS MCP 工具的交互，包括：
- 用户上下文的加载与解析
- 计划的保存与版本控制（upsert with tag 逻辑）
- 周数据汇总与统计
- 时间判断辅助函数

来源: code.md 第120-185行, 第823-926行
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any


def safe_load_context(user_input: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    从 MemOS 加载用户上下文，失败时返回 None 触发降级

    参数:
        user_input: 用户输入数据，包含 conversation_id 和 user_id

    返回:
        用户上下文字典，包含 user_profile, yesterday_plan, weekly_progress 等
        失败时返回 None
    """
    try:
        # 注意: search_memory 需要在技能调用时可用
        from mcp__MemoryOperatingSystem__search_memory import search_memory

        results = search_memory(
            query=f"用户画像配置 学习进度记录",
            conversation_first_message=user_input.get("conversation_id", ""),
            memory_limit_number=10
        )
        return parse_memory_results_to_context(results)
    except Exception as e:
        log_warning(f"MemOS unavailable, using defaults: {e}")
        return None


def safe_save_plan(plan: Dict[str, Any], user_input: Dict[str, Any], mode: str) -> None:
    """
    保存生成的计划（v3.1 增强: upsert with tag 逻辑）

    功能：
        1. 先尝试查找今日已有计划
        2. 如果存在，标记旧版本为历史，保存新版本为当前
        3. 如果不存在，直接保存新计划

    参数:
        plan: 生成的计划数据
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")
    """
    try:
        # 注意: search_memory 和 add_message 需要在技能调用时可用
        from mcp__MemoryOperatingSystem__search_memory import search_memory
        from mcp__MemoryOperatingSystem__add_message import add_message

        today = datetime.now().strftime("%Y-%m-%d")
        user_id = user_input.get("user_id", "")

        # v3.1: 先尝试查找今日已有计划
        try:
            today_plan = search_memory(
                query=f"#daily_plan_current {user_id} {today}",
                conversation_first_message=user_input.get("conversation_id", ""),
                memory_limit_number=1
            )
        except:
            today_plan = []

        if today_plan:
            # 更新: 标记旧版本为历史，保存新版本为当前
            old_plan = today_plan[0]
            try:
                add_message(
                    conversation_first_message=user_input.get("conversation_id", ""),
                    messages=[{
                        "role": "assistant",
                        "content": {
                            "type": "daily_plan",
                            "version": old_plan.get("version", "v1"),
                            "status": "superseded",
                            "data": old_plan.get("data"),
                            "superseded_at": datetime.now().isoformat()
                        }
                    }],
                    feedback_content="",
                    agent_id=user_id
                )
            except:
                pass  # 保存历史版本失败不影响主流程

        # 保存新计划为当前版本
        add_message(
            conversation_first_message=user_input.get("conversation_id", ""),
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "daily_plan",
                    "mode": mode,
                    "version": f"v{datetime.now().strftime('%H%M')}",
                    "status": "current",
                    "data": plan,
                    "timestamp": datetime.now().isoformat()
                }
            }],
            feedback_content="",
            agent_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to save plan to memory: {e}")


def parse_memory_results_to_context(memory_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    解析 MemOS 搜索结果为用户上下文

    参数:
        memory_results: MemOS 搜索结果列表

    返回:
        用户上下文字典，包含:
        - user_profile: 用户画像
        - yesterday_plan: 昨日计划
        - weekly_progress: 本周进度
        - historical_stats: 历史统计
    """
    context = {
        "user_profile": None,
        "yesterday_plan": None,
        "weekly_progress": None,
        "historical_stats": None
    }

    for result in memory_results:
        content = result.get("content", {})
        if isinstance(content, dict):
            content_type = content.get("type")
            if content_type == "user_profile":
                context["user_profile"] = content.get("data")
            elif content_type == "daily_plan" and is_yesterday(result.get("timestamp", "")):
                context["yesterday_plan"] = content.get("data")
            elif content_type == "task_completion" and is_this_week(result.get("timestamp", "")):
                if not context["weekly_progress"]:
                    context["weekly_progress"] = []
                context["weekly_progress"].append(content.get("data"))

    return context


def load_weekly_data_for_review(user_id: str) -> Optional[Dict[str, Any]]:
    """
    加载本周数据用于周日复盘

    参数:
        user_id: 用户ID

    返回:
        本周统计数据，失败时返回 None
    """
    try:
        from mcp__MemoryOperatingSystem__search_memory import search_memory

        results = search_memory(
            query=f"本周学习记录 {user_id}",
            conversation_first_message=user_id,
            memory_limit_number=20
        )
        return aggregate_weekly_stats(results)
    except Exception:
        return None


def aggregate_weekly_stats(weekly_records: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    汇总本周统计数据

    参数:
        weekly_records: 本周完成记录列表

    返回:
        汇总统计字典，包含各科的 planned, actual, rate, debt
    """
    if not weekly_records:
        return None

    aggregated = {
        "math": {"planned": 0, "actual": 0},
        "english": {"planned": 0, "actual": 0},
        "major": {"planned": 0, "actual": 0},
        "politics": {"planned": 0, "actual": 0}
    }

    for record in weekly_records:
        for subject in aggregated.keys():
            aggregated[subject]["planned"] += record.get(f"{subject}_planned", 0)
            aggregated[subject]["actual"] += record.get(f"{subject}_actual", 0)

    # 计算完成率和欠账
    for subject in aggregated.keys():
        planned = aggregated[subject]["planned"]
        actual = aggregated[subject]["actual"]
        aggregated[subject]["rate"] = (actual / planned * 100) if planned > 0 else 0
        aggregated[subject]["debt"] = max(0, planned - actual)

    return aggregated


def calculate_completion_stats(completed_tasks: List[Dict[str, Any]],
                               planned_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    计算任务完成统计

    参数:
        completed_tasks: 完成的任务列表
        planned_tasks: 计划的任务列表

    返回:
        统计字典，包含 total_planned_hours, total_actual_hours, completion_rate, debt_hours
    """
    total_planned = sum(t.get("planned_duration", 0) for t in planned_tasks)
    total_actual = sum(t.get("actual_duration", 0) for t in completed_tasks)
    completion_rate = (total_actual / total_planned * 100) if total_planned > 0 else 0

    return {
        "total_planned_hours": total_planned,
        "total_actual_hours": total_actual,
        "completion_rate": completion_rate,
        "debt_hours": max(0, total_planned - total_actual)
    }


def is_yesterday(timestamp_str: str) -> bool:
    """
    判断时间戳是否为昨天

    参数:
        timestamp_str: ISO 格式时间戳字符串

    返回:
        是否为昨天
    """
    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        yesterday = datetime.now() - timedelta(days=1)
        return timestamp.date() == yesterday.date()
    except:
        return False


def is_this_week(timestamp_str: str) -> bool:
    """
    判断时间戳是否为本周

    参数:
        timestamp_str: ISO 格式时间戳字符串

    返回:
        是否为本周
    """
    try:
        timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        week_end = week_start + timedelta(days=6)
        return week_start.date() <= timestamp.date() <= week_end.date()
    except:
        return False


def log_info(message: str) -> None:
    """记录信息日志"""
    # 在实际实现中可以使用 logger
    pass


def log_warning(message: str) -> None:
    """记录警告日志"""
    # 在实际实现中可以使用 logger
    pass
