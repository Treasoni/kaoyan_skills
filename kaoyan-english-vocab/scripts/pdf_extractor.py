"""
PDF词汇提取模块

从墨墨背单词、百词斩等APP导出的PDF中提取单词列表。
"""

import re
from typing import List, Dict


def extract_words_from_pdf(pdf_path: str, app_type: str = "momo") -> List[Dict]:
    """从PDF中提取单词列表

    Args:
        pdf_path: PDF文件路径
        app_type: APP类型（momo/baici/generic）

    Returns:
        list: 单词列表，每个元素为包含word/pronunciation/meaning的字典

    Raises:
        FileNotFoundError: 如果PDF文件不存在
        ValueError: 如果app_type不支持
    """
    # 读取PDF内容
    content = read_pdf(pdf_path)

    # 根据APP类型选择解析器
    if app_type == "momo":
        words = parse_momo_format(content)
    elif app_type == "baici":
        words = parse_baici_format(content)
    elif app_type == "generic":
        words = parse_generic_format(content)
    else:
        raise ValueError(f"不支持的app_type: {app_type}")

    return words


def parse_momo_format(content: str) -> List[Dict]:
    """解析墨墨背单词导出格式

    墨墨格式示例:
    abandon [əˈbændən] vt. 遗弃；放弃

    Args:
        content: PDF文本内容

    Returns:
        list: 单词列表
    """
    words = []
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 墨墨格式: 单词 [音标] 释义
        match = re.match(r'^(\w+)\s*\[([^\]]+)\]\s*(.+)$', line)
        if match:
            words.append({
                "word": match.group(1),
                "pronunciation": match.group(2),
                "meaning": match.group(3).strip()
            })

    return words


def parse_baici_format(content: str) -> List[Dict]:
    """解析百词斩导出格式

    百词斩格式示例:
    abandon vt.遗弃；放弃

    Args:
        content: PDF文本内容

    Returns:
        list: 单词列表
    """
    words = []
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 百词斩格式可能不同（无音标）
        match = re.match(r'^(\w+)\s+(.+)$', line)
        if match:
            words.append({
                "word": match.group(1),
                "pronunciation": "",
                "meaning": match.group(2).strip()
            })

    return words


def parse_generic_format(content: str) -> List[Dict]:
    """解析通用格式

    尝试识别常见的单词表格式。

    Args:
        content: PDF文本内容

    Returns:
        list: 单词列表
    """
    words = []
    lines = content.split('\n')

    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue

        # 尝试匹配多种格式
        # 格式1: word [音标] 释义
        match = re.match(r'^(\w+)\s*\[([^\]]+)\]\s*(.+)$', line)
        if match:
            words.append({
                "word": match.group(1),
                "pronunciation": match.group(2),
                "meaning": match.group(3).strip()
            })
            continue

        # 格式2: word 释义
        match = re.match(r'^(\w+)\s+(.+)$', line)
        if match:
            words.append({
                "word": match.group(1),
                "pronunciation": "",
                "meaning": match.group(2).strip()
            })

    return words


# ========== 辅助函数 ==========

def read_pdf(pdf_path: str) -> str:
    """读取PDF文件内容

    Args:
        pdf_path: PDF文件路径

    Returns:
        str: PDF文本内容

    Raises:
        FileNotFoundError: 如果文件不存在
    """
    try:
        # 尝试导入pdfplumber
        import pdfplumber

        with pdfplumber.open(pdf_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"
            return text

    except ImportError:
        # 如果没有pdfplumber，尝试PyPDF2
        try:
            import PyPDF2

            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text

        except ImportError:
            raise ImportError(
                "需要安装PDF解析库。请运行: pip install pdfplumber 或 pip install PyPDF2"
            )

    except FileNotFoundError:
        raise FileNotFoundError(f"PDF文件不存在: {pdf_path}")
