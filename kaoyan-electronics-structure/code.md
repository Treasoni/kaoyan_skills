# kaoyan-electronics-structure 代码模块

> 📋 **返回主文档**: [SKILL.md](SKILL.md)

---

## 概述

本文件提供 kaoyan-electronics-structure 技能的代码实现逻辑，包括知识图谱查询、前置知识检查、知识点卡片生成、进度追踪等功能。

---

## 核心依赖

```python
import yaml
from typing import Dict, List, Optional, Set
from pathlib import Path
```

---

## 主入口 API

### 1. 知识图谱查询器

```python
def query_knowledge_graph(
    topic: str,
    query_type: str = "full"
) -> Dict:
    """
    查询知识点图谱。

    参数:
        topic: ���识点名称
        query_type: 查询类型 (prerequisites/related/full)

    返回:
        {
            "knowledge_point": str,
            "module": str,
            "prerequisites": List[str],
            "related_points": List[str],
            "cross_chapter_prompts": List[str],
            "exam_importance": int
        }
    """
    graph = load_knowledge_graph()

    if topic not in graph:
        return {"error": f"知识点 '{topic}' 不存在"}

    node = graph[topic]

    result = {"knowledge_point": topic}

    if query_type in ["prerequisites", "full"]:
        result["prerequisites"] = get_prerequisites(topic, graph)

    if query_type in ["related", "full"]:
        result["related_points"] = get_related_points(topic, graph)

    if query_type == "full":
        result.update(node)

    return result
```

---

## 知识图谱数据结构

### 模电知识图谱

```python
MODIAN_GRAPH = {
    "基本放大器": {
        "module": "模电",
        "chapter": "第2章",
        "difficulty": 4,
        "importance": 5,
        "exam_frequency": "高",
        "prerequisites": ["BJT特性曲线", "直流工作点概念"],
        "combinations": ["多级放大", "负反馈"],
        "applications": ["差分放大", "功率放大"],
        "cross_chapter_prompts": [
            "注意：掌握三种基本组态（共射/共基/共集）的对比",
            "建议：静态分析和动态分析要分开进行"
        ],
        "sop_links": ["SOP1", "SOP2"]
    },
    "反馈放大器": {
        "module": "模电",
        "chapter": "第6章",
        "difficulty": 5,
        "importance": 5,
        "exam_frequency": "高",
        "prerequisites": ["基本放大器", "频率响应"],
        "combinations": ["运算电路", "波形产生电路"],
        "cross_chapter_prompts": [
            "注意：深度负反馈是高频考点",
            "提醒：反馈类型判断是难点，需要大量练习",
            "关联：负反馈改善性能的本质是牺牲增益"
        ],
        "sop_links": ["SOP3"]
    },
    # ... 更多知识点
}
```

### 数电知识图谱

```python
SHUDIAN_GRAPH = {
    "时序逻辑电路": {
        "module": "数电",
        "chapter": "第5章",
        "difficulty": 5,
        "importance": 5,
        "exam_frequency": "高",
        "prerequisites": ["触发器", "组合逻辑"],
        "combinations": ["计数器", "移位寄存器"],
        "cross_chapter_prompts": [
            "注意：同步和异步时序的区别",
            "提醒：自启动检查必不可少",
            "重点：驱动方程、状态方程、输出方程的写法"
        ],
        "sop_links": ["SOP12", "SOP13"]
    },
    "计数器": {
        "module": "数电",
        "chapter": "第5章",
        "difficulty": 4,
        "importance": 5,
        "exam_frequency": "高",
        "prerequisites": ["触发器特性", "时钟概念"],
        "cross_chapter_prompts": [
            "注意：同步计数器和异步计数器的区别",
            "建议：掌握74LS161/74LS160的功能表",
            "重点：置数法和复位法设计任意进制计数器"
        ],
        "sop_links": ["SOP14", "SOP15"]
    },
    # ... 更多知识点
}
```

---

## 前置知识检查

```python
def check_prerequisites(topic: str, mastered_points: Set[str]) -> Dict:
    """
    检查学习某知识点前的前置知识掌握情况。

    参数:
        topic: 目标知识点
        mastered_points: 已掌握的知识点集合

    返回:
        {
            "can_proceed": bool,
            "missing_prerequisites": List[str],
            "recommendation": str
        }
    """
    graph = load_knowledge_graph()

    if topic not in graph:
        return {"error": f"知识点 '{topic}' 不存在"}

    prerequisites = get_all_prerequisites(topic, graph)
    missing = [p for p in prerequisites if p not in mastered_points]

    return {
        "can_proceed": len(missing) == 0,
        "missing_prerequisites": missing,
        "recommendation": generate_prerequisite_recommendation(missing)
    }


def get_all_prerequisites(topic: str, graph: Dict) -> List[str]:
    """递归获取所有前置知识（包括间接前置）"""
    visited = set()
    result = []

    def dfs(node):
        if node in visited:
            return
        visited.add(node)

        if node in graph:
            for prereq in graph[node].get("prerequisites", []):
                dfs(prereq)
                if prereq not in result:
                    result.append(prereq)

    dfs(topic)
    return result
```

