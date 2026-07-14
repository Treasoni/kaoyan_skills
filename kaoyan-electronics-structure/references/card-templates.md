# 知识点卡片模板

由 [code.md](../code.md) 按需引用，用于生成模电/数电知识点卡片。

## 模电卡片模板

```python
def generate_modian_card(topic: str, content: Dict) -> str:
    """生成模电知识点卡片"""

    return f"""# {topic}

---
tags:
  - 模拟电子技术
  - {content.get('chapter', '知识点')}
  - 考研822
mastery: 0
exam_importance: {content.get('importance', 3)}
---

## 基本概念
{content.get('concept', '> [!info] 待补充')}

## 核心公式
$$
{content.get('formula', '\\text{待补充}')}
$$

## 分析方法
1. {content.get('step1', '步骤一')}
2. {content.get('step2', '步骤二')}

## 重要参数
| 参数 | 符号 | 单位 | 说明 |
|------|------|------|------|
| ... | ... | ... | ... |

## 注意事项
- ⚠️ {content.get('warning', '注意事项')}

## 关联知识点
- 前置知识: {', '.join(content.get('prerequisites', ['无']))}
- 后续知识: {', '.join(content.get('applications', ['无']))}

## 考试重点
- {content.get('exam_tip', '重点内容')}

## 错题记录
> [!mistake] 相关错题链接到错题本
"""
```

## 数电卡片模板

```python
def generate_shudian_card(topic: str, content: Dict) -> str:
    """生成数电知识点卡片"""

    return f"""# {topic}

---
tags:
  - 数字电子技术
  - {content.get('chapter', '知识点')}
  - 考研822
mastery: 0
exam_importance: {content.get('importance', 3)}
---

## 功能描述
{content.get('function', '> [!info] 待补充')}

## 真值表/状态表
| 输入 | 输出 |
|------|------|
| ... | ... |

## 逻辑表达式
$$
{content.get('expression', '\\text{待补充}')}
$$

## 工作波形
{content.get('waveform', '波形描述')}

## 典型应用
- 应用1: {content.get('application1', '描述')}

## 注意事项
- ⚠️ {content.get('warning', '注意事项')}

## 关联知识点
- 前置知识: {', '.join(content.get('prerequisites', ['无']))}
- 后续知识: {', '.join(content.get('applications', ['无']))}
"""
```
