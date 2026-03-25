"""
SM-2 单词复习间隔算法模块

本模块实现标准的 SM-2 (SuperMemo 2) 间隔重复算法，包括：
- 计算下次复习日期
- 验证单词表复习任务（防止遗漏新学单词）
- 计划生成后一致性检查

来源: code.md 第1481-1755行

SM-2 算法标准间隔：
- 第1次复习：学习后 1天
- 第2次复习：第1次复习后 3天（累计4天）
- 第3次复习：第2次复习后 7天（累计11天）
"""

import os
import re
import glob
from datetime import datetime, timedelta, date
from typing import Dict, List, Any, Optional


# SM-2 算法标准间隔常量
SM2_INTERVALS = {
    1: 1,   # 第1次复习：学习后1天
    2: 3,   # 第2次复习：第1次后3天
    3: 7,   # 第3次复习：第2次后7天
}


def calculate_sm2_next_review(learning_date: date, review_count: int) -> Dict[str, Any]:
    """
    计算下次复习日期（标准 SM-2 算法）

    参数:
        learning_date: 学习日期
        review_count: 已完成复习次数（0=刚学，1=已复习1次，2=已复习2次）

    返回:
        字典，包含:
        - next_review_date: 下次复习日期
        - review_type: 复习类型（第N次复习）
        - cumulative_days: 累计天数
        - is_overdue: 是否逾期
    """
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
        'is_overdue': date.today() > next_review_date
    }


def validate_vocabulary_review_files() -> List[Dict[str, Any]]:
    """
    验证是否有单词表需要复习（v3.3 修正版 - 完整 SM-2 算法）

    功能：
        1. 读取学习进度文件获取每个 Day 的复习历史
        2. 根据 SM-2 算法计算每个 Day 的下次复习日期
        3. 检查是否有到期/逾期的复习任务
        4. 返回需要复习的任务列表（按优先级排序）

    返回:
        需要添加到复习计划的任务列表
    """
    today = date.today()
    missed_reviews = []

    # 1. 读取学习进度文件
    progress_file = os.path.join("考研英语", "📊 学习进度.md")
    try:
        with open(progress_file, 'r', encoding='utf-8') as f:
            progress_content = f.read()
    except Exception as e:
        log_warning(f"无法读取学习进度文件: {e}")
        return []

    # 2. 提取每个 Day 的学习日期和复习记录
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
    vocab_files = glob.glob(os.path.join(vocab_dir, "*.md"))

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

        # 从文件内容提取 Day 编号和单词数量
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

        # 补充或创建 Day 记录
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

    # 4. 计算每个 Day 的下次复习日期
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
                'estimated_duration': max(15, word_count * 0.4)  # 估算复习时长（分钟）
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


def consistency_check_after_plan_generation(plan: Any, vocab_dir: str = "考研英语/英语单词") -> List[Dict[str, Any]]:
    """
    计划生成后的一致性检查（v3.2 新增）

    功能：
        验证生成的计划是否包含所有必要的复习任务

    参数:
        plan: 已生成的学习计划
        vocab_dir: 单词表目录路径

    返回:
        发现的问题列表
    """
    issues = []

    # 1. 获取最新的单词表文件
    vocab_files = glob.glob(os.path.join(vocab_dir, "2026-3-*.md"))
    vocab_files.sort(reverse=True)

    if not vocab_files:
        return issues

    latest_file = vocab_files[0]

    # 2. 提取学习日期和 Day 编号
    date_match = re.search(r'(\d{4}-\d{2}-\d{2})\.md$', latest_file)
    if not date_match:
        return issues

    try:
        file_date = datetime.strptime(date_match.group(1), "%Y-%m-%d").date()
    except ValueError:
        return issues

    # 3. 检查是否需要复习
    days_since_learning = (date.today() - file_date).days

    if days_since_learning >= 1:
        # 提取 Day 编号
        try:
            with open(latest_file, 'r', encoding='utf-8') as f:
                content = f.read()
                day_match = re.search(r'Day\s*(\d+)', content)
                day_num = int(day_match.group(1)) if day_match else None
        except Exception:
            return issues

        if day_num:
            # 4. 检查计划中是否包含该 Day 的复习任务
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


def log_info(message: str) -> None:
    """记录信息日志"""
    pass


def log_warning(message: str) -> None:
    """记录警告日志"""
    pass
