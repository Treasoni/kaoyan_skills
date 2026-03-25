"""
笔记更新函数模块

本模块处理考研数学笔记的更新，包括：
- 根据反馈更新笔记
- 分析理解障碍类型

来源: code.md 第210-342行
"""

from datetime import datetime
from typing import Dict, Any, Optional


def update_note_with_feedback(note_path: str, feedback: str, feedback_type: str) -> bool:
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


def analyze_understanding_barrier(feedback: str) -> Dict[str, Any]:
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
            "suggestions": [
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
            "suggests": [
                "多角度解释",
                "补充例题和推导",
                "添加对比分析"
            ]
        }
