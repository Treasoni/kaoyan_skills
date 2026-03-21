# kaoyan-electronics 路由器代码实现

> 本文件包含路由器的详细代码实现

---

## 1. 路由逻辑

### 1.1 意图分类路由

```python
def route_electronics_request(user_input):
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
```

### 1.2 上下文分析

```python
def analyze_context(user_input):
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
```

### 1.3 图片上传检测

```python
def has_image_upload(user_input):
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
```

---

## 2. 子技能调用

### 2.1 调用子技能

```python
def invoke_skill(skill_name, user_input):
    """调用指定的子技能

    Args:
        skill_name: 子技能名称
        user_input: 用户输入内容

    Returns:
        子技能处理结果
    """
    # 记录路由日志
    log_route(skill_name, user_input)

    # 调用子技能
    skill_map = {
        "kaoyan-electronics-core": kaoyan_electronics_core,
        "kaoyan-electronics-sop": kaoyan_electronics_sop,
        "kaoyan-electronics-circuit": kaoyan_electronics_circuit,
        "kaoyan-electronics-structure": kaoyan_electronics_structure,
    }

    handler = skill_map.get(skill_name)
    if handler:
        return handler(user_input)
    else:
        return error_response(f"未知的子技能: {skill_name}")
```

### 2.2 请求澄清

```python
def ask_for_clarification():
    """请求用户澄清需求

    Returns:
        澄清请求消息
    """
    return {
        "message": "请告诉我您具体需要什么帮助？",
        "options": [
            "分析电路图",
            "查询解题步骤",
            "复习知识点",
            "检查学习状态"
        ],
        "hints": [
            "您可以上传电路图让我分析",
            "您可以询问某个题型的解题方法",
            "您可以说\"帮我复习XX\"来获取知识点卡片"
        ]
    }
```

---

## 3. 辅助函数

### 3.1 路由日志

```python
def log_route(skill_name, user_input):
    """记录路由日志

    Args:
        skill_name: 目标子技能
        user_input: 用户输入
    """
    import logging
    logger = logging.getLogger("kaoyan-electronics-router")
    logger.info(f"Routing to {skill_name}: {user_input[:50]}...")
```

### 3.2 错误响应

```python
def error_response(message):
    """生成错误响应

    Args:
        message: 错误消息

    Returns:
        错误响应对象
    """
    return {
        "error": True,
        "message": message,
        "fallback": ask_for_clarification()
    }
```

---

## 4. 子技能接口定义

### 4.1 kaoyan-electronics-core

```python
def kaoyan_electronics_core(user_input):
    """核心协调层

    功能：
    - MemOS集成管理
    - 调度信号处理
    - 跨学科知识关联
    - 数学前置检查
    - 考点权重计算
    """
    pass
```

### 4.2 kaoyan-electronics-sop

```python
def kaoyan_electronics_sop(user_input):
    """SOP模板库

    功能：
    - 17个标准化解题流程
    - 康华光符号体系
    - LaTeX标准
    - Mermaid波形图
    """
    pass
```

### 4.3 kaoyan-electronics-circuit

```python
def kaoyan_electronics_circuit(user_input):
    """电路图解析

    功能：
    - 电路图智能识别
    - 元件参数提取
    - 静态分析+动态分析
    - 康华光符号体系强制
    """
    pass
```

### 4.4 kaoyan-electronics-structure

```python
def kaoyan_electronics_structure(user_input):
    """知识点结构

    功能：
    - 知识点图谱
    - 前置知识关联
    - 跨章节提示
    - 知识点卡片模板
    """
    pass
```

---

## 5. 数据类定义

### 5.1 Context 类

```python
class Context:
    """用户输入上下文"""

    def __init__(self):
        self.has_circuit_image = False
        self.needs_solution_steps = False
        self.needs_knowledge_structure = False
        self.needs_core_config = False
```

---

*创建日期: 2026-03-12*
*版本: 1.0.0*
