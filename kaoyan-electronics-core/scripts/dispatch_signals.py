"""
调度信号处理模块

本模块处理来自kaoyan-plan的调度信号，包括：
- 调度信号检查
- 信号处理
- 信号标记

来源: code.md 第355-437行
"""

from typing import Dict, Any, List, Optional
import json


CONVERSATION_ID = None  # 在运行时设置


def check_dispatch_signals(user_id: str) -> List[Dict[str, Any]]:
    """检查来自kaoyan-plan的调度信号

    Args:
        user_id: 用户ID

    Returns:
        待处理的调度信号列表
    """
    try:
        signals = search_memory(
            query=f"#dispatch_signal #target_kaoyan-electronics #user_{user_id}",
            conversation_first_message=CONVERSATION_ID,
            memory_limit_number=5
        )

        pending = []
        for signal in signals:
            if not signal.get("processed"):
                pending.append(signal)

        return pending
    except Exception as e:
        log_warning(f"检查调度信号失败: {e}")
        return []


def process_dispatch_signal(signal: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """处理调度信号

    Args:
        signal: 调度信号字典

    Returns:
        处理结果
    """
    action = signal.get("action")
    context = signal.get("context", {})

    if action == "check_math_prerequisites":
        topic = context.get("topic")
        return {
            "mode": "prerequisite_check",
            "topic": topic,
            "required_math": context.get("required_math", []),
            "instructions": f"检查学习「{topic}」所需的数学基础"
        }

    elif action == "circuit_analysis_sop":
        circuit_type = context.get("circuit_type")
        return {
            "mode": "circuit_analysis",
            "circuit_type": circuit_type,
            "instructions": f"使用标准SOP分析{circuit_type}"
        }

    elif action == "weekly_error_analysis":
        return {
            "mode": "weekly_review",
            "aggregate": context.get("aggregate", True)
        }

    return None


def mark_signal_processed(signal_id: str, user_id: str) -> None:
    """标记调度信号为已处理

    Args:
        signal_id: 信号ID
        user_id: 用户ID
    """
    try:
        add_feedback(
            conversation_first_message=CONVERSATION_ID,
            feedback_content=f"调度信号 {signal_id} 已处理"
        )
    except Exception as e:
        log_warning(f"标记信号失败: {e}")


def log_warning(message: str) -> None:
    """记录警告日志"""
    print(f"[WARNING] {message}")
