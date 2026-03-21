#!/usr/bin/env python3
"""
数学函数绘图脚本
生成教科书级别的数学函数图像

使用示例:
    # 单函数绘图
    python plot_functions.py --function "abs(x)" --range "-2,2" --output assets/corner.png --title "角点"

    # 多函数对比（并排）
    python plot_functions.py --compare --functions "abs(x)" "np.cbrt(x)" --titles "角点" "无穷导数" --output assets/compare.png

    # 带标注的图
    python plot_functions.py --function "abs(x)" --annotate "0,0:角点" --output assets/corner_annotated.png
"""

import argparse
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from typing import List, Tuple, Optional

# 设置中文字体支持
import matplotlib.font_manager as fm

# 尝试找到可用的中文字体
def get_chinese_font():
    """查找可用的中文字体"""
    chinese_fonts = ['PingFang SC', 'Heiti TC', 'STHeiti', 'Songti SC', 'Kailasa',
                     'Hiragino Sans GB', 'Microsoft YaHei', 'SimHei', 'WenQuanYi Micro Hei']

    available_fonts = [f.name for f in fm.fontManager.ttflist]

    for font in chinese_fonts:
        if font in available_fonts:
            return font

    # 如果没有找到中文字体，返回默认字体
    return None

chinese_font = get_chinese_font()
if chinese_font:
    matplotlib.rcParams['font.sans-serif'] = [chinese_font, 'DejaVu Sans', 'Arial']
    print(f"使用中文字体: {chinese_font}")
else:
    matplotlib.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
    print("未找到中文字体，使用默认字体")

matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
matplotlib.rcParams['mathtext.fontset'] = 'cm'  # 使用 Computer Modern 数学字体

# 设置 seaborn 风格
try:
    import seaborn as sns
    sns.set_style("whitegrid")
    sns.set_context("notebook", font_scale=1.2)
except ImportError:
    plt.style.use('seaborn-v0_8-whitegrid')


def setup_axis(ax, x_range: Tuple[float, float], y_range: Optional[Tuple[float, float]] = None):
    """设置坐标轴样式，使其穿过原点"""
    # 移除默认的顶部和右侧边框
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # 将左侧和底部边框移动到原点
    ax.spines['left'].set_position('zero')
    ax.spines['bottom'].set_position('zero')

    # 设置边框颜色
    ax.spines['left'].set_color('#333333')
    ax.spines['bottom'].set_color('#333333')

    # 设置刻度
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # 设置范围
    ax.set_xlim(x_range)
    if y_range:
        ax.set_ylim(y_range)

    # 添加坐标轴标签
    ax.set_xlabel('x', loc='right', fontsize=12)
    ax.set_ylabel('y', loc='top', fontsize=12, rotation=0)


def plot_single_function(
    ax,
    func_str: str,
    x_range: Tuple[float, float] = (-3, 3),
    title: str = "",
    color: str = '#2E86AB',
    linewidth: float = 2.5,
    num_points: int = 1000
):
    """绘制单个函数"""
    x = np.linspace(x_range[0], x_range[1], num_points)

    # 安全地计算函数值
    try:
        y = eval(func_str, {'x': x, 'np': np, 'abs': np.abs, 'sin': np.sin,
                           'cos': np.cos, 'tan': np.tan, 'exp': np.exp,
                           'log': np.log, 'sqrt': np.sqrt, 'pi': np.pi, 'e': np.e})
    except Exception as e:
        print(f"函数表达式错误: {e}")
        return

    # 处理无穷大和 NaN
    y = np.ma.masked_invalid(y)

    ax.plot(x, y, color=color, linewidth=linewidth, label=f'$y = {func_str}$')

    if title:
        ax.set_title(title, fontsize=14, pad=10)

    return ax


def plot_corner_point(ax, x_range: Tuple[float, float] = (-2, 2)):
    """绘制角点示例 (y = |x|)"""
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = np.abs(x)

    ax.plot(x, y, color='#2E86AB', linewidth=2.5, label=r'$y = |x|$')

    # 绘制两条单侧切线
    x_left = np.linspace(-1.5, 0, 100)
    x_right = np.linspace(0, 1.5, 100)

    ax.plot(x_left, -x_left, '--', color='#E94F37', linewidth=1.5, alpha=0.8,
            label=r'Left derivative: $f^{\prime}_{-}(0) = -1$')
    ax.plot(x_right, x_right, '--', color='#F39C12', linewidth=1.5, alpha=0.8,
            label=r'Right derivative: $f^{\prime}_{+}(0) = +1$')

    # 标记原点
    ax.plot(0, 0, 'ko', markersize=8, zorder=5)
    ax.annotate('Corner Point\n$(0, 0)$', xy=(0, 0), xytext=(0.5, 0.8),
                fontsize=11, ha='left',
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1))

    ax.set_title(r'Corner Point: $y = |x|$ at $x = 0$', fontsize=14, pad=10)
    ax.legend(loc='upper right', fontsize=10)


