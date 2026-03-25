"""
单词查询模块

提供快速查词功能，包含单词信息查询和卡片格式化。
"""

from typing import Dict, List, Optional


def lookup_word(word: str, exam_type: str = "english_2") -> Dict:
    """快速查询单词信息

    Args:
        word: 目标单词
        exam_type: 考试类型（english_1/english_2）

    Returns:
        dict: 单词信息卡片，包含：
            - word: 单词
            - pronunciation: 音标
            - part_of_speech: 词性
            - meanings: 释义列表
            - polysemy_alert: 僻义预警（如果有）
            - real_exam_examples: 真题例句
            - collocations: 常用搭配
            - word_family: 词族
    """
    # 1. 获取基本信息
    basic_info = get_basic_word_info(word)

    # 2. 检测僻义
    polysemy_alert = detect_polysemy(word)

    # 3. 获取真题例句
    real_exam_examples = get_real_exam_examples(word, exam_type)

    # 4. 获取搭配
    collocations = get_common_collocations(word)

    # 5. 获取词族
    word_family = get_word_family(word)

    return {
        "word": word,
        "pronunciation": basic_info.get("pronunciation"),
        "part_of_speech": basic_info.get("part_of_speech"),
        "meanings": basic_info.get("meanings"),
        "polysemy_alert": polysemy_alert,
        "real_exam_examples": real_exam_examples,
        "collocations": collocations,
        "word_family": word_family
    }


def format_word_card(word_info: Dict) -> str:
    """格式化单词卡片输出

    Args:
        word_info: 单词信息字典

    Returns:
        str: Markdown格式的单词卡片
    """
    card = f"""# {word_info['word']}

## 基本信息
**音标**: {word_info.get('pronunciation', 'N/A')}
**词性**: {word_info.get('part_of_speech', 'N/A')}
"""

    # 僻义预警
    if word_info.get('polysemy_alert'):
        alert = word_info['polysemy_alert']
        icon = "⚠️" if alert.alert_type == "critical" else "⚡"
        card += f"""
## {icon} 僻义预警 [{alert.alert_type}]

> [!danger] 陷阱提示
> 此词在考研中 **{alert.exam_frequency}** 考查僻义

**考研常考僻义**: {', '.join(alert.rare_meanings)}

### 常用搭配
"""
        for col in alert.collocations:
            card += f"- {col}\n"

    # 真题例句
    if word_info.get('real_exam_examples'):
        card += "\n### 真题例句\n"
        for example in word_info['real_exam_examples'][:3]:
            card += f"""> [!example] {example['year']}年真题 {example['section']}
> {example['sentence']}
"""

    return card


# ========== 辅助函数 ==========

def get_basic_word_info(word: str) -> Dict:
    """获取单词基本信息

    Args:
        word: 目标单词

    Returns:
        dict: 包含音标、词性、释义的字典
    """
    # TODO: 实现实际的词典查询逻辑
    return {
        "pronunciation": f"/{word}/",
        "part_of_speech": "n.",
        "meanings": ["示例释义"]
    }


def detect_polysemy(word: str) -> Optional[Dict]:
    """检测单词是否在考研中有僻义

    Args:
        word: 目标单词

    Returns:
        PolysemyAlert对象或None
    """
    # 导入僻义检测模块
    from .polysemy_detector import detect_polysemy as detect
    return detect(word)


def get_real_exam_examples(word: str, exam_type: str) -> List[Dict]:
    """获取真题例句

    Args:
        word: 目标单词
        exam_type: 考试类型

    Returns:
        list: 真题例句列表
    """
    # TODO: 实现真题例句检索
    return []


def get_common_collocations(word: str) -> List[str]:
    """获取常用搭配

    Args:
        word: 目标单词

    Returns:
        list: 搭配列表
    """
    # TODO: 实现搭配检索
    return []


def get_word_family(word: str) -> List[str]:
    """获取词族

    Args:
        word: 目标单词

    Returns:
        list: 词族成员列表
    """
    # TODO: 实现词族提取
    return []
