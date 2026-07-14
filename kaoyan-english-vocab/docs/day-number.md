# Day 编号计算规则

> ⚠️ **强制要求**：本技能**必须**使用 `kaoyan-english-core` 提供的共享Day编号计算函数！
>
> **禁止手动填写 Day 编号！** 必须通过计算获取！

---

## 计算步骤

### 步骤0: 调用核心模块（强制！）

```python
from kaoyan_english_core.day_calculator import (
    calculate_day_number,
    get_validated_day_number,
    generate_day_filenames
)

# 从用户输入的文件路径中提取日期
target_date = "2026-04-06"  # 例如：考研英语/英语单词/2026-4-6.md

# ���法1: 基于日期计算（2026-02-28 = Day 001）
day_number_by_date = calculate_day_number(target_date)
# 返回: 37

# 方法2: 双重验证（推荐！同时检查现有文件）
day_number = get_validated_day_number(target_date, "考研英语/📰 真题语境文章")
# 返回: 37 (取日期计算和文件检查的较大值)

# 生成四类文件名
filenames = generate_day_filenames(target_date, day_number)
# {
#     "context_article": "Context-Day-037-2026-04-06.md",
#     "quiz": "Quiz-Day-037-2026-04-06.md",
#     "statistics": "Statistics-Day-037-2026-04-06.md",
#     "writing": "Writing-Day-037-2026-04-06.md"
# }
```

### 步骤1: 双重验证机制

`get_validated_day_number()` 函数会同时执行两种验证：

1. **日期计算**：基于 2026-02-28 = Day 001 的基准
2. **文件检查**：扫描现有文件获取最大 Day 编号
3. **取较大值**：确保不会覆盖现有文件

### 步骤2: 生成统一文件名

所有4类文件必须使用**相同的Day编号**：

| 笔记类型 | 文件名格式 | 示例 |
|----------|-----------|------|
| 📊 词汇统计 | `Statistics-Day-{XXX}-{YYYY-MM-DD}.md` | `Statistics-Day-037-2026-04-06.md` |
| 📰 真题语境文章 | `Context-Day-{XXX}-{YYYY-MM-DD}.md` | `Context-Day-037-2026-04-06.md` |
| 📝 测试记录 | `Quiz-Day-{XXX}-{YYYY-MM-DD}.md` | `Quiz-Day-037-2026-04-06.md` |
| ✍️ 写作输出 | `Writing-Day-{XXX}-{YYYY-MM-DD}.md` | `Writing-Day-037-2026-04-06.md` |

---

## 禁止事项

| 禁止行为 | 原因 |
|----------|------|
| ❌ 手动硬编码 "Day-001" | 会导致编号冲突 |
| ❌ 跳过 `get_validated_day_number()` 调用 | 可能覆盖现有文件 |
| ❌ 不同文件使用不同 Day 编号 | 破坏文件关联性 |
| ❌ 使用错误的日期格式 | 导致计算错误 |

---

## 验证步骤

执行前必须验证：

1. **检查现有文件列表**：
   ```bash
   ls -la "考研英语/📊 词汇统计/" | tail -5
   ls -la "考研英语/📰 真题语境文章/" | tail -5
   ```

2. **验证编号连续性**：
   - 如果最新是 Day-036，新文件应该是 Day-037
   - 不允许跳号（如 Day-036 → Day-040）

3. **检查日期匹配**：
   - 2026-04-06 应该对应 Day-037（基于 2026-02-28 = Day 001）

---

## Day编号对应关系

| 日期 | Day编号 | 计算公式 |
|------|---------|----------|
| 2026-02-28 | Day 001 | 基准日期 |
| 2026-03-01 | Day 002 | 1 + 1 |
| 2026-04-01 | Day 032 | 1 + 31 |
| 2026-04-05 | Day 036 | 1 + 35 |
| 2026-04-06 | Day 037 | 1 + 36 |

---

## 核心函数位置

详细实现请参考：`../.claude/skills/kaoyan-english-core/scripts/day_calculator.py`

---

*更新日期: 2026-04-06*
*版本: 2.0.0*
