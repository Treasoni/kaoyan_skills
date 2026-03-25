"""
kaoyan-electronics 路由器模块

本模块是 kaoyan-electronics 技能的Python实现，包含：
- 主路由逻辑
- 上下文分析
- 子技能调用

版本: v2.0.0 (模块化重构)
"""

from .router import route_electronics_request
from .context import analyze_context, has_image_upload, Context
from .invocation import (
    invoke_skill,
    ask_for_clarification,
    log_route,
    error_response,
)

__all__ = [
    # 主路由
    "route_electronics_request",
    # 上下文分析
    "analyze_context",
    "has_image_upload",
    "Context",
    # 子技能调用
    "invoke_skill",
    "ask_for_clarification",
    "log_route",
    "error_response",
]

__version__ = "2.0.0"
