---
name: kaoyan-math
description: This skill should be used when the user asks to generate/modify study notes for 考研数学 (Chinese graduate entrance math exam), specifically when the user provides existing notes and wants to create exam-oriented learning notes, or when the user provides feedback to update existing study notes. Now integrated with MemOS for persistent mistake tracking and cross-device synchronization.
version: 3.0.0
---

# 考研数学学习笔记生成技能 (Kaoyan Mathematics Note Generation Skill)

This skill is designed for **iterative generation of exam-oriented study notes** for 考研数学 (Chinese Postgraduate Mathematics Exam). It transforms user's existing notes into structured, exam-focused learning materials and continuously updates them based on user feedback.

**v3.0.0新增**:
- **LaTeX格式强制**: 所有数学公式必须使用LaTeX格式以确保在Obsidian中正确渲染
- **知识点主动关联**: AI主动提示跨章节关联（如洛必达法则与变限积分求导的结合）
- **MemOS集成**: 实现真正的"千人千面"个性化笔记，记住所有错题历史，支持跨设备同步

---

## MemOS集成说明 (v3.0.0)

### 核心原则
- **增强功能**: MemOS集成是可选增强，不影响基础功能使用
- **优雅降级**: 当MemOS不可用时，自动降级为v2.0.0无状态模式
- **数据持久化**: 错误记录、用户画像、学习历史均持久化存储
- **跨设备同步**: 支持多设备间学习进度同步

### MemOS功能特性
1. **用户画像追踪**: 记录考试类型（数一/数二/数三）、数学水平、学习偏好
2. **错误记录持久化**: 永久保存所有错误历史（条件遗漏、方法误选、推导跳步、计算失误）
3. **个性化提醒**: 基于历史错误生成千人千面的提示
4. **知识点卡片追踪**: 记录每个知识点的掌握程度
5. **画像刷新机制**: 30天未更新时提示确认学习配置

### 降级行为
当MemOS不可用时：
- ✅ 所有v2.0.0功能正常工作
- ✅ LaTeX格式和主动关联功能正常
- ❌ 不保存学习历史到持久存储
- ❌ 不进行跨设备同步
- ❌ 不启用个性化错误模式追踪

---

---

## 用户工作流

```
1. 用户提供现成数学笔记 + 模块信息
   ↓
2. AI 基于现成笔记生成考研导向学习笔记
   ↓
3. 用户学习笔记 + 听课
   ↓
4. 用户反馈理解问题/听课不理解的地方
   ↓
5. AI 分析反馈 + 更新笔记
   ↓
6. 循环步骤3-5
```

---

## 适用场景

### 触发条件

**触发此技能当**：
- 用户提供笔记 + "生成考研学习笔记"
- 用户提供笔记 + "帮我整理成考研笔记"
- 用户说"我对XX不理解" + 之前有生成的笔记文件
- 用户说"听课时不理解XX" + 之前有生成的笔记文件
- 用户要求更新/完善已有的考研学习笔记
- 明确提到"考研数学笔记"或"生成笔记"且涉及高数/线代/概率

### 不触发条件

**不触发此技能当**：
- 普通数学概念问答（如"什么是导数？"）
- 一般数学题目解答
- 没有明确"考研"上下文的数学学习
- 没有笔记生成意图的纯知识点讲解

---

## 核心功能设计

### 功能1：基于现成笔记生成考研学习笔记

**输入**：
- 用户现成的数学笔记（文本或文件）
- 目标模块信息（高数/线代/概率 + 具体章节）
- 目标考试类型（数一/数二/数三）

**处理**：
1. 解析现成笔记，提取知识点
2. 补充考研导向内容：
   - 考试重点标注
   - 常考题型
   - 易错点
   - 解题技巧
   - 典型例题
3. 生成结构化学习笔记

**输出**：
- 保存为 Markdown/Obsidian 笔记文件
- 提供笔记预览

### 功能2：根据反馈更新笔记

**输入**：
- 已有笔记文件路径
- 用户反馈：
  - 理解困难的地方
  - 听课时不理解的地方
  - 希望补充的内容

**处理**：
1. **分析理解障碍**
   - 为什么不理解？（概念抽象/逻辑跳跃/缺乏直观解释）
   - 在笔记中定位对应知识点
2. **优化表达方式**
   - 增加直观解释/类比
   - 分步骤详细讲解
   - 调整叙述顺序
3. **添加辅助内容**
   - 更多例题
   - 图示说明（用文字描述或调用excalidraw-diagram技能）
   - 对比分析
4. **标注易错点**
   - 记录用户思维误区
   - 在易错点部分补充说明
5. **记录思维过程**
   - 在"我的理解记录"中记录用户的原始理解
   - 在"我的错误类型"中标注个性化错误模式
   - 建立用户错误档案，用于后续个性化建议

**输出**：
- 更新笔记文件
- 标注修改位置和内容

---

## 工作流设计

### 阶段1：笔记生成

```
【输入】现成笔记 + 模块信息

【步骤1】解析笔记内容
- 识别知识点结构
- 提取定义、定理、公式
- 识别例题和练习

【步骤2】补充考研导向内容
- 标注考试重点（根据数一/数二/数三）
- 增加常考题型总结
- 补充易错点
- 添加解题技巧
- 提供典型真题示例

【步骤3】生成结构化笔记
使用标准格式：
# [模块名]

## 知识点1

### 定义
[原始笔记中的定义]

### 考试重点 ⭐
[标注是否为高频考点]

### 典型题型
[常考题目类型]

### 解题方法
[解题技巧和步骤]

### 易错点 ⚠️
[常见错误]

### 例题
[例题 + 解析]

【输出】保存为文件
```

