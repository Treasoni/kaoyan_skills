# LaTeX电子电路符号指南

> 822电子技术基础专用LaTeX符号速查表

---

## 康华光教材专用符号

> ⚠️ 以下符号遵循康华光《电子技术基础》第7版

### 静态工作点符号

| 符号 | 含义 | LaTeX |
|------|------|-------|
| $I_{BQ}$ | 基极静态电流 | `I_{BQ}` |
| $I_{CQ}$ | 集电极静态电流 | `I_{CQ}` |
| $U_{CEQ}$ | 集射极静态电压 | `U_{CEQ}` |
| $U_{BEQ}$ | 基射极静态电压 | `U_{BEQ}` |

### 动态参数符号

| 符号 | 含义 | LaTeX |
|------|------|-------|
| $r_{be}$ | BJT输入电阻（注意：不是$h_{ie}$） | `r_{be}` |
| $r_{ce}$ | BJT输出电阻 | `r_{ce}` |
| $g_m$ | 场效应管跨导 | `g_m` |

### FET参数符号

| 符号 | 含义 | LaTeX |
|------|------|-------|
| $U_{GS(off)}$ | 夹断电压（结型FET） | `U_{GS(off)}` |
| $U_{GS(th)}$ | 开启电压（MOSFET） | `U_{GS(th)}` |
| $I_{DSS}$ | 饱和漏极电流 | `I_{DSS}` |

### 与其他教材的区别

| 康华光 | 其他教材 | 说明 |
|--------|----------|------|
| $r_{be}$ | $h_{ie}$ | BJT输入电阻 |
| $U_{GS(off)}$ | $U_P$ | 夹断电压 |
| $U_{GS(th)}$ | $U_T$ | 开启电压 |

⚠️ **使用注意**: 所有静态参数必须使用Q下标，动态参数使用小写字母。

---

## 基本器件符号

### 无源器件

| 器件 | 符号 | 单位 | LaTeX示例 |
|------|------|------|-----------|
| 电阻 | $R$ | 欧姆($\Omega$) | `$R = 10k\Omega$` |
| 电容 | $C$ | 法拉(F) | `$C = 100\mu F$` |
| 电感 | $L$ | 亨利(H) | `$L = 10mH$` |
| 电导 | $G$ | 西门子(S) | `$G = 1/R$` |

### 有源器件

| 器件 | 符号 | 说明 | LaTeX示例 |
|------|------|------|-----------|
| 二极管 | $D$ | - | `$D_1, D_2$` |
| 稳压管 | $D_Z$ | - | `$D_{Z1}$` |
| 三极管 | $T$ 或 $Q$ | BJT | `$T_1, Q_1$` |
| 场效应管 | $T$ 或 $FET$ | MOSFET/JFET | `$T_1, FET_1$` |
| 运算放大器 | $A$ 或 $OP$ | Op-Amp | `$A_1, OP_1$` |

---

## 模电常用公式

### 基本放大电路

#### 静态工作点（BJT）

```latex
$$
I_B = \frac{V_{CC} - U_{BE}}{R_b}
$$

$$
I_C = \beta I_B
$$

$$
U_{CE} = V_{CC} - I_C R_c
$$
```

#### 静态工作点（FET）

```latex
$$
I_D = I_{DSS} \left(1 - \frac{U_{GS}}{U_{GS(off)}}\right)^2
$$

$$
U_{GS} = U_G - U_S
$$

$$
U_{DS} = V_{DD} - I_D R_d
$$
```

#### 动态指标

```latex
$$
A_u = \frac{U_o}{U_i} = -\frac{\beta R'_L}{r_{be}}
$$

$$
R_i = R_b // r_{be}
$$

$$
R_o = R_c
$$

$$
r_{be} = r_{bb'} + (1+\beta)\frac{26(mV)}{I_E(mA)}
$$
```

### 差分放大电路

```latex
$$
A_{ud} = -\frac{\beta R'_L}{2r_{be}}
$$

$$
A_{uc} = -\frac{\beta R'_L}{R_e + 2r_{be}}
$$

$$
K_{CMRR} = \left| \frac{A_{ud}}{A_{uc}} \right|
$$

$$
U_o = A_{ud}U_{id} + A_{uc}U_{ic}
$$
```

