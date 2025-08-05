# 📚 BibTeX风格引用系统使用指南

## 🎯 概述

这个系统实现了类似Overleaf BibTeX的自动引用序号管理，可以自动为论文分配引用序号，并在图表中显示这些序号。

## ✨ 主要功能

### 1. 自动引用序号分配
- 根据论文信息自动生成BibTeX风格的引用键
- 按首次引用顺序自动分配序号 [1], [2], [3]...
- 支持连续引用格式 [1-3] 和多个引用 [1,3,5]

### 2. 引用键生成规则
- 格式：`第一作者姓氏 + 年份 + 标题首词`
- 示例：`srinivasan2024improving`
- 自动跳过冠词（a, an, the等）

### 3. 表格集成
- 在表格中显示BibTeX引用序号而不是原始编号
- 自动生成参考文献列表
- 支持引用文本生成

## 🚀 使用方法

### 1. 基本使用

```python
from bibtex_citation_manager import BibTeXCitationManager

# 创建引用管理器
manager = BibTeXCitationManager()

# 添加引用
key1 = manager.add_citation(
    "Improving Selection of Analogical Inspirations through Chunking and Recombination",
    "Arvind Srinivasan",
    "C&C",
    "2024"
)

# 获取引用序号
citation_number = manager.get_citation_number(key1)  # 返回 1

# 生成引用文本
citation_text = manager.generate_citation_text([key1])  # 返回 "[1]"
```

### 2. 与现有系统集成

```python
from bibtex_citation_manager import PaperCitationManager

# 从CSV数据创建论文引用管理器
paper_manager = PaperCitationManager(csv_data)

# 获取论文的引用序号
citation_number = paper_manager.get_paper_citation_number("1")  # 返回论文1的引用序号

# 生成引用报告
report = paper_manager.generate_citation_report()
```

### 3. 在表格生成器中使用

```python
# 在Complete41PapersTableGenerator中
citation_number = self.citation_manager.get_paper_citation_number(paper['no'])
citation_text = f"[{citation_number}]" if citation_number > 0 else paper['no']

# 在表格中显示引用序号
self._draw_data_cell(ax, x, y, width, height, citation_text, color)
```

## 📊 输出示例

### 引用序号报告
```
📚 论文引用序号报告
==================================================

[ 1] Arvind Srinivasan. Improving Selection of Analogical Inspirations through Chunking and Recombination. C&C, 2024.
[ 2] Hyeonsu Kang. BioSpark: Beyond Analogical Inspiration to LLM-augmented Transfer. CHI, 2025.
[ 3] Adam G. Emerson. Anther: Cross-Pollinating Communities of Practice via Video Tutorials. DIS, 2024.
...
```

### 表格中的显示
- 原始编号：1, 2, 3, 4...
- BibTeX引用序号：[1], [2], [3], [4]...

### 引用文本格式
- 单个引用：`[1]`
- 多个引用：`[1,3,5]`
- 连续引用：`[1-3]`

## 🔧 高级功能

### 1. 自定义引用键生成

```python
def custom_citation_key(self, title, authors, year):
    # 自定义引用键生成逻辑
    first_author = authors.split(',')[0].strip()
    last_name = first_author.split()[-1].lower()
    return f"{last_name}{year}"
```

### 2. 引用排序

```python
# 按引用序号排序
papers_with_citations = paper_manager.get_all_papers_with_citations()
sorted_papers = sorted(papers_with_citations, key=lambda x: x[1])
```

### 3. BibTeX条目生成

```python
# 生成BibTeX条目
bibtex_entry = manager.generate_bibtex_entry(key)
print(bibtex_entry)
```

## 📁 文件结构

```
PaperTable_Vis/
├── bibtex_citation_manager.py    # 核心引用管理器
├── test_bibtex_citation.py      # 测试脚本
├── complete_41_papers_generator.py  # 集成引用系统的表格生成器
├── paper-process-4-vis.csv      # 论文数据
└── BibTeX_Citation_Guide.md     # 本使用指南
```

## 🎨 在图表中的应用

### 1. 表格编号列
- 显示BibTeX引用序号 `[1]`, `[2]`, `[3]`...
- 替代原始编号 1, 2, 3...

### 2. 图例和说明
- 在图表底部添加参考文献列表
- 引用格式：`[序号] 作者. 标题. 会议, 年份.`

### 3. 自动更新
- 添加新论文时自动重新分配序号
- 保持引用顺序的一致性

## 🔄 工作流程

1. **数据加载**：从CSV文件读取论文信息
2. **引用初始化**：为每篇论文生成引用键和序号
3. **表格生成**：在表格中显示引用序号
4. **报告生成**：输出完整的引用报告

## 💡 最佳实践

### 1. 引用键命名
- 使用有意义的引用键
- 避免特殊字符
- 保持一致性

### 2. 序号管理
- 按首次引用顺序分配序号
- 保持序号的连续性
- 支持手动调整

### 3. 数据一致性
- 确保论文信息完整
- 验证引用键的唯一性
- 定期更新引用列表

## 🐛 故障排除

### 1. 引用键冲突
```python
# 检查是否存在重复的引用键
all_keys = [citation.key for citation in manager.citations.values()]
duplicates = [key for key in all_keys if all_keys.count(key) > 1]
```

### 2. 序号错误
```python
# 验证序号的连续性
numbers = [citation.citation_number for citation in manager.citations.values()]
expected_numbers = list(range(1, len(numbers) + 1))
if numbers != expected_numbers:
    print("序号不连续，需要重新分配")
```

### 3. 数据格式问题
```python
# 检查CSV数据格式
for paper in csv_data:
    required_fields = ['title', 'author', 'venue', 'year']
    missing_fields = [field for field in required_fields if not paper.get(field)]
    if missing_fields:
        print(f"论文 {paper.get('no', 'Unknown')} 缺少字段: {missing_fields}")
```

## 📈 扩展功能

### 1. 支持更多引用格式
- IEEE格式
- APA格式
- Chicago格式

### 2. 引用统计
- 引用频率统计
- 作者引用分析
- 会议引用分布

### 3. 自动更新
- 监控新论文添加
- 自动重新排序
- 版本控制支持

## 🎯 总结

这个BibTeX风格的引用系统提供了：

✅ **自动化**：自动生成引用键和序号  
✅ **一致性**：保持引用格式的统一  
✅ **可扩展**：支持自定义和扩展  
✅ **易集成**：与现有系统无缝集成  
✅ **高质量**：适合学术发表和演示  

通过这个系统，你可以像在Overleaf中一样管理论文引用，实现自动化的引用序号分配和表格生成。 