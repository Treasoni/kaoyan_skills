"""
状态与调度规则引擎模块

本模块处理学习计划的各种状态判断和调度规则，包括：
- 任务欠账检测与熔断机制（>10h 触发恢复模式）
- 心理健康干预（连续3天疲惫触发调节模式）
- 用户画像新鲜度检查（30天刷新）
- 疲劳度混合模型计算
- 时段偏好与 Chronotype 适配
- 时间块切分算法（基于脑科学）

来源: code.md 第1164-1479行, 第1759-1798行
"""

from datetime import datetime, timedelta, date
from typing import Dict, List, Any, Optional

# 欠账熔断阈值
DEBT_LIMIT = 10  # 10小时熔断阈值


# =============================================================================
# 欠账检测与熔断机制
# =============================================================================

def check_task_debt_with_memory(previous_plan: Optional[Dict[str, Any]],
                                user_input: Dict[str, Any],
                                user_context: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    检查任务欠账（v3.1 增强版：含熔断机制）

    参数:
        previous_plan: 昨日计划
        user_input: 用户输入
        user_context: 用户上下文

    返回:
        欠账任务信息 或 熔断信息，无欠账时返回 None
    """
    debt_tasks = []

    # 如果提供了 previous_plan 参数，直接使用
    if previous_plan:
        debt_tasks = check_task_debt(previous_plan, user_input.get("completed_tasks", []))
    # 否则尝试从 MemOS 读取昨日计划
    elif user_context:
        yesterday_plan = user_context.get("yesterday_plan")
        if yesterday_plan:
            debt_tasks = check_task_debt(yesterday_plan, user_input.get("completed_tasks", []))

    if not debt_tasks:
        return None

    # v3.1: 熔断检查
    total_debt_hours = calculate_total_debt_hours(user_context, debt_tasks)

    if total_debt_hours > DEBT_LIMIT:
        return {
            "type": "debt_emergency",
            "total_hours": total_debt_hours,
            "strategy": "recovery_only",
            "message": f"⚠️ 欠账已达{total_debt_hours}小时，超过安全阈值（{DEBT_LIMIT}小时）",
            "suggestion": "暂停所有新内容，专注补账",
            "tasks": generate_recovery_plan(total_debt_hours)
        }

    return {
        "type": "debt_warning",
        "tasks": debt_tasks,
        "total_hours": total_debt_hours
    }


def calculate_total_debt_hours(user_context: Optional[Dict[str, Any]],
                                current_debt_tasks: List[Dict[str, Any]]) -> float:
    """
    计算总欠账时长（含历史累计）

    参数:
        user_context: 用户上下文
        current_debt_tasks: 当前欠账任务列表

    返回:
        总欠账小时数
    """
    current_debt = sum(task.get("duration", 0) for task in current_debt_tasks)

    # 从用户上下文中获取历史累计欠账
    historical_debt = 0
    if user_context and user_context.get("weekly_progress"):
        for record in user_context.get("weekly_progress", []):
            historical_debt += record.get("debt_hours", 0)

    return current_debt + historical_debt


def generate_recovery_plan(total_debt_hours: float) -> List[Dict[str, Any]]:
    """
    生成紧急恢复计划（熔断触发后使用）

    参数:
        total_debt_hours: 总欠账小时数

    返回:
        恢复任务列表
    """
    recovery_tasks = [
        {
            "subject": "数学",
            "duration": min(total_debt_hours * 0.4, 4),
            "task": "【补账】数学错题重做 + 未完成练习",
            "priority": 1
        },
        {
            "subject": "专业课",
            "duration": min(total_debt_hours * 0.3, 3),
            "task": "【补账】专业课复习",
            "priority": 2
        },
        {
            "subject": "英语",
            "duration": min(total_debt_hours * 0.2, 2),
            "task": "【补账】英语阅读补做",
            "priority": 3
        },
        {
            "subject": "政治",
            "duration": min(total_debt_hours * 0.1, 1),
            "task": "【补账】政治选择题补做",
            "priority": 4
        }
    ]

    return recovery_tasks


def generate_emergency_recovery_plan(debt_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成紧急恢复计划（熔断模式）

    参数:
        debt_result: 欠账检测结果

    返回:
        紧急恢复计划字典
    """
    return {
        "type": "emergency_recovery",
        "total_debt_hours": debt_result.get("total_hours"),
        "message": debt_result.get("message"),
        "suggestion": debt_result.get("suggestion"),
        "recovery_plan": debt_result.get("tasks"),
        "notice": "⚠️ 今日暂停所有新内容学习，专注补账。欠账降至安全阈值后自动恢复正常模式。"
    }


def check_task_debt(previous_plan: Optional[Dict[str, Any]],
                   completed_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    检查任务欠账（基础版本）

    参数:
        previous_plan: 昨日计划
        completed_tasks: 完成的任务列表

    返回:
        欠账任务列表
    """
    if not previous_plan:
        return []

    debt_tasks = []
    planned_tasks = previous_plan.get("tasks", [])

    for task in planned_tasks:
        task_description = task.get("task", "")
        # 检查是否在已完成任务中
        is_completed = any(
            completed_task.get("task", "") == task_description
            for completed_task in completed_tasks
        )
        if not is_completed:
            debt_tasks.append(task)

    return debt_tasks


def generate_debt_handling_plan(user_input: Dict[str, Any],
                                debt_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成补课计划（实战补丁1）

    欠账处理策略：
    - 轻微（<1h）：碎片时间补
    - 中等（1-3h）：压缩低优先任务
    - 严重（>3h）：建议补课日

    参数:
        user_input: 用户输入
        debt_tasks: 欠账任务列表

    返回:
        补课计划字典
    """
    total_debt_hours = sum(task.get("duration", 0) for task in debt_tasks)

    if total_debt_hours < 1:
        strategy = "fragment"
    elif total_debt_hours < 3:
        strategy = "compress"
    else:
        strategy = "recovery_day"

    return {
        "type": "debt_handling",
        "debt_tasks": debt_tasks,
        "total_hours": total_debt_hours,
        "strategy": strategy,
        "options": generate_debt_options(debt_tasks, strategy)
    }


def generate_debt_options(debt_tasks: List[Dict[str, Any]],
                          strategy: str) -> List[str]:
    """
    生成欠账处理选项

    参数:
        debt_tasks: 欠账任务列表
        strategy: 处理策略

    返回:
        选项列表
    """
    if strategy == "fragment":
        return ["利用碎片时间补做", "推迟到明天"]
    elif strategy == "compress":
        return ["压缩低优先任务时间", "延后部分任务"]
    else:
        return ["安排补课日", "周末集中补做"]


# =============================================================================
# 心理干预检查
# =============================================================================

def check_mental_health_intervention(user_context: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """
    检查是否需要心理干预（v3.1 mental_status 追踪）

    参数:
        user_context: 用户上下文

    返回:
        干预信息字典，无需干预时返回 None
    """
    if not user_context:
        return None

    profile = user_context.get("user_profile")
    if not profile:
        return None

    mental_history = profile.get("mental_history", [])
    if not mental_history or len(mental_history) < 3:
        return None

    # 检查最近3天的状态
    recent_days = mental_history[-3:]
    tired_count = sum(1 for d in recent_days if d.get("status") in ["tired", "burned_out"])

    if tired_count >= 3:
        # 分析压力水平
        avg_stress = sum(d.get("stress_level", 0.5) for d in recent_days) / len(recent_days)

        # 找出触发原因
        triggers = [d.get("trigger") for d in recent_days if d.get("trigger")]
        common_trigger = max(set(triggers), key=triggers.count) if triggers else "持续学习"

        return {
            "intervention_needed": True,
            "mode": "psychological_adjustment",
            "tired_days": tired_count,
            "avg_stress": avg_stress,
            "common_trigger": common_trigger,
            "actions": [
                "在计划开头添加鼓励语",
                "强制安排休息活动",
                "减少学习量30%"
            ]
        }

    return None


def record_mental_status(user_id: str, mental_status: str,
                         stress_level: float, trigger: Optional[str] = None) -> None:
    """
    记录用户心理状态到 MemOS

    参数:
        user_id: 用户ID
        mental_status: 心理状态（ energetic, normal, tired, burned_out）
        stress_level: 压力水平（0.0-1.0）
        trigger: 触发原因（可选）
    """
    try:
        from mcp__MemoryOperatingSystem__add_message import add_message

        add_message(
            conversation_first_message=user_id,
            messages=[{
                "role": "user",
                "content": {
                    "type": "mental_status_update",
                    "data": {
                        "date": date.today().isoformat(),
                        "status": mental_status,
                        "stress_level": stress_level,
                        "trigger": trigger
                    }
                }
            }],
            feedback_content="",
            agent_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to record mental status: {e}")


# =============================================================================
# 画像刷新检查
# =============================================================================

def check_context_freshness(user_context: Optional[Dict[str, Any]],
                           current_date: datetime) -> Optional[Dict[str, Any]]:
    """
    检查用户画像是否需要刷新（v3.1 context_refresh 机制）

    参数:
        user_context: 用户上下文（含用户画像）
        current_date: 当前日期

    返回:
        刷新询问信息字典，无需刷新时返回 None
    """
    if not user_context:
        return None

    profile = user_context.get("user_profile")
    if not profile:
        return None

    # 检查画像更新时间
    updated_at = profile.get("updated_at")
    if not updated_at:
        return None

    try:
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)

        days_since_update = (current_date.date() - updated_at.date()).days

        # 超过30天自动触发刷新询问
        if days_since_update > 30:
            refresh_config = profile.get("refresh_config", {})
            auto_refresh_interval = refresh_config.get("auto_refresh_interval", 30)

            if days_since_update > auto_refresh_interval:
                return {
                    "needs_refresh": True,
                    "reason": f"画像已{days_since_update}天未更新",
                    "days_since_update": days_since_update,
                    "current_chronotype": profile.get("profile", {}).get("chronotype", "未知"),
                    "current_sensitivity": profile.get("preferences", {}).get("fatigue_sensitivity", "未知"),
                    "questions": [
                        "你的作息类型有变化吗？(晨型人/夜型人/正常)",
                        "科目优先级需要调整吗？",
                        "疲劳敏感度有变化吗？(高/中/低)"
                    ]
                }
    except Exception as e:
        log_warning(f"Failed to check context freshness: {e}")

    return {"needs_refresh": False}


def generate_profile_refresh_question(refresh_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成画像刷新询问

    参数:
        refresh_info: 刷新信息字典

    返回:
        询问信息字典
    """
    return {
        "type": "profile_refresh",
        "reason": refresh_info.get("reason"),
        "days_since_update": refresh_info.get("days_since_update"),
        "current_settings": {
            "chronotype": refresh_info.get("current_chronotype"),
            "fatigue_sensitivity": refresh_info.get("current_sensitivity")
        },
        "questions": refresh_info.get("questions"),
        "message": f"⚠️ {refresh_info.get('reason')}，为了提供更准确的计划，请确认以下设置是否有变化："
    }


# =============================================================================
# 疲劳度与时段
# =============================================================================

def calculate_mixed_fatigue(self_report: str, behavior_data: Optional[Dict[str, Any]] = None) -> float:
    """
    混合疲劳度计算

    参数:
        self_report: 用户主观感受
        behavior_data: 行为数据（可选）

    返回:
        疲劳度 (0.0-1.0)
    """
    # 主观感受权重 0.6
    self_report_map = {
        "精力很好": 0.0,
        "正常": 0.3,
        "有点累": 0.6,
        "很累": 0.9
    }
    subjective = self_report_map.get(self_report, 0.3)

    # 行为数据权重 0.4
    if behavior_data:
        behavioral = calculate_behavior_fatigue(behavior_data)
    else:
        behavioral = 0.0

    return subjective * 0.6 + behavioral * 0.4


def calculate_behavior_fatigue(behavior_data: Dict[str, Any]) -> float:
    """
    根据行为数据计算疲劳度

    参数:
        behavior_data: 行为数据字典

    返回:
        疲劳度 (0.0-1.0)
    """
    # 简化实现：根据学习时长和连续学习天数计算
    study_hours = behavior_data.get("study_hours", 0)
    consecutive_days = behavior_data.get("consecutive_days", 0)

    # 学习时长疲劳因子
    hours_fatigue = min(study_hours / 12, 1.0) * 0.5

    # 连续学习疲劳因子
    days_fatigue = min(consecutive_days / 7, 1.0) * 0.5

    return hours_fatigue + days_fatigue


def get_slot_preferences(chronotype: str) -> Dict[str, List[str]]:
    """
    根据作息类型返回时段偏好

    参数:
        chron_type: "morning_person" | "night_person" | "normal"

    返回:
        时段偏好字典
    """
    if chronotype == "night_person":
        return {
            "morning": ["单词", "轻松内容"],
            "afternoon": ["英语阅读", "专业课"],
            "evening": ["数学", "高难度内容"],
            "late_night": ["适度复习"]
        }
    else:  # 默认晨型人
        return {
            "morning": ["数学", "英语单词"],
            "afternoon": ["英语阅读", "专业课"],
            "evening": ["专业课", "政治", "复盘"],
            "late_night": ["仅复习"]
        }


def check_min_block_duration(slot: Dict[str, Any], subject: str) -> str:
    """
    检查时段是否满足科目最小时长要求（实战补丁3）

    如果不满足，自动替换为可碎片化的科目

    参数:
        slot: 时段信息字典
        subject: 科目名称

    返回:
        原科目或替换后的科目
    """
    min_duration = get_min_block_duration(subject)

    if slot.get("duration", 0) < min_duration:
        # 不满足，自动替换
        return suggest_fragment_subject(slot.get("duration", 0))

    return subject


def get_min_block_duration(subject: str) -> float:
    """
    获取科目最小时长要求

    参数:
        subject: 科目名称

    返回:
        最小时长（小时）
    """
    requirements = {
        "数学": 1.5,      # 需要90分钟以上进入状态
        "英语阅读": 1.0,  # 需要完整文章语境
        "专业课": 1.0,    # 需要深度思考
        "单词": 0.25,     # 15分钟即可
        "政治选择": 0.33, # 20分钟即可
        "错题复习": 0.5   # 30分钟即可
    }
    return requirements.get(subject, 1.0)


def suggest_fragment_subject(duration: float) -> str:
    """
    为碎片时段建议合适的科目

    参数:
        duration: 时段时长（小时）

    返回:
        建议的科目名称
    """
    if duration <= 0.25:  # 15分钟以内
        return "单词"
    elif duration <= 0.5:  # 30分钟以内
        return "政治选择题"
    else:  # 30-60分钟
        return "错题复习"


def split_large_time_block(duration: float, subject: str) -> List[Dict[str, Any]]:
    """
    将长时间块自动切分为高效的小时间块

    参数:
        duration: 原始时长（分钟）
        subject: 科目类型

    返回:
        切分后的时间块列表
    """
    # 数学等高强度科目：45分钟一块
    if subject in ["数学", "专业课"]:
        block_duration = 45
        break_duration = 15
    # 英语阅读等中等强度：60分钟一块
    elif subject in ["英语阅读"]:
        block_duration = 60
        break_duration = 15
    # 单词等低强度：可直接延续
    else:
        return [{"type": "continuous", "duration": duration}]

    blocks = []
    remaining = duration

    while remaining > 0:
        if remaining <= block_duration:
            blocks.append({"type": "study", "duration": remaining})
            break
        else:
            blocks.append({"type": "study", "duration": block_duration})
            blocks.append({"type": "break", "duration": break_duration})
            remaining -= (block_duration + break_duration)

    return blocks


def is_sunday(check_date: Optional[date] = None) -> bool:
    """
    判断是否为周日

    参数:
        check_date: 要检查的日期，默认为今天

    返回:
        是否为周日
    """
    if check_date is None:
        check_date = date.today()
    return check_date.weekday() == 6  # 6 = Sunday


def log_warning(message: str) -> None:
    """记录警告日志"""
    pass
