"""
Day 编号计算模块（共享功能）

基于日期计算 Day 编号，所有英语子技能共享此函数。
提供统一的 Day 编号计算、验证和格式化功能。

版本: 2.0.0
创建日期: 2026-03-24
最后更新: 2026-03-24
"""

import os
import re
from datetime import datetime
from typing import Optional, Dict


# 常量定义
START_DATE = "2026-02-28"
START_DAY = 1
DEFAULT_DIRECTORY = "考研英语/📰 真题语境文章"


def calculate_day_number(target_date: Optional[str] = None) -> int:
    """基于日期计算 Day 编号

    起始日期：2026-02-28 = Day 001
    计算公式：Day编号 = 1 + (目标日期 - 起始日期)的天数

    Args:
        target_date: 目标日期（YYYY-MM-DD格式字符串）
                     默认为None，使用当前日期

    Returns:
        int: Day编号（例如：17表示Day 017）

    Examples:
        >>> calculate_day_number("2026-02-28")
        1
        >>> calculate_day_number("2026-03-01")
        2
        >>> calculate_day_number("2026-03-16")
        17
        >>> calculate_day_number("2026-03-17")
        18
    """
    # 处理输入参数
    if target_date is None:
        target_date = datetime.now()
    elif isinstance(target_date, str):
        target_date = datetime.strptime(target_date, "%Y-%m-%d")

    # 解析起始日期
    start_date = datetime.strptime(START_DATE, "%Y-%m-%d")

    # 计算天数差
    days_diff = (target_date - start_date).days

    # 计算Day编号
    day_number = START_DAY + days_diff

    # 确保Day编号不小于1
    return max(day_number, START_DAY)


def get_max_day_number_from_files(
    directory: str = DEFAULT_DIRECTORY
) -> int:
    """从现有文件中提取最大Day编号

    扫描指定目录中的所有.md文件，从文件名格式
    'Day-XXX-YYYY-MM-DD.md' 中提取Day编号。

    Args:
        directory: 要扫描的目录路径

    Returns:
        int: 找到的最大Day编号，如果没有文件则返回0

    Examples:
        >>> max_day = get_max_day_number_from_files()
        >>> max_day >= 0
        True
    """
    max_day = 0

    try:
        for filename in os.listdir(directory):
            if filename.endswith(".md"):
                # 匹配文件名格式：Day-XXX-YYYY-MM-DD.md
                match = re.match(r"Day-(\d+)-\d{4}-\d{2}-\d{2}\.md", filename)
                if match:
                    day_num = int(match.group(1))
                    max_day = max(max_day, day_num)
    except FileNotFoundError:
        # 目录不存在，返回0
        pass
    except Exception as e:
        # 其他错误，记录警告并返回0
        print(f"Warning: Failed to scan directory {directory}: {e}")

    return max_day


def get_validated_day_number(
    target_date: Optional[str] = None,
    directory: str = DEFAULT_DIRECTORY
) -> int:
    """获取验证后的Day编号（双重验证机制）

    同时使用两种方法计算Day编号：
    1. 基于现有文件的最大Day编号 + 1
    2. 基于日期计算的Day编号

    取两者中的较大值，确保：
    - 不覆盖现有文件（使用较大的编号）
    - Day编号与日期基本一致（差异过大时警告）

    Args:
        target_date: 目标日期（YYYY-MM-DD格式），默认为今天
        directory: 用于文件检查的目录

    Returns:
        int: 验证后的Day编号

    Examples:
        >>> day = get_validated_day_number("2026-03-16")
        >>> day >= 1
        True
    """
    from_files = get_max_day_number_from_files(directory) + 1
    from_date = calculate_day_number(target_date)

    # 检查差异
    diff = abs(from_files - from_date)
    if diff > 2:
        print(
            f"Warning: Day编号差异较大：文件检查显示Day {from_files}，"
            f"但日期计算显示Day {from_date}（差异{diff}天）"
        )
        print("Info: 将使用较大的Day编号以避免覆盖现有文件")

    # 返回较大的值（防止覆盖）
    return max(from_files, from_date)


def format_day_number(day_number: int, padding: int = 3) -> str:
    """格式化Day编号为字符串

    Args:
        day_number: Day编号（整数）
        padding: 填充宽度，默认为3（例如：17 → "017"）

    Returns:
        str: 格式化后的Day编号字符串

    Examples:
        >>> format_day_number(1)
        '001'
        >>> format_day_number(17)
        '017'
        >>> format_day_number(100)
        '100'
    """
    return f"{day_number:0{padding}d}"


def generate_day_filenames(
    target_date: Optional[str] = None,
    day_number: Optional[int] = None
) -> Dict[str, str]:
    """生成四类学习笔记的文件名

    Args:
        target_date: 目标日期（YYYY-MM-DD格式）
        day_number: Day编号（整数），如果为None则自动计算

    Returns:
        dict: 包含四类文件名的字典

    Examples:
        >>> filenames = generate_day_filenames("2026-03-16", 17)
        >>> filenames['context_article']
        'Context-Day-017-2026-03-16.md'
        >>> filenames['quiz']
        'Quiz-Day-017-2026-03-16.md'
    """
    if day_number is None:
        day_number = get_validated_day_number(target_date)

    if target_date is None:
        target_date = datetime.now().strftime("%Y-%m-%d")

    day_str = format_day_number(day_number)

    return {
        "context_article": f"Context-Day-{day_str}-{target_date}.md",
        "quiz": f"Quiz-Day-{day_str}-{target_date}.md",
        "statistics": f"Statistics-Day-{day_str}-{target_date}.md",
        "writing": f"Writing-Day-{day_str}-{target_date}.md"
    }


def parse_day_number_from_filename(filename: str) -> Optional[int]:
    """从文件名中解析Day编号

    Args:
        filename: 文件名（如 "Context-Day-017-2026-03-16.md"）

    Returns:
        int: Day编号，如果无法解析则返回None

    Examples:
        >>> parse_day_number_from_filename("Context-Day-017-2026-03-16.md")
        17
        >>> parse_day_number_from_filename("other-file.md")
        None
    """
    match = re.search(r"Day-(\d+)-", filename)
    if match:
        return int(match.group(1))
    return None


def get_day_range(
    start_date: str,
    end_date: str
) -> list:
    """获取日期范围内的Day编号列表

    Args:
        start_date: 开始日期（YYYY-MM-DD）
        end_date: 结束日期（YYYY-MM-DD）

    Returns:
        list: Day编号列表

    Examples:
        >>> days = get_day_range("2026-03-01", "2026-03-03")
        >>> days
        [2, 3, 4]
    """
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    days = []
    current = start
    while current <= end:
        days.append(calculate_day_number(current.strftime("%Y-%m-%d")))
        current = datetime.fromordinal(current.toordinal() + 1)

    return days


# 导出的公共函数和常量
__all__ = [
    "calculate_day_number",
    "get_max_day_number_from_files",
    "get_validated_day_number",
    "format_day_number",
    "generate_day_filenames",
    "parse_day_number_from_filename",
    "get_day_range",
    "START_DATE",
    "START_DAY",
    "DEFAULT_DIRECTORY",
]
