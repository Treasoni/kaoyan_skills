# 考研数学LaTeX快速参考指南

## 基础语法

### 内联公式
使用单个美元符号包裹：
```
设函数 $f(x)$ 在点 $x_0$ 处可导
```

### 独立公式行
使用双美元符号包裹：
```
$$
\lim_{x \to x_0} \frac{f(x) - f(x_0)}{x - x_0} = f'(x_0)
$$
```

---

## 常用符号

### 希腊字母
| 符号 | LaTeX | 符号 | LaTeX |
|------|-------|------|-------|
| $\alpha$ | `\alpha` | $\beta$ | `\beta` |
| $\gamma$ | `\gamma` | $\delta$ | `\delta` |
| $\epsilon$ | `\epsilon` | $\theta$ | `\theta` |
| $\lambda$ | `\lambda` | $\mu$ | `\mu` |
| $\pi$ | `\pi` | $\sigma$ | `\sigma` |
| $\phi$ | `\phi` | $\omega$ | `\omega` |
| $\Delta$ | `\Delta` | $\Sigma$ | `\Sigma` |
| $\Omega$ | `\Omega` | $\Phi$ | `\Phi` |

### 运算符号
| 符号 | LaTeX | 说明 |
|------|-------|------|
| $+$ | `+` | 加号 |
| $-$ | `-` | 减号 |
| $\times$ | `\times` | 乘号 |
| $\div$ | `\div` | 除号 |
| $\pm$ | `\pm` | 正负号 |
| $\cdot$ | `\cdot` | 点乘 |
| $\ast$ | `\ast` | 星号 |

### 关系符号
| 符号 | LaTeX | 说明 |
|------|-------|------|
| $=$ | `=` | 等于 |
| $\neq$ | `\neq` | 不等于 |
| $\approx$ | `\approx` | 约等于 |
| $<$ | `<` | 小于 |
| $>$ | `>` | 大于 |
| $\leq$ | `\leq` | 小于等于 |
| $\geq$ | `\geq` | 大于等于 |
| $\ll$ | `\ll` | 远小于 |
| $\gg$ | `\gg` | 远大于 |

### 集合符号
| 符号 | LaTeX | 说明 |
|------|-------|------|
| $\in$ | `\in` | 属于 |
| $\notin$ | `\notin` | 不属于 |
| $\subset$ | `\subset` | 子集 |
| $\subseteq$ | `\subseteq` | 子集或等于 |
| $\supset$ | `\supset` | 超集 |
| $\supseteq$ | `\supseteq` | 超集或等于 |
| $\cup$ | `\cup` | 并集 |
| $\cap$ | `\cap` | 交集 |
| $\emptyset$ | `\emptyset` | 空集 |
| $\mathbb{R}$ | `\mathbb{R}` | 实数集 |
| $\mathbb{N}$ | `\mathbb{N}` | 自然数集 |
| $\mathbb{Z}$ | `\mathbb{Z}` | 整数集 |
| $\mathbb{Q}$ | `\mathbb{Q}` | 有理数集 |
| $\mathbb{C}$ | `\mathbb{C}` | 复数集 |

### 逻辑符号
| 符号 | LaTeX | 说明 |
|------|-------|------|
| $\forall$ | `\forall` | 对所有 |
| $\exists$ | `\exists` | 存在 |
| $\Rightarrow$ | `\Rightarrow` | 推出 |
| $\Leftarrow$ | `\Leftarrow` | 由...推出 |
| $\Leftrightarrow$ | `\Leftrightarrow` | 当且仅当 |
| $\because$ | `\because` | 因为 |
| $\therefore$ | `\therefore` | 所以 |

### 箭头符号
| 符号 | LaTeX | 说明 |
|------|-------|------|
| $\to$ | `\to` | 趋向 |
| $\rightarrow$ | `\rightarrow` | 右箭头 |
| $\leftarrow$ | `\leftarrow` | 左箭头 |
| $\leftrightarrow$ | `\leftrightarrow` | 双箭头 |
| $\mapsto$ | `\mapsto` | 映射 |

---

## 微积分符号