### 阶段2：笔记更新

```
【输入】笔记文件路径 + 用户反馈

【步骤1】定位问题点
- 扫描笔记，找到反馈对应的知识点
- 记录当前位置

【步骤2】分析反馈类型
- 概念抽象 → 增加直观解释/类比 + 记录到"我的理解记录"
- 逻辑跳跃 → 增加中间步骤 + 记录到"我的错误类型-推导跳步"
- 条件遗漏 → 补充条件说明 + 记录到"我的错误类型-条件遗漏"
- 方法误选 → 添加方法对比 + 记录到"我的错误类型-方法误选"

【步骤3】更新笔记
- 在对应位置插入补充内容
- 添加"补充说明"标记
- 记录修改历史

【步骤4】记录思维过程
- 在"我的理解记录"中记录用户的原始理解
- 在"我的错误类型"中标注个性化错误模式
- 建立用户错误档案，用于后续个性化建议

【步骤5】验证
- 检查笔记结构完整性
- 确认修改位置正确
- 验证思维过程记录的准确性

【输出】更新文件
```

---

## 笔记格式标准

### 数学公式格式标准 ⚠️ [强制要求]

所有数学公式必须使用 LaTeX 格式，以确保在 Obsidian 中正确渲染。

#### 内联公式
使用单个美元符号 `$...$`
```markdown
示例：设函数 $f(x)$ 在点 $x_0$ 处可导
```

#### 独立公式行
使用双美元符号 `$$...$$`
```markdown
示例：
$$
\lim_{x \to x_0} \frac{f(x) - f(x_0)}{x - x_0} = f'(x_0)
$$
```

#### 特殊符号 LaTeX 映射表

| 数学符号 | LaTeX 代码 | 说明 |
|---------|-----------|------|
| $\alpha, \beta, \gamma$ | `\alpha`, `\beta`, `\gamma` | 希腊字母 |
| $\infty$ | `\infty` | 无穷大 |
| $\int$ | `\int` | 积分号 |
| $\sum$ | `\sum` | 求和 |
| $\leq, \geq$ | `\leq`, `\geq` | 不等号 |
| $\neq$ | `\neq` | 不等于 |
| $\approx$ | `\approx` | 约等于 |
| $\subset$ | `\subset` | 子集 |
| $\in$ | `\in` | 属于 |
| $\partial$ | `\partial` | 偏导数 |
| $\nabla$ | `\nabla` | 梯度 |
| $\oint$ | `\oint` | 闭曲线积分 |
| $\pm$ | `\pm` | 正负号 |
| $\times$ | `\times` | 乘号 |
| $\div$ | `\div` | 除号 |
| $\sqrt{x}$ | `\sqrt{x}` | 平方根 |
| $\sqrt[n]{x}$ | `\sqrt[n]{x}` | n次方根 |
| $x^n$ | `x^n` | 上标 |
| $x_n$ | `x_n` | 下标 |
| $\frac{a}{b}$ | `\frac{a}{b}` | 分数 |
| $\frac{\partial f}{\partial x}$ | `\frac{\partial f}{\partial x}` | 偏导数 |
| $\int_a^b f(x)dx$ | `\int_a^b f(x)dx` | 定积分 |
| $\iint_D f(x,y)dxdy$ | `\iint_D f(x,y)dxdy` | 二重积分 |
| $\iiint_\Omega f(x,y,z)dxdydz$ | `\iiint_\Omega f(x,y,z)dxdydz` | 三重积分 |
| $\oint_L Pdx + Qdy$ | `\oint_L Pdx + Qdy` | 曲线积分 |
| $\lim_{x \to x_0}$ | `\lim_{x \to x_0}` | 极限 |
| $\sum_{i=1}^n$ | `\sum_{i=1}^n` | 求和 |
| $\prod_{i=1}^n$ | `\prod_{i=1}^n` | 求积 |
| $\exists$ | `\exists` | 存在 |
| $\forall$ | `\forall` | 对所有 |
| $\Rightarrow$ | `\Rightarrow` | 推出 |
| $\Leftrightarrow$ | `\Leftrightarrow` | 当且仅当 |
| $\because$ | `\because` | 因为 |
| $\therefore$ | `\therefore` | 所以 |
| $\in$ | `\in` | 属于 |
| $\notin$ | `\notin` | 不属于 |
| $\subset$ | `\subset` | 子集 |
| $\subseteq$ | `\subseteq` | 子集或等于 |
| $\cup$ | `\cup` | 并集 |
| $\cap$ | `\cap` | 交集 |
| $\emptyset$ | `\emptyset` | 空集 |
| $\mathbb{R}$ | `\mathbb{R}` | 实数集 |
| $\mathbb{N}$ | `\mathbb{N}` | 自然数集 |
| $\mathbb{Z}$ | `\mathbb{Z}` | 整数集 |
| $\mathbb{Q}$ | `\mathbb{Q}` | 有理数集 |
| $\mathbb{C}$ | `\mathbb{C}` | 复数集 |
| $f'(x)$ | `f'(x)` | 一阶导数 |
| $f''(x)$ | `f''(x)` | 二阶导数 |
| $f^{(n)}(x)$ | `f^{(n)}(x)` | n阶导数 |
| $\frac{dy}{dx}$ | `\frac{dy}{dx}` | 导数 |
| $\frac{\partial z}{\partial x}$ | `\frac{\partial z}{\partial x}` | 偏导数 |
| $A^{-1}$ | `A^{-1}` | 逆矩阵 |
| $A^T$ | `A^T` | 转置矩阵 |
| $|A|$ | `|A|` | 行列式 |
| $\det(A)$ | `\det(A)` | 行列式 |
| $\text{rank}(A)$ | `\text{rank}(A)` | 矩阵的秩 |
| $\text{tr}(A)$ | `\text{tr}(A)` | 矩阵的迹 |
| $\lambda$ | `\lambda` | 特征值（希腊字母） |
| $\vec{v}$ | `\vec{v}` | 向量 |
| $\|\vec{v}\|$ | `\|\vec{v}\|` | 向量的模 |
| $\vec{a} \cdot \vec{b}$ | `\vec{a} \cdot \vec{b}` | 向量点积 |
| $\vec{a} \times \vec{b}$ | `\vec{a} \times \vec{b}` | 向量叉积 |
| $P(A)$ | `P(A)` | 事件概率 |
| $P(A|B)$ | `P(A|B)` | 条件概率 |
| $E(X)$ | `E(X)` | 期望 |
| $D(X)$ | `D(X)` | 方差 |
| $\text{Var}(X)$ | `\text{Var}(X)` | 方差 |
| $\sigma$ | `\sigma` | 标准差 |
| $\rho$ | `\rho` | 相关系数 |

#### AI 生成约束
生成笔记时：
1. **自动检测**公式并转换为 LaTeX
2. **验证**LaTeX 语法正确性
3. **提供预览**确保渲染正确
4. **优先使用**内联公式 `$...$` 对于行内表达式
5. **独立公式行**使用 `$$...$$` 对于重要公式

### 知识点模板

```markdown
## [知识点名称]

