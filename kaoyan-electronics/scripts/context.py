"""
上下文分析模块

本模块处理电子技术学习请求的上下文分析，包括：
- 用户输入上下文解析
- 图片上传检测

来源: code.md 第72-115行, 第283-295行
"""

from typing import Any


class Context:
    """用户输入上下文"""

    def __init__(self):
        self.has_circuit_image = False
        self.needs_solution_steps = False
        self.needs_knowledge_structure = False
        self.needs_core_config = False


def analyze_context(user_input: str) -> Context:
    """分析用户输入上下文

    Args:
        user_input: 用户输入内容

    Returns:
        上下文对象，包含各种标志
    """
    context = Context()

    # 检查是否有电路图
    context.has_circuit_image = has_image_upload(user_input)

    # 检查是否需要解题步骤
    solution_keywords = ["怎么做", "解题", "步骤", "SOP", "方法"]
    context.needs_solution_steps = any(kw in user_input for kw in solution_keywords)

    # 检查是否需要知识结构
    structure_keywords = ["复习", "学习", "知识点", "结构", "图谱"]
    context.needs_knowledge_structure = any(kw in user_input for kw in structure_keywords)

    return context


def has_image_upload(user_input: Any) -> bool:
    """检测用户是否上传了图片

    Args:
        user_input: 用户输入内容

    Returns:
        bool: 是否包含图片
    """
    # 检查消息中是否有图片附件
    # 实际实现依赖于平台API
    return hasattr(user_input, 'attachments') and \
           any(att.type.startswith('image/') for att in user_input.attachments)
