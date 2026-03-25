# kaoyan-english-vocab 技能代码

**版本**: 2.0.0 (模块化重构版)
**创建日期**: 2026-03-10
**最后更新**: 2026-03-24

## 概述

本技能提供考研英语词汇学习的核心功能，代码已完全模块化。

### 模块结构

```
scripts/
├── __init__.py              # 模块导出（版本 2.0.0）
├── context_retrieval.py     # 真题语境检索
├── polysemy_detector.py     # 熟词僻义检测
├── word_lookup.py           # 快速查词
├── pdf_extractor.py         # PDF词汇提取
└── word_formatter.py        # 单词表整理格式化
```

### 核心功能

| 功能 | 模块 | 说明 |
|------|------|------|
| **真题语境检索** | `context_retrieval.py` | 优先使用真题语境，其次外刊，最后AI生成 |
| **熟词僻义检测** | `polysemy_detector.py` | Critical/Warning两级预警 |
| **快速查词** | `word_lookup.py` | 查单词、生成单词卡片 |
| **PDF提取** | `pdf_extractor.py` | 支持墨墨/百词斩/通用格式 |
| **单词表整理** | `word_formatter.py` | ⚠️ 必须首先执行！ |

---

## 使用方式

### Python导入

```python
import sys
import os

# 确保能正确导入 scripts 模块
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, "scripts")
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

from scripts import (
    # 真题语境
    generate_context_article,
    search_real_exam_pool,

    # 僻义检测
    detect_polysemy,
    POLYSEMY_CRITICAL,
    POLYSEMY_WARNING,

    # 查词
    lookup_word,
    format_word_card,

    # PDF提取
    extract_words_from_pdf,

    # 单词表整理
    organize_word_list,
)
```

### 标准工作流

```
[用户提供单词表]
      ↓
[步骤0: organize_word_list] ← 必须首先执行！
      ↓
[覆盖原始单词表文件]
      ↓
[步骤1: detect_polysemy]
      ↓
[步骤2: generate_context_article + 生成四类笔记]
```

---

## 关键数据结构

### 僻义预警数据

**Critical级别（高频陷阱）**:
- address: 地址 → vt. 处理，解决 (80%)
- school: 学校 → n. 流派，学派 (70%)
- novel: 新颖的 → n. 长篇小说 (65%)
- fine: 好的 → n./v. 罚款 (60%)

**Warning级别（中等陷阱）**:
- spring: 春天 → v. 突然出现，涌现 (40%)
- table: 桌子 → v. 搁置，暂缓讨论 (35%)
- book: 书 → v. 预订 (30%)

---

## 验证标准

1. ✅ 必须在生成四类笔记**之前**执行单词表整理
2. ✅ 整理后的单词表必须覆盖原始文件
3. ✅ 必须按词族分类
4. ✅ 必须按考研重点分级（⭐⭐⭐ / ⭐⭐ / ⭐）
5. ✅ 必须检测并标记僻义预警（🔴 Critical / 🟡 Warning）

---

## 完整API文档

详见各模块源码：
- `scripts/context_retrieval.py` - 真题语境检索
- `scripts/polysemy_detector.py` - 僻义检测算法
- `scripts/word_lookup.py` - 查词功能
- `scripts/pdf_extractor.py` - PDF解析
- `scripts/word_formatter.py` - 单词表整理

---

*备份文件*: `code.md.backup` (v1.1.0 完整版)
*当前版本*: v2.0.0 (模块化重构版)
