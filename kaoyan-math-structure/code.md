# kaoyan-math-structure 代码模块

本文档包含 kaoyan-math-structure 技能的所有数据结构和代码实现。

---

## 1. 知识点关系图数据结构

### 1.1 极限模块关系图

```yaml
KNOWLEDGE_GRAPH:
  "洛必达法则":
    prerequisites: ["极限定义", "导数定义"]
    combinations: ["等价无穷小", "泰勒公式"]
    applications: ["定积分应用", "变限积分求导"]
    cross_chapter_prompts:
      - "注意：当遇到变限积分求导时，通常会结合洛必达法则考查"
      - "建议：同时复习 [[定积分应用]] 中的变限积分部分"
      - "关联：洛必达法则常与泰勒公式结合考查极限问题"

  "泰勒公式":
    prerequisites: ["导数定义", "高阶导数"]
    combinations: ["洛必达法则", "等价无穷小"]
    applications: ["级数展开", "近似计算"]
    cross_chapter_prompts:
      - "注意：泰勒公式在处理复杂函数极限时比洛必达法则更简洁"
      - "建议：掌握常见函数的泰勒展开式（sin x, cos x, e^x, ln(1+x)）"
      - "关联：泰勒公式是级数展开的基础，参考 [[幂级数]]"

  "变限积分求导":
    prerequisites: ["定积分定义", "导数定义"]
    combinations: ["洛必达法则", "复合函数求导"]
    applications: ["积分方程", "微分方程"]
    cross_chapter_prompts:
      - "注意：变限积分求导常与洛必达法则结合考查极限"
      - "建议：熟练掌握牛顿-莱布尼茨公式和链式法则"
      - "关联：遇到积分方程时，常需先求导转化为微分方程"
```

---

## 2. 目录结构模板

### 2.1 函数极限与连续模块目录结构

```yaml
MODULE_STRUCTURE:
  name: "函数极限与连续"
  path: "考研数学/高数-函数极限与连续/"
  submodules:
    - name: "函数的概念与特性"
      folder: "1-函数的概念与特性/"
      files:
        - "函数的定义.md"
        - "反函数.md"
        - "复合函数.md"
        - "隐函数.md"
      subfolder:
        name: "四种特性/"
        files:
          - "有界性.md"
          - "单调性.md"
          - "奇偶性.md"
          - "周期性.md"

    - name: "函数的图像"
      folder: "2-函数的图像/"
      files:
        - "基本初等函数.md"
        - "初等函数.md"
        - "分段函数.md"

    - name: "函数极限的概念与性质"
      folder: "3-函数极限的概念与性质/"
      files:
        - "邻域.md"
        - "极限定义.md"
        - "超实数.md"
        - "极限性质.md"
        - "无穷小定义.md"
        - "无穷小比阶.md"
        - "等价无穷小.md"
        - "无穷大.md"

    - name: "极限计算方法"
      folder: "4-极限计算方法/"
      files:
        - "四则运算.md"
        - "洛必达法则.md"
        - "泰勒公式.md"
        - "泰勒展开原则.md"
        - "无穷小运算.md"
        - "重要极限.md"
        - "夹逼准则.md"
        - "七种未定式.md"

    - name: "函数的连续与间断"
      folder: "5-函数的连续与间断/"
      files:
        - "连续性定义.md"
        - "间断点分类.md"
        - "闭区间性质.md"
```

---

## 3. 高等数学知识点树

```yaml
HIGHER_MATH_KNOWLEDGE_TREE:
  name: "高等数学"
  children:
    - name: "极限与连续"
      children:
        - name: "极限计算"
          keywords: ["洛必达法则", "泰勒公式", "等价无穷小"]
        - name: "函数连续性与间断点"
        - name: "数列极限与级数初步"

    - name: "一元函数微分学"
      children:
        - name: "导数定义与计算"
        - name: "导数应用"
          keywords: ["单调性", "极值", "凹凸性", "渐近线"]
        - name: "微分中值定理"
          keywords: ["罗尔", "拉格朗日", "柯西"]
        - name: "洛必达法则应用"

    - name: "一元函数积分学"
      children:
        - name: "不定积分"
          keywords: ["换元法", "分部积分法"]
        - name: "定积分"
          keywords: ["牛顿-莱布尼茨公式"]
        - name: "反常积分"
          keywords: ["无穷区间", "无界函数"]
        - name: "定积分应用"
          keywords: ["面积", "体积", "弧长", "旋转体"]

    - name: "多元函数微积分"
      children:
        - name: "多元函数极限与连续"
        - name: "偏导数与全微分"
        - name: "多元函数极值与最值"
        - name: "重积分"
          keywords: ["二重", "三重"]
        - name: "曲线积分与曲面积分"
        - name: "三大公式"
          keywords: ["格林", "高斯", "斯托克斯"]

    - name: "微分方程"
      children:
        - name: "一阶微分方程"
          keywords: ["可分离变量", "齐次", "线性"]
        - name: "可降阶的高阶方程"
        - name: "二阶常系数线性微分方程"

    - name: "无穷级数"
      children:
        - name: "数项级数"
          keywords: ["正项级数", "交错级数"]
        - name: "幂级数"
          keywords: ["收敛域", "展开式"]
        - name: "傅里叶级数"
```

---

## 4. 线性代数知识点树

