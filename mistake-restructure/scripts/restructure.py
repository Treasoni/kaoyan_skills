#!/usr/bin/env python3
"""
错题本重构脚本 - 自动分析关联、分类索引、生成关联网络
Usage: python restructure.py --input "path/to/错题本.md" [--preview]
"""

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional


class Mistake:
    """错题数据结构"""
    def __init__(self, num: int, title: str, content: str):
        self.num = num
        self.title = title
        self.content = content
        self.category = ""
        self.trap = ""
        self.difficulty = ""
        self.related: List[str] = []

    @property
    def anchor(self) -> str:
        """生成锚点链接"""
        clean_title = re.sub(r'[^\w\u4e00-\u9fff]', '', self.title)
        return f"错题{self.num:02d}{clean_title}"


class MistakeRestructurer:
    """错题本重构器"""

    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.mistakes: List[Mistake] = []

    def _load_config(self, path: str) -> dict:
        """加载配置文件"""
        if path is None:
            path = Path(__file__).parent / "config.json"
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def parse_file(self, file_path: str) -> None:
        """解析错题本文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 匹配错题块: ## 错题XX：标题
        pattern = r'## (错题\d+[：:].+?)(?=## 错题|## 🔗|## 📚|$)'
        matches = re.findall(pattern, content, re.DOTALL)

        for i, match in enumerate(matches, 1):
            lines = match.strip().split('\n')
            title_line = lines[0]
            # 提取标题
            title_match = re.match(r'错题\d+[：:](.+)', title_line)
            title = title_match.group(1).strip() if title_match else f"错题{i}"

            mistake = Mistake(i, title, match)

            # 提取核心陷阱和难度
            trap_match = re.search(r'核心陷阱[：:]\s*(.+)', match)
            if trap_match:
                mistake.trap = trap_match.group(1).strip()[:30]

            diff_match = re.search(r'难度[：:]\s*(.+)', match)
            if diff_match:
                mistake.difficulty = diff_match.group(1).strip()

            # 分类
            mistake.category = self._classify(mistake.content)

            self.mistakes.append(mistake)

    def _classify(self, content: str) -> str:
        """根据内容分类错题"""
        categories = self.config['categories']
        scores = {}

        for cat_name, cat_info in categories.items():
            score = sum(1 for kw in cat_info['keywords'] if kw in content)
            if score > 0:
                scores[cat_name] = score

        if scores:
            return max(scores, key=scores.get)
        return "综合应用"

    def build_relations(self) -> None:
        """构建错题关联关系"""
        for i, m1 in enumerate(self.mistakes):
            for m2 in self.mistakes[i+1:]:
                if self._are_related(m1, m2):
                    m1.related.append(m2.anchor)
                    m2.related.append(m1.anchor)

    def _are_related(self, m1: Mistake, m2: Mistake) -> bool:
        """判断两道错题是否相关"""
        # 同类别相关
        if m1.category == m2.category and m1.category != "综合应用":
            return True

        # 关键词重叠检查
        categories = self.config['categories']
        cat1_keywords = set(categories.get(m1.category, {}).get('keywords', []))
        cat2_keywords = set(categories.get(m2.category, {}).get('keywords', []))

        common = cat1_keywords & cat2_keywords
        if common:
            kw_pattern = '|'.join(common)
            if re.search(kw_pattern, m1.content) and re.search(kw_pattern, m2.content):
                return True

        return False

    def generate_categorized_index(self) -> str:
        """生成按知识点分类的索引"""
        output = "## 📚 按知识点分类索引\n\n"

        # 按类别分组
        categorized: Dict[str, List[Mistake]] = {}
        for m in self.mistakes:
            cat = m.category
            if cat not in categorized:
                categorized[cat] = []
            categorized[cat].append(m)

        # 生成各类别索引
        for cat, mistakes in categorized.items():
            icon = self.config['categories'].get(cat, {}).get('icon', '📌')
            output += f"### {icon} {cat}\n\n"
            output += "| 序号 | 错题标题 | 核心陷阱 | 难度 |\n"
            output += "|------|----------|----------|------|\n"

            for m in mistakes:
                anchor = f"#{m.anchor}"
                trap = m.trap or "-"
                diff = m.difficulty or "-"
                output += f"| [{m.num:02d}]({anchor}) | {m.title} | {trap} | {diff} |\n"
            output += "\n"

        return output

    def generate_mermaid_graph(self) -> str:
        """生成Mermaid关联图"""
        edges = []
        seen_pairs = set()

        for m in self.mistakes:
            for related_anchor in m.related:
                # 找到关联的错题编号
                related_num = int(related_anchor.split('错题')[1][:2])
                pair = tuple(sorted([m.num, related_num]))
                if pair not in seen_pairs:
                    seen_pairs.add(pair)
                    edges.append(f"    M{m.num:02d}[错题{m.num:02d}] --> M{related_num:02d}[错题{related_num:02d}]")

        if not edges:
            return ""

        output = "## 🔗 错题关联网络\n\n```mermaid\ngraph LR\n"
        output += "\n".join(edges)
        output += "\n```\n\n"
        return output

    def restructure(self, file_path: str, preview: bool = False) -> str:
        """执行重构"""
        self.parse_file(file_path)
        self.build_relations()

        # 读取原文件
        with open(file_path, 'r', encoding='utf-8') as f:
            original = f.read()

        # 生成新索引
        new_index = self.generate_categorized_index()
        mermaid = self.generate_mermaid_graph()

        # 替换索引部分 (从 > [!info] 到下一个 ## 之前)
        index_pattern = r'(> \[!info\] 本模块错题索引.*?)(?=## 错题\d|## 🔗|$)'
        new_callout = f"""> [!info] 本模块错题索引
>
> 按知识点分类，快速定位薄弱环节。

{new_index}
{mermaid}"""

        restructured = re.sub(index_pattern, new_callout, original, flags=re.DOTALL)

        # 添加关联标签到每道错题
        for m in self.mistakes:
            if m.related:
                related_links = "\n".join([f"- [[#{a}]]" for a in m.related[:3]])
                tag = f"\n**关联错题**：\n{related_links}\n"
                # 在 --- 前插入
                old_sep = "\n---\n\n## 错题"
                if old_sep in restructured:
                    restructured = restructured.replace(
                        f"\n---\n\n## 错题",
                        f"{tag}\n---\n\n## 错题",
                        1
                    )

        if preview:
            print(restructured[:2000])
            print("\n... [预览模式，未修改文件] ...")
            return restructured

        # 备份原文件
        date_str = datetime.now().strftime("%Y%m%d")
        backup_path = file_path.replace('.md', f'_backup_{date_str}.md')
        shutil.copy(file_path, backup_path)
        print(f"✅ 已备份: {backup_path}")

        # 写入新文件
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(restructured)
        print(f"✅ 已重构: {file_path}")

        return restructured


def main():
    parser = argparse.ArgumentParser(description='错题本重构工具')
    parser.add_argument('--input', '-i', required=True, help='错题本文件路径')
    parser.add_argument('--preview', '-p', action='store_true', help='预览模式')
    parser.add_argument('--config', '-c', help='配置文件路径')
    args = parser.parse_args()

    restructurer = MistakeRestructurer(args.config)
    restructurer.restructure(args.input, args.preview)


if __name__ == '__main__':
    main()
