---
name: math-graph
description: 使用 Python + Matplotlib 生成教科书级别的数学函数图像。当用户想要画函数图、生成图像、可视化数学概念、替换 ASCII 字符图时使用此技能。支持任意函数表达式、多图对比、专业标注。
version: 1.0.0
---

# 数学函数绘图 (Math Graph)

## 技能概述

本技能使用 Python + Matplotlib 生成高质量、教科书风格的数学函数图像，用于替换模糊的 ASCII 字符图，让数学概念更加清晰直观。

## 触发条件

- 用户提到"画函数图"、"生成图像"、"绘图"、"graph"
- 用户想替换 ASCII 字符图
- 用户需要可视化数学概念（导数、极限、连续性等）
- 用户请求"绑图"、"画图"

## 核心功能

### 1. 按需生成（无预设模板）

支持任意 Python/math 语法函数表达式：
- 基本函数：`abs(x)`, `x**2`, `sin(x)`, `exp(x)`
- 分段函数：通过条件表达式
- 组合函数

### 2. 多图对比

支持并排展示多个函数，便于对比分析：
- 角点 vs 无穷导数
- 连续 vs 间断
- 可导 vs 不可导

### 3. 专业标注

- 特殊点标记（圆点、箭头）
- 坐标轴标注（$x$, $y$）
- 切线绘制
- 中文标题支持

## 使用方法

### 基本调用

```
/math-graph 画 y = |x| 的图像
/math-graph 对比 y = |x| 和 y = x^(1/3)
/math-graph 生成角点和无穷导数的对比图
```

### 脚本调用

```bash
# 单函数绘图
python .claude/skills/math-graph/scripts/plot_functions.py \
  --function "abs(x)" \
  --range "-2,2" \
  --output "考研数学/高数-一元微分学/.../assets/corner.png" \
  --title "角点"

# 多函数对比（并排）
python .claude/skills/math-graph/scripts/plot_functions.py \
  --compare \
  --functions "abs(x)" "np.cbrt(x)" \
  --titles "角点 (|x|)" "无穷导数 (x^{1/3})" \
  --output "assets/compare.png"
```

## 输出规范

- **格式**：PNG 图片（300 DPI）
- **存放位置**：当前笔记所在目录的 `assets/` 子文件夹
- **嵌入语法**：`![](assets/graph_name.png)`

## 图形美化规范

- seaborn 白色背景风格
- 蓝色主曲线，红色标注
- 坐标轴穿过原点
- 清晰的网格线
- 中文字体支持（SimHei / PingFang SC）

## 常用函数示例

| 概念 | 函数表达式 | 说明 |
|------|-----------|------|
| 角点 | `abs(x)` | $y = \|x\|$，左右导数不等 |
| 无穷导数 | `np.cbrt(x)` | $y = x^{1/3}$，垂直切线 |
| 尖点 | `np.sign(x) * np.abs(x)**(2/3)` | $y = x^{2/3} \cdot \text{sgn}(x)$ |
| 可去间断 | `(x**2 - 1) / (x - 1)` if x != 1 else None | $y = \frac{x^2-1}{x-1}$ |
| 跳跃间断 | `np.where(x < 0, -1, 1)` | 阶梯函数 |
| 渐近线 | `1/x` | $y = 1/x$ |

## 依赖

```bash
pip install matplotlib numpy seaborn
```

---

*创建日期: 2026-03-16*
*维护者: Claude Code + 用户协作*