### 原始定义
[来自用户现成笔记]

### 直观理解 💡
[新增：直观解释、类比、几何意义]

### 考试重点 ⭐
[新增：考试频率、题型分布]

### 定理条件 ⚠️
[新增：充要条件、适用范围]

### 典型题型
[新增：常考题目类型]

### 解题方法
[新增：解题步骤、技巧]

### 易错点 ⚠️
[新增：常见错误、思维误区]

### 我的理解记录 🧠
[个性化学习轨迹]

#### 初始理解
- 我一开始以为……
- 我之前的理解是……

#### 误区记录
- 我误以为……
- ❌ 为什么会这样想：（条件/经验/直觉）
- ✅ 正确的理解应该是……

#### 学习进展
- 听课后我发现……
- 做题时我注意到……

#### 未解疑问
- 我仍然不清楚的是……
- 希望进一步了解……

### 我的错误类型 📌
[个性化错误模式]

#### 条件遗漏 ⚠️
- [ ] 经常忘记……条件
- [ ] 例子：……

#### 方法误选 ⚠️
- [ ] 总是想用……方法，但实际应该用……
- [ ] 原因分析：

#### 推导跳步 ⚠️
- [ ] 经常跳过……步骤
- [ ] 导致……

#### 计算失误 ⚠️
- [x] 经常算错……
- [ ] 提醒：……

#### 其他个性化问题
- [ ] ……

### 例题
#### 例1
**题目**：...
**分析**：...
**解答**：...
**评注**：...

### 补充说明 📝
[根据用户反馈动态添加的内容]
```

### 更新标记

```markdown
<!-- UPDATE: 2025-XX-XX 用户反馈不理解XX -->
[补充内容]
<!-- END UPDATE -->
```

---

## 关键组件

### 1. 知识点定位器
- 根据用户反馈找到对应知识点
- 模糊匹配（用户说的"那个函数"→识别为具体函数）

### 2. 理解障碍分析器
- 分析反馈内容
- 分类：概念抽象/逻辑跳跃/缺乏例题/条件不清
- 生成补充策略

### 3. 表达优化器
- 生成直观解释
- 增加类比
- 分步骤讲解

### 4. 例题生成器
- 根据知识点选择典型例题
- 生成详细解答
- 添加评注

---

## 笔记文件组织（按知识点分文件）

### 目录结构

```
考研数学笔记/
├── 📑 索引.md              # MOC (Map of Content)，链接所有知识点
├── 📊 学习进度.md          # Dashboard 显示所有知识点状态
│
├── 高数-极限/
│   ├── 极限定义.md
│   ├── 等价无穷小.md
│   ├── 洛必达法则.md
│   └── 泰勒公式.md
│
├── 高数-导数/
│   ├── 导数定义.md
│   ├── 中值定理.md
│   ├── 极值问题.md
│   └── 凹凸性.md
│
├── 高数-积分/
│   ├── 不定积分.md
│   ├── 定积分.md
│   └── 积分应用.md
│
├── 高数-多元函数/
│   ├── 偏导数.md
│   ├── 全微分.md
│   └── 重积分.md
│
├── 高数-微分方程/
│   ├── 一阶方程.md
│   └── 二阶常系数方程.md
│
├── 高数-级数/
│   ├── 数项级数.md
│   └── 幂级数.md
│
├── 线代/
│   ├── 矩阵运算.md
│   ├── 行列式.md
│   ├── 线性方程组.md
│   ├── 特征值.md
│   └── 二次型.md
│
└── 概率/
    ├── 随机变量.md
    ├── 常用分布.md
    └── 数字特征.md
