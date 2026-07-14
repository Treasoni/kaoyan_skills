---
name: kaoyan-math-structure
description: This skill provides knowledge point structure templates and module organization for 考研数学 (Chinese graduate entrance math exam). Use it when users want to query the directory structure of high math/linear algebra/probability, get knowledge point relationship graphs, or understand chapter organization.
version: 1.1.0
---

# 考研数学知识点结构

> 详细代码见 [code.md](code.md)，完整知识树见 [references/knowledge-trees.md](references/knowledge-trees.md)

## 技能概述

提供考研数学的知识点结构模板和模块组织：
1. 各模块的标准目录结构
2. 知识点之间的依赖和关联关系图
3. 考研数学三大模块的知识点参考

---

## 触发条件

**触发**：「数学知识点结构」「高数/线代/概率目录结构」「知识点关系图」「某章结构」

**不触发**：生成/更新笔记 → `kaoyan-math-notes`；配置/欠账 → `kaoyan-math-core`

---

## 目录结构优先级

1. 用户提供的图片结构（最高优先级）
2. 本文档定义的标准结构
3. 高数资料：`/Users/zhqznc/Documents/高数资料/`
4. AI 推断结构（最低优先级）

---

## 函数极限与连续模块结构

### 1-函数的概念与特性/

```
函数的概念与特性
├── 函数的定义.md          # y = f(x) 的定义、定义域、值域
├── 反函数.md              # y = f⁻¹(x)，水平画线法
├── 复合函数.md            # y = f[g(x)]，运算法则
├── 隐函数.md              # F(x,y) = 0
└── 四种特性/
    ├── 有界性.md          # |f(x)| ≤ M，重要结论
    ├── 单调性.md          # 增减性判断方法
    ├── 奇偶性.md          # f(-x) = ±f(x)，重要结论
    └── 周期性.md          # f(x+T) = f(x)，重要结论
```

### 2-函数的图像/

```
函数的图像
├── 基本初等函数.md        # 六类基本初等函数
├── 初等函数.md            # 定义与性质
└── 分段函数.md            # 绝对值、符号、取整函数
```

### 3-函数极限的概念与性质/

```
函数极限的概念与性质
├── 邻域.md                # δ邻域、去心邻域
├── 极限定义.md            # ε-δ 语言
├── 超实数.md              # 超实数在极限中的应用
├── 极限性质.md            # 唯一性、局部有界、保号性
├── 无穷小定义.md          # 定义与性质
├── 无穷小比阶.md          # 比阶方法
├── 等价无穷小.md          # ⭐ 常用等价无穷小（必记）
└── 无穷大.md              # 定义与关系
```

### 4-极限计算方法/（重中之重）

```
极限计算方法
├── 四则运算.md            # 极限四则运算法则
├── 洛必达法则.md          # ⭐⭐⭐⭐⭐ 重中之重
├── 泰勒公式.md            # ⭐⭐⭐⭐⭐ 重中之重
├── 泰勒展开原则.md        # 上下同阶、幂次最低
├── 无穷小运算.md          # 代换技巧
├── 重要极限.md            # sinx/x, (1+1/x)^x
├── 夹逼准则.md            # 使用条件与方法
└── 七种未定式.md          # 0/0, ∞/∞, 0·∞, ∞-∞, ∞⁰, 0⁰, 1^∞
```

### 5-函数的连续与间断/

```
函数的连续与间断
├── 连续性定义.md          # 左连续、右连续
├── 间断点分类.md          # 第一类、第二类间断点
└── 闭区间性质.md          # 有界性、最值、零点、介值定理
```

### 笔记存储路径

```
考研数学/
└── 高数-函数极限与连续/
    ├── 📑 索引.md
    ├── 📊 学习进度.md
    ├── 1-函数的概念与特性/
    ├── 2-函数的图像/
    ├── 3-函数极限的概念与性质/
    ├── 4-极限计算方法/
    └── 5-函数的连续与间断/
```

---

## 三大模块完整知识树

高等数学、线性代数、概率论与数理统计的完整知识点树形结构及知识点关系图，详见 [references/knowledge-trees.md](references/knowledge-trees.md)。

---

## 技能集成

| 技能 | 用途 |
|------|------|
| kaoyan-math-core | 知识点联动关系 |
| kaoyan-math-notes | 提供结构模板供笔记生成使用 |

---

*创建日期: 2026-03-10*
*版本: 1.1.0 (知识树→references/, 2026-07-12)*