### 负反馈放大器

```latex
$$
A_f = \frac{A}{1 + AF}
$$

$$
F = 1 + AF \quad (\text{反馈深度})
$$

$$
A_{uf} \approx \frac{1}{F} \quad (\text{深度负反馈})
$$
```

### 运算电路

```latex
$$
U_o = -\frac{R_f}{R_1}U_i \quad (\text{反相比例})
$$

$$
U_o = \left(1 + \frac{R_f}{R_1}\right)U_i \quad (\text{同相比例})
$$

$$
U_o = -\left(\frac{R_f}{R_1}U_{i1} + \frac{R_f}{R_2}U_{i2}\right) \quad (\text{反相加法})
$$

$$
U_o = \frac{R_f}{R_1}(U_{i2} - U_{i1}) \quad (\text{减法})
$$
```

### 功率放大器

```latex
$$
P_{om} = \frac{V_{CC}^2}{2R_L} \quad (\text{OCL})
$$

$$
\eta = \frac{P_o}{P_V} \times 100\%
$$

$$
P_V = \frac{2V_{CC}^2}{\pi R_L} \quad (\text{乙类})
$$
```

### 波形产生电路

```latex
$$
f = \frac{1}{2\pi RC} \quad (\text{RC桥式振荡})
$$

$$
f = \frac{1}{2\pi\sqrt{LC}} \quad (\text{LC振荡})
$$

$$
|AF| \geq 1 \quad (\text{起振条件})
$$
```

### 稳压电源

```latex
$$
U_o = U_Z + U_{BE} \quad (\text{串联型})
$$

$$
S_r = \left.\frac{\Delta U_o/\Delta U_i}{U_o/U_i}\right|_{\Delta I_L=0}
$$

$$
R_o = \left.\frac{\Delta U_o}{\Delta I_L}\right|_{\Delta U_i=0}
$$
```

---

## 数电常用公式

### 逻辑运算

```latex
$$
Y = A \cdot B + C \cdot D
$$

$$
Y = \overline{A \cdot B} \quad (\text{与非})
$$

$$
Y = \overline{A + B} \quad (\text{或非})
$$
```

### 卡诺图化简

```latex
$$
ABC + AB\overline{C} = AB(C + \overline{C}) = AB
$$

$$
A + \overline{A}B = A + B
$$

$$
A + AB = A
$$

$$
A + \overline{A} = 1
$$
```

### 触发器特性方程

```latex
$$
Q^{n+1} = JQ^n + \overline{K}Q^n \quad (\text{JK触发器})
$$

$$
Q^{n+1} = D \quad (\text{D触发器})
$$

$$
Q^{n+1} = T\overline{Q^n} + \overline{T}Q^n \quad (\text{T触发器})
$$

$$
Q^{n+1} = \overline{Q^n} \quad (\text{T'触发器})
$$
```

### 计数器

```latex
$$
N = 2^n \quad (\text{n位二进制计数器模})
$$

$$
f_{out} = \frac{f_{in}}{N} \quad (\text{分频器})
$$
```

### ADC/DAC

```latex
$$
U_o = -\frac{U_{REF}}{2^n} \sum_{i=0}^{n-1} D_i 2^i \quad (\text{DAC})
$$

$$
Resolution = \frac{U_{REF}}{2^n} \quad (\text{分辨率})
$$

$$
t_q = \frac{1}{f} \quad (\text{量化周期})
$$
```

---

## 希腊字母表