def plot_infinite_derivative(ax, x_range: Tuple[float, float] = (-2, 2)):
    """绘制无穷导数示例 (y = x^(1/3))"""
    x = np.linspace(x_range[0], x_range[1], 1000)
    y = np.cbrt(x)  # 使用 cbrt 处理负数

    ax.plot(x, y, color='#2E86AB', linewidth=2.5, label=r'$y = x^{1/3}$')

    # 绘制垂直切线（用虚线表示）
    ax.axvline(x=0, color='#E94F37', linestyle='--', linewidth=1.5,
               alpha=0.8, label=r'Vertical tangent: $x = 0$')

    # 标记原点
    ax.plot(0, 0, 'ko', markersize=8, zorder=5)
    ax.annotate('Vertical Tangent\n$f^{\prime}(0) = +\infty$', xy=(0, 0), xytext=(0.8, 0.8),
                fontsize=11, ha='left',
                arrowprops=dict(arrowstyle='->', color='#333333', lw=1))

    # 添加向上的箭头表示切线方向
    ax.annotate('', xy=(0, 1.2), xytext=(0, 0.3),
                arrowprops=dict(arrowstyle='->', color='#E94F37', lw=2))

    ax.set_title(r'Infinite Derivative: $y = x^{1/3}$ at $x = 0$', fontsize=14, pad=10)
    ax.legend(loc='upper left', fontsize=10)


def create_comparison_plot(output_path: str, x_range: Tuple[float, float] = (-2, 2)):
    """创建角点和无穷导数的对比图"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # 调整布局
    plt.subplots_adjust(wspace=0.3)

    # 左图：角点
    setup_axis(ax1, x_range, (-0.5, 2.5))
    plot_corner_point(ax1, x_range)

    # 右图：无穷导数
    setup_axis(ax2, x_range, (-1.5, 1.5))
    plot_infinite_derivative(ax2, x_range)

    # 保存图片
    ensure_dir(output_path)
    fig.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"图片已保存: {output_path}")


def create_single_plot(
    func_str: str,
    output_path: str,
    x_range: Tuple[float, float] = (-3, 3),
    title: str = "",
    annotations: List[str] = None
):
    """创建单个函数的图像"""
    fig, ax = plt.subplots(figsize=(8, 6))

    setup_axis(ax, x_range)
    plot_single_function(ax, func_str, x_range, title)

    # 处理标注
    if annotations:
        for ann in annotations:
            try:
                parts = ann.split(':')
                coords = parts[0].split(',')
                x, y = float(coords[0]), float(coords[1])
                label = parts[1] if len(parts) > 1 else ""

                ax.plot(x, y, 'ko', markersize=8, zorder=5)
                if label:
                    ax.annotate(label, xy=(x, y), xytext=(x + 0.3, y + 0.3),
                               fontsize=11, ha='left',
                               arrowprops=dict(arrowstyle='->', color='#333333', lw=1))
            except Exception as e:
                print(f"标注解析错误: {e}")

    ax.legend(loc='best', fontsize=10)

    # 保存图片
    ensure_dir(output_path)
    fig.savefig(output_path, dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"图片已保存: {output_path}")


def ensure_dir(filepath: str):
    """确保输出目录存在"""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def parse_range(range_str: str) -> Tuple[float, float]:
    """解析范围字符串"""
    parts = range_str.split(',')
    return (float(parts[0]), float(parts[1]))


def main():
    parser = argparse.ArgumentParser(description='数学函数绘图工具')
    parser.add_argument('--function', '-f', type=str, help='函数表达式，如 "abs(x)" 或 "x**2"')
    parser.add_argument('--range', '-r', type=str, default='-3,3', help='x 轴范围，如 "-2,2"')
    parser.add_argument('--output', '-o', type=str, required=True, help='输出文件路径')
    parser.add_argument('--title', '-t', type=str, default='', help='图像标题')
    parser.add_argument('--annotate', '-a', type=str, nargs='+', help='标注点，格式: "x,y:标签"')
    parser.add_argument('--compare', '-c', action='store_true', help='生成角点和无穷导数对比图')
    parser.add_argument('--functions', nargs='+', help='多个函数表达式（用于对比）')
    parser.add_argument('--titles', nargs='+', help='多个标题（用于对比）')

    args = parser.parse_args()

    x_range = parse_range(args.range)

    if args.compare:
        # 生成预设的对比图
        create_comparison_plot(args.output, x_range)
    elif args.function:
        # 生成单个函数图
        create_single_plot(args.function, args.output, x_range, args.title, args.annotate)
    elif args.functions:
        # 多函数对比（未完成，可扩展）
        print("多函数对比功能开发中...")
    else:
        print("请指定 --function 或 --compare 参数")
        sys.exit(1)


if __name__ == '__main__':
    main()
