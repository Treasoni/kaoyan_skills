"""
统一错误模型模块

本模块处理822电子技术基础的统一错误记录，包括：
- 错误记录保存（含学科标签）
- 标签管理

来源: code.md 第441-479行
"""

from typing import Dict, Any, List
from datetime import datetime
import json


CONVERSATION_ID = None  # 在运行时设置


def save_mistake_with_subject_tag(mistake_data: Dict[str, Any], user_id: str) -> None:
    """保存错误记录（含学科标签）

    Args:
        mistake_data: 错误数据字典
        user_id: 用户ID
    """
    mistake_data["subject"] = "electronics"

    # 添加学科标签
    tags = mistake_data.get("tags", [])
    tags.append("#mistake_record")
    tags.append("#subject_electronics")

    # 添加知识点标签
    kp = mistake_data.get("knowledge_point", "")
    if kp:
        tags.append(f"#kp_{kp}")

    # 添加错误类型标签
    mistake_type = mistake_data.get("type", "unknown")
    tags.append(f"#mistake_type_{mistake_type}")

    mistake_data["tags"] = tags

    try:
        add_message(
            conversation_first_message=CONVERSATION_ID,
            messages=[{
                "role": "assistant",
                "content": json.dumps(mistake_data),
                "chat_time": get_current_time()
            }]
        )
    except Exception as e:
        log_warning(f"保存错误记录失败: {e}")


def get_current_time() -> str:
    """获取当前时间字符串"""
    return datetime.now().isoformat()


def log_warning(message: str) -> None:
    """记录警告日志"""
    print(f"[WARNING] {message}")
