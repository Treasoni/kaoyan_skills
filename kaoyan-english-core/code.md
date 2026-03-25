# kaoyan-english-core 代码模块

本文档包含 kaoyan-english-core 技能的所有代码实现。

---

## 模块化架构（v2.0.0）

本技能已完成模块化重构，所有代码已拆分至 `scripts/` 目录：

### 核心模块

| 模块 | 文件 | 功能描述 |
|------|------|----------|
| **MemOS 集成** | `memos_client.py` | 用户上下文加载、词汇卡片保存、复习会话记录、画像新鲜度检查 |
| **欠账疲劳检查** | `debt_fatigue_checker.py` | 词汇欠账检测（熔断机制）、疲劳度干预、恢复计划生成 |
| **调度信号** | `dispatch_signals.py` | 跨科目调度信号处理、模式切换、信号标记 |
| **记忆压缩** | `memory_compression.py` | 时间压缩模式、学习策略调整、恢复计划 |
| **阶段目标** | `phase_targets.py` | 基于倒计时的动态目标、僻义权重、复习时间分配 |
| **统一错误** | `unified_mistake.py` | 错误记录保存、错误模式分析、僻义错误追踪 |
| **Day 计算** | `day_calculator.py` | Day 编号计算、文件名生成、双重验证 |
| **数据模型** | `data_models.py` | 枚举类型、数据类、常量定义 |

### 快速导入

```python
import sys
import os

# 确保能正确导入 scripts 模块
current_dir = os.path.dirname(os.path.abspath(__file__))
scripts_dir = os.path.join(current_dir, "scripts")
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

# 从技能根目录导入所有公共函数
from scripts import (
    # MemOS 集成
    load_user_context_from_memory,
    save_word_card_to_memory,
    record_review_session,

    # 欠账与疲劳检查
    check_vocabulary_debt_with_memory,
    check_vocabulary_fatigue_intervention,

    # 调度信号处理
    check_dispatch_signals,
    process_dispatch_signal,

    # 记忆压缩模式
    activate_memory_compression_mode,

    # 动态权重响应
    get_phase_vocabulary_target,
    calculate_polysemy_priority_score,

    # 统一错误模型
    save_unified_english_mistake,
    analyze_mistake_patterns,

    # Day 编号计算
    calculate_day_number,
    get_validated_day_number,
    generate_day_filenames,

    # 数据模型
    UserProfile,
    WordCard,
    ReviewRecord,
)
```

### 使用示例

#### 1. MemOS 集成

```python
from scripts import load_user_context_from_memory, save_word_card_to_memory

# 加载用户上下文
user_input = {"user_id": "user123"}
context = load_user_context_from_memory(user_input)

# 保存词汇卡片
word_card = {"word": "example", "meaning": "例子"}
save_word_card_to_memory(word_card, "user123")
```

#### 2. 欠账检查

```python
from scripts import check_vocabulary_debt_with_memory, DEBT_LIMIT

# 检查欠账状态
result = check_vocabulary_debt_with_memory(context)
if result["type"] == "vocabulary_emergency":
    print(f"⚠️ 待复习词汇已达{result['overdue_count']}个，超过阈值{DEBT_LIMIT}")
```

#### 3. 阶段目标

```python
from scripts import get_phase_vocabulary_target

# 获取当前阶段目标（距离考试60天）
target = get_phase_vocabulary_target(60)
print(f"每日新词: {target['daily_new_words']}")
print(f"复习比例: {target['review_ratio']}")
print(f"学习重点: {target['focus']}")
```

#### 4. Day 编号计算

```python
from scripts import calculate_day_number, generate_day_filenames

# 计算今天的 Day 编号
day_num = calculate_day_number()
print(f"Today is Day {day_num}")

# 生成四类文件名
filenames = generate_day_filenames("2026-03-16", 17)
# {
#     "context_article": "Context-Day-017-2026-03-16.md",
#     "quiz": "Quiz-Day-017-2026-03-16.md",
#     "statistics": "Statistics-Day-017-2026-03-16.md",
#     "writing": "Writing-Day-017-2026-03-16.md"
# }
```

#### 5. 统一错误记录

```python
from scripts import create_mistake_record, save_unified_english_mistake

# 创建错误记录
mistake = create_mistake_record(
    mistake_type="polysemy_error",
    word="address",
    correct_answer="演讲",
    user_answer="地址",
    context="真题语境：2020年Text1"
)

# 保存到 MemOS
save_unified_english_mistake(mistake, "user123")
```

---

## API 索引

### MemOS 集成（memos_client.py）