| 大写 | 小写 | LaTeX | 用途 |
|------|------|-------|------|
| $\Alpha$ | $\alpha$ | `\Alpha` `\alpha` | 电流放大倍数 |
| $\Beta$ | $\beta$ | `\Beta` `\beta` | 电流放大倍数 |
| $\Delta$ | $\delta$ | `\Delta` `\delta` | 增量、变化量 |
| $\Eta$ | $\eta$ | `\Eta` `\eta` | 效率 |
| $\Theta$ | $\theta$ | `\Theta` `\theta` | 角度 |
| $\Lambda$ | $\lambda$ | `\Lambda` `\lambda` | 波长 |
| $\Mu$ | $\mu$ | `\Mu` `\mu` | 微($10^{-6}$) |
| $\Omega$ | $\omega$ | `\Omega` `\omega` | 欧姆、角频率 |
| $\Phi$ | $\phi$ | `\Phi` `\phi` | 磁通、相位 |
| $\Psi$ | $\psi$ | `\Psi` `\psi` | 磁链 |
| $\Tau$ | $\tau$ | `\Tau` `\tau` | 时间常数 |

---

## 常用数学符号

| 符号 | LaTeX | 说明 |
|------|-------|------|
| $\frac{a}{b}$ | `\frac{a}{b}` | 分数 |
| $\sqrt{x}$ | `\sqrt{x}` | 平方根 |
| $x^n$ | `x^n` | 指数 |
| $\sum$ | `\sum` | 求和 |
| $\prod$ | `\prod` | 连乘 |
| $\int$ | `\int` | 积分 |
| $\partial$ | `\partial` | 偏导数 |
| $\infty$ | `\infty` | 无穷大 |
| $\approx$ | `\approx` | 约等于 |
| $\propto$ | `\propto` | 正比于 |
| $\because$ | `\because` | 因为 |
| $\therefore$ | `\therefore` | 所以 |
| $\rightarrow$ | `\rightarrow` | 趋于、变换 |
| $\leftrightarrow$ | `\leftrightarrow` | 等价 |
| $\parallel$ | `\parallel` | 并联 |
| $\perp$ | `\perp` | 垂直 |

---

## 下标和上标

```latex
$$
I_{BQ} \quad \text{基极静态电流}
$$

$$
U_{CES} \quad \text{集电极饱和压降}
$$

$$
f_{H} \quad \text{上限截止频率}
$$

$$
A_{uL} \quad \text{低频电压增益}
$$

$$
Q^{n+1} \quad \text{次态}
$$
```

---

## 真值表格式

```markdown
| A | B | Y |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |
```

渲染效果：

| A | B | Y |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

---

## 卡诺图格式 ⭐

> ⚠️ **重要**: 所有卡诺图**必须**使用 Markdown 表格格式，**禁止**使用 ASCII 字符画

### 格式规范

1. **使用 Markdown 表格**：表头使用 LaTeX 公式标注变量值
2. **居中对齐**：所有列使用 `:---:` 居中
3. **LaTeX 符号**：最小项下标、反变量等使用 LaTeX（`$m_0$`, `$\bar{A}$`）
4. **行标签加粗**：左侧行标签使用 `**$A=0$**` 格式

### 一变量卡诺图

```markdown
| | $D=0$ | $D=1$ |
|:---:|:---:|:---:|
| | $m_0$<br>$\bar{D}$ | $m_1$<br>$D$ |
```

渲染效果：

| | $D=0$ | $D=1$ |
|:---:|:---:|:---:|
| | $m_0$<br>$\bar{D}$ | $m_1$<br>$D$ |

### 二变量卡诺图

```markdown
|  | $B=0$ | $B=1$ |
|:---:|:---:|:---:|
| **$A=0$** | $m_0$<br>$\bar{A}\bar{B}$ | $m_1$<br>$\bar{A}B$ |
| **$A=1$** | $m_2$<br>$A\bar{B}$ | $m_3$<br>$AB$ |
```

渲染效果：

|  | $B=0$ | $B=1$ |
|:---:|:---:|:---:|
| **$A=0$** | $m_0$<br>$\bar{A}\bar{B}$ | $m_1$<br>$\bar{A}B$ |
| **$A=1$** | $m_2$<br>$A\bar{B}$ | $m_3$<br>$AB$ |

### 三变量卡诺图

