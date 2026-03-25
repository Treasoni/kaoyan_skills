"""
主规划器模块

本模块是 kaoyan-plan 技能的核心规划引擎，负责：
- 组装主规划流程
- 协调各子模块调用
- 处理降级逻辑（MemOS 不可用时）
- 导入所有子模块

来源: code.md 第23-116行, 第930-1158行

版本: v3.11.0
"""

from datetime import datetime, date
from typing import Dict, List, Any, Optional, Union

# 导入子模块
from . import memos_client
from . import progress_tracker
from . import sm2_algorithm
from . import rules_engine


# =============================================================================
# 主规划算法 v3.0 (MemOS 集成版)
# =============================================================================

def generate_daily_plan_v3(user_input: Dict[str, Any],
                           mode: str = "minimal",
                           previous_plan: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    根据用户输入模式生成计划（含 MemOS 记忆集成）

    这是系统默认应调用的主规划器，包含完整的 MemOS 集成功能。

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")
        previous_plan: 昨日计划（用于检测欠账）

    返回:
        每日计划字典
    """
    # 1. MemOS: 读取用户上下文 (可降级)
    user_context = memos_client.safe_load_context(user_input)

    # 1.5 v3.1: 检查画像新鲜度 (context_refresh 机制)
    profile_refresh = rules_engine.check_context_freshness(user_context, datetime.now())
    if profile_refresh and profile_refresh.get("needs_refresh"):
        # 返回画像刷新询问，等待用户确认后再继续
        return rules_engine.generate_profile_refresh_question(profile_refresh)

    # 1.6 v3.1: 检查心理状态是否需要干预
    mental_intervention = rules_engine.check_mental_health_intervention(user_context)
    if mental_intervention and mental_intervention.get("intervention_needed"):
        # 标记为心理调节模式，后续生成计划时应用
        user_input["mental_mode"] = mental_intervention.get("mode")

    # 2. 检查任务欠账（v3.1 增强: 含熔断机制）
    debt_result = rules_engine.check_task_debt_with_memory(previous_plan, user_input, user_context)
    if debt_result:
        # v3.1: 检查是否触发熔断
        if debt_result.get("type") == "debt_emergency":
            return rules_engine.generate_emergency_recovery_plan(debt_result)
        # 普通欠账处理
        return generate_debt_handling_plan_v3(user_input, debt_result.get("tasks", []))

    # 3. 检查周日复盘（增强: 从 MemOS 读取本周数据）
    if rules_engine.is_sunday():
        return generate_sunday_review_plan_with_memory(user_input, user_context)

    # 4. 根据模式确定数据丰富度
    if mode == "minimal":
        user_data = apply_defaults(user_input, user_context)
    elif mode == "standard":
        user_data = enrich_with_exam_info(user_input, user_context)
    else:
        user_data = merge_user_input_with_memory(user_input, user_context)

    # 5. 获取空闲时段
    free_slots = extract_free_slots(user_data.get("schedule", {}))

    # 6. 应用 chronotype 适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = rules_engine.get_slot_preferences(chronotype)

    # 7. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = rules_engine.calculate_mixed_fatigue(
            user_data.get("self_report"),
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0

    # 8. v3.2: 验证单词表复习任务（防止遗漏新学单词）
    missed_vocab_tasks = sm2_algorithm.validate_vocabulary_review_files()
    if missed_vocab_tasks:
        memos_client.log_warning(f"发现 {len(missed_vocab_tasks)} 个未安排复习的单词表，已自动添加")
        # 将遗漏的复习任务添加到上午时段
        user_input.setdefault("morning_tasks", []).extend(missed_vocab_tasks)

    # 9. 分配时段到科目（含最小块时长检查）
    plan = allocate_slots_to_subjects(
        free_slots,
        slot_preferences,
        fatigue,
        min_block_check=True
    )

    # 10. v3.2: 计划生成后一致性检查
    consistency_issues = sm2_algorithm.consistency_check_after_plan_generation(plan)
    if consistency_issues:
        memos_client.log_warning(f"发现 {len(consistency_issues)} 个一致性问题:")
        for issue in consistency_issues:
            memos_client.log_warning(f"  - {issue.get('message')}")

    # 11. MemOS: 保存计划 (可降级)
    memos_client.safe_save_plan(plan, user_input, mode)

    return plan


# =============================================================================
# 主规划算法 v2.1 (降级兼容版)
# =============================================================================

def generate_daily_plan(user_input: Dict[str, Any],
                       mode: str = "minimal",
                       previous_plan: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    根据用户输入模式生成计划（含实战补丁，无 MemOS 降级版）

    当 MemOS 不可用时，系统会降级使用此算法。

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")
        previous_plan: 昨日计划（用于检测欠账）

    返回:
        每日计划字典
    """
    # 1. 检查任务欠账（实战补丁1）
    debt_tasks = rules_engine.check_task_debt(previous_plan, user_input.get("completed_tasks", []))

    if debt_tasks:
        # 欠账处理
        return rules_engine.generate_debt_handling_plan(user_input, debt_tasks)

    # 2. 检查是否周日（实战补丁2）
    if rules_engine.is_sunday():
        return generate_sunday_review_plan(user_input)

    # 3. 根据模式确定数据丰富度
    if mode == "minimal":
        user_data = apply_defaults(user_input)
    elif mode == "standard":
        user_data = enrich_with_exam_info(user_input)
    else:
        user_data = user_input

    # 4. 获取空闲时段
    free_slots = extract_free_slots(user_data.get("schedule", {}))

    # 5. 应用 chronotype 适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = rules_engine.get_slot_preferences(chronotype)

    # 6. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = rules_engine.calculate_mixed_fatigue(
            user_data.get("self_report"),
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0

    # 7. 分配时段到科目（含最小块时长检查）
    plan = allocate_slots_to_subjects(
        free_slots,
        slot_preferences,
        fatigue,
        min_block_check=True
    )

    return plan


# =============================================================================
# 主规划算法 (自适应版/极简版)
# =============================================================================

def generate_daily_plan_adaptive(user_input: Dict[str, Any], mode: str = "minimal") -> Dict[str, Any]:
    """
    根据用户输入模式生成计划（极简自适应版）

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")

    返回:
        每日计划字典
    """
    # 1. 根据模式确定数据丰富度
    if mode == "minimal":
        user_data = apply_defaults(user_input)
    elif mode == "standard":
        user_data = enrich_with_exam_info(user_input)
    else:
        user_data = user_input

    # 2. 获取空闲时段
    free_slots = extract_free_slots(user_data.get("schedule", {}))

    # 3. 应用 chronotype 适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = rules_engine.get_slot_preferences(chronotype)

    # 4. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = rules_engine.calculate_mixed_fatigue(
            user_data.get("self_report"),
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0

    # 5. 分配时段到科目
    plan = allocate_slots_to_subjects(
        free_slots,
        slot_preferences,
        fatigue
    )

    return plan


# =============================================================================
# 周日复盘计划生成
# =============================================================================

def generate_sunday_review_plan_with_memory(user_input: Dict[str, Any],
                                             user_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成周日复盘计划（增强版：从 MemOS 读取本周数据）

    参数:
        user_input: 用户输入
        user_context: 用户上下文

    返回:
        周日复盘计划字典
    """
    weekly_stats = None
    if user_context:
        weekly_stats = user_context.get("weekly_progress")

    return {
        "type": "sunday_review",
        "date": date.today().isoformat(),
        "weekly_stats": weekly_stats,
        "tasks": [
            {"time": "19:00-19:30", "task": "本周完成度统计", "required": True},
            {"time": "19:30-20:00", "task": "数学错题重做", "required": True},
            {"time": "20:00-20:30", "task": "英语错题重做", "required": True},
            {"time": "20:30-21:00", "task": "专业课错题重做", "required": True},
            {"time": "21:00-21:30", "task": "政治错题重做", "required": True},
            {"time": "21:30-22:00", "task": "进度对齐检查", "required": True},
            {"time": "22:00-23:00", "task": "下周计划调整", "required": True}
        ]
    }


def generate_sunday_review_plan(user_input: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成周日复盘计划（基础版）

    参数:
        user_input: 用户输入

    返回:
        周日复盘计划字典
    """
    return {
        "type": "sunday_review",
        "date": date.today().isoformat(),
        "tasks": [
            {"time": "19:00-19:30", "task": "本周完成度统计", "required": True},
            {"time": "19:30-20:00", "task": "数学错题重做", "required": True},
            {"time": "20:00-20:30", "task": "英语错题重做", "required": True},
            {"time": "20:30-21:00", "task": "专业课错题重做", "required": True},
            {"time": "21:00-21:30", "task": "政治错题重做", "required": True},
            {"time": "21:30-22:00", "task": "进度对齐检查", "required": True},
            {"time": "22:00-23:00", "task": "下周计划调整", "required": True}
        ]
    }


# =============================================================================
# 辅助函数
# =============================================================================

def apply_defaults(user_input: Dict[str, Any],
                   user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    应用默认值到用户输入（极简模式）

    参数:
        user_input: 用户输入
        user_context: 用户上下文（可选）

    返回:
        补充后的用户数据
    """
    defaults = {
        "chronotype": "morning_person",
        "exam_date": "2026-12-25",
        "subjects": {
            "math": {"priority": 1.5, "progress": 0},
            "english": {"priority": 1.2, "progress": 0},
            "major": {"priority": 1.0, "progress": 0},
            "politics": {"priority": 0.6, "progress": 0}
        }
    }

    # 从用户上下文补充数据
    if user_context and user_context.get("user_profile"):
        profile = user_context["user_profile"]
        if profile.get("chronotype"):
            defaults["chronotype"] = profile["chronotype"]
        if profile.get("subjects"):
            defaults["subjects"] = profile["subjects"]

    result = defaults.copy()
    result.update(user_input)
    return result


def enrich_with_exam_info(user_input: Dict[str, Any],
                           user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    用考试信息丰富用户输入（标准模式）

    参数:
        user_input: 用户输入
        user_context: 用户上下文（可选）

    返回:
        丰富后的用户数据
    """
    result = apply_defaults(user_input, user_context)

    # 标准模式可能包含的额外信息
    if "exam_date" not in result:
        result["exam_date"] = "2026-12-25"

    return result


def merge_user_input_with_memory(user_input: Dict[str, Any],
                                  user_context: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    合并用户输入与记忆数据（高级模式）

    参数:
        user_input: 用户输入
        user_context: 用户上下文

    返回:
        合并后的用户数据
    """
    result = user_input.copy()

    if user_context:
        if user_context.get("user_profile"):
            result.setdefault("chronotype", user_context["user_profile"].get("chronotype", "morning_person"))
            result.setdefault("subjects", user_context["user_profile"].get("subjects", {}))
        if user_context.get("weekly_progress"):
            result["weekly_progress"] = user_context["weekly_progress"]

    return result


def extract_free_slots(schedule: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    从课表中提取空闲时段

    参数:
        schedule: 课表数据

    返回:
        空闲时段列表
    """
    # 简化实现：假设 schedule 已包含空闲时段信息
    # 实际实现需要解析课表图片/PDF/文字
    if isinstance(schedule, list):
        return schedule
    elif isinstance(schedule, dict) and "free_slots" in schedule:
        return schedule["free_slots"]
    else:
        # 默认返回一个标准空闲时段
        return [
            {"period": "morning", "start": "08:00", "end": "12:00", "duration": 4},
            {"period": "afternoon", "start": "14:00", "end": "18:00", "duration": 4},
            {"period": "evening", "start": "19:00", "end": "23:00", "duration": 4}
        ]


def allocate_slots_to_subjects(free_slots: List[Dict[str, Any]],
                               slot_preferences: Dict[str, List[str]],
                               fatigue: float,
                               min_block_check: bool = False) -> Dict[str, Any]:
    """
    分配时段到科目

    参数:
        free_slots: 空闲时段列表
        slot_preferences: 时段偏好字典
        fatigue: 疲劳度 (0.0-1.0)
        min_block_check: 是否检查最小块时长

    返回:
        生成的计划字典
    """
    plan = {
        "type": "daily_plan",
        "date": date.today().isoformat(),
        "tasks": [],
        "fatigue_adjusted": fatigue > 0.5
    }

    # 根据疲劳度调整休息比例
    if fatigue < 0.3:
        rest_ratio = 0.15
    elif fatigue < 0.6:
        rest_ratio = 0.20
    elif fatigue < 0.8:
        rest_ratio = 0.25
    else:
        rest_ratio = 0.30

    # 为每个空闲时段分配科目
    for slot in free_slots:
        period = slot.get("period", "")
        duration = slot.get("duration", 0)

        # 获取该时段的科目偏好
        preferred_subjects = slot_preferences.get(period, ["复习"])

        # 选择科目
        subject = preferred_subjects[0] if preferred_subjects else "复习"

        # 检查最小块时长
        if min_block_check:
            subject = rules_engine.check_min_block_duration(slot, subject)

        # 计算学习时长（扣除休息）
        study_duration = duration * (1 - rest_ratio)

        task = {
            "period": period,
            "time": f"{slot.get('start', '')}-{slot.get('end', '')}",
            "subject": subject,
            "duration": study_duration,
            "rest_duration": duration * rest_ratio
        }

        plan["tasks"].append(task)

    return plan


def generate_debt_handling_plan_v3(user_input: Dict[str, Any],
                                    debt_tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    生成补课计划（v3.0 版本，带 MemOS 集成）

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
        "options": rules_engine.generate_debt_options(debt_tasks, strategy)
    }


# 便捷导出函数
__all__ = [
    "generate_daily_plan_v3",
    "generate_daily_plan",
    "generate_daily_plan_adaptive",
    "generate_sunday_review_plan_with_memory",
    "generate_sunday_review_plan",
]
