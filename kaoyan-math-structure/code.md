# kaoyan-math-structure 代码模块

本文档提供 kaoyan-math-structure 技能的入口逻辑。具体数据结构和算法实现已模块化至 `scripts/` 目录下。

> 📋 **返回主文档**: [skill.md](skill.md)

---

## 概述

kaoyan-math-structure 技能的核心数据结构和函数已拆分为2个专业Python模块：

| 模块 | 文件 | 职责 |
|------|------|------|
| 数据结构 | [scripts/data.py](scripts/data.py) | 知识点关系图、目录结构模板、知识点树 |
| 查询函数 | [scripts/queries.py](scripts/queries.py) | 知识点查询、关联获取、目录生成 |

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

from scripts.data import (
    KNOWLEDGE_GRAPH,
    MODULE_STRUCTURE,
    HIGHER_MATH_KNOWLEDGE_TREE,
    LINEAR_ALGEBRA_KNOWLEDGE_TREE,
    PROBABILITY_KNOWLEDGE_TREE,
)

from scripts.queries import (
    get_knowledge_structure,
    find_submodule,
    get_knowledge_relations,
    generate_directory_structure,
    get_all_keywords,
    search_knowledge_point,
)
```

---

## 主入口 API

### 1. 获取知识点结构

```python
# 获取高等数学知识点树
tree = get_knowledge_structure("高数")

# 获取线性代数知识点树
tree = get_knowledge_structure("线代")

# 获取概率论知识点树
tree = get_knowledge_structure("概率")

# 获取特定子模块
submodule = get_knowledge_structure("高数", "极限计算")
```

### 2. 获取知识点关联

```python
# 获取洛必达法则的关联信息
relations = get_knowledge_relations("洛必达法则")
# 返回: {
#     "prerequisites": ["极限定义", "导数定义"],
#     "combinations": ["等价无穷小", "泰勒公式"],
#     "applications": ["定积分应用", "变限积分求导"],
#     "cross_chapter_prompts": [...]
# }
```

### 3. 生成目录结构

```python
# 生成函数极限与连续模块的目录结构
created_dirs = generate_directory_structure("函数极限与连续", "/path/to/output")
```

### 4. 搜索知识点

```python
# 搜索包含关键词的知识点
results = search_knowledge_point(HIGHER_MATH_KNOWLEDGE_TREE, "极限")

# 获取所有关键词
keywords = get_all_keywords(HIGHER_MATH_KNOWLEDGE_TREE)
```

---

## 核心数据结构

### KNOWLEDGE_GRAPH (知识点关系图)

```python
KNOWLEDGE_GRAPH = {
    "洛必达法则": {
        "prerequisites": ["极限定义", "导数定义"],
        "combinations": ["等价无穷小", "泰勒公式"],
        "applications": ["定积分应用", "变限积分求导"],
        "cross_chapter_prompts": [...]
    },
    # ...
}
```

### MODULE_STRUCTURE (目录结构模板)

```python
MODULE_STRUCTURE = {
    "函数极限与连续": {
        "name": "函数极限与连续",
        "path": "考研数学/高数-函数极限与连续/",
        "submodules": [...]
    }
}
```

### 知识点树 (HIGHER_MATH / LINEAR_ALGEBRA / PROBABILITY)

```python
HIGHER_MATH_KNOWLEDGE_TREE = {
    "name": "高等数学",
    "children": [
        {"name": "极限与连续", "children": [...]},
        {"name": "一元函数微分学", "children": [...]},
        # ...
    ]
}
```

---

## 知识点树结构概览

### 高等数学
- 极限与连续
- 一元函数微分学
- 一元函数积分学
- 多元函数微积分
- 微分方程
- 无穷级数

### 线性代数
- 行列式
- 矩阵
- 向量
- 线性方程组
- 特征值与特征向量
- 二次型

### 概率论与数理统计
- 概率基础
- 随机变量
- 常用分布
- 多维随机变量
- 数字特征
- 大数定律与中心极限定理
- 数理统计

---

## 版本兼容性

重构后保持功能完全不变：
- ✅ 知识点关系图查询
- ✅ 目录结构模板
- ✅ 三科知识点树
- ✅ 知识点搜索
- ✅ 目录生成

---

## 模块化说明

详细的模块文档请参考各模块源文件中的 docstring。

---

## 历史版本

原 `code.md` (394行) 已备份为 `code.md.backup`，包含所有历史实现细节。

---

> 📋 **返回主文档**: [skill.md](skill.md)
