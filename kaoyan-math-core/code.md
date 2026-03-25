# kaoyan-math-core 代码模块

本文档提供 kaoyan-math-core 技能的入口逻辑。具体算法实现已模块化至 `scripts/` 目录下。

> 📋 **返回主文档**: [SKILL.md](SKILL.md)

---

## 概述

kaoyan-math-core 技能的核心算法已拆分为2个专业Python模块：

| 模块 | 文件 | 职责 |
|------|------|------|
| MemOS集成 | [scripts/memos_client.py](scripts/memos_client.py) | 用户上下文加载、错题保存、知识卡片保存 |
| 知识图谱 | [scripts/knowledge_graph.py](scripts/knowledge_graph.py) | 模块结构、知识点关系、学习路径计算 |

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

from scripts.memos_client import (
    load_user_context_from_memory,
    save_mistake_to_memory,
    save_knowledge_card_to_memory,
)

from scripts.knowledge_graph import (
    get_module_structure,
    get_knowledge_point_relationships,
    calculate_learning_path,
)
```

---

## 主入口 API

### 1. MemOS 集成

```python
# 加载用户上下文
context = load_user_context_from_memory(user_input)

# 保存错题记录
save_mistake_to_memory(mistake_data, user_id)
```

### 2. 知识图谱

```python
# 获取模块结构
structure = get_module_structure("高数", "极限与连续")

# 计算学习路径
path = calculate_learning_path(current_progress, target_module)
```

---

## 版本兼容性

重构后保持功能完全不变：
- ✅ MemOS集成（可降级）
- ✅ 错题记录保存
- ✅ 知识卡片管理
- ✅ 学习路径计算

---

## 模块化说明

详细的模块文档请参考各模块源文件中的 docstring。

---

## 历史版本

原 `code.md` (469行) 已备份为 `code.md.backup`，包含所有历史实现细节。

---

> 📋 **返回主文档**: [SKILL.md](SKILL.md)
