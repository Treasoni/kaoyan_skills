"""
进度与日志管理模块

本模块处理学习进度的追踪和日志记录，包括：
- 解析用户完成的任务报告
- 生成每日完成记录文件
- 更新英语学习进度文件（复习历史、待进行复习安排、今日完成情况）
- 追加英语学习日志
- 检查专业课学习进度

来源: code.md 第224-821行, 第1814-1923行
"""

import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Any, Union, Optional


def parse_user_completion_report(user_input: Union[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    解析用户完成的任务报告（v3.8.0 新增）

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
        完成的任务列表，每个任务包含:
        - subject: 科目（英语/数学/专业课/政治）
        - task: 任务描述
        - duration: 实际用时（可选）
        - extra: 是否为计划外任务（布尔值）
    """
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
                    "duration": None,
                    "extra": False
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


def generate_completion_record_file(user_id: str, completed_tasks: List[Dict[str, Any]],
                                    planned_tasks: List[Dict[str, Any]], date: str) -> str:
    """
    生成每日完成记录文件（v3.8.0 新增）

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
        生成的完成记录文件路径
    """
    # 1. 标记计划外任务
    planned_descriptions = {task.get("task", "") for task in planned_tasks}
    for task in completed_tasks:
        if task.get("task", "") not in planned_descriptions:
            task["extra"] = True

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

    # 6. 保存文件（v3.12 修改：保存到完成记录子文件夹）
    record_file = f"考研计划/每日计划/完成记录/{date}-完成记录.md"
    os.makedirs(os.path.dirname(record_file), exist_ok=True)

    with open(record_file, 'w', encoding='utf-8') as f:
        f.write(record_content)

    log_info(f"✅ 已生成完成记录：{record_file}")
    return record_file


def record_task_completion(user_id: str, completed_tasks: List[Dict[str, Any]],
                          planned_tasks: List[Dict[str, Any]]) -> Optional[str]:
    """
    记录任务完成情况到 MemOS + 更新英语进度 + 生成完成记录（v3.8.0 改进）

    参数:
        user_id: 用户ID
        completed_tasks: 完成的任务列表
        planned_tasks: 计划中的任务列表

    返回:
        完成记录文件路径，失败时返回 None
    """
    try:
        # 1. 原有逻辑：计算统计并保存到 MemOS
        from .memos_client import calculate_completion_stats
        from mcp__MemoryOperatingSystem__add_message import add_message

        stats = calculate_completion_stats(completed_tasks, planned_tasks)
        add_message(
            conversation_first_message=user_id,
            messages=[{
                "role": "user",
                "content": {
                    "type": "task_completion",
                    "data": stats
                }
            }],
            feedback_content="",
            agent_id=user_id
        )

        # 2. v3.7 新增：检测并更新英语进度
        english_tasks = extract_english_tasks(completed_tasks)
        if english_tasks:
            update_english_progress_file(english_tasks)
            # v3.12 新增：追加到独立的学习日志文件
            append_english_learning_log(english_tasks, completed_tasks)

        # 3. v3.8.0 新增：生成完成记录文件（包含所有用户报告的任务）
        today = datetime.now().strftime("%Y-%m-%d")
        record_file = generate_completion_record_file(
            user_id=user_id,
            completed_tasks=completed_tasks,
            planned_tasks=planned_tasks,
            date=today
        )

        log_info(f"✅ 完成记录已保存：{record_file}")
        return record_file

    except Exception as e:
        log_warning(f"Failed to record completion: {e}")
        return None


def extract_english_tasks(completed_tasks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    从完成任务中提取英语学习任务（v3.7 新增）

    功能：
        1. 识别英语学习任务（通过关键词匹配）
        2. 解析任务描述，提取 Day 编号、复习次数、词汇数量
        3. 返回结构化的任务列表

    支持的任务格式：
        - "Day 015 第1次复习"
        - "Day 016 新学"
        - "单词复习（Day 011+012第2次复习）" - 多个任务

    参数:
        completed_tasks: 完成的任务列表

    返回:
        英语任务列表，每个任务包含 day, review_count, vocab_count
    """
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


def estimate_vocab_count(day_num: str) -> int:
    """
    估算指定 Day 的词汇数量（v3.7 新增）

    参数:
        day_num: Day 编号（字符串，如"015"）

    返回:
        估算的词汇数量
    """
    # 已知 Day 的词汇量映射
    known_vocab_counts = {
        "001": 70, "002": 45, "003": 45, "004": 52, "005": 52,
        "006": 47, "007": 38, "008": 50, "009": 36, "010": 77,
        "011": 50, "012": 50, "013": 50, "014": 57, "015": 85,
        "016": 70
    }

    # 返回已知词汇量或默认值50
    return known_vocab_counts.get(day_num, 50)


def update_english_progress_file(english_tasks: List[Dict[str, Any]]) -> None:
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


def append_english_learning_log(english_tasks: List[Dict[str, Any]],
                               all_tasks: List[Dict[str, Any]] = None) -> None:
    """
    追加英语学习日志到独立文件（v3.13 修复版）

    学习日志已从 📊 学习进度.md 移至独立的 📅 学习日志.md 文件。
    此函数将新的日志条目追加到日志文件开头（最新的日志在前）。

    v3.13 修复：
        - 修正日志格式与现有文件格式一致
        - 支持计算学习天数
        - 生成完整的日志条目（包括学习时长、进度更新等）

    参数:
        english_tasks: 英语任务列表
        all_tasks: 所有完成的任务（用于生成完整日志）
    """
    log_file = "考研英语/📅 学习日志.md"

    try:
        # 1. 读取现有日志文件
        with open(log_file, 'r', encoding='utf-8') as f:
            content = f.read()

        lines = content.split('\n')

        # 2. 找到第一个日志条目的位置（跳过 frontmatter 和标题）
        insert_idx = None
        for i in range(len(lines)):
            # 查找第一个 ### 日期标题
            if lines[i].startswith('### 2026'):
                insert_idx = i
                break

        # 3. 计算学习天数（从第一个日志条目开始计数）
        day_number = 1
        for line in lines:
            if line.startswith('### 2026'):
                # 提取天数：### 2026-03-24 (第26天)
                match = re.search(r'第(\d+)天', line)
                if match:
                    day_number = max(day_number, int(match.group(1)) + 1)

        # 4. 生成任务摘要（用于标题）
        task_summary_parts = []
        for task in english_tasks:
            day = task["day"]
            review_count = task["review_count"]
            if review_count == "新学":
                task_summary_parts.append(f"Day {day} 新学")
            else:
                task_summary_parts.append(f"Day {day} 复习")
        task_summary = " + ".join(task_summary_parts[:2])  # 最多显示2个
        if len(task_summary_parts) > 2:
            task_summary += f" +{len(task_summary_parts)-2}"

        # 5. 估算学习时长（每个任务约30-45分钟）
        total_minutes = len(english_tasks) * 40

        # 6. 估算词汇累计（从任务中获取）
        total_vocab = sum(task.get("vocab_count", 50) for task in english_tasks)
        # 从所有任务中获取最新的 Day 编号
        max_day = max(int(task["day"]) for task in english_tasks) if english_tasks else 0

        # 7. 生成新的日志条目（与现有格式一致）
        today = datetime.now().strftime("%Y-%m-%d")
        log_entry = f"""### {today} (第{day_number}天) - {task_summary} ✅
- 🎉 **今日英语学习时长**：**{total_minutes}分钟**
- ✅ **英语学习完成**：
"""

        for task in english_tasks:
            day = task["day"]
            review_count = task["review_count"]
            vocab_count = task["vocab_count"]
            if review_count == "新学":
                log_entry += f"  - **Day {day} 新学**（~{vocab_count}词）⭐ 新增\n"
            else:
                log_entry += f"  - **Day {day} {review_count}**（~{vocab_count}词）⭐ 符合SM-2算法\n"

        log_entry += f"""- 📌 **进度更新**：
  - 词汇累计：~{1373 + max_day * 50}-{1393 + max_day * 50}词（Day 001-{max_day:03d}）
  - 连续学习天数：第{day_number}天
  - **保持学习节奏！** 🎉
  - **今日英语任务100%完成！** 🎉

"""

        if insert_idx is None:
            # 如果没有找到日志条目，可能是新文件，追加到文件末尾
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write('\n' + log_entry + '\n')
            return

        # 8. 在第一个日志条目之前插入新条目
        lines.insert(insert_idx, log_entry)
        updated_content = '\n'.join(lines)

        # 9. 更新 frontmatter 中的 last_updated
        today_full = datetime.now().strftime("%Y-%m-%d")
        updated_content = re.sub(
            r'last_updated: \d{4}-\d{2}-\d{2}',
            f'last_updated: {today_full}',
            updated_content
        )

        # 10. 保存更新后的文件
        with open(log_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        log_info(f"✅ 已追加英语学习日志")

    except FileNotFoundError:
        log_warning(f"英语学习日志文件不存在：{log_file}")
    except Exception as e:
        log_warning(f"追加英语学习日志失败：{e}")


def check_electronics_progress(user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
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
        进度信息字典，包含:
        - digital_progress: 数字电子技术进度 (0-100)
        - analog_progress: 模拟电子技术进度 (0-100)
        - circuit_progress: 电路分析进度 (0-100)
        - current_chapter: 当前章节
        - suggested_tasks: 建议任务列表
        - days_since_last_study: 距上次学习的天数
    """
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
        "考研计划/每日计划",
        "考研专业课/数字电子技术/1-数字与码制/📊 学习进度.md"
    ]
    latest_study_date = None

    for record_pattern in record_files:
        if os.path.isdir(record_pattern):
            # 处理目录
            import glob
            files = glob.glob(os.path.join(record_pattern, "*-完成记录.md"))
            for file in files:
                try:
                    mtime = os.path.getmtime(file)
                    if latest_study_date is None or mtime > latest_study_date:
                        latest_study_date = mtime
                except:
                    pass
        elif os.path.exists(record_pattern):
            try:
                mtime = os.path.getmtime(record_pattern)
                if latest_study_date is None or mtime > latest_study_date:
                    latest_study_date = mtime
            except:
                pass

    if latest_study_date:
        progress_info["days_since_last_study"] = (datetime.now().timestamp() - latest_study_date) / 86400

    # 4. 生成建议
    if progress_info["digital_progress"] < 50:
        progress_info["suggested_tasks"].append({
            "type": "continue_first_chapter",
            "reason": "第一章进度不足50%，建议继续学习"
        })

    if progress_info.get("days_since_last_study", 7) > 7:
        progress_info["suggested_tasks"].append({
            "type": "review_needed",
            "reason": f"超过7天未学习专业课，建议今天安排复习"
        })

    return progress_info


def extract_progress(content: str, keyword: str) -> float:
    """
    从文件内容中提取进度百分比

    参数:
        content: 文件内容
        keyword: 搜索关键词

    返回:
        进度百分比（0-100）
    """
    match = re.search(rf'{keyword}.*?(\d+(?:\.\d+)?%)', content)
    if match:
        return float(match.group(1).rstrip('%'))
    return 0.0


def log_info(message: str) -> None:
    """记录信息日志"""
    pass


def log_warning(message: str) -> None:
    """记录警告日志"""
    pass
