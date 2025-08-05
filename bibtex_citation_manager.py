#!/usr/bin/env python3
"""
BibTeX风格的自动引用序号管理器
类似Overleaf的引用系统，自动管理论文的引用序号
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Citation:
    """引用条目"""
    key: str                    # 引用键（如 "srinivasan2024improving"）
    title: str                  # 论文标题
    authors: str                # 作者
    venue: str                  # 会议/期刊
    year: str                   # 年份
    citation_number: int = 0    # 自动分配的引用序号
    first_cited: bool = False   # 是否首次被引用

class BibTeXCitationManager:
    """BibTeX风格的引用管理器"""
    
    def __init__(self):
        self.citations: Dict[str, Citation] = {}
        self.citation_order: List[str] = []  # 按首次引用顺序排列
        self.next_citation_number = 1
        
    def generate_citation_key(self, title: str, authors: str, year: str) -> str:
        """
        生成BibTeX风格的引用键
        格式: 第一作者姓氏 + 年份 + 标题首词
        """
        # 提取第一作者姓氏
        first_author = authors.split(',')[0].strip() if authors else "Unknown"
        last_name = first_author.split()[-1].lower() if first_author else "unknown"
        
        # 提取标题首词（去除冠词）
        title_words = re.findall(r'\b[a-zA-Z]+\b', title.lower())
        if title_words:
            # 跳过冠词
            articles = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            first_word = next((word for word in title_words if word not in articles), title_words[0])
        else:
            first_word = "paper"
        
        # 生成键 - 使用更简单的格式，与LaTeX文档匹配
        key = f"{last_name}{year}{first_word}"
        return key
    
    def generate_latex_style_key(self, title: str, authors: str, year: str) -> str:
        """
        生成LaTeX风格的引用键（与LaTeX文档中的格式匹配）
        格式: 第一作者姓氏 + 年份 + 标题关键词
        """
        # 提取第一作者姓氏
        first_author = authors.split(',')[0].strip() if authors else "Unknown"
        last_name = first_author.split()[-1].lower() if first_author else "unknown"
        
        # 清理年份（移除.0）
        clean_year = year.split('.')[0] if '.' in year else year
        
        # 从标题中提取关键词（通常是第一个有意义的词）
        title_words = re.findall(r'\b[a-zA-Z]+\b', title.lower())
        if title_words:
            # 跳过冠词和常见词
            skip_words = {'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'design', 'analysis', 'study', 'review', 'system', 'method', 'approach', 'framework', 'model', 'tool', 'application', 'evaluation', 'investigation', 'examination', 'exploration', 'development', 'implementation', 'creation', 'generation', 'production', 'construction', 'building', 'making', 'creating', 'developing', 'implementing', 'evaluating', 'analyzing', 'studying', 'reviewing', 'examining', 'exploring', 'investigating'}
            first_word = next((word for word in title_words if word not in skip_words), title_words[0])
        else:
            first_word = "paper"
        
        # 生成键
        key = f"{last_name}{clean_year}{first_word}"
        return key
    
    def add_citation(self, title: str, authors: str, venue: str, year: str) -> str:
        """
        添加新的引用条目
        
        Returns:
            str: 生成的引用键
        """
        key = self.generate_citation_key(title, authors, year)
        
        # 如果键已存在，返回现有键
        if key in self.citations:
            return key
        
        # 创建新的引用条目
        citation = Citation(
            key=key,
            title=title,
            authors=authors,
            venue=venue,
            year=year,
            citation_number=self.next_citation_number,
            first_cited=True
        )
        
        self.citations[key] = citation
        self.citation_order.append(key)
        self.next_citation_number += 1
        
        return key
    
    def get_citation_number(self, key: str) -> int:
        """获取引用序号"""
        if key in self.citations:
            return self.citations[key].citation_number
        return 0
    
    def get_citation_by_number(self, number: int) -> Optional[Citation]:
        """根据序号获取引用"""
        for citation in self.citations.values():
            if citation.citation_number == number:
                return citation
        return None
    
    def get_all_citations_ordered(self) -> List[Citation]:
        """获取按引用顺序排列的所有引用"""
        return [self.citations[key] for key in self.citation_order]
    
    def generate_bibtex_entry(self, key: str) -> str:
        """生成BibTeX条目"""
        if key not in self.citations:
            return ""
        
        citation = self.citations[key]
        return f"""@inproceedings{{{citation.key},
  title={{{citation.title}}},
  author={{{citation.authors}}},
  booktitle={{{citation.venue}}},
  year={{{citation.year}}},
  pages={{{citation.citation_number}}}
}}"""
    
    def generate_reference_list(self) -> str:
        """生成参考文献列表（类似Overleaf的参考文献）"""
        references = []
        for citation in self.get_all_citations_ordered():
            ref = f"[{citation.citation_number}] {citation.authors}. {citation.title}. {citation.venue}, {citation.year}."
            references.append(ref)
        
        return "\n".join(references)
    
    def generate_citation_text(self, keys: List[str]) -> str:
        """生成引用文本，如 [1,3,5] 或 [1-3]"""
        if not keys:
            return ""
        
        # 获取所有有效的引用序号
        numbers = []
        for key in keys:
            if key in self.citations:
                numbers.append(self.citations[key].citation_number)
        
        if not numbers:
            return ""
        
        # 排序并去重
        numbers = sorted(list(set(numbers)))
        
        # 生成引用文本
        if len(numbers) == 1:
            return f"[{numbers[0]}]"
        elif len(numbers) == 2:
            return f"[{numbers[0]},{numbers[1]}]"
        else:
            # 检查是否连续
            if numbers == list(range(min(numbers), max(numbers) + 1)):
                return f"[{min(numbers)}-{max(numbers)}]"
            else:
                return f"[{','.join(map(str, numbers))}]"

class PaperCitationManager:
    """论文引用管理器，集成到现有系统中"""
    
    def __init__(self, csv_data: List[Dict]):
        self.bibtex_manager = BibTeXCitationManager()
        self.paper_citations: Dict[str, str] = {}  # 论文编号 -> 引用键
        
        # 从CSV数据初始化引用
        self._initialize_citations(csv_data)
    
    def _initialize_citations(self, csv_data: List[Dict]):
        """从CSV数据初始化引用"""
        for paper in csv_data:
            if paper.get('title') and paper.get('author'):
                # 使用LaTeX风格的引用键
                key = self.bibtex_manager.generate_latex_style_key(
                    title=paper['title'],
                    authors=paper['author'],
                    year=paper.get('year', '')
                )
                # 添加到BibTeX管理器
                self.bibtex_manager.add_citation(
                    title=paper['title'],
                    authors=paper['author'],
                    venue=paper.get('venue', ''),
                    year=paper.get('year', '')
                )
                self.paper_citations[paper['no']] = key
    
    def get_paper_citation_number(self, paper_no: str) -> int:
        """获取论文的引用序号"""
        key = self.paper_citations.get(paper_no)
        if key:
            return self.bibtex_manager.get_citation_number(key)
        return 0
    
    def get_paper_citation_key(self, paper_no: str) -> str:
        """获取论文的引用键"""
        return self.paper_citations.get(paper_no, "")
    
    def get_all_papers_with_citations(self) -> List[Tuple[str, int, str]]:
        """获取所有论文及其引用信息"""
        result = []
        for paper_no, key in self.paper_citations.items():
            citation_number = self.bibtex_manager.get_citation_number(key)
            result.append((paper_no, citation_number, key))
        return sorted(result, key=lambda x: x[1])  # 按引用序号排序
    
    def generate_citation_report(self) -> str:
        """生成引用报告"""
        report = "📚 论文引用序号报告\n"
        report += "=" * 50 + "\n\n"
        
        # 按引用序号排序的论文列表
        papers_with_citations = self.get_all_papers_with_citations()
        
        for paper_no, citation_number, key in papers_with_citations:
            if key in self.bibtex_manager.citations:
                citation = self.bibtex_manager.citations[key]
                report += f"[{citation_number:2d}] {citation.authors}. {citation.title}. {citation.venue}, {citation.year}.\n"
            else:
                # 如果没有找到引用，使用默认信息
                report += f"[{citation_number:2d}] Paper {paper_no} (key: {key})\n"
        
        report += f"\n总计: {len(papers_with_citations)} 篇论文"
        return report

# 使用示例
if __name__ == "__main__":
    # 测试代码
    manager = BibTeXCitationManager()
    
    # 添加一些测试引用
    key1 = manager.add_citation(
        "Improving Selection of Analogical Inspirations through Chunking and Recombination",
        "Arvind Srinivasan",
        "C&C",
        "2024"
    )
    
    key2 = manager.add_citation(
        "BioSpark: Beyond Analogical Inspiration to LLM-augmented Transfer",
        "Hyeonsu Kang",
        "CHI",
        "2025"
    )
    
    print("引用键:", key1, key2)
    print("引用序号:", manager.get_citation_number(key1), manager.get_citation_number(key2))
    print("引用文本:", manager.generate_citation_text([key1, key2]))
    print("\n参考文献列表:")
    print(manager.generate_reference_list()) 