```markdown
|  | $BC=00$ | $BC=01$ | $BC=11$ | $BC=10$ |
|:---:|:---:|:---:|:---:|:---:|
| **$A=0$** | $m_0$ | $m_1$ | $m_3$ | $m_2$ |
| **$A=1$** | $m_4$ | $m_5$ | $m_7$ | $m_6$ |
```

渲染效果：

|  | $BC=00$ | $BC=01$ | $BC=11$ | $BC=10$ |
|:---:|:---:|:---:|:---:|:---:|
| **$A=0$** | $m_0$ | $m_1$ | $m_3$ | $m_2$ |
| **$A=1$** | $m_4$ | $m_5$ | $m_7$ | $m_6$ |

### 四变量卡诺图

```markdown
|  | $CD=00$ | $CD=01$ | $CD=11$ | $CD=10$ |
|:---:|:---:|:---:|:---:|:---:|
| **$AB=00$** | $m_0$ | $m_1$ | $m_3$ | $m_2$ |
| **$AB=01$** | $m_4$ | $m_5$ | $m_7$ | $m_6$ |
| **$AB=11$** | $m_{12}$ | $m_{13}$ | $m_{15}$ | $m_{14}$ |
| **$AB=10$** | $m_8$ | $m_9$ | $m_{11}$ | $m_{10}$ |
```

渲染效果：

|  | $CD=00$ | $CD=01$ | $CD=11$ | $CD=10$ |
|:---:|:---:|:---:|:---:|:---:|
| **$AB=00$** | $m_0$ | $m_1$ | $m_3$ | $m_2$ |
| **$AB=01$** | $m_4$ | $m_5$ | $m_7$ | $m_6$ |
| **$AB=11$** | $m_{12}$ | $m_{13}$ | $m_{15}$ | $m_{14}$ |
| **$AB=10$** | $m_8$ | $m_9$ | $m_{11}$ | $m_{10}$ |

### 填值卡诺图（用于化简题）

```markdown
|  | $BC=00$ | $BC=01$ | $BC=11$ | $BC=10$ |
|:---:|:---:|:---:|:---:|:---:|
| **$A=0$** | 1 | 0 | 1 | 1 |
| **$A=1$** | × | 0 | 1 | × |
```

渲染效果：

|  | $BC=00$ | $BC=01$ | $BC=11$ | $BC=10$ |
|:---:|:---:|:---:|:---:|:---:|
| **$A=0$** | 1 | 0 | 1 | 1 |
| **$A=1$** | × | 0 | 1 | × |

> **说明**：`×` 表示无关项（Don't Care），可以是1或0

### 格式要点

| 要点 | 说明 |
|------|------|
| 列编码 | 使用**格雷码**顺序：00, 01, 11, 10 |
| 下标 | 两位数下标用花括号：`$m_{12}$` 而非 `$m_12$` |
| 换行 | 单元格内换行用 `<br>`：`$m_0$<br>$\bar{A}\bar{B}$` |
| 对齐 | 全部使用居中对齐 `:---:` |
| 禁止 | ❌ 禁止使用 ASCII 字符画卡诺图 |

---

## 波特图格式

```latex
$$
20\lg|A_u| = 20\lg\frac{\omega_L}{\sqrt{\omega_L^2 + \omega^2}}
$$

$$
\varphi = \arctan\frac{\omega_L}{\omega}
$$
```

---

## 注意事项

1. **分数嵌套**: 多层分数使用 `\cfrac` 命令
2. **长公式**: 使用 `\begin{split}...\end{split}` 分行
3. **对齐**: 使用 `\begin{align}...\end{align}` 对齐多行公式
4. **单位**: 单位与数值之间用空格隔开，如 `$10 k\Omega$`
5. **下标**: 两个字符的下标用花括号，如 `$I_{BQ}$`

---

## Obsidian中的LaTeX

Obsidian原生支持LaTeX数学公式，使用以下格式：

- **行内公式**: `$公式$`
- **独立公式**: `$$公式$$`

示例：
```markdown
电压增益为 $A_u = -\frac{\beta R'_L}{r_{be}}$

静态工作点计算：
$$
I_B = \frac{V_{CC} - U_{BE}}{R_b}
$$
```
