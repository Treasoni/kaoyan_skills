---
name: kaoyan-english-vocab
description: This skill handles vocabulary organization and word lookup for 考研英语 (Chinese graduate entrance English exam). Use it when users want to extract vocabulary from PDF exports (墨墨/百词斩), generate real exam context articles, detect polysemy (rare word meanings), look up word information, or organize vocabulary cards.
---

# 考研英语词汇整理技能

> 📁 详细执行指南见 [code.md](code.md)

## 核心功能

| 功能 | 说明 |
|------|------|
| **PDF词汇提取** | 从墨墨/百词斩等APP导出的PDF中提取词汇 |
| **单词表整理** | 按词族分类、按考频分级、添加记忆方法、僻义预警 |
| **熟词僻义检测** | 识别考研中的僻义陷阱（Critical/Warning两级预警） |
| **快速查词** | 查询单词信息（含僻义预警、真题例句、搭配） |
| **真题语境文章** | 将目标词汇串联成真题风格的语境文章 |

---

## 触发条件

### ✅ 触发此技能

**词汇整理**：
- "整理考研英语单词" + 提供PDF/单词表
- "从PDF提取单词" / "墨墨背单词导出" / "百词斩导出"
- "处理单词表" + 提供单词表文件
- "生成词汇表" / "格式化单词" / "分类单词"

**语境文章**：
- "真题语境文章" / "外刊风格"
- "生成考研英语复习文章"

**查词**：
- "查单词"（考研语境下）/ "查询单词" / "word lookup"

**僻���**：
- "熟词僻义" / "僻义词" / "陷阱词" / "一词多义"

### ❌ 不触发此技能

| 场景 | 使用技能 |
|------|----------|
| 生成复习计划 | `kaoyan-english-review` |
| 单词测试 | `kaoyan-english-quiz` |
| 写作训练 | `kaoyan-english-writing` |

---

## 默认行为（重要）

**当用户提供单词表文件时，默认执行完整流程，禁止询问用户：**

```
[用户提供单词表]
      ↓
[步骤0: 计算 Day 编号] ← ⚠️ 必须首先执行！使用 day_calculator
      ↓
[步骤1: 整理格式化单词表] ← 覆盖原文件
      ↓
[步骤2: 检测熟词僻义]
      ↓
[步骤3: 生成四类笔记]
      ├── 📊 词汇统计 → 考研英语/📊 词汇统计/Statistics-Day-{XXX}-{YYYY-MM-DD}.md
      ├── 📰 真题语境文章 → 考研英语/📰 真题语境文章/Context-Day-{XXX}-{YYYY-MM-DD}.md
      ├── 📝 测试记录 → 考研英语/📝 测试记录/Quiz-Day-{XXX}-{YYYY-MM-DD}.md
      └── ✍️ 写作输�� → 考研英语/✍️ 写作输出/Writing-Day-{XXX}-{YYYY-MM-DD}.md
```

### ⚠️ Day 编号强制要求

**必须使用 `kaoyan-english-core` 的 `day_calculator` 模块计算 Day 编号！**

```python
from kaoyan_english_core.day_calculator import get_validated_day_number, generate_day_filenames

# 步骤0: 获取验证后的 Day 编号（必须首先执行！）
day_number = get_validated_day_number(target_date, "考研英语/📰 真题语境文章")
filenames = generate_day_filenames(target_date, day_number)
```

**禁止事项**:
- ❌ 禁止手动硬编码 Day 编号（如 Day-001）
- ❌ 禁止使用错误的 Day 编号
- ❌ 禁止跳过 Day 编号计算步骤

详细说明见: [docs/day-number.md](docs/day-number.md)

---

## 文档索引

| 文件 | 内容 |
|------|------|
| [code.md](code.md) | **执行指南**（工作流、格式规范） |
| [docs/output-paths.md](docs/output-paths.md) | 四类笔记输出路径 |
| [docs/markdown-table.md](docs/markdown-table.md) | Markdown表格格式规范 |
| [docs/day-number.md](docs/day-number.md) | Day编号计算规则 |
| [templates/formatted-wordlist.md](templates/formatted-wordlist.md) | 整理版单词表模板 |
| [templates/word-card.md](templates/word-card.md) | 词汇卡片模板 |
| [data/polysemy-database.md](data/polysemy-database.md) | 熟词僻义库 |

---

## 验证标准

1. ⚠️ **单词数量必须一致**：输入N个单词 → 输出必须是N个单词（**禁止过滤任何单词！**）
2. ✅ 整理后的单词表必须覆盖原始文件
3. ✅ 必须按词族分类、按考研重点分级（⭐⭐⭐/⭐⭐/⭐）
4. ✅ **记忆方法覆盖率100%**：每个单词都必须有 `> 🧠 **记忆方法**` 块
5. ✅ 必须检测并标记僻义预警（🔴 Critical / 🟡 Warning）
6. ✅ 优先使用真题语境，而非AI生成文章
7. ✅ 四类笔记必须输出到正确的目录

---

## 技能集成

### 依赖技能
- `kaoyan-english-core` - MemOS存储
- `obsidian-markdown` - 笔记创建
- `pdf` - PDF读取

### 被调用场景
- `kaoyan-english-review` - 获取单词信息生成复习计划
- `kaoyan-english-quiz` - 获取单词信息生成测试题
- `kaoyan-english-writing` - 获取单词信息用于写作训练

---

*版本: 2.2.0*
*最后更新: 2026-03-31*