- `load_user_context_from_memory(user_input)` - 从 MemOS 加载用户上下文
- `parse_memory_to_english_context(memory_results)` - 解析记忆结果为上下文
- `save_word_card_to_memory(word_card, user_id)` - 保存词汇卡片
- `record_review_session(user_id, session_data)` - 记录复习会话
- `check_context_freshness_english(user_context, current_date)` - 检查画像新鲜度

### 欠账与疲劳检查（debt_fatigue_checker.py）

- `check_vocabulary_debt_with_memory(user_context)` - 检查词汇欠账
- `calculate_overdue_words(user_context)` - 计算逾期词汇数
- `generate_vocabulary_recovery_plan(overdue_count)` - 生成恢复计划
- `check_vocabulary_fatigue_intervention(user_context)` - 检查疲劳干预
- `calculate_vocabulary_fatigue_score(...)` - 计算疲劳度分数

### 调度信号处理（dispatch_signals.py）

- `check_dispatch_signals(user_id)` - 检查待处理信号
- `process_dispatch_signal(signal)` - 处理调度信号
- `mark_signal_as_processed(signal_id, user_id)` - 标记信号已处理
- `create_dispatch_signal(...)` - 创建调度信号

### 记忆压缩模式（memory_compression.py）

- `activate_memory_compression_mode(context)` - 激活压缩模式
- `get_planned_english_hours()` - 获取原计划学习时间
- `calculate_compression_ratio(...)` - 计算压缩比例
- `adjust_vocabulary_target_for_compression(...)` - 调整词汇目标
- `generate_compression_recovery_plan(...)` - 生成恢复计划

### 动态权重响应（phase_targets.py）

- `get_phase_vocabulary_target(days_to_exam)` - 获取阶段目标
- `calculate_polysemy_priority_score(...)` - 计算僻义优先级
- `adjust_review_list_by_phase(...)` - 按阶段调整复习列表
- `get_phase_specific_instructions(days_to_exam)` - 获取阶段指导
- `calculate_daily_review_time(...)` - 计算时间分配

### 统一错误模型（unified_mistake.py）

- `save_unified_english_mistake(mistake_data, user_id)` - 保存错误记录
- `create_mistake_record(...)` - 创建错误记录
- `batch_save_mistakes(mistakes, user_id)` - 批量保存
- `analyze_mistake_patterns(mistakes)` - 分析错误模式
- `get_polysemy_critical_words(mistakes, min_error_count)` - 获取僻义关键词

### Day 编号计算（day_calculator.py）

- `calculate_day_number(target_date)` - 计算Day编号
- `get_max_day_number_from_files(directory)` - 从文件获取最大Day编号
- `get_validated_day_number(target_date, directory)` - 获取验证后的Day编号
- `format_day_number(day_number, padding)` - 格式化Day编号
- `generate_day_filenames(target_date, day_number)` - 生成四类文件名
- `parse_day_number_from_filename(filename)` - 从文件名解析Day编号
- `get_day_range(start_date, end_date)` - 获取日期范围内的Day列表

### 数据模型（data_models.py）

**枚举类型：**
- `ExamType` - 考试类型（英语一/英语二）
- `CurrentLevel` - 当前水平（基础/中级/高级）
- `ReviewFocus` - 复习重点（均衡/僻义优先/写作优先）
- `LearningStyle` - 学习风格（语境优先/死记优先）
- `PolysemySensitivity` - 僻义敏感度（高/中/低）
- `MentalStatus` - 心理状态（精力充沛/正常/疲惫/倦怠）
- `WarningLevel` - 预警级别（严重/警告/关注）
- `ExamFrequency` - 考试频率（高/中/低）

**数据类：**
- `UserProfile` - 用户画像
- `WordCard` - 词汇卡片（SM-2 + 考研适配）
- `ReviewRecord` - 复习记录
- `MentalStateRecord` - 心理状态记录

**常量：**
- `DEFAULT_DAILY_NEW_WORD_TARGET` - 默认每日新词目标（50）
- `DEBT_LIMIT` - 词汇欠账熔断阈值（200）
- `POLYSEMY_CRITICAL_THRESHOLD` - 僻义严重阈值（0.3）
- `POLYSEMY_WARNING_THRESHOLD` - 僻义警告阈值（0.5）
- `SM2_DEFAULT_EASE_FACTOR` - SM-2 默认难度系数（2.5）

---

## 版本历史

- **v2.0.0** (2026-03-24) - 模块化重构，拆分为 8 个独立模块
- **v1.1.0** (2026-03-24) - 统一文件命名规范（Context-Day/Writing-Day）
- **v1.0.0** (2026-03-10) - 初始版本

---

## 备份文件

原始代码已备份至 `code.md.backup`，包含所有实现细节。