```

### 单个知识点笔记格式

```markdown
---
知识点: 洛必达法则
模块: 高数-极限
考试类型: 数一/数二/数三
考试频率: ⭐⭐⭐⭐⭐
学习状态: 待学习
tags: [高数, 极限, 重要]
---

# 洛必达法则

## 原始定义
[来自用户用户现成笔记的定义内容]

## 直观理解 💡
[直观解释、类比、几何意义]

## 定理条件 ⚠️
[充要条件、适用范围]

## 考试重点 ⭐
[考试频率、题型分布]

## 典型题型
[常考题目类型]

## 解题方法
[解题步骤、技巧]

## 易错点 ⚠️
[常见错误、思维误区]

## 我的理解记录 🧠

### 初始理解
- 我一开始以为洛必达法则就是直接求导...
- 我之前的理解是只要看到分式就可以用洛必达...

### 误区记录
- 我误以为g'(x)=0的情况不存在...
- ❌ 为什么会这样想：因为题目通常不会设计这种陷阱
- ✅ 正确的理解应该是：g'(x)=0是重要的边界条件，需要特殊处理

### 学习进展
- 听课后我发现必须先验证0/0或∞/∞型...
- 做题时我注意到等价无穷小可以简化计算...

### 未解疑问
- 我仍然不清楚的是洛必达法则的几何证明...
- 希望进一步了解如何判断何时停止使用洛必达...

## 我的错误类型 📌

### 条件遗漏 ⚠️
- [x] 经常忘记验证0/0或∞/∞型条件
- [ ] 例子：直接对(1-cosx)/x使用洛必达

### 方法误选 ⚠️
- [ ] 总是想用洛必达方法，但实际应该用泰勒公式
- [ ] 原因分析：没有意识到泰勒公式更简洁

### 推导跳步 ⚠️
- [ ] 经常跳过验证g'(x)≠0的步骤
- [ ] 导致忽略特殊情况

### 计算失误 ⚠️
- [ ] 经常算错导数
- [ ] 提醒：注意链式法则的应用

### 其他个性化问题
- [ ] 容易混淆一阶导和二阶导的计算...

## 例题
> [!example] 例1
> **题目**：...
> **分析**：...
> **解答**：...
> **评注**：...

## 相关知识点 📚

### 前置知识
- [[极限定义]] - 必须掌握极限的基本概念
- [[导数定义]] - 需要理解导数的几何意义

### 常考组合
- [[等价无穷小]] - 结合使用可简化计算
- [[泰勒公式]] - 复杂函数的替代方法

### 跨章节应用 ⚠️
**重要提醒**：
- 当遇到**变限积分求导**时，通常会结合洛必达法则考查，建议同时复习 [[定积分应用]]
- 在**级数收敛性判定**中可能用到洛必达法则，参考 [[数项级数]]

### 易错点关联
- 条件遗漏 → 回顾 [[定理条件⚠️]]
- g'(x)=0陷阱 → 参见 [[导数计算]]

## 补充说明 📝
<!-- UPDATE: 2025-XX-XX 用户反馈不理解XX -->
[根据用户反馈动态添加的内容]
<!-- END UPDATE -->
```

---

## MemOS集成核心函数 (v3.0.0新增)

### 函数1: load_user_context_from_memory

从MemOS加载用户上下文，失败时返回None触发降级。

```python
def load_user_context_from_memory(user_input):
    """从MemOS加载用户上下文

    Returns:
        dict: 用户上下文信息，包含用户画像、错题库等
        None: MemOS不可用时触发降级
    """
    try:
        results = search_memory(
            query=f"#user_profile {user_input.get('user_id')}",
            top_k=10
        )
        return parse_memory_to_math_context(results)
    except Exception as e:
        log_warning(f"MemOS unavailable: {e}")
        return None


def parse_memory_to_math_context(memory_results):
    """将MemOS结果解析为数学学习上下文"""
    if not memory_results:
        return create_default_user_context()

    context = {
        "user_profile": extract_user_profile(memory_results),
        "mistake_records": extract_mistake_records(memory_results),
        "knowledge_cards": extract_knowledge_cards(memory_results)
    }

    return context
```

### 函数2: save_mistake_to_memory

保存错误记录到MemOS，含降级处理。

```python
def save_mistake_to_memory(mistake_data, user_id):
    """保存错误记录到MemOS

    Args:
        mistake_data: 错误记录数据
        user_id: 用户ID
    """
    try:
        add_message(
            messages=[{
                "role": "assistant",
                "content": {
                    "type": "mistake_record",
                    "data": mistake_data
                },
                "tags": [
                    "#mistake_record",
                    f"#kp_{mistake_data['knowledge_point']}",
                    f"#mistake_type_{mistake_data['type']}",
                    f"#user_{user_id}"
                ]
            }],
            user_id=user_id
        )
        log_info(f"Saved mistake: {mistake_data['knowledge_point']}")
    except Exception as e:
        log_warning(f"Failed to save mistake {mistake_data['knowledge_point']}: {e}")
        # 降级：不影响主流程，仅不保存
