# skill-refactor 代码架构

> 📋 **返回主文档**: [SKILL.md](SKILL.md)

本文件提供 `skill-refactor` 的整体代码架构和模块索引。详细的 Python 实现请参考 `scripts/` 目录。

---

## 📂 模块索引

| 模块名称 | 文件路径 | 核心功�� |
| :--- | :--- | :--- |
| **模块入口** | [`__init__.py`](scripts/__init__.py) | 暴露对外的核心 API 和数据类 |
| **检测器** | [`detector.py`](scripts/detector.py) | 代码块检测、行数统计、结构分析、重构判断 |
| **拆分器** | [`splitter.py`](scripts/splitter.py) | 章节拆分、Frontmatter 保留、模块文件生成 |
| **重构器** | [`refactor.py`](scripts/refactor.py) | 执行代码提取、防御性写入、变更报告生成 |

---

## 🧠 核心数据结构

以下是模块间传递数据的核心类定义：

```python
@dataclass
class CodeBlock:
    """代码块信息（detector.py）"""
    language: str
    code: str
    start_line: int
    end_line: int
    start_pos: int
    end_pos: int

@dataclass
class ContentSection:
    """内容章节（splitter.py）"""
    level: int           # 0=Frontmatter, 1-6=标题级别
    title: str
    content: str
    start_line: int
    end_line: int
    line_count: int

@dataclass
class RefactorAnalysis:
    """重构分析结果"""
    skill_name: str
    skill_exists: bool
    skill_lines: int
    has_code_blocks: bool
    code_block_count: int
    needs_code_extraction: bool
    needs_skill_split: bool
    needs_code_split: bool
    needs_refactor: bool

@dataclass
class RefactorResult:
    """重构执行结果"""
    success: bool
    changes: List[str]
    files_modified: List[str]
    files_created: List[str]
    lines_before: Dict[str, int]
    lines_after: Dict[str, int]
    error: Optional[str]
```

---

## ⚙️ 配置常量

位于 `refactor.py` 顶部：

| 常量 | 默认值 | 说明 |
|------|--------|------|
| `SKILL_THRESHOLD` | 300 | SKILL.md 行数阈值 |
| `CODE_THRESHOLD` | 400 | code.md 行数阈值 |

---

## 🔧 核心 API

### 入口函数（refactor.py）

```python
class SkillRefactor:
    def __init__(self, skill_path: Path): ...
    def analyze(self) -> RefactorAnalysis: ...
    def execute(self, analysis: RefactorAnalysis) -> RefactorResult: ...

def format_confirmation_prompt(analysis: RefactorAnalysis) -> str: ...
def generate_refactor_report(skill_name: str, analysis: RefactorAnalysis, result: RefactorResult) -> str: ...
```

### 检测函数（detector.py）

```python
def detect_code_blocks(content: str) -> List[CodeBlock]: ...
def analyze_skill_structure(skill_path: Path) -> Dict: ...
def needs_refactor(skill_path: Path, skill_threshold: int = 300, code_threshold: int = 400) -> Dict: ...
```

### 拆分函数（splitter.py）

```python
class ContentSplitter:
    def extract_sections(self) -> List[ContentSection]: ...
    def should_split_section(self, section: ContentSection, threshold: int = 50) -> bool: ...
    def execute_split(self, output_dir: Path, skill_name: str) -> Tuple[str, List[Path]]: ...

def split_by_sections(content: str, output_dir: Path, skill_name: str) -> Tuple[str, List[Path]]: ...
def analyze_split_preview(content: str, threshold: int = 50) -> str: ...
```

---

## 🛡️ 防御机制

1. **Frontmatter 保护**：`splitter.py` 中 `level=0` 的章节强制保留
2. **追加写入**：`code.md` 已存在时使用追加模式而非覆盖
3. **章节顺序**：按 `all_sections` 原顺序遍历，保持文档结构

---

> 💡 **提示**: 如需修改正则匹配规则，请直接编辑 `scripts/detector.py` 中的 `CODE_BLOCK_PATTERN`。
