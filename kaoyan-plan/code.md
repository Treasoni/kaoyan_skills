# kaoyan-plan 核心算法模块

本文档包含 kaoyan-plan 技能的所有核心算法实现。

> 📋 **返回主文档**: [skill.md](skill.md)

---

## 目录

1. [主规划算法 v3.0 (MemOS集成版)](#主规划算法v30-memos集成版)
2. [主规划算法 v2.1 (降级兼容版)](#主规划算法v21-降级兼容版)
3. [主规划算法 (自适应版)](#主规划算法自适应版)
4. [辅助函数](#辅助函数)
   - [疲劳度计算](#疲劳度计算)
   - [时段偏好](#时段偏好)
   - [欠账检测](#欠账检测)
   - [画像刷新检查](#画像刷新检查)
   - [心理干预检查](#心理干预检查)

---

## 主规划算法（v3.0 MemOS集成版）

```python
def generate_daily_plan_v3(user_input, mode="minimal", previous_plan=None):
    """
    根据用户输入模式生成计划（含MemOS记忆集成）

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")
        previous_plan: 昨日计划（用于检测欠账）

    返回:
        每日计划
    """

    # 1. MemOS: 读取用户上下文 (可降级)
    user_context = safe_load_context(user_input)

    # 1.5 v3.1: 检查画像新鲜度 (context_refresh机制)
    profile_refresh = check_context_freshness(user_context, datetime.now())
    if profile_refresh and profile_refresh.get("needs_refresh"):
        # 返回画像刷新询问，等待用户确认后再继续
        return generate_profile_refresh_question(profile_refresh)

    # 1.6 v3.1: 检查心理状态是否需要干预
    mental_intervention = check_mental_health_intervention(user_context)
    if mental_intervention and mental_intervention.get("intervention_needed"):
        # 标记为心理调节模式，后续生成计划时应用
        user_input["mental_mode"] = mental_intervention.get("mode")

    # 2. 检查任务欠账（v3.1增强: 含熔断机制）
    debt_result = check_task_debt_with_memory(previous_plan, user_input, user_context)
    if debt_result:
        # v3.1: 检查是否触发熔断
        if debt_result.get("type") == "debt_emergency":
            return generate_emergency_recovery_plan(debt_result)
        return generate_debt_handling_plan(user_input, debt_result.get("tasks"))

    # 3. 检查周日复盘（增强: 从MemOS读取本周数据）
    if is_sunday(today):
        return generate_sunday_review_plan_with_memory(user_input, user_context)

    # 4. 根据模式确定数据丰富度
    if mode == "minimal":
        user_data = apply_defaults(user_input, user_context)
    elif mode == "standard":
        user_data = enrich_with_exam_info(user_input, user_context)
    else:
        user_data = merge_user_input_with_memory(user_input, user_context)

    # 5. 获取空闲时段
    free_slots = extract_free_slots(user_data.schedule)

    # 6. 应用chronotype适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = get_slot_preferences(chronotype)

    # 7. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = calculate_mixed_fatigue(
            user_input.self_report,
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0

    # 8. v3.2: 验证单词表复习任务（防止遗漏新学单词）
    missed_vocab_tasks = validate_vocabulary_review_files()
    if missed_vocab_tasks:
        logger.warning(f"发现 {len(missed_vocab_tasks)} 个未安排复习的单词表，已自动添加")
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
    consistency_issues = consistency_check_after_plan_generation(plan)
    if consistency_issues:
        logger.warning(f"发现 {len(consistency_issues)} 个一致性问题:")
        for issue in consistency_issues:
            logger.warning(f"  - {issue.get('message')}")

    # 11. MemOS: 保存计划 (可降级)
    safe_save_plan(plan, user_input, mode)

    return plan
```

### v3.0 辅助函数

```python
def safe_load_context(user_input):
    """从MemOS加载用户上下文，失败时返回None触发降级"""
    try:
        results = search_memory(
            conversation_id=user_input.get("conversation_id"),
            user_id=user_input.get("user_id"),
            query=f"用户画像配置 学习进度记录",
            top_k=10
        )
        return parse_memory_results_to_context(results)
    except Exception as e:
        log_warning(f"MemOS unavailable, using defaults: {e}")
        return None


def safe_save_plan(plan, user_input, mode):
    """保存生成的计划（v3.1增强: upsert with tag逻辑）"""
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        user_id = user_input.get("user_id")

        # v3.1: 先尝试查找今日已有计划
        today_plan = search_memory(
            query=f"#daily_plan_current {user_id} {today}",
            top_k=1
        )

        if today_plan:
            # 更新: 标记旧版本为历史，保存新版本为当前
            old_plan = today_plan[0]
            add_message(
                messages=[{
                    "role": "assistant",
                    "content": {
                        "type": "daily_plan",
                        "version": old_plan.get("version", "v1"),
                        "status": "superseded",
                        "data": old_plan.get("data"),
                        "superseded_at": datetime.now().isoformat()
                    },
                    "tags": ["#daily_plan_history", f"#date_{today}"]
                }],
                user_id=user_id
            )

        # 保存新计划为当前版本
        add_message(
            conversation_id=user_input.get("conversation_id"),
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "daily_plan",
                    "mode": mode,
                    "version": f"v{datetime.now().strftime('%H%M')}",
                    "status": "current",
                    "data": plan.to_dict(),
                    "timestamp": datetime.now().isoformat()
                },
                "tags": ["#daily_plan_current", f"#date_{today}"]
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to save plan to memory: {e}")


def check_task_debt_with_memory(previous_plan, user_input, user_context):
    """检查任务欠账（增强版：从MemOS读取昨日计划）"""
    # 如果提供了previous_plan参数，直接使用
    if previous_plan:
        return check_task_debt(previous_plan, user_input.get("completed_tasks"))

    # 否则尝试从MemOS读取昨日计划
    if user_context:
        yesterday_plan = user_context.get("yesterday_plan")
        if yesterday_plan:
            return check_task_debt(yesterday_plan, user_input.get("completed_tasks"))

    return []


def generate_sunday_review_plan_with_memory(user_input, user_context):
    """生成周日复盘计划（增强版：从MemOS读取本周数据）"""
    weekly_stats = None
    if user_context:
        weekly_stats = user_context.get("weekly_progress")

    return {
        "type": "sunday_review",
        "date": today,
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


def parse_user_completion_report(user_input):
    """
    解析用户完成的任务报告（v3.8.0新增）

    功能：
        从用户输入中提取所有完成的任务，包括计划外的任务

    支持的任务格式：
        - "Day 015 第1次复习"
        - "Day 016 新学"
        - "1-导数模块全部6个知识点"
        - "数学错题10道"
        - "单词复习（Day 011+012第2次复习）"

    参数:
        user_input: 用户输入字符串或字典

    返回:
        list: 完成的任务列表，每个任务包含:
            - subject: 科目（英语/数学/专业课/政治）
            - task: 任务描述
            - duration: 实际用时（可选）
            - extra: 是否为计划外任务（布尔值）
    """
    import re

    # 如果是字典，提取文本内容
    if isinstance(user_input, dict):
        text = user_input.get("content", user_input.get("text", ""))
    else:
        text = str(user_input)

    completed_tasks = []
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # 检测英语学习任务
        if any(keyword in line for keyword in ["Day", "单词", "词汇", "复习", "新学"]):
            day_match = re.search(r'Day\s*(\d+)', line)
            if day_match:
                task = {
                    "subject": "英语",
                    "task": line,
                    "duration": None,  # 可以后续解析
                    "extra": False  # 默认为计划内，后续对比时标记
                }
                completed_tasks.append(task)
                continue

        # 检测数学学习任务
        if any(keyword in line for keyword in ["导数", "极限", "积分", "微分", "知识点", "模块", "错题"]):
            task = {
                "subject": "数学",
                "task": line,
                "duration": None,
                "extra": False
            }
            completed_tasks.append(task)
            continue

        # 检测专业课任务
        if any(keyword in line for keyword in ["电路", "模电", "数电", "电子技术"]):
            task = {
                "subject": "专业课",
                "task": line,
                "duration": None,
                "extra": False
            }
            completed_tasks.append(task)
            continue

        # 检测政治任务
        if any(keyword in line for keyword in ["马原", "毛中特", "史纲", "思修"]):
            task = {
                "subject": "政治",
                "task": line,
                "duration": None,
                "extra": False
            }
            completed_tasks.append(task)
            continue

    return completed_tasks


def generate_completion_record_file(user_id, completed_tasks, planned_tasks, date):
    """
    生成每日完成记录文件（v3.8.0新增）

    关键改进：
        1. completed_tasks = 用户报告的所有任务（包括计划外的）
        2. planned_tasks = 计划中的任务（用于对比和标记）
        3. 完成记录包含所有 completed_tasks

    参数:
        user_id: 用户ID
        completed_tasks: 用户完成的任务列表（包含计划外任务）
        planned_tasks: 计划中的任务列表（用于对比）
        date: 日期字符串（YYYY-MM-DD）

    返回:
        str: 生成的完成记录文件路径
    """
    from datetime import datetime
    import os

    # 1. 标记计划外任务
    planned_descriptions = {task.get("task", "") for task in planned_tasks}
    for task in completed_tasks:
        if task.get("task", "") not in planned_descriptions:
            task["extra"] = True  # 标记为计划外任务

    # 2. 按科目分组
    tasks_by_subject = {
        "英语": [],
        "数学": [],
        "专业课": [],
        "政治": []
    }

    for task in completed_tasks:
        subject = task.get("subject", "")
        if subject in tasks_by_subject:
            tasks_by_subject[subject].append(task)

    # 3. 生成完成记录 Markdown
    record_content = f"""# 今日学习完成记录 - {date}

> 📊 **完成日期**：{date}
> 🎉 **基于用户实际报告生成**

---

## 📊 今日学习统计

| 统计项 | 数据 |
|--------|------|
| **完成任务总数** | **{len(completed_tasks)}个** |
| **计划内任务** | **{len([t for t in completed_tasks if not t.get("extra")])}个** |
| **计划外任务** | **{len([t for t in completed_tasks if t.get("extra")])}个** ⭐ |

---

## ✅ 任务完成详情

"""

    # 4. 按科目生成完成记录
    for subject in ["英语", "数学", "专业课", "政治"]:
        tasks = tasks_by_subject.get(subject, [])
        if not tasks:
            continue

        record_content += f"### {subject}学习完成情况\n\n"

        for i, task in enumerate(tasks, 1):
            extra_mark = " ⭐**计划外**" if task.get("extra") else ""
            record_content += f"{i}. {task.get('task', '')}{extra_mark}\n"

        record_content += "\n"

    # 5. 添加完成统计
    record_content += "---\n\n## 📈 完成统计\n\n"
    record_content += f"- ✅ **总完成任务**：{len(completed_tasks)}个\n"
    record_content += f"- 📋 **计划内完成**：{len([t for t in completed_tasks if not t.get('extra')])}个\n"
    record_content += f"- ⭐ **计划外完成**：{len([t for t in completed_tasks if t.get('extra')])}个\n"

## 工作流程

```
[用户输入]
      ↓
[MemOS: 读取用户上下文]
  - 用户画像
  - 昨日计划
  - 本周进度
  - **专业课进度** (新增 v3.9.0)
      ↓
[识别输入模式]
  ├─ 极简模式 → 使用默认值/记忆数据
  ├─ 标准模式 → 询问考试日期/偏好
  └─ 高级模式 → 分析完整数据
      ↓
[检查特殊状态]
  ├─ 任务欠账 → 生成补课方案（>10h触发熔断)
  ├─ 周日复盘 → 生成复盘计划
  └─ 连续疲惫 → 触发心理调节模式
      ↓
[解析课表 + 个性化适配]
  - Chronotype适配
  - 疬劳度调整
  - 最小块时长检查
  - **专业课进度适配** (新增 v3.9.0)
  - 科学时间块切分
      ↓
[生成计划 + MemOS保存]
```

> ⚠️ **重要**：生成计划前，应检查以下专业课进度文件：
> - `考研专业课/📊 学习进度.md`
> - `考研专业课/数字电子技术/1-数字与码制/📊 学习进度.md`
> - 以及其他章节的进度文件
>
> **专业课进度适配规则**：
> 1. 如果专业课进度为0%，优先安排基础章节
> 2. 如果专业课进度<50%，在计划中包含复习环节
> 3. 如果专业课进度≥50%，可以安排新的学习内容

> 4. 裂痕检测：如果超过7天未学习专业课，发出提醒

---

## 概念

    with open(record_file, 'w', encoding='utf-8') as f:
        f.write(record_content)

    log_info(f"✅ 已生成完成记录：{record_file}")
    return record_file


def record_task_completion(user_id, completed_tasks, planned_tasks):
    """记录任务完成情况到MemOS + 更新英语进度 + 生成完成记录（v3.8.0改进）"""
    from datetime import datetime

    try:
        # 1. 原有逻辑：计算统计并保存到MemOS
        stats = calculate_completion_stats(completed_tasks, planned_tasks)
        add_message(
            conversation_id=user_id,
            messages=[{
                "role": "user",
                "content": {
                    "type": "task_completion",
                    "data": stats
                }
            }],
            user_id=user_id
        )

        # 2. v3.7新增：检测并更新英语进度
        english_tasks = extract_english_tasks(completed_tasks)
        if english_tasks:
            update_english_progress_file(english_tasks)

        # 3. v3.8.0新增：生成完成记录文件（包含所有用户报告的任务）
        today = datetime.now().strftime("%Y-%m-%d")
        record_file = generate_completion_record_file(
            user_id=user_id,
            completed_tasks=completed_tasks,
            planned_tasks=planned_tasks,
            date=today
        )

        log_info(f"✅ 完成记录已保存：{record_file}")

    except Exception as e:
        log_warning(f"Failed to record completion: {e}")


def extract_english_tasks(completed_tasks):
    """
    从完成任务中提取英语学习任务（v3.7新增）

    功能：
        1. 识别英语学习任务（通过关键词匹配）
        2. 解析任务描述，提取Day编号、复习次数、词汇数量
        3. 返回结构化的任务列表

    支持的任务格式：
        - "Day 015 第1次复习"
        - "Day 016 新学"
        - "单词复习（Day 011+012第2次复习）" - 多个任务

    返回:
        list: 英语任务列表，每个任务包含 day, review_count, vocab_count
    """
    import re

    english_tasks = []

    for task in completed_tasks:
        task_desc = task.get("description", "")
        if not task_desc:
            task_desc = str(task.get("task", ""))

        # 检查是否为英语学习任务
        english_keywords = ["Day", "单词", "词汇", "复习", "新学"]
        if not any(keyword in task_desc for keyword in english_keywords):
            continue

        # 解析单个任务
        # 格式1: "Day 015 第1次复习"
        single_match = re.search(r'Day\s*(\d+).*?(第\d+次|新学)', task_desc)
        if single_match:
            day_num = single_match.group(1).zfill(3)  # 补零到3位：15 -> 015
            review_type = single_match.group(2)

            # 估算词汇数量（从学习进度文件或默认值）
            vocab_count = estimate_vocab_count(day_num)

            english_tasks.append({
                "day": day_num,
                "review_count": review_type,
                "vocab_count": vocab_count,
                "description": f"Day {day_num} {review_type}"
            })
            continue

        # 格式2: "单词复习（Day 011+012第2次复习）" - 多个任务
        multi_match = re.search(r'Day\s*(\d+).*?\+\s*Day\s*(\d+).*?第(\d+)次', task_desc)
        if multi_match:
            day1 = multi_match.group(1).zfill(3)
            day2 = multi_match.group(2).zfill(3)
            review_num = multi_match.group(3)
            review_type = f"第{review_num}次"

            vocab_count1 = estimate_vocab_count(day1)
            vocab_count2 = estimate_vocab_count(day2)

            english_tasks.append({
                "day": day1,
                "review_count": review_type,
                "vocab_count": vocab_count1,
                "description": f"Day {day1} {review_type}"
            })

            english_tasks.append({
                "day": day2,
                "review_count": review_type,
                "vocab_count": vocab_count2,
                "description": f"Day {day2} {review_type}"
            })
            continue

    return english_tasks


def estimate_vocab_count(day_num):
    """
    估算指定Day的词汇数量（v3.7新增）

    参数:
        day_num: Day编号（字符串，如"015"）

    返回:
        int: 估算的词汇数量
    """
    # 已知Day的词汇量映射
    known_vocab_counts = {
        "001": 70, "002": 45, "003": 45, "004": 52, "005": 52,
        "006": 47, "007": 38, "008": 50, "009": 36, "010": 77,
        "011": 50, "012": 50, "013": 50, "014": 57, "015": 85,
        "016": 70
    }

    # 返回已知词汇量或默认值50
    return known_vocab_counts.get(day_num, 50)


def update_english_progress_file(english_tasks):
    """
    更新英语学习进度文件（v3.11.0 修复版）

    功能：
        1. 读取当前进度文件
        2. 在复习历史记录中添加新记录
        3. 更新待进行复习安排（标记已完成 + 添加新计划）
        4. 更新今日完成情况
        5. 保存更新后的文件

    v3.11.0 修复：
        - 修复正则表达式无法匹配实际文件结构的问题
        - 新增：将已完成的复习任务在"待进行复习安排"中标记为"已完成"
        - 新增：更新待进行复习安排时同时处理新学和复习任务

    参数:
        english_tasks: 英语任务列表
    """
    import re
    from datetime import datetime, timedelta

    progress_file = "考研英语/📊 学习进度.md"

    try:
        # 1. 读取当前进度文件
        with open(progress_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # 2. 准备今日日期
        today = datetime.now().strftime("%m-%d")  # 格式：03-15
        today_full = datetime.now().strftime("%Y-%m-%d")  # 格式：2026-03-15

        # 3. 生成需要添加的内容
        review_records = []  # 复习历史记录
        completion_records = []  # 今日完成情况
        pending_completed_days = []  # 待标记为已完成的 Day 列表

        for task in english_tasks:
            day = task["day"]
            review_count = task["review_count"]
            vocab_count = task["vocab_count"]

            # 生成复习历史记录
            if review_count == "新学":
                review_records.append(f"| **{today}** | **Day {day}** | **新学**  | **~{vocab_count}词** | -       | -      | ✅ **已完成**   | ⭐ **新增** |")
            else:
                review_records.append(f"| **{today}** | **Day {day}** | **{review_count}** | **~{vocab_count}词** | **1天**  | **1天** | ✅ **已完成**   | -         |")

            # 生成今日完成情况记录
            if review_count == "新学":
                completion_records.append(f"> - ✅ Day {day} 新学（~{vocab_count}词）⭐ 新增")
            else:
                completion_records.append(f"> - ✅ Day {day} {review_count}（~{vocab_count}词）")

            # 记录需要标记为已完成的 Day（用于更新待进行复习安排）
            pending_completed_days.append(day)

        # 4. 更新文件内容
        updated_content = content

        # 4.1 【修复】在复习历史记录表格末尾添加新记录
        # 查找表格最后一行（在"### 待进行复习安排"之前）
        # 修复：使用更精确的正则表达式
        lines = updated_content.split('\n')
        history_start = -1
        pending_start = -1

        for i, line in enumerate(lines):
            if '### 复习历史记录（已修正）' in line:
                history_start = i
            elif '### 待进行复习安排' in line and history_start > 0:
                pending_start = i
                break

        if history_start > 0 and pending_start > 0:
            # 找到历史记录表格的最后一行数据（以 | 开头）
            last_table_row = pending_start - 1
            while last_table_row > history_start and not lines[last_table_row].strip().startswith('|'):
                last_table_row -= 1

            # 在最后一行后插入新记录
            for record in review_records:
                lines.insert(last_table_row + 1, record)
                last_table_row += 1

            updated_content = '\n'.join(lines)

        # 4.2 【修复】更新待进行复习安排 - 标记已完成 + 添加新计划
        lines = updated_content.split('\n')
        pending_table_start = -1
        today_section_start = -1

        for i, line in enumerate(lines):
            if '### 待进行复习安排' in line:
                pending_table_start = i
            elif '> [!info] 今日完成情况' in line:
                today_section_start = i
                break

        if pending_table_start > 0 and today_section_start > 0:
            # 遍历待进行复习安排表格，标记已完成的任务
            for i in range(pending_table_start, today_section_start):
                line = lines[i]
                if line.strip().startswith('|') and 'Day' in line:
                    # 检查是否包含已完成的 Day
                    for day in pending_completed_days:
                        # 匹配格式：| **03-19** | **Day 019** | **第1次** |
                        if f"Day {day}" in line or f"Day **{day}" in line:
                            # 检查是否已经标记为已完成
                            if '✅ **已完成**' not in line and '⏳ 待进行' in line:
                                # 将状态更新为已完成
                                line = line.replace('⏳ 待进行', '✅ **已完成**')
                                # 高亮日期和 Day
                                line = re.sub(r'\|\s*(\d{2}-\d{2})\s*\|', r'| **\1** |', line)
                                line = re.sub(r'\|\s*Day\s*(\d+)\s*\|', r'| **Day \1** |', line)
                                lines[i] = line
                            break

            # 添加新学任务的次日复习计划
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%m-%d")
            for task in english_tasks:
                if task["review_count"] == "新学":
                    day = task["day"]
                    vocab_count = task["vocab_count"]
                    new_row = f"| **{tomorrow}** | Day {day} | 第1次 | ~{vocab_count}词 | 1天 | ⭐ **明日** |"

                    # 检查是否已存在
                    exists = any(f"Day {day}" in line for line in lines[pending_table_start:today_section_start])
                    if not exists:
                        # 找到合适的插入位置（按日期排序）
                        insert_idx = today_section_start - 1
                        while insert_idx > pending_table_start:
                            if lines[insert_idx].strip().startswith('|'):
                                # 提取当前行的日期
                                date_match = re.search(r'\|\s*\*{0,2}(\d{2}-\d{2})\*{0,2}\s*\|', lines[insert_idx])
                                if date_match and date_match.group(1) > tomorrow:
                                    break
                            insert_idx -= 1
                        lines.insert(insert_idx + 1, new_row)

            updated_content = '\n'.join(lines)

        # 4.3 【修复】更新今日完成情况
        lines = updated_content.split('\n')
        today_section_idx = -1

        for i, line in enumerate(lines):
            if f'> [!info] 今日完成情况 ({today_full})' in line:
                today_section_idx = i
                break

        if today_section_idx > 0:
            # 找到今日完成情况块的结束位置
            end_idx = today_section_idx + 1
            while end_idx < len(lines) and (lines[end_idx].startswith('>') or lines[end_idx].strip() == ''):
                end_idx += 1

            # 替换整个今日完成情况块
            new_block = [f'> [!info] 今日完成情况 ({today_full})']
            new_block.extend(completion_records)
            new_block.append(f'> - **词汇累计**：需从文件中读取')  # 占位符

            lines = lines[:today_section_idx] + new_block + lines[end_idx:]
            updated_content = '\n'.join(lines)

        # 5. 保存更新后的文件
        with open(progress_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        log_info(f"✅ 已自动更新英语学习进度：{len(english_tasks)}个任务")

    except FileNotFoundError:
        log_warning(f"英语进度文件不存在：{progress_file}")
    except Exception as e:
        log_warning(f"更新英语进度文件失败：{e}")


def log_info(message):
    """记录信息日志（v3.7新增）"""
    # 在实际实现中可以使用logger
    pass


def load_weekly_data_for_review(user_id):
    """加载本周数据用于周日复盘"""
    try:
        results = search_memory(
            query=f"本周学习记录 {user_id}",
            top_k=20
        )
        return aggregate_weekly_stats(results)
    except Exception:
        return None


def parse_memory_results_to_context(memory_results):
    """解析MemOS搜索结果为用户上下文"""
    context = {
        "user_profile": None,
        "yesterday_plan": None,
        "weekly_progress": None,
        "historical_stats": None
    }

    for result in memory_results:
        content_type = result.get("content", {}).get("type")
        if content_type == "user_profile":
            context["user_profile"] = result.get("content", {}).get("data")
        elif content_type == "daily_plan" and is_yesterday(result.get("timestamp")):
            context["yesterday_plan"] = result.get("content", {}).get("data")
        elif content_type == "task_completion" and is_this_week(result.get("timestamp")):
            if not context["weekly_progress"]:
                context["weekly_progress"] = []
            context["weekly_progress"].append(result.get("content", {}).get("data"))

    return context


def calculate_completion_stats(completed_tasks, planned_tasks):
    """计算任务完成统计"""
    total_planned = sum(t.get("planned_duration", 0) for t in planned_tasks)
    total_actual = sum(t.get("actual_duration", 0) for t in completed_tasks)
    completion_rate = (total_actual / total_planned * 100) if total_planned > 0 else 0

    return {
        "total_planned_hours": total_planned,
        "total_actual_hours": total_actual,
        "completion_rate": completion_rate,
        "debt_hours": max(0, total_planned - total_actual)
    }


def aggregate_weekly_stats(weekly_records):
    """汇总本周统计数据"""
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


def log_warning(message):
    """记录警告日志"""
    pass


def is_yesterday(timestamp_str):
    """判断时间戳是否为昨天"""
    try:
        from datetime import datetime, timedelta
        timestamp = datetime.fromisoformat(timestamp_str)
        yesterday = datetime.now() - timedelta(days=1)
        return timestamp.date() == yesterday.date()
    except:
        return False


def is_this_week(timestamp_str):
    """判断时间戳是否为本周"""
    try:
        from datetime import datetime
        timestamp = datetime.fromisoformat(timestamp_str)
        now = datetime.now()
        week_start = now - timedelta(days=now.weekday())
        week_end = week_start + timedelta(days=6)
        return week_start.date() <= timestamp.date() <= week_end.date()
    except:
        return False
```

---

## 主规划算法（v2.1 降级兼容版）

当MemOS不可用时，系统会降级使用v2.1.0算法：

```python
def generate_daily_plan(user_input, mode="minimal", previous_plan=None):
    """
    根据用户输入模式生成计划（含实战补丁，无MemOS降级版）

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")
        previous_plan: 昨日计划（用于检测欠账）

    返回:
        每日计划
    """

    # 1. 检查任务欠账（实战补丁1）
    debt_tasks = check_task_debt(previous_plan, user_input.get("completed_tasks"))

    if debt_tasks:
        # 欠账处理
        return generate_debt_handling_plan(user_input, debt_tasks)

    # 2. 检查是否周日（实战补丁2）
    if is_sunday(today):
        return generate_sunday_review_plan(user_input)

    # 3. 根据模式确定数据丰富度
    if mode == "minimal":
        user_data = apply_defaults(user_input)
    elif mode == "standard":
        user_data = enrich_with_exam_info(user_input)
    else:
        user_data = user_input

    # 4. 获取空闲时段
    free_slots = extract_free_slots(user_data.schedule)

    # 5. 应用chronotype适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = get_slot_preferences(chronotype)

    # 6. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = calculate_mixed_fatigue(
            user_input.self_report,
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0

    # 7. 分配时段到科目（含最小块时长检查）
    plan = allocate_slots_to_subjects(
        free_slots,
        slot_preferences,
        fatigue,
        min_block_check=True  # 实战补丁3
    )

    return plan


def check_task_debt(previous_plan, completed_tasks):
    """
    检查任务欠账（实战补丁1）

    返回:
        欠账任务列表
    """
    if not previous_plan:
        return []

    debt_tasks = []
    for task in previous_plan.tasks:
        if task not in completed_tasks:
            debt_tasks.append(task)

    return debt_tasks


def generate_debt_handling_plan(user_input, debt_tasks):
    """
    生成补课计划（实战补丁1）

    欠账处理策略：
    - 轻微（<1h）：碎片时间补
    - 中等（1-3h）：压缩低优先任务
    - 严重（>3h）：建议补课日
    """
    total_debt_hours = sum(task.duration for task in debt_tasks)

    if total_debt_hours < 1:
        strategy = "fragment"
    elif total_debt_hours < 3:
        strategy = "compress"
    else:
        strategy = "recovery_day"

    # 生成AI询问
    question = format_debt_question(debt_tasks, total_debt_hours, strategy)

    # 返回补课计划选项
    return {
        "type": "debt_handling",
        "debt_tasks": debt_tasks,
        "total_hours": total_debt_hours,
        "strategy": strategy,
        "question": question,
        "options": generate_debt_options(debt_tasks, strategy)
    }


def generate_sunday_review_plan(user_input):
    """
    生成周日复盘计划（实战补丁2）

    强制包含：
    - 本周完成度统计
    - 2小时错题重做
    - 进度对齐检查
    """
    return {
        "type": "sunday_review",
        "date": today,
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


def check_min_block_duration(slot, subject):
    """
    检查时段是否满足科目最小时长要求（实战补丁3）

    如果不满足，自动替换为可碎片化的科目
    """
    min_duration = get_min_block_duration(subject)

    if slot.duration < min_duration:
        # 不满足，自动替换
        return suggest_fragment_subject(slot.duration)

    return subject


def get_min_block_duration(subject):
    """获取科目最小时长要求"""
    requirements = {
        "数学": 1.5,      # 需要90分钟以上进入状态
        "英语阅读": 1.0,  # 需要完整文章语境
        "专业课": 1.0,    # 需要深度思考
        "单词": 0.25,     # 15分钟即可
        "政治选择": 0.33, # 20分钟即可
        "错题复习": 0.5   # 30分钟即可
    }
    return requirements.get(subject, 1.0)


def suggest_fragment_subject(duration):
    """为碎片时段建议合适的科目"""
    if duration <= 0.25:  # 15分钟以内
        return "单词"
    elif duration <= 0.5:  # 30分钟以内
        return "政治选择题"
    else:  # 30-60分钟
        return "错题复习"
```

---

## 主规划算法（自适应版）

```python
def generate_daily_plan(user_input, mode="minimal"):
    """
    根据用户输入模式生成计划

    参数:
        user_input: 用户输入数据
        mode: 输入模式 ("minimal", "standard", "advanced")

    返回:
        每日计划
    """

    # 1. 根据模式确定数据丰富度
    if mode == "minimal":
        # 极简模式：使用默认值
        user_data = apply_defaults(user_input)
    elif mode == "standard":
        # 标准模式：考虑考试日期
        user_data = enrich_with_exam_info(user_input)
    else:
        # 高级模式：使用完整数据
        user_data = user_input

    # 2. 获取空闲时段
    free_slots = extract_free_slots(user_data.schedule)

    # 3. 应用chronotype适配
    chronotype = user_data.get("chronotype", "morning_person")
    slot_preferences = get_slot_preferences(chronotype)

    # 4. 计算疲劳度（混合模型）
    if "self_report" in user_data:
        fatigue = calculate_mixed_fatigue(
            user_data.self_report,
            user_data.get("behavior_data")
        )
    else:
        fatigue = 0.0  # 默认精力良好

    # 5. 分配时段到科目
    plan = allocate_slots_to_subjects(
        free_slots,
        slot_preferences,
        fatigue
    )

    return plan
```

---

## 辅助函数

### 疲劳度计算

```python
def calculate_mixed_fatigue(self_report, behavior_data=None):
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
```

### 时段偏好

```python
def get_slot_preferences(chronotype):
    """
    根据作息类型返回时段偏好

    参数:
        chronotype: "morning_person" | "night_person" | "normal"

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
```

### 欠账检测（v3.1增强版）

```python
def check_task_debt_with_memory(previous_plan, user_input, user_context):
    """
    检查任务欠账（v3.1增强版：含熔断机制）

    参数:
        previous_plan: 昨日计划
        user_input: 用户输入
        user_context: 用户上下文

    返回:
        欠账任务信息 或 熔断信息
    """
    debt_tasks = []

    # 如果提供了previous_plan参数，直接使用
    if previous_plan:
        debt_tasks = check_task_debt(previous_plan, user_input.get("completed_tasks"))
    # 否则尝试从MemOS读取昨日计划
    elif user_context:
        yesterday_plan = user_context.get("yesterday_plan")
        if yesterday_plan:
            debt_tasks = check_task_debt(yesterday_plan, user_input.get("completed_tasks"))

    if not debt_tasks:
        return None

    # v3.1: 熔断检查
    total_debt_hours = calculate_total_debt_hours(user_context, debt_tasks)
    DEBT_LIMIT = 10  # 10小时熔断阈值

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


def calculate_total_debt_hours(user_context, current_debt_tasks):
    """计算总欠账时长（含历史累计）"""
    current_debt = sum(task.get("duration", 0) for task in current_debt_tasks)

    # 从用户上下文中获取历史累计欠账
    historical_debt = 0
    if user_context and user_context.get("weekly_progress"):
        for record in user_context.get("weekly_progress", []):
            historical_debt += record.get("debt_hours", 0)

    return current_debt + historical_debt


def generate_recovery_plan(total_debt_hours):
    """生成紧急恢复计划（熔断触发后使用）"""
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


def generate_emergency_recovery_plan(debt_result):
    """生成紧急恢复计划（熔断模式）"""
    return {
        "type": "emergency_recovery",
        "total_debt_hours": debt_result.get("total_hours"),
        "message": debt_result.get("message"),
        "suggestion": debt_result.get("suggestion"),
        "recovery_plan": debt_result.get("tasks"),
        "notice": "⚠️ 今日暂停所有新内容学习，专注补账。欠账降至安全阈值后自动恢复正常模式。"
    }
```

### 画像刷新检查

```python
def check_context_freshness(user_context, current_date):
    """
    检查用户画像是否需要刷新（v3.1 context_refresh机制）

    参数:
        user_context: 用户上下文（含用户画像）
        current_date: 当前日期

    返回:
        None 或 刷新询问信息字典
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
        from datetime import datetime
        if isinstance(updated_at, str):
            updated_at = datetime.fromisoformat(updated_at)

        days_since_update = (current_date - updated_at.date()).days

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


def generate_profile_refresh_question(refresh_info):
    """生成画像刷新询问"""
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
```

### 心理干预检查

```python
def check_mental_health_intervention(user_context):
    """
    检查是否需要心理干预（v3.1 mental_status追踪）

    参数:
        user_context: 用户上下文

    返回:
        None 或 干预信息字典
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


def record_mental_status(user_id, mental_status, stress_level, trigger=None):
    """记录用户心理状态到MemOS"""
    try:
        from datetime import datetime

        add_message(
            messages=[{
                "role": "user",
                "content": {
                    "type": "mental_status_update",
                    "data": {
                        "date": datetime.now().date().isoformat(),
                        "status": mental_status,
                        "stress_level": stress_level,
                        "trigger": trigger
                    }
                },
                "tags": ["#mental_status", f"#date_{datetime.now().strftime('%Y-%m-%d')}"]
            }],
            user_id=user_id
        )
    except Exception as e:
        log_warning(f"Failed to record mental status: {e}")
```

### 单词表验证（v3.2新增）

> [!important] SM-2算法标准间隔（已修正）
> - 第1次复习：学习后 **1天**
> - 第2次复习：第1次复习后 **3天**（累计4天）
> - 第3次复习：第2次复习后 **7天**（累计11天）

```python
# SM-2算法标准间隔常量
SM2_INTERVALS = {
    1: 1,   # 第1次复习：学习后1天
    2: 3,   # 第2次复习：第1次后3天
    3: 7,   # 第3次复习：第2次后7天
}


def calculate_sm2_next_review(learning_date, review_count):
    """
    计算下次复习日期（标准SM-2算法）

    参数:
        learning_date: 学习日期
        review_count: 已完成复习次数（0=刚学，1=已复习1次，2=已复习2次）

    返回:
        dict: {
            'next_review_date': 下次复习日期,
            'review_type': 复习类型（第N次复习）,
            'cumulative_days': 累计天数,
            'is_overdue': 是否逾期
        }
    """
    from datetime import timedelta

    next_review = review_count + 1  # 下次是第N次复习

    # 计算累计间隔
    cumulative_days = 0
    for i in range(1, next_review + 1):
        if i == 1:
            cumulative_days += SM2_INTERVALS[1]  # 1天
        elif i == 2:
            cumulative_days += SM2_INTERVALS[2]  # +3天 = 4天
        else:
            cumulative_days += SM2_INTERVALS[3]  # +7天 = 11天

    next_review_date = learning_date + timedelta(days=cumulative_days)

    return {
        'next_review_date': next_review_date,
        'review_type': f"第{next_review}次复习",
        'cumulative_days': cumulative_days,
        'is_overdue': datetime.now().date() > next_review_date
    }


def validate_vocabulary_review_files():
    """
    验证是否有单词表需要复习（v3.3修正版 - 完整SM-2算法）

    功能：
        1. 读取学习进度文件获取每个Day的复习历史
        2. 根据SM-2算法计算每个Day的下次复习日期
        3. 检查是否有到期/逾期的复习任务
        4. 返回需要复习的任务列表（按优先级排序）

    返回:
        list: 需要添加到复习计划的任务列表
    """
    from datetime import datetime, timedelta
    import re
    import os

    today = datetime.now().date()
    missed_reviews = []

    # 1. 读取学习进度文件
    progress_file = os.path.join("考研英语", "📊 学习进度.md")
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_content = f.read()
    except Exception as e:
        log_warning(f"无法读取学习进度文件: {e}")
        return []

    # 2. 提取每个Day的学习日期和复习记录
    # 格式：| 日期 | Day | 复习次数 | ...
    day_records = {}  # {day_num: {'learning_date': date, 'review_count': int, 'word_count': int}}

    # 匹配复习历史记录表格中的行
    # 例如：| 03-02 | Day 001 | 第1次 | 70词 | ...
    review_pattern = r'\|\s*(\d{2}-\d{2})\s*\|\s*Day\s*(\d+)\s*\|\s*第(\d+)次\s*\|'
    for match in re.finditer(review_pattern, progress_content):
        date_str = match.group(1)
        day_num = int(match.group(2))
        review_num = int(match.group(3))

        # 解析日期（假设2026年）
        try:
            record_date = datetime.strptime(f"2026-{date_str}", "%Y-%m-%d").date()
        except ValueError:
            continue

        if day_num not in day_records:
            day_records[day_num] = {
                'learning_date': record_date,
                'review_count': 0,
                'word_count': 0
            }

        # 更新复习次数（取最大值）
        day_records[day_num]['review_count'] = max(
            day_records[day_num]['review_count'],
            review_num
        )

    # 3. 从单词表目录补充学习日期和词汇量
    vocab_dir = "考研英语/英语单词"
    import glob as glob_module
    vocab_files = glob_module.glob(os.path.join(vocab_dir, "*.md"))

    for vocab_file in vocab_files:
        # 从文件名提取日期
        date_match = re.search(r'(\d{4}-\d{2}-\d{2})\.md$', vocab_file)
        if not date_match:
            continue

        file_date_str = date_match.group(1)
        try:
            file_date = datetime.strptime(file_date_str, "%Y-%m-%d").date()
        except ValueError:
            continue

        # 从文件内容提取Day编号和单词数量
        try:
            with open(vocab_file, 'r', encoding='utf-8') as f:
                content = f.read()
                day_match = re.search(r'#\s*(?:考研英语单词表\s*-\s*)?Day\s*(\d+)', content)
                day_num = int(day_match.group(1)) if day_match else None

                count_match = re.search(r'单词总[数词量].*?(\d+)', content)
                word_count = int(count_match.group(1)) if count_match else 50
        except Exception:
            continue

        if not day_num:
            continue

        # 补充或创建Day记录
        if day_num not in day_records:
            day_records[day_num] = {
                'learning_date': file_date,
                'review_count': 0,
                'word_count': word_count
            }
        else:
            day_records[day_num]['word_count'] = word_count
            # 如果没有学习日期，从文件名推断
            if not day_records[day_num].get('learning_date'):
                day_records[day_num]['learning_date'] = file_date

    # 4. 计算每个Day的下次复习日期
    for day_num, record in day_records.items():
        learning_date = record.get('learning_date')
        review_count = record.get('review_count', 0)
        word_count = record.get('word_count', 50)

        if not learning_date:
            continue

        # 计算下次复习信息
        review_info = calculate_sm2_next_review(learning_date, review_count)
        next_review_date = review_info['next_review_date']
        review_type = review_info['review_type']
        is_overdue = review_info['is_overdue']

        # 检查是否需要复习（今天或之前）
        days_until_review = (next_review_date - today).days

        if days_until_review <= 0:  # 今天或逾期
            missed_reviews.append({
                'day': day_num,
                'review_type': review_type,
                'next_review_date': next_review_date.isoformat(),
                'word_count': word_count,
                'priority': 'critical' if is_overdue else 'high',
                'subject': '英语',
                'is_overdue': is_overdue,
                'days_overdue': abs(days_until_review),
                'estimated_duration': max(15, word_count * 0.4)  # 估算复习时长
            })

            if is_overdue:
                log_warning(f"发现逾期复习: Day {day_num} {review_type}（已逾期{abs(days_until_review)}天）")
            else:
                log_info(f"发现今日复习: Day {day_num} {review_type}")

    # 5. 按优先级排序（逾期>今日>高词汇量）
    missed_reviews.sort(key=lambda x: (
        -int(x.get('is_overdue', False)),  # 逾期优先
        -x.get('days_overdue', 0),          # 逾期越久越优先
        -x.get('word_count', 0)             # 词汇量大的优先
    ))

    return missed_reviews


def consistency_check_after_plan_generation(plan, vocab_dir="考研英语/英语单词"):
    """
    计划生成后的一致性检查（v3.2新增）

    功能：
        验证生成的计划是否包含所有必要的复习任务

    参数:
        plan: 已生成的学习计划
        vocab_dir: 单词表目录路径

    返回:
        list: 发现的问题列表
    """
    from datetime import datetime
    import re
    import os
    import glob as glob_module

    issues = []

    # 1. 获取最新的单词表文件
    vocab_files = glob_module.glob(os.path.join(vocab_dir, "2026-3-*.md"))
    vocab_files.sort(reverse=True)

    if not vocab_files:
        return issues

    latest_file = vocab_files[0]

    # 2. 提取学习日期和Day编号
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})\.md$', latest_file)
    if not date_match:
        return issues

    try:
        file_date = datetime.strptime(date_match.group(1), "%Y-%m-%d").date()
    except ValueError:
        return issues

    # 3. 检查是否需要复习
    days_since_learning = (datetime.now().date() - file_date).days

    if days_since_learning >= 1:
        # 提取Day编号
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                content = f.read()
                day_match = re.search(r'Day\s*(\d+)', content)
                day_num = int(day_match.group(1)) if day_match else None
        except Exception:
            return issues

        if day_num:
            # 4. 检查计划中是否包含该Day的复习任务
            plan_content = str(plan)
            search_pattern = f"Day\\s*{day_num}\\s*第?\\d*次?复习"

            if not re.search(search_pattern, plan_content):
                issues.append({
                    'type': 'missed_review',
                    'day': day_num,
                    'file': os.path.basename(latest_file),
                    'message': f"Day {day_num} 需要第1次复习，但未在计划中发现"
                })

    return issues
```

---

## 时间块切分算法

```python
def split_large_time_block(duration, subject):
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
```

**示例**：
```
原计划：14:00-17:00 数学（连续3小时）
↓ 自动切分为高效时间块
14:00-14:45 | 数学 | 第1块（45分钟）
14:45-15:00 | ☕ 休息 | 15分钟
15:00-15:45 | 数学 | 第2块（45分钟）
15:45-16:00 | ☕ 休息 | 15分钟
16:00-16:45 | 数学 | 第3块（45分钟）
16:45-17:00 | ☕ 休息 | 15分钟
```

---

### 专业课进度检查函数

```python
def check_electronics_progress(user_context):
    """
    检查专业课学习进度（新增 v3.9.0）

    功能：
        1. 读取专业课进度文件
        2. 返回进度信息，包括：
           - 数字电子技术进度
           - 模拟电子技术进度
           - 电路分析进度
        3. 返回需要学习的知识点建议

    参数:
        user_context: 用户上下文（可选）

    返回:
        dict: {
            "digital_progress": float (0-100),
            "analog_progress": float (0-100),
            "circuit_progress": float (0-100),
            "current_chapter": str,
            "suggested_tasks": list
            "days_since_last_study": int  # 距上次学习的天数
        }
    """
    from datetime import datetime
    import os

    progress_info = {
        "digital_progress": 0.0,
        "analog_progress": 0.0,
        "circuit_progress": 0.0,
        "current_chapter": None,
        "suggested_tasks": [],
        "days_since_last_study": float('inf')
    }

    # 1. 读取数字电子技术进度
    digital_progress_file = "考研专业课/数字电子技术/1-数字与码制/📊 学习进度.md"
    if os.path.exists(digital_progress_file):
        try:
        with open(digital_progress_file, 'r', encoding='utf-8') as f:
            content = f.read()
            # 解析进度信息
            # 简单的实现：查找完成率
            if "完成率" in content:
                progress_info["digital_progress"] = extract_progress(content, "完成率")
                # 查找当前章节
                progress_info["current_chapter"] = "数字电子技术"
    except:
        pass

    # 2. 读取总进度文件
    main_progress_file = "考研专业课/📊 学习进度.md"
    if os.path.exists(main_progress_file):
        try:
        with open(main_progress_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取各模块进度
                # 这里可以解析总体进度
                pass
        except:
            pass

    # 3. 计算距上次学习的天数
    # 查找最近的完成记录文件
    record_files = [
        "考研计划/每日计划/*-完成记录.md",
        "考研专业课/数字电子技术/1-数字与码制/📊 学习进度.md"
    ]
    latest_study_date = None
    for record_file in record_files:
        if os.path.exists(record_file):
            try:
                mtime = os.path.getmtime(record_file)
                if latest_study_date is None or mtime > latest_study_date:
                    latest_study_date = mtime
            except:
                pass

    if latest_study_date:
        progress_info["days_since_last_study"] = (datetime.now() - latest_study_date).days

    # 4. 生成建议
    if progress_info["digital_progress"] < 50:
        progress_info["suggested_tasks"].append({
            "type": "continue_first_chapter",
            "reason": "第一章进度不足50%，建议继续学习"
        })

    if progress_info.get("days_since_last_study", 7:
        progress_info["suggested_tasks"].append({
            "type": "review_needed",
            "reason": f"超过7天未学习专业课，建议今天安排复习"
        })

    return progress_info


def extract_progress(content, keyword):
    """从文件内容中提取进度百分比"""
    import re
    match = re.search(rf'{keyword}.*?(\d+(?:\.\d+)?%')
    if match:
        return float(match.group(1))
    return 0.0

---

> 📋 **返回主文档**: [skill.md](skill.md)