```

### 函数3: generate_personalized_reminders

基于用户历史错误生成个性化提醒。

```python
def generate_personalized_reminders(user_id, current_kp):
    """生成个性化提醒

    Args:
        user_id: 用户ID
        current_kp: 当前知识点

    Returns:
        list: 个性化提醒列表
    """
    try:
        # 从MemOS读取该知识点的错误历史
        mistake_history = search_memory(
            query=f"#mistake_record #user_{user_id} #kp_{current_kp}",
            top_k=50
        )

        if not mistake_history:
            return []

        # 分析错误模式
        error_patterns = aggregate_error_patterns(mistake_history)

        reminders = []
        for pattern in error_patterns:
            if pattern["frequency"] >= 3:  # 重复犯错
                reminders.append(
                    f"⚠️ 你在 {pattern['type']} 方面已出错 {pattern['frequency']} 次，"
                    f"特别注意 {pattern['trigger']}"
                )

        return reminders
    except Exception as e:
        log_warning(f"Failed to generate reminders: {e}")
        return []
```

### 函数4: check_context_freshness_math

检查用户画像是否需要刷新。

```python
def check_context_freshness_math(user_context, current_date):
    """检查数学学习画像是否需要刷新

    Args:
        user_context: 用户上下文
        current_date: 当前日期

    Returns:
        dict: 包含needs_refresh, reason, questions等信息
        None: 不需要刷新
    """
    profile = user_context.get("user_profile")
    if not profile:
        return None

    updated_at = profile.get("updated_at")
    days_since_update = (current_date - updated_at).days

    # 超过30天自动触发刷新询问
    if days_since_update > 30:
        return {
            "needs_refresh": True,
            "reason": f"画像已{days_since_update}天未更新",
            "questions": [
                "你的数学水平有变化吗？(基础/中级/高级)",
                f"考试类型需要调整吗？(当前: {profile.get('exam_type', '数一')})",
                f"考试日期需要更新吗？(当前: {profile.get('exam_date', '未设置')})",
                "重点模块需要调整吗？(高数/线代/概率)"
            ]
        }

    return {"needs_refresh": False}
```

### 主流程整合

```python
def process_math_learning_v3(user_input):
    """数学学习主流程（含MemOS集成）

    Args:
        user_input: 用户输入

    Returns:
        dict: 处理结果
    """
    # 1. MemOS: 读取用户上下文 (可降级)
    user_context = safe_load_context(user_input)

    # 1.5 检查画像新鲜度
    profile_refresh = check_context_freshness_math(
        user_context, datetime.now()
    )
    if profile_refresh and profile_refresh.get("needs_refresh"):
        return generate_profile_refresh_question(profile_refresh)

    # 2. 处理用户请求（生成笔记/更新笔记）
    result = process_math_request(user_input, user_context)

    # 3. MemOS: 保存结果 (可降级)
    if result.get("mistake_records"):
        for mistake in result["mistake_records"]:
            save_mistake_to_memory(mistake, user_input.get("user_id"))

    return result


def safe_load_context(user_input):
    """安全加载用户上下文（含降级）"""
    context = load_user_context_from_memory(user_input)
    if context is None:
        log_info("MemOS unavailable, using default context")
        return create_default_user_context()
    return context
```

---

## 知识点联动主动性增强 (v3.0.0新增)

### 知识点关系图数据结构

```python
# 知识点关系图
KNOWLEDGE_GRAPH = {
    "洛必达法则": {
        "prerequisites": ["极限定义", "导数定义"],
        "combinations": ["等价无穷小", "泰勒公式"],
        "applications": ["定积分应用", "变限积分求导"],
        "cross_chapter_prompts": [
            "注意：当遇到变限积分求导时，通常会结合洛必达法则考查",
            "建议：同时复习 [[定积分应用]] 中的变限积分部分",
            "关联：洛必达法则常与泰勒公式结合考查极限问题"
        ]
    },
    "泰勒公式": {
        "prerequisites": ["导数定义", "高阶导数"],
        "combinations": ["洛必达法则", "等价无穷小"],
        "applications": ["级数展开", "近似计算"],
        "cross_chapter_prompts": [
            "注意：泰勒公式在处理复杂函数极限时比洛必达法则更简洁",
            "建议：掌握常见函数的泰勒展开式（sin x, cos x, e^x, ln(1+x)）",
            "关联：泰勒公式是级数展开的基础，参考 [[幂级数]]"
        ]
    },
    "变限积分求导": {
        "prerequisites": ["定积分定义", "导数定义"],
        "combinations": ["洛必达法则", "复合函数求导"],
        "applications": ["积分方程", "微分方程"],
        "cross_chapter_prompts": [
            "注意：变限积分求导常与洛必达法则结合考查极限",
            "建议：熟练掌握牛顿-莱布尼茨公式和链式法则",
            "关联：遇到积分方程时，常需先求导转化为微分方程"
        ]
    }
}
```

### 主动关联算法

```python
def generate_proactive_links(knowledge_point, user_mistakes=None):
    """生成主动关联提示

    Args:
        knowledge_point: 当前知识点
        user_mistakes: 用户历史错误（可选）

    Returns:
        dict: 关联提示结构
    """
    graph = KNOWLEDGE_GRAPH.get(knowledge_point, {})

    links = {
        "prerequisites": graph.get("prerequisites", []),
        "combinations": graph.get("combinations", []),
        "cross_chapter_prompts": graph.get("cross_chapter_prompts", []),
        "personalized": []
    }

    # 个性化提示（基于用户历史错误）
    if user_mistakes:
        for mistake in user_mistakes:
            if mistake["type"] == "条件遗漏":
                links["personalized"].append(
                    f"💡 你经常遗漏{mistake['condition']}条件，"
                    f"复习时重点看 [[{knowledge_point}]] 的定理条件部分"
                )

    return links