---

## 知识点卡片生成器

模电/数电卡片模板的完整实现见 [references/card-templates.md](references/card-templates.md)。

---

## 进度追踪

### 进度文件生成

```python
def create_progress_file(chapter_path: str, chapter_name: str) -> str:
    """创建章节进度文件"""

    return f"""---
创建日期: {get_current_date()}
更新日期: {get_current_date()}
tags:
  - 学习进度
  - {chapter_name}
---

# {chapter_name} - 学习进度

## 📊 总体进度

| 统计项 | 数量 |
|--------|------|
| 总知识点 | 0 |
| 已完成 | 0 |
| 待学习 | 0 |
| **完成率** | **0%** |

## 📋 详细进度

| 知识点 | 状态 | 开始日期 | 完成日期 | 备注 |
|--------|------|----------|----------|------|
| ... | ⬜ | ... | ... | ... |

## 状态说明
- ⬜ 未开始
- 🟡 进行中
- ✅ 已完成
"""

def update_progress(
    progress_file: str,
    knowledge_point: str,
    status: str = "completed"
) -> None:
    """更新知识点进度"""
    # 实现进度更新逻辑
    pass
```

---

## 常见错误模式

```python
COMMON_MISTAKES = {
    "模电": [
        {
            "type": "反馈类型判断错误",
            "example": "混淆电压/电流反馈",
            "correction": "使用短路输出端法"
        },
        {
            "type": "忘记U_BE",
            "example": "I_B = V_CC/R_b",
            "correction": "I_B = (V_CC - U_BE)/R_b"
        },
        {
            "type": "忘记负载电阻",
            "example": "A_u = -βR_c/r_be",
            "correction": "R'_L = R_c // R_L"
        },
        {
            "type": "混淆虚短虚断条件",
            "example": "比较器也用虚短",
            "correction": "线性区才有虚短虚断"
        }
    ],
    "数电": [
        {
            "type": "忘记检查自启动",
            "example": "设计时序逻辑",
            "correction": "无效状态必须能进入有效循环"
        },
        {
            "type": "卡诺图圈组错误",
            "example": "不按2^n圈组",
            "correction": "按规则圈组，每个圈尽可能大"
        },
        {
            "type": "忘记异步置数端",
            "example": "忽略优先级",
            "correction": "异步置数优先级最高"
        },
        {
            "type": "状态编码错误",
            "example": "编码不合理",
            "correction": "满足2^(n-1) < N ≤ 2^n"
        }
    ]
}


def get_mistake_patterns(topic_type: str) -> List[Dict]:
    """获取常见错误模式"""
    return COMMON_MISTAKES.get(topic_type, [])
```

---

## 前置知识关系图生成

```python
def generate_prerequisite_diagram(topic: str) -> str:
    """生成前置知识关系图（Mermaid格式）"""

    graph = load_knowledge_graph()
    prerequisites = get_all_prerequisites(topic, graph)

    mermaid_code = """```mermaid
flowchart TD
    subgraph 前置知识
"""

    # 添加节点
    for i, prereq in enumerate(prerequisites):
        mermaid_code += f"        P{i}[{prereq}]\n"

    mermaid_code += "    end\n\n"
    mermaid_code += f"    subgraph 目标\n"
    mermaid_code += f"        T[{topic}]\n"
    mermaid_code += f"    end\n\n"

    # 添加连接
    for i, prereq in enumerate(prerequisites):
        mermaid_code += f"    P{i} --> T\n"

    mermaid_code += "```"
    return mermaid_code
```

---

## 数据文件引用

| 文件 | 路径 | 用途 |
|------|------|------|
| 知识图谱 | `/kaoyan-electronics/scripts/data/knowledge_graph_electronics.yaml` | 完整知识图谱数据 |
| 知识点卡片模板 | `/kaoyan-electronics/scripts/templates/knowledge_card_electronics.md` | 卡片模板 |
| 错误记录模板 | `/kaoyan-electronics/scripts/templates/mistake_record_electronics.md` | 错误记录格式 |

---

## 版本信息

- **创建日期**: 2026-03-27
- **版本**: 1.1.0 (模块化重构)

> 📋 **返回主文档**: [SKILL.md](SKILL.md)
