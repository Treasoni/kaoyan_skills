"""
知识点查询函数模块

本模块包含考研数学知识点结构的查询函数，包括：
- 获取知识点结构
- 获取知识点关联
- 生成目录结构

来源: code.md 第288-389行
"""

from pathlib import Path
from typing import Dict, Any, List, Optional

from .data import (
    KNOWLEDGE_GRAPH,
    MODULE_STRUCTURE,
    HIGHER_MATH_KNOWLEDGE_TREE,
    LINEAR_ALGEBRA_KNOWLEDGE_TREE,
    PROBABILITY_KNOWLEDGE_TREE,
)


def get_knowledge_structure(module_name: str, sub_module: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """获取知识点结构

    Args:
        module_name: 模块名称（高数/线代/概率）
        sub_module: 子模块名称（可选）

    Returns:
        dict: 知识点结构
    """
    if module_name == "高数":
        tree = HIGHER_MATH_KNOWLEDGE_TREE
    elif module_name == "线代":
        tree = LINEAR_ALGEBRA_KNOWLEDGE_TREE
    elif module_name == "概率":
        tree = PROBABILITY_KNOWLEDGE_TREE
    else:
        return None

    if sub_module:
        # 查找子模块
        return find_submodule(tree, sub_module)

    return tree


def find_submodule(tree: Dict[str, Any], name: str) -> Optional[Dict[str, Any]]:
    """递归查找子模块

    Args:
        tree: 知识点树
        name: 要查找的名称

    Returns:
        dict: 找到的子模块，未找到返回None
    """
    if tree.get("name") == name:
        return tree

    for child in tree.get("children", []):
        result = find_submodule(child, name)
        if result:
            return result

    return None


def get_knowledge_relations(knowledge_point: str) -> Dict[str, Any]:
    """获取知识点的关联信息

    Args:
        knowledge_point: 知识点名称

    Returns:
        dict: {
            "prerequisites": [...],
            "combinations": [...],
            "applications": [...],
            "cross_chapter_prompts": [...]
        }
    """
    return KNOWLEDGE_GRAPH.get(knowledge_point, {
        "prerequisites": [],
        "combinations": [],
        "applications": [],
        "cross_chapter_prompts": []
    })


def generate_directory_structure(module_name: str, output_path: str) -> List[str]:
    """生成目录结构

    Args:
        module_name: 模块名称
        output_path: 输出路径

    Returns:
        list: 创建的目录列表
    """
    structure = MODULE_STRUCTURE.get(module_name)
    if not structure:
        return []

    created_dirs = []
    base_path = Path(output_path) / structure["path"]

    for submodule in structure["submodules"]:
        subdir = base_path / submodule["folder"]
        subdir.mkdir(parents=True, exist_ok=True)
        created_dirs.append(str(subdir))

        # 创建子文件夹
        if "subfolder" in submodule:
            subfolder = subdir / submodule["subfolder"]["name"]
            subfolder.mkdir(exist_ok=True)
            created_dirs.append(str(subfolder))

    return created_dirs


def get_all_keywords(tree: Dict[str, Any]) -> List[str]:
    """获取知识点树中的所有关键词

    Args:
        tree: 知识点树

    Returns:
        list: 关键词列表
    """
    keywords = []

    if "keywords" in tree:
        keywords.extend(tree["keywords"])

    for child in tree.get("children", []):
        keywords.extend(get_all_keywords(child))

    return list(set(keywords))


def search_knowledge_point(tree: Dict[str, Any], keyword: str) -> List[Dict[str, Any]]:
    """搜索包含关键词的知识点

    Args:
        tree: 知识点树
        keyword: 搜索关键词

    Returns:
        list: 匹配的知识点列表
    """
    results = []

    # 检查当前节点
    if keyword.lower() in tree.get("name", "").lower():
        results.append(tree)
    elif "keywords" in tree and keyword.lower() in [k.lower() for k in tree["keywords"]]:
        results.append(tree)

    # 递归检查子节点
    for child in tree.get("children", []):
        results.extend(search_knowledge_point(child, keyword))

    return results
