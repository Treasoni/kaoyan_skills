# 考研英语单词测试技能 - 实现代码

## 测试题型

### 题型1: 词义选择

四选一词义测试，重点考查僻义词。

```markdown
## 词义选择

1. exemplify
   - [ ] A. 忽略
   - [ ] B. 举例说明
   - [ ] C. 夸大
   - [ ] D. 简化

2. address (在考研中最常见的意义是)
   - [ ] A. 地址
   - [ ] B. 处理、解决 ⚠️ 僻义
   - [ ] C. 称呼
   - [ ] D. 演讲
```

### 题型2: 搭配填空

测试常用词组搭配。

```markdown
## 搭配填空

3. The report _____ the need for reform.
   - [ ] A. exemplifies
   - [ ] B. exemplify

4. We must _____ the root causes of inequality.
   - [ ] A. address
   - [ ] B. addresses
   - [ ] C. addressing
```

### 题型3: 僻义词专项

专门针对熟词僻义的强化测试。

```markdown
## ⚠️ 僻义词专项测试

5. school 在"Chicago school of economics"中的意思是：
   - [ ] A. 学校
   - [ ] B. 流派，学派 ⚠️ 僻义

6. novel 在"a novel approach"中的意思是：
   - [ ] A. 长篇小说
   - [ ] B. 新颖的，创新的 ⚠️ 僻义
```

---

## 测试题模板

```markdown
# 单词测试 - Day {day_number}

**日期**: {date}
**测试范围**: {review_words | polysemy_words | random}
**题目数量**: {count}

---

## 词义选择

1. exemplify
   - [ ] A. 忽略
   - [ ] B. 举例说明
   - [ ] C. 夸大
   - [ ] D. 简化

## ⚠️ 僻义测试

3. school 在"Chicago school of economics"中的意思是：
   - [ ] A. 学校
   - [ ] B. 流派，学派

## 搭配填空

4. The report _____ the need for reform.
   - [ ] A. exemplifies
   - [ ] B. exemplify

---

## 答案与解析

### 词义选择
1. **B. 举例说明** - exemplify: 举例说明，例证
2. **B. 处理、解决** - ⚠️ address在考研中80%考查"处理"义

### 僻义测试
3. **B. 流派，学派** - ⚠️ school在学术语境中指"学派"

### 搭配填空
4. **A. exemplifies** - 第三人称单数，主语report是单数

---

## 成绩统计

| 项目 | 结果 |
|------|------|
| 总分 | ___ / 100 |
| 正确率 | ___% |
| 僻义词错误 | {count}个 |
| 需加强词汇 | {words} |

---

## 薄弱项分析

### 高频错误词
- address (僻义错误)
- school (搭配错误)

### 建议复习
- [ ] 重新学习address的僻义用法
- [ ] 复习school的学术语境用法
```

---

## 工作流程

```
[从MemOS加载用户上下文]
      ↓
[选择测试范围]
      ↓
[生成测试题]
      ↓
[优先包含僻义词]
      ↓
[执行测试]
      ↓
[统计结果]
      ↓
[记录错误到MemOS]
```

---

## 测试数据模型

```yaml
test_record:
  test_id: string
  user_id: string
  test_type: enum (meaning_quiz | collocation_quiz | polysemy_quiz)
  date: date
  created_at: datetime

  test_data:
    word_count: int
    questions: array
    polysemy_count: int  # 僻义词数量

  results:
    score: float
    correct_count: int
    incorrect_count: int
    polysemy_errors: array  # 僻义词错误列表
    weak_words: array  # 薄弱词汇列表

  memos_test_id: string
```

---

## Day编号计算规则

本技能使用 `kaoyan-english-core` 提供的共享Day编号计算函数。

### 推荐做法

```python
from kaoyan_english_core import get_validated_day_number, generate_day_filenames

day_number = get_validated_day_number("2026-03-16")  # 返回：17
filenames = generate_day_filenames("2026-03-16", day_number)
quiz_filename = filenames["quiz"]  # "Quiz-Day-017-2026-03-16.md"
```

### Day编号对应关系

| 日期 | Day编号 |
|------|---------|
| 2026-02-28 | Day 001 |
| 2026-03-01 | Day 002 |
| 2026-03-15 | Day 016 |
| 2026-03-16 | Day 017 |
