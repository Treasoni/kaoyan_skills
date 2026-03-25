"""
已有笔记保护机制模块

本模块处理考研数学笔记的保护机制，包括：
- 检查已有笔记
- 刌断文件是否有实际内容

来源: code.md 第7-60行
"""

import os
from typing import Dict, Any, List


def check_existing_notes(target_path: str, knowledge_points: List[str]) -> Dict[str, List[str]]:
    """检查已有笔记，返回待创建列表

    确保不会覆盖已有内容。

    Args:
        target_path: 目标路径
        knowledge_points: 知识点列表

    Returns:
        dict: {
            "existing": [...],    # 已有笔记，不会被修改
            "to_create": [...]    # 将新建的笔记
        }
    """
    existing = []
    to_create = []

    for kp in knowledge_points:
        file_path = f"{target_path}/{kp}.md"
        if os.path.exists(file_path) and has_content(file_path):
            existing.append(kp)
        else:
            to_create.append(kp)

    return {
        "existing": existing,      # 已有笔记，不会被修改
        "to_create": to_create     # 将新建的笔记
    }


def has_content(file_path: str) -> bool:
    """检查文件是否有实际内容（非空）

    Args:
        file_path: 文件路径

    Returns:
        bool: 是否有实际内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # 排除只有 frontmatter 或空行的情况
            if not content:
                return False
            # 检查是否有实际内容（除了 frontmatter）
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 2:
                    body = parts[2].strip()
                    return bool(body)
            return True
    except Exception:
        return False