### 极限与导数
| 符号 | LaTeX | 说明 |
|------|-------|------|
| $\lim$ | `\lim` | 极限 |
| $\lim_{x \to 0}$ | `\lim_{x \to 0}` | 极限（带条件） |
| $\lim_{x \to \infty}$ | `\lim_{x \to \infty}` | 无穷极限 |
| $f'(x)$ | `f'(x)` | 一阶导数 |
| $f''(x)$ | `f''(x)` | 二阶导数 |
| $f^{(n)}(x)$ | `f^{(n)}(x)` | n阶导数 |
| $\frac{dy}{dx}$ | `\frac{dy}{dx}` | 导数（分数形式） |
| $\frac{d^n y}{dx^n}$ | `\frac{d^n y}{dx^n}` | n阶导数（分数形式） |
| $\frac{\partial f}{\partial x}$ | `\frac{\partial f}{\partial x}` | 偏导数 |
| $\frac{\partial^2 f}{\partial x^2}$ | `\frac{\partial^2 f}{\partial x^2}` | 二阶偏导数 |
| $\nabla f$ | `\nabla f` | 梯度 |

### 积分
| 符号 | LaTeX | 说明 |
|------|-------|------|
| $\int$ | `\int` | 不定积分 |
| $\int_a^b$ | `\int_a^b` | 定积分 |
| $\int_a^\infty$ | `\int_a^\infty` | 反常积分 |
| $\oint$ | `\oint` | 闭曲线积分 |
| $\iint$ | `\iint` | 二重积分 |
| $\iiint$ | `\iiint` | 三重积分 |

### 积分示例
```
$$
\int_a^b f(x)dx = F(b) - F(a)
$$

$$
\iint_D f(x,y)dxdy = \int_\alpha^\beta d\theta \int_{r_1(\theta)}^{r_2(\theta)} f(r\cos\theta, r\sin\theta)rdr
$$
```

---

## 级数与求和

| 符号 | LaTeX | 说明 |
|------|-------|------|
| $\sum$ | `\sum` | 求和 |
| $\sum_{i=1}^n$ | `\sum_{i=1}^n` | 求和（带范围） |
| $\prod$ | `\prod` | 求积 |
| $\prod_{i=1}^n$ | `\prod_{i=1}^n` | 求积（带范围） |
| $\infty$ | `\infty` | 无穷大 |

### 级数示例
```
$$
\sum_{n=1}^{\infty} \frac{1}{n^2} = \frac{\pi^2}{6}
$$

$$
\prod_{i=1}^n i = n!
$$
```

---

## 矩阵与线性代数

### 矩阵符号
| 符号 | LaTeX | 说明 |
|------|-------|------|
| $A^{-1}$ | `A^{-1}` | 逆矩阵 |
| $A^T$ | `A^T` | 转置矩阵 |
| $|A|$ | `|A|` | 行列式 |
| $\det(A)$ | `\det(A)` | 行列式 |
| $\text{rank}(A)$ | `\text{rank}(A)` | 矩阵的秩 |
| $\text{tr}(A)$ | `\text{tr}(A)` | 矩阵的迹 |
| $\lambda$ | `\lambda` | 特征值 |

### 向量
| 符号 | LaTeX | 说明 |
|------|-------|------|
| $\vec{v}$ | `\vec{v}` | 向量 |
| $\|\vec{v}\|$ | `\|\vec{v}\|` | 向量的模 |
| $\vec{a} \cdot \vec{b}$ | `\vec{a} \cdot \vec{b}` | 向量点积 |
| $\vec{a} \times \vec{b}$ | `\vec{a} \times \vec{b}` | 向量叉积 |

---

## 概率统计

| 符号 | LaTeX | 说明 |
|------|-------|------|
| $P(A)$ | `P(A)` | 事件概率 |
| $P(A|B)$ | `P(A|B)` | 条件概率 |
| $E(X)$ | `E(X)` | 期望 |
| $D(X)$ | `D(X)` | 方差 |
| $\text{Var}(X)$ | `\text{Var}(X)` | 方差 |
| $\sigma$ | `\sigma` | 标准差 |
| $\rho$ | `\rho` | 相关系数 |
| $\sim$ | `\sim` | 服从分布 |

### 分布示例
```
设 $X \sim N(\mu, \sigma^2)$，则 $E(X) = \mu$，$D(X) = \sigma^2$
```

---

## 分数与根号

| 符号 | LaTeX | 说明 |
|------|-------|------|
| $\frac{a}{b}$ | `\frac{a}{b}` | 分数 |
| $\sqrt{x}$ | `\sqrt{x}` | 平方根 |
| $\sqrt[n]{x}$ | `\sqrt[n]{x}` | n次方根 |

### 复杂分数
```
$$
\frac{\partial^2 z}{\partial x \partial y} = \frac{\partial}{\partial x}\left(\frac{\partial z}{\partial y}\right)
$$
```

---

## 上下标

| 符号 | LaTeX | 说明 |
|------|-------|------|
| $x^n$ | `x^n` | 上标 |
| $x_n$ | `x_n` | 下标 |
| $x^{n+1}$ | `x^{n+1}` | 复杂上标（需要大括号） |
| $a_{ij}$ | `a_{ij}` | 双下标 |

### 极限示例
```
$$
\lim_{n \to \infty} \left(1 + \frac{1}{n}\right)^n = e
$$
```

---

## 括号

| 符号 | LaTeX | 说明 |
|------|-------|------|
| $( )$ | `( )` | 圆括号 |
| $[ ]$ | `[ ]` | 方括号 |
| $\{ \}$ | `\{ \}` | 花括号（需要转义） |
| $\langle \rangle$ | `\langle \rangle` | 角括号 |
| $| |$ | `| |` | 绝对值 |
| $\| \|$ | `\| \|` | 范数 |

### 自动调整大小的括号
使用 `\left` 和 `\right` 使括号大小自适应：
```
$$
\left(\frac{a}{b}\right), \quad \left[\frac{a}{b}\right], \quad \left\{\frac{a}{b}\right\}
$$