```

---

## 考研数学三大模块（知识点参考）

### 高等数学 (微积分)
```
高等数学核心知识点:
├── 极限与连续
│   ├── 极限计算 (洛必达法则、泰勒公式、等价无穷小)
│   ├── 函数连续性与间断点
│   └── 数列极限与级数初步
│
├── 一元函数微分学
│   ├── 导数定义与计算
│   ├── 导数应用 (单调性、极值、凹凸性、渐近线)
│   ├── 微分中值定理 (罗尔、拉格朗日、柯西)
│   └── 洛必达法则应用
│
├── 一元函数积分学
│   ├── 不定积分 (换元法、分部积分法)
│   ├── 定积分 (牛顿-莱布尼茨公式)
│   ├── 反常积分 (无穷区间、无界函数)
│   └── 定积分应用 (面积、体积、弧长、旋转体)
│
├── 多元函数微积分
│   ├── 多元函数极限与连续
│   ├── 偏导数与全微分
│   ├── 多元函数极值与最值
│   ├── 重积分 (二重、三重)
│   ├── 曲线积分与曲面积分
│   └── 格林公式、高斯公式、斯托克斯公式
│
├── 微分方程
│   ├── 一阶微分方程 (可分离变量、齐次、线性)
│   ├── 可降阶的高阶方程
│   └── 二阶常系数线性微分方程
│
└── 无穷级数
    ├── 数项级数 (正项级数、交错级数)
    ├── 幂级数 (收敛域、展开式)
    └── 傅里叶级数
```

### 线性代数
```
线性代数核心知识点:
├── 行列式
│   ├── 行列式定义与性质
│   ├── 行列式计算 (展开、三角化)
│   └── 克莱姆法则
│
├── 矩阵
│   ├── 矩阵运算 (加、减、乘、转置)
│   ├── 逆矩阵与伴随矩阵
│   ├── 矩阵的秩与等价标准形
│   └── 分块矩阵
│
├── 向量
│   ├── 向量运算与线性组合
│   ├── 线性相关与线性无关
│   ├── 极大线性无关组与秩
│   └── 向量空间与基
│
├── 线性方程组
│   ├── 克莱姆法则
│   ├── 矩阵法求解 (初等行变换)
│   └── 解的结构 (基础解系、通解)
│
├── 特征值与特征向量
│   ├── 特征值特征向量的定义与计算
│   ├── 特征值的性质 (迹、行列式)
│   └── 矩阵对角化
│
└── 二次型
    ├── 二次型的矩阵表示
    ├── 化为标准形 (配方法、正交变换)
    └── 正定二次型判定
```

### 概率论与数理统计
```
概率论与数理统计核心知识点:
├── 概率基础
│   ├── 样本空间与事件
│   ├── 古典概型与几何概型
│   ├── 条件概率与独立性
│   └── 全概率公式与贝叶斯公式
│
├── 随机变量
│   ├── 离散型随机变量 (分布律)
│   ├── 连续型随机变量 (密度函数)
│   ├── 分布函数
│   └── 随机变量函数的分布
│
├── 常用分布
│   ├── 离散型: 0-1分布、二项分布、泊松分布、几何分布
│   └── 连续型: 均匀分布、指数分布、正态分布
│
├── 多维随机变量
│   ├── 联合分布
│   ├── 边缘分布与条件分布
│   ├── 随机变量的独立性
│   └── 随机变量函数的分布 (和、差、积、商、最大最小)
│
├── 数字特征
│   ├── 数学期望
│   ├── 方差与标准差
│   ├── 协方差与相关系数
│   └── 矩
│
├── 大数定律与中心极限定理
│   ├── 切比雪夫不等式
│   ├── 大数定律 (辛钦、伯努利)
│   └── 中心极限定理 (棣莫弗-拉普拉斯、列维-林德伯格)
│
└── 数理统计
    ├── 统计量 (样本均值、样本方差)
    ├── 三大抽样分布 (χ²分布、t分布、F分布)
    ├── 点估计 (矩估计、最大似然估计)
    └── 区间估计
```

---

## MemOS数据模型 (v3.0.0新增)

### 用户画像 (User Profile)

```yaml
user_profile:
  user_id: string
  conversation_id: string
  created_at: datetime
  updated_at: datetime

  profile:
    exam_date: date
    exam_type: enum (math_1 | math_2 | math_3)
    current_level: enum (basic | intermediate | advanced)

  mistake_base:
    total_mistakes: int
    condition_mistakes: int
    method_mistakes: int
    calculation_mistakes: int

  preferences:
    focus_modules: array  # [高数, 线代, 概率]
    learning_style: enum (theory_first | practice_first | balanced)

  refresh_config:
    last_refreshed: date
    auto_refresh_interval: int
```

### 错误记录 (Mistake Record)

```yaml
mistake_record:
  record_id: string
  user_id: string
  knowledge_point: string
  date: date
  created_at: datetime

  mistake_info:
    mistake_type: enum (condition_omission | method_error | calculation_error | logic_jump)
    original_understanding: string
    correction: string
    trigger: string

  context:
    question_type: string
    related_theorems: array
```

### 知识点卡片 (Knowledge Card)

```yaml
knowledge_card:
  card_id: string
  user_id: string
  knowledge_point: string
  module: enum (高数 | 线代 | 概率)
  mastery_level: enum (unfamiliar | learning | familiar | mastered)
  mistake_count: int

  review_data:
    last_reviewed: date
    next_review: date
    review_count: int
