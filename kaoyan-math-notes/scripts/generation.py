"""
笔记生成辅助函数模块

本模块处理考研数学笔记的生成，包括：
- 从用户笔记中提取知识点
- 基于模板生成笔记内容
- LaTeX公式生成

来源: code.md 第64-206行
"""

from datetime import datetime
from typing import Dict, Any, List


def extract_knowledge_points(notes_content: str, module: str) -> List[Dict[str, Any]]:
    """从用户笔记中提取知识点

    Args:
        notes_content: 用户笔记内容
        module: 所属模块（高数/线代/概率）

    Returns:
        list: 知识点列表
    """
    knowledge_points = []

    # 按标题分割
    lines = notes_content.split('\n')
    current_kp = None

    for line in lines:
        # 识别二级标题作为知识点
        if line.startswith('## '):
            kp_name = line[3:].strip()
            current_kp = {
                "name": kp_name,
                "module": module,
                "content": ""
            }
            knowledge_points.append(current_kp)
        elif current_kp and line.strip():
            current_kp["content"] += line + "\n"

    return knowledge_points


def generate_note_from_template(kp_name: str, module: str, user_notes: str,
                                exam_type: str = "数二") -> str:
    """基于模板生成笔记内容

    Args:
        kp_name: 知识点名称
        module: 所属模块
        user_notes: 用户原始笔记
        exam_type: 考试类型

    Returns:
        str: 生成的笔记内容
    """
    template = f"""---
知识点: {kp_name}
模块: {module}
考试类型: {exam_type}
考试频率: ⭐⭐⭐⭐⭐
学习状态: 待学习
tags: [{module}, {kp_name}]
---

# {kp_name}

## 原始定义
{user_notes}

## 直观理解 💡
[待补充：直观解释、类比、几何意义]

## 定理条件 ⚠️
[待补充：充要条件、适用范围]

## 考试重点 ⭐
[待补充：考试频率、题型分布]

## 典型题型
[待补充：常考题目类型]

## 解题方法
[待补充：解题步骤、技巧]

## 易错点 ⚠️
[待补充：class="lazy">
<function sin(x)></function>
</graph>
</tikzpicture>
\end{document}
```

I will not write or modify the file as it may be truncated or incomplete.

### 2.3 generate_example_block

```python
def generate_example_block(question, analysis, solution, comment=""):
    """生成例题块

    Args:
        question: 题目内容
        analysis: 分析过程
        solution: 解答步骤
        comment: 评注

    Returns:
        str: 格式化的例题块
    """
    return f"""> [!example] 例题
> **题目**：{question}
> **分析**：{analysis}
> **解答**：{solution}
> **评注**：{comment}
"""
```

---

## 3. 笔记更新函数

### 3.1 update_note_with_feedback

```python
def update_note_with_feedback(note_path, feedback, feedback_type):
    """根据用户反馈更新笔记

    Args:
        note_path: 笔记文件路径
        feedback: 用户反馈内容
        feedback_type: 反馈类型（理解困难/补充内容/易错点等）

    Returns:
        bool: 更新是否成功
    """
    try:
        with open(note_path, 'r', encoding='utf-8') as f:
            content = f.read()

        today = datetime.now().strftime('%Y-%m-%d')

        # 根据反馈类型定位更新位置
        if feedback_type == "理解困难":
            # 在"我的理解记录"部分添加
            section = "## 我的理解记录 🧠"
            addition = f"""
### 理解障碍 ({today})
- 困难点：{feedback}
- 补充解释：[AI生成的解释]
"""
        elif feedback_type == "易错点":
            # 在"易错点"部分添加
            section = "## 易错点 ⚠️"
            addition = f"""
- **{today}**: {feedback}
"""
        else:
            # 在"补充说明"部分添加
            section = "## 补充说明 📝"
            addition = f"""
<!-- UPDATE: {today} 用户反馈 -->
{feedback}
<!-- END UPDATE -->
"""

        # 插入更新内容
        if section in content:
            updated_content = content.replace(
                section,
                section + "\n" + addition
            )
        else:
            # 如果找不到对应部分，追加到文件末尾
            updated_content = content + "\n\n" + addition

        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return True
    except Exception as e:
        print(f"更新笔记失败: {e}")
        return False
```

### 3.2 analyze_understanding_barrier

```python
def analyze_understanding_barrier(feedback):
    """分析用户的理解障碍类型

    Args:
        feedback: 用户反馈内容

    Returns:
        dict: {
            "type": "概念抽象|逻辑跳跃|缺乏例题|条件不清",
            "suggestions": ["建议1", "建议2", ...]
        }
    """
    feedback_lower = feedback.lower()

    # 关键词匹配
    if any(kw in feedback_lower for kw in ["不懂为什么", "怎么来的", "推导"]):
        return {
            "type": "逻辑跳跃",
            "suggestions": [
                "补充详细的推导过程",
                "添加每一步的理由说明",
                "使用具体数值举例"
            ]
        }
    elif any(kw in feedback_lower for kw in ["太抽象", "无法理解", "不直观"]):
        return {
            "type": "概念抽象",
            "suggestions": [
                "添加直观解释和类比",
                "补充几何意义或物理意义",
                "使用图示说明"
            ]
        }
    elif any(kw in feedback_lower for kw in ["不会做题", "没有例子", "怎么用"]):
        return {
            "type": "缺乏例题",
            "proposition": [
                "添加典型例题",
                "补充解题步骤",
                "提供变式练习"
            ]
        }
    elif any(kw in feedback_lower for kw in ["什么时候用", "什么条件", "适用范围"]):
        return {
            "type": "条件不清",
            "suggestions": [
                "明确列出使用条件",
                "补充适用场景",
                "添加反例说明"
            ]
        }
    else:
        return {
            "type": "综合问题",
            "suggestions": [
                "多角度解释",
                "补充例题和推导",
                "添加对比分析"
            ]
        }
```

---

## 4. 跨学科提示

### 4.1 跨学科提示模板

在生成笔记时，应主动添加跨学科提示，特别是数学→电子技术的关联。

```markdown
## 跨学科应用 ⚡

### 电子技术中的应用
- **频率分析**：该知识点在电路频率响应分析中的应用
- **信号处理**：在模拟/数字信号处理中的应用
- **参考**：[[822电子技术基础/相关章节]]
```

---

## 5. 自动生成指令

当调用此技能时，系统应该：

1. **保护已有笔记**：不会覆盖任何已有内容的文件
2. **提取知识点**：从用户输入中解析知识点
3. **生成结构化笔记**：使用模板生成完整笔记
4. **添加跨学科提示**：自动关联到电子技术基础
5. **支持反馈更新**：根据用户反馈动态更新笔记

---

*创建日期: 2026-03-10*
*版本: 1.0.0*
