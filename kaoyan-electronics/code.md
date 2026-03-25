# kaoyan-electronics 路由器代码实现

> 本文件提供 kaoyan-electronics 技能的入口逻辑。具体算法实现已模块化至 `scripts/` 目录下。

> 📋 **返回主文档**: [skill.md](skill.md)

---

## 核心依赖导入

```python
import sys
import os

# 确保能正确导入 scripts 模块
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, "scripts")
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from scripts.router import route_electronics_request
from scripts.context import analyze_context, has_image_upload, Context
from scripts.invocation import invoke_skill, ask_for_clarification
```

---

## 主入口 API

### 1. 路由电子技术请求

```python
def process_electronics_request(user_input):
    """
    包装函数：调用主路由器

    参数:
        user_input: 用户输入内容

    返回:
        路由到对应子技能的结果
    """
    return route_electronics_request(user_input)
```

---

## 路由规则速查

| 关键词 | 目标子技能 | 说明 |
|--------|-----------|------|
| 电路图、分析电路、静态/动态分析 | `kaoyan-electronics-circuit` | 电路图解析 |
| 怎么做、SOP、解题步骤 | `kaoyan-electronics-sop` | 解题模板 |
| 知识图谱、前置知识、我要学习 | `kaoyan-electronics-structure` | 知识结构 |
| 配置、专业课状态、跨学科 | `kaoyan-electronics-core` | 核心配置 |
| 上传图片 | `kaoyan-electronics-circuit` | 优先电路分析 |

---

## 模块化说明

| 模块 | 文件 | 职责 |
|------|------|------|
| 主路由器 | [scripts/router.py](scripts/router.py) | 意图分类路由 |
| 上下文分析 | [scripts/context.py](scripts/context.py) | 用户输入解析、图片检测 |
| 子技能调用 | [scripts/invocation.py](scripts/invocation.py) | 子技能调用、错误响应 |

---

## 子技能列表

| 子技能 | 功能 |
|--------|------|
| `kaoyan-electronics-core` | MemOS集成、调度信号、跨学科关联、数学前置检查 |
| `kaoyan-electronics-sop` | 17个标准化解题流程、康华光符号、LaTeX标准 |
| `kaoyan-electronics-circuit` | 电路图识别、元件参数提取、静动态分析 |
| `kaoyan-electronics-structure` | 知识图谱、前置关联、跨章节提示 |

---

## 版本兼容性

重构后保持 **v2.0.0** 功能完全不变：
- ✅ 意图分类路由
- ✅ 图片上传检测
- ✅ 上下文分析
- ✅ 子技能调用
- ✅ 错误处理与澄清请求

---

*创建日期: 2026-03-12*
*版本: 2.0.0 (模块化重构)*