```

---

## MemOS标签系统 (v3.0.0新增)

| 标签 | 用途 | 唯一性 |
|------|------|--------|
| `#user_profile` | 用户画像 | 每用户1条 |
| `#mistake_record` | 错误历史 | 多条 |
| `#knowledge_card` | 知识点卡片 | 每知识点每用户1条 |
| `#kp_{knowledge_point}` | 知识点索引 | 多条 |
| `#mistake_type_{type}` | 错误类型索引 | 多条 |

---

## 输出格式

### 文件输出
- 使用 obsidian-markdown 技能生成 Obsidian 笔记
- 格式：Obsidian Flavored Markdown (wikilinks, callouts, properties)
- 按知识点分文件

### 会话输出
- 生成预览
- 标注修改位置
- 提供文件路径

---

## 实例演示

### 演示1：初始笔记生成

**用户输入**：
```
这是我的极限笔记：
函数f(x)在x₀处的极限是A，当x趋近于x₀时，f(x)无限接近A。
洛必达法则：lim f(x)/g(x) = lim f'(x)/g'(x)，当f(x)和g(x)都趋向0或无穷大时。

帮我生成考研数一的极限学习笔记。
```

**AI 处理**：
1. 解析笔记内容，识别"极限定义"和"洛必达法则"两个知识点
2. 按知识点点分文件生成笔记
3. 补充考研导向内容

**生成文件**：
```
考研数学笔记/
├── 📑 索引.md
├── 📊 学习进度.md
└── 高数-极限/
    ├── 极限定义.md
    └── 洛必达法则.md
```

**AI 输出**：
```
已生成考研数一极限学习笔记，共2个知识点文件：

📁 文件位置：考研数学笔记/高数-极限/
  1. 极限定义.md
  2. 洛必达法则.md

预览：
# 洛必达法则

## 原始定义
洛必达法则：lim f(x)/g(x) = lim f'(x)/g'(x)，当f(x)和g(x)都趋向0或无穷大时。

## 直观理解 💡
洛必达法则的本质是比较两个函数"变化速度"的快慢。当两个函数都趋向0或∞时，通过比较它们的导数（变化率）来确定原函数的比值趋向。

**类比**：就像赛跑，如果两个选手都同时冲过终点线（都趋向0），通过比较他们的加速度（导数）来判断谁更快。

## 定理条件 ⚠️
⚠️ 使用洛必达法则必须满足以下条件：
1. lim f(x) = lim g(x) = 0 或 ∞（必须是0/0或∞/∞型）
2. f(x)和g(x)在某去心邻域内可导，且g'(x)≠0
3. lim f'(x)/g'(x) 存在或为∞

⚠️ 常见错误：忽略条件1，直接对非0/0型使用

## 考试重点 ⭐
⭐⭐⭐⭐⭐ 高频考点，几乎每年必考

**常考题型**：
1. 直接使用洛必达法则求极限
2. 需要多次应用洛必达法则
3. 结合泰勒公式的极限计算
4. 识别陷阱题（不满足洛必达条件）

## 典型题型
1. 基本应用：0/0或∞/∞型极限
2. 连续应用：需要多次求导
3. 结合其他方法：等价无穷小+洛必达
4. 识别不适用：导数极限不存在的情况

## 解题方法
**步骤**：
1. 识别极限类型（0/0、∞/∞等）
2. 验证洛必达法则条件
3. 对分子分母分别求导
4. 判断是否继续应用
5. 求出最终极限

**技巧**：
- 优先考虑等价无穷小简化
- 注意结合泰勒公式处理复杂函数
- 使用洛必达前先检查是否可化简

## 易错点 ⚠️
⚠️ 易错点1：对非0/0、∞/∞型使用洛必达
   - 错误：lim(x→∞) (x+1)/x 使用洛必达
   - 正确：直接计算 = 1

⚠️ 易错点2：导数极限不存在就认为原极限不存在
   - 错误：lim f/g 的导数极限不存在就放弃
   - 正确：导数极限不存在时，洛必达失效，需要其他方法

⚠️ 易错点3：忘记验证g'(x)≠0

## 例题

> [!example] 例1：基本应用
> **题目**：求 lim(x→0) (eˣ - 1 - x) / x²
>
> **分析**：x→0时，eˣ-1-x→0，x²→0，是0/0型，满足洛必达条件
>
> **解答**：
> 原式 = lim(x→0) [eˣ - 1] / (2x)  (第一次洛必达，仍是0/0)
>      = lim(x→0) [eˣ] / 2  (第二次洛必达)
>      = 1/2
>
> **评注**：本题考查洛必达法则的连续应用和最后极限的确定

> [!example] 例2：结合等价无穷小
> **题目**：求 lim(x→0) (1-cosx) / x²
>
> **分析**：是0/0型，可以先用等价无穷小简化
>
> **解答**：
> 方法1 - 直接洛必达：
> = lim(x→0) [sinx] / (2x)
> = lim(x→0) [cosx] / 2
> = 1/2
>
> 方法2 - 等价无穷小：
> 1-cosx ~ x²/2 (x→0)
> 原式 = lim(x→0) (x²/2) / x² = 1/2
>
> **评注**：等价无穷小可以简化计算，是重要的解题技巧

## 相关知识点
- [[极限定义]]
- [[等价无穷小]]
- [[泰勒公式]]
```

### 演示2：笔记更新

**用户输入**：
```
我在学习洛必达法则笔记时，对"直观理解"部分不太理解。
"变化速度"这个概念还是有点抽象，能不能用更直观的例子？
而且我对条件2不太明白，为什么要求g'(x)≠0？
```