```yaml
LINEAR_ALGEBRA_KNOWLEDGE_TREE:
  name: "线性代数"
  children:
    - name: "行列式"
      children:
        - name: "行列式定义与性质"
        - name: "行列式计算"
          keywords: ["展开", "三角化"]
        - name: "克莱姆法则"

    - name: "矩阵"
      children:
        - name: "矩阵运算"
          keywords: ["加", "减", "乘", "转置"]
        - name: "逆矩阵与伴随矩阵"
        - name: "矩阵的秩与等价标准形"
        - name: "分块矩阵"

    - name: "向量"
      children:
        - name: "向量运算与线性组合"
        - name: "线性相关与线性无关"
        - name: "极大线性无关组与秩"
        - name: "向量空间与基"

    - name: "线性方程组"
      children:
        - name: "克莱姆法则"
        - name: "矩阵法求解"
          keywords: ["初等行变换"]
        - name: "解的结构"
          keywords: ["基础解系", "通解"]

    - name: "特征值与特征向量"
      children:
        - name: "特征值特征向量的定义与计算"
        - name: "特征值的性质"
          keywords: ["迹", "行列式"]
        - name: "矩阵对角化"

    - name: "二次型"
      children:
        - name: "二次型的矩阵表示"
        - name: "化为标准形"
          keywords: ["配方法", "正交变换"]
        - name: "正定二次型判定"
```

---

## 5. 概率论与数理统计知识点树

```yaml
PROBABILITY_KNOWLEDGE_TREE:
  name: "概率论与数理统计"
  children:
    - name: "概率基础"
      children:
        - name: "样本空间与事件"
        - name: "古典概型与几何概型"
        - name: "条件概率与独立性"
        - name: "全概率公式与贝叶斯公式"

    - name: "随机变量"
      children:
        - name: "离散型随机变量"
          keywords: ["分布律"]
        - name: "连续型随机变量"
          keywords: ["密度函数"]
        - name: "分布函数"
        - name: "随机变量函数的分布"

    - name: "常用分布"
      children:
        - name: "离散型分布"
          keywords: ["0-1分布", "二项分布", "泊松分布", "几何分布"]
        - name: "连续型分布"
          keywords: ["均匀分布", "指数分布", "正态分布"]

    - name: "多维随机变量"
      children:
        - name: "联合分布"
        - name: "边缘分布与条件分布"
        - name: "随机变量的独立性"
        - name: "随机变量函数的分布"
          keywords: ["和", "差", "积", "商", "最大最小"]

    - name: "数字特征"
      children:
        - name: "数学期望"
        - name: "方差与标准差"
        - name: "协方差与相关系数"
        - name: "矩"

    - name: "大数定律与中心极限定理"
      children:
        - name: "切比雪夫不等式"
        - name: "大数定律"
          keywords: ["辛钦", "伯努利"]
        - name: "中心极限定理"
          keywords: ["棣莫弗-拉普拉斯", "列维-林德伯格"]

    - name: "数理统计"
      children:
        - name: "统计量"
          keywords: ["样本均值", "样本方差"]
        - name: "三大抽样分布"
          keywords: ["χ²分布", "t分布", "F分布"]
        - name: "点估计"
          keywords: ["矩估计", "最大似然估计"]
        - name: "区间估计"
```

---

## 6. 辅助函数

### 6.1 获取知识点结构

```python
def get_knowledge_structure(module_name, sub_module=None):
    """获取知识点结构

    Args:
        module_name: 模块名称（高数/线代/概率）
        sub_module: 子模块名称（可选）

    Returns:
        dict: 知识点结构
    """
    if module_name == "高数":
        tree = HIGHER_MATH_KNOWLEDGE_TREE
    elif module_name == "线代":
        tree = LINEAR_ALGEBRA_KNOWLEDGE_TREE
    elif module_name == "概率":
        tree = PROBABILITY_KNOWLEDGE_TREE
    else:
        return None

    if sub_module:
        # 查找子模块
        return find_submodule(tree, sub_module)

    return tree


def find_submodule(tree, name):
    """递归查找子模块"""
    if tree.get("name") == name:
        return tree

    for child in tree.get("children", []):
        result = find_submodule(child, name)
        if result:
            return result

    return None
```

### 6.2 获取知识点关联

```python
def get_knowledge_relations(knowledge_point):
    """获取知识点的关联信息

    Args:
        knowledge_point: 知识点名称

    Returns:
        dict: {
            "prerequisites": [...],
            "combinations": [...],
            "applications": [...],
            "cross_chapter_prompts": [...]
        }
    """
    return KNOWLEDGE_GRAPH.get(knowledge_point, {
        "prerequisites": [],
        "combinations": [],
        "applications": [],
        "cross_chapter_prompts": []
    })
```

### 6.3 生成目录结构

```python
def generate_directory_structure(module_name, output_path):
    """生成目录结构

    Args:
        module_name: 模块名称
        output_path: 输出路径

    Returns:
        list: 创建的目录列表
    """
    structure = MODULE_STRUCTURE.get(module_name)
    if not structure:
        return []

    created_dirs = []
    base_path = Path(output_path) / structure["path"]

    for submodule in structure["submodules"]:
        subdir = base_path / submodule["folder"]
        subdir.mkdir(parents=True, exist_ok=True)
        created_dirs.append(str(subdir))

        # 创建子文件夹
        if "subfolder" in submodule:
            subfolder = subdir / submodule["subfolder"]["name"]
            subfolder.mkdir(exist_ok=True)
            created_dirs.append(str(subfolder))

    return created_dirs
```

---

*创建日期: 2026-03-10*
*版本: 1.0.0*