$$
\left| \int_a^b f(x)dx \right| \leq \int_a^b |f(x)|dx
$$
```

---

## 常用函数

| 函数 | LaTeX | 说明 |
|------|-------|------|
| $\sin x$ | `\sin x` | 正弦 |
| $\cos x$ | `\cos x` | 余弦 |
| $\tan x$ | `\tan x` | 正切 |
| $\cot x$ | `\cot x` | 余切 |
| $\arcsin x$ | `\arcsin x` | 反正弦 |
| $\arccos x$ | `\arccos x` | 反余弦 |
| $\arctan x$ | `\arctan x` | 反正切 |
| $\ln x$ | `\ln x` | 自然对数 |
| $\log x$ | `\log x` | 对数 |
| $\log_a x$ | `\log_a x` | 以a为底的对数 |
| $e^x$ | `e^x` | 指数函数 |
| $\exp(x)$ | `\exp(x)` | 指数函数 |

---

## 空格与间距

| 命令 | 效果 | 说明 |
|------|------|------|
| `\,` | 小空格 | $3\,dx$ |
| `\:` | 中等空格 | |
| `\;` | 大空格 | |
| `\quad` | 空格 | 相当于一个M宽度 |
| `\qquad` | 双空格 | 相当于两个M宽度 |

---

## 高级技巧

### 多行公式对齐
使用 `align` 环境（需要MathJax或KaTeX支持）：
```
$$
\begin{aligned}
\frac{d}{dx}[\sin(x)\cos(x)] &= \sin(x)(-\sin(x)) + \cos(x)\cos(x) \\
&= \cos^2(x) - \sin^2(x) \\
&= \cos(2x)
\end{aligned}
$$
```

### 矩阵表示
```
$$
A = \begin{pmatrix}
a_{11} & a_{12} \\
a_{21} & a_{22}
\end{pmatrix}
$$
```

### 方程组
```
$$
\begin{cases}
x + y = 1 \\
2x - y = 0
\end{cases}
$$
```

---

## 考研常用公式LaTeX示例

### 导数定义
```
$$
f'(x_0) = \lim_{\Delta x \to 0} \frac{f(x_0 + \Delta x) - f(x_0)}{\Delta x}
$$
```

### 洛必达法则
```
$$
\lim_{x \to x_0} \frac{f(x)}{g(x)} = \lim_{x \to x_0} \frac{f'(x)}{g'(x)}
$$
```

### 牛顿-莱布尼茨公式
```
$$
\int_a^b f(x)dx = F(b) - F(a)
$$
```

### 格林公式
```
$$
\oint_L Pdx + Qdy = \iint_D \left(\frac{\partial Q}{\partial x} - \frac{\partial P}{\partial y}\right)dxdy
$$
```

### 斯托克斯公式
```
$$
\oint_L \vec{A} \cdot d\vec{l} = \iint_S (\nabla \times \vec{A}) \cdot d\vec{S}
$$