**AI 处理**：
1. 定位到"洛必达法则.md"文件
2. 分析反馈：需要更直观的例子 + 解释条件2
3. 在"直观理解"和"定理条件"部分更新内容
4. 添加更新标记

**更新后的笔记片段**：
```markdown
## 直观理解 💡
洛必达法则的本质是比较两个函数"变化速度"的快慢。当两个函数都趋向0或∞时，通过比较它们的导数（变化率）来确定原函数的比值趋向。

**类比**：就像赛跑，如果两个选手都同时冲过终点线（都趋向0），通过比较他们的加速度（导数）来判断谁更快。

<!-- UPDATE: 2025-XX-XX 用户反馈需要更直观的例子 -->
**更直观的例子**：

想象两个队伍的人数都在变化：
- 甲队：第一天100人，第二天110人，第三天121人（每天增加10%）
- 乙队：第一天100人，第二天108人，第三天116.64人（每天增加8%）

两天后两队人数相同（从100开始），但增长率（导数）不同，甲队增长更快。

这就像求极限时，两个函数同时趋向0，但趋向的"速度"不同，洛必达法则就是比较这个"速度"。

**几何理解**：
函数的导数是切线的斜率，表示变化率。洛必达法则就是说：当x趋近x₀时，f(x)/g(x)的比值由它们在该点的变化率之比决定。
<!-- END UPDATE -->

## 定理条件 ⚠️
⚠️ 使用洛必达法则必须满足以下条件：
1. lim f(x) = lim g(x) = 0 或 ∞（必须是0/0或∞/∞型）
2. f(x)和g(x)在某去心邻域内可导，且g'(x)≠0
3. lim f'(x)/g'(x) 存在或为∞

<!-- UPDATE: 2025-XX-XX 用户反馈不理解条件2 -->
**为什么要求g'(x)≠0？**

从数学公式看：
洛必达法则计算的是 f'(x)/g'(x)，如果g'(x)=0x，则这个分数无法计算。

从实际意义看：
g'(x)=0意味着函数g(x)在该点的变化率为0，即g(x)在该点附近是"平的"（常数）。如果g(x)的变化率为0而f(x)的变化率不为0，那么f(x)/g(x)会趋向无穷大（或不存在），这种情况洛必达法则不适用。

**例子**：
求 lim(x→0) x / sin(x³)

这里g'(x) = 3x²cos(x³)，当x→0时，g'(x)→0，洛必达法则失效。
需要直接用等价无穷小：x ~ x，sin(x³) ~ x³，所以原式 = lim x/x³ = lim 1/x² = ∞
<!-- END UPDATE -->

⚠️ 常见错误：忽略条件1，直接对非0/0型使用
```

---

## 验证标准

### 基础功能验证 (v2.0.0)
1. 能正确解析用户现成笔记
2. 能识别知识点结构并按知识点分文件
3. 生成的笔记包含 Obsidian 格式（properties、tags、callouts、wikilinks）
4. 生成的笔记包含考研导向内容（考试重点、题型、易错点）
5. 能根据用户反馈定位对应的知识点文件
6. 能正确更新笔记文件并添加更新标记
7. 索引文件能正确链接所有知识点
8. 学习进度 dashboard 能显示状态
9. 触发条件准确（不会误触发）
10. 生成的笔记包含"我的理解记录 🧠"部分，记录用户的学习轨迹
11. 生成的笔记包含"我的错误类型 📌"部分，标注个性化错误模式
12. AI能根据用户反馈正确更新思维过程记录字段
13. 用户可以基于这些记录进行自我反思和改进

### LaTeX格式验证 (v3.0.0新增)
14. 所有数学公式使用LaTeX格式（`$...$`或`$$...$$`）
15. 内联公式使用单个美元符号，独立公式行使用双美元符号
16. 特殊符号正确转换为LaTeX代码（如`\alpha`, `\infty`, `\int`）
17. 验证LaTeX语法正确性，确保在Obsidian中正确渲染
18. 提供公式预览确认渲染效果

### 主动关联验证 (v3.0.0新增)
19. 生成笔记时包含"前置知识"、"常考组合"、"跨章节应用"部分
20. 提供跨章节关联提醒（如洛必达法则与变限积分求导）
21. 关联提醒包含具体知识点链接和复习建议
22. 关联内容基于知识图谱数据结构

### MemOS集成验证 (v3.0.0新增)
23. 记录错误时能正确保存到MemOS（带标签）
24. 基于历史错误生成个性化提醒
25. 用户画像能正确保存和更新
26. 知识点卡片能追踪掌握程度
27. 超过30天未更新时提示刷新画像
28. MemOS不可用时优雅降级为v2.0.0模式
29. 向后兼容：v2.0.0笔记无需修改即可使用

---

## 限制条件

- 需要用户提供现成笔记或文件路径
- 需要明确模块信息（高数/线代/概率）
- 笔记更新需要提供之前的笔记文件路径
- 触发条件明确要求"考研"上下文

---

## 技能调用提示

### 生成笔记时：
1. 首先确认用户是否提供了现成笔记
2. 识别模块信息（高数/线代/概率）
3. 确认考试类型（数一/数二/数三）
4. 解析笔记内容，识别知识点
5. 按知识点点生成文件
6. 创建索引和学习进度文件

### 更新笔记时：
1. 确认有之前生成的笔记文件
2. 定位用户反馈对应的知识点
3. 分析理解障碍类型
4. 生成补充内容
5. 更新文件并添加标记
