# kaoyan-math-notes 代码模块

本文档包含 kaoyan-math-notes 技能的所有代码实现。

---

## 1. 已有笔记保护机制

### 1.1 check_existing_notes

检查已有笔记，返回待创建列表。确保不会覆盖已有内容。

```python
def check_existing_notes(target_path, knowledge_points):
    """检查已有笔记，返回待创建列表

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


def has_content(file_path):
    """检查文件是否有实际内容（非空）"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # 排除只有 frontmatter 或空行的情况
            if not content:
                return False
            # 检查是否有实际内容（除了 frontmatter）
            if content.startswith('---'):
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    body = parts[2].strip()
                    return bool(body)
            return True
    except Exception:
        return False
```

---

## 2. 笔记生成辅助函数

### 2.1 extract_knowledge_points

从用户笔记中提取知识点列表。

```python
def extract_knowledge_points(notes_content, module):
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
```

### 2.2 generate_note_from_template

基于模板生成笔记内容。

```python
def generate_note_from_template(kp_name, module, user_notes, exam_type="数二"):
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
[待补充：常见错误、思维误区]

## 我的理解记录 🧠

### 初始理解
- 我一开始以为……

### 误区记录
- 我误以为……

### 学习进展
- 听课后我发现……

### 未解疑问
- 我仍然不清楚的是……

## 我的错误类型 📌

### 条件遗漏 ⚠️
- [ ] 经常忘记……条件

### 方法误选 ⚠️
- [ ] 总是想用……方法

### 推导跳步 ⚠️
- [ ] 经常跳过……步骤

### 计算失误 ⚠️
- [ ] 经常算错……

## 例题
> [!example] 例1
> **题目**：...
> **分析**：...
> **解答**：...
> **评注**：...

## 相关知识点 📚

### 前置知识
- [[相关知识点1]] - 说明

### 常考组合
- [[相关知识点2]] - 结合使用说明

### 跨章节应用 ⚠️
- 与[[其他章节知识点]]的结合

## 补充说明 📝
<!-- UPDATE: YYYY-MM-DD 用户反馈 -->
[根据用户反馈动态添加的内容]
<!-- END UPDATE -->

---
*创建日期: {datetime.now().strftime('%Y-%m-%d')}*
"""
    return template
```

---

## 3. 笔记更新函数

### 3.1 update_note_with_feedback

根据用户反馈更新笔记。

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

分析用户的理解障碍类型。

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
            "suggestions": [
                "多角度解释",
                "补充例题和推导",
                "添加对比分析"
            ]
        }
```

---

*创建日期: 2026-03-10*
*版本: 1.0.0*
