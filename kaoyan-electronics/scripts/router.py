"""
主路由器模块

本模块处理电子技术学习请求的路由，包括：
- 意图分类路由
- 上下文分析调用

来源: code.md 第7-69行
"""

from typing import Any, Dict

from .context import analyze_context, has_image_upload
from .invocation import invoke_skill, ask_for_clarification


def route_electronics_request(user_input: str) -> Dict[str, Any]:
    """路由电子技术学习请求

    Args:
        user_input: 用户输入内容

    Returns:
        调用对应子技能
    """

    # 1. 电路图分析相关
    if any(keyword in user_input for keyword in [
        "电路图", "分析电路", "帮我看看这个电路",
        "静态分析", "动态分析", "计算工作点", "计算增益"
    ]):
        return invoke_skill("kaoyan-electronics-circuit", user_input)

    # 2. SOP/解题步骤相关
    elif any(keyword in user_input for keyword in [
        "怎么做", "解题步骤", "SOP", "反馈类型判断",
        "计数器设计", "卡诺图化简", "时序逻辑分析"
    ]):
        return invoke_skill("kaoyan-electronics-sop", user_input)

    # 3. 知识点结构相关
    elif any(keyword in user_input for keyword in [
        "知识点结构", "知识图谱", "前置知识",
        "复习负反馈", "学习计数器", "我要学习"
    ]):
        return invoke_skill("kaoyan-electronics-structure", user_input)

    # 4. 核心配置相关
    elif any(keyword in user_input for keyword in [
        "电子技术配置", "专业课状态", "电子技术欠账检查",
        "跨学科关联", "数学前置检查"
    ]):
        return invoke_skill("kaoyan-electronics-core", user_input)

    # 5. 上传电路图 - 优先电路分析
    elif has_image_upload(user_input):
        return invoke_skill("kaoyan-electronics-circuit", user_input)

    # 6. 通用电子技术请求 - 智能推断
    elif "电子技术" in user_input or "822" in user_input or "模电" in user_input or "数电" in user_input:
        context = analyze_context(user_input)
        if context.has_circuit_image:
            return invoke_skill("kaoyan-electronics-circuit", user_input)
        elif context.needs_solution_steps:
            return invoke_skill("kaoyan-electronics-sop", user_input)
        elif context.needs_knowledge_structure:
            return invoke_skill("kaoyan-electronics-structure", user_input)
        else:
            return invoke_skill("kaoyan-electronics-sop", user_input)

    # 7. 默认：询问用户具体需求
    else:
        return ask_for_clarification()
