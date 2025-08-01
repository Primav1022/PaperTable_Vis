import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np
from pathlib import Path
import seaborn as sns
from matplotlib.font_manager import FontProperties
from datetime import datetime
from domain_map import DOMAIN_ZH2EN

class Complete41PapersTableGenerator:
    def __init__(self, csv_file_path):
        """
        完整41篇论文表格图片生成器
        
        Args:
            csv_file_path: CSV文件路径
        """
        self.csv_file = csv_file_path
        self.data = []
        self.load_csv_data()
        
        # 优化的颜色方案
        self.colors = {
            'header_basic': '#403C73',
            'header_analogy': '#596B3B', 
            'header_create': '#769E35',
            'header_representation': '#A45541',
            'supported': '#5FBBA6',
            'not_supported': '#F1EFF0',
            'basic_info': '#ecf0f1',
            'venue': '#fff3cd',
            'year': '#d1ecf1',
            'auto': '#e2e3e5',
            'domain': '#f8f9fa',
            'border': '#dee2e6',
            'legend_bg': '#f8f9fa',
            'text_supported': '#155724',
            'text_not_supported': '#721c24'
        }
        
        # 设置字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 8
        


    def load_csv_data(self):
        """加载完整CSV数据"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # 解析所有有效数据行（从第3行开始）
            for i, line in enumerate(lines[2:], start=3):
                row = [cell.strip() for cell in line.split(',')]
                if len(row) > 5 and row[0] and row[0].strip():  # 确保有有效的编号
                    paper_data = {
                        'no': row[0].strip(),
                        'title': row[1].strip() if len(row) > 1 else '',
                        'venue': row[2].strip() if len(row) > 2 else '',
                        'year': row[3].strip() if len(row) > 3 else '',
                        'author': row[4].strip() if len(row) > 4 else '',
                        'analogy_process': [
                            row[5].strip() if len(row) > 5 else '', 
                            row[6].strip() if len(row) > 6 else '', 
                            row[7].strip() if len(row) > 7 else '', 
                            row[8].strip() if len(row) > 8 else ''
                        ],
                        'create_process': [
                            row[9].strip() if len(row) > 9 else '', 
                            row[10].strip() if len(row) > 10 else '', 
                            row[11].strip() if len(row) > 11 else '', 
                            row[12].strip() if len(row) > 12 else '', 
                            row[13].strip() if len(row) > 13 else '', 
                            row[14].strip() if len(row) > 14 else '', 
                            row[15].strip() if len(row) > 15 else ''
                        ],
                        'representation': [
                            row[16].strip() if len(row) > 16 else '', 
                            row[17].strip() if len(row) > 17 else '', 
                            row[18].strip() if len(row) > 18 else '', 
                            row[19].strip() if len(row) > 19 else '', 
                            row[20].strip() if len(row) > 20 else '', 
                            row[21].strip() if len(row) > 21 else ''
                        ],
                        'automation': row[22].strip() if len(row) > 22 else '',
                        'application': row[23].strip() if len(row) > 23 else '',
                        'domain': row[24].strip() if len(row) > 24 else ''
                    }
                    self.data.append(paper_data)
            
            print(f"✅ 成功加载 {len(self.data)} 篇论文的完整数据")
            
        except Exception as e:
            print(f"❌ 加载数据失败: {e}")

    def translate_domain(self, domain):
        """翻译domain为英文"""
        if not domain or pd.isna(domain):
            return ''
        domain_str = str(domain).strip()
        return DOMAIN_ZH2EN.get(domain_str, domain_str)

    def create_complete_table_image(self, save_path="complete_41_papers_table.png",
                                  image_width=20, image_height=28, dpi=300):
        """
        创建包含全部41篇论文的完整表格图片
        
        Args:
            save_path: 保存路径
            image_width: 图片宽度（英寸）
            image_height: 图片高度（英寸）
            dpi: 分辨率
        """
        # 创建超大图形以容纳所有数据
        fig, ax = plt.subplots(figsize=(image_width, image_height), dpi=dpi)
        ax.set_xlim(0, 100)
        ax.set_ylim(0, 100)
        ax.axis('off')
        
        # 绘制标题
        self._draw_title(ax)
        
        # 绘制表格
        self._draw_complete_table_headers(ax)
        self._draw_complete_table_data(ax)
        
        # 在表格下方绘制图例
        self._draw_bottom_legend(ax)
        
        # 保存高质量图片
        plt.tight_layout()
        plt.savefig(save_path, dpi=dpi, bbox_inches='tight', 
                   facecolor='white', edgecolor='none', 
                   pad_inches=0.2)
        print(f"📸 完整41篇论文表格图片已保存: {save_path}")
        
        plt.close()
        return fig

    def _draw_title(self, ax):
        """绘制表格标题"""
        ax.text(50, 97, 'Analogy-based Design Research Analysis (Complete Dataset: 41 Papers)', 
               ha='center', va='center', fontsize=20, fontweight='bold',
               bbox=dict(boxstyle="round,pad=0.5", facecolor='#ecf0f1', edgecolor='#bdc3c7'))

    def _draw_complete_table_headers(self, ax):
        """绘制完整表格表头"""
        # 表头位置设置 - 为41行数据优化
        header_y = 92
        header_height = 2.5
        col_widths = [2.5, 14, 3.5, 3, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 4.7, 8]  # Auto Level从3.5增加到4.7
        
        # 计算列位置
        col_positions = []
        current_x = 1
        for width in col_widths:
            col_positions.append(current_x)
            current_x += width
        
        # 绘制第一行表头
        self._draw_header_cell(ax, col_positions[0], header_y, col_widths[0], header_height, 
                              '#', self.colors['header_basic'])
        self._draw_header_cell(ax, col_positions[1], header_y, col_widths[1], header_height, 
                              'Paper Title', self.colors['header_basic'])
        self._draw_header_cell(ax, col_positions[2], header_y, col_widths[2], header_height, 
                              'Venue', self.colors['header_basic'])
        self._draw_header_cell(ax, col_positions[3], header_y, col_widths[3], header_height, 
                              'Year', self.colors['header_basic'])
        
        # Analogy Process (4列)
        analogy_start = col_positions[4]
        analogy_width = sum(col_widths[4:8])
        self._draw_header_cell(ax, analogy_start, header_y, analogy_width, header_height, 
                              'Analogy Process', self.colors['header_analogy'])
        
        # Create Process (7列) 
        create_start = col_positions[8]
        create_width = sum(col_widths[8:15])
        self._draw_header_cell(ax, create_start, header_y, create_width, header_height, 
                              'Create Process', self.colors['header_create'])
        
        # Representation (6列)
        repr_start = col_positions[15]
        repr_width = sum(col_widths[15:21])
        self._draw_header_cell(ax, repr_start, header_y, repr_width, header_height, 
                              'Representation', self.colors['header_representation'])
        
        # Auto Level 和 Domain
        self._draw_header_cell(ax, col_positions[21], header_y, col_widths[21], header_height, 
                              'Auto Level', self.colors['header_basic'])
        self._draw_header_cell(ax, col_positions[22], header_y, col_widths[22], header_height, 
                              'Domain', self.colors['header_basic'])
        
        # 绘制第二行表头（子分类）
        subheader_y = header_y - header_height
        subheader_labels = [
            '', '', '', '',  # 前4列空白（跨行）
            'Enc', 'Ret', 'Map', 'Eva',  # Analogy Process
            'Vis', 'Ins', 'Ide', 'Pro', 'Fab', 'Eva', 'Met',  # Create Process
            'Txt', 'Vis', 'Str', 'Fun', 'Wor', 'Unc',  # Representation
            '', ''  # Auto Level 和 Domain 空白（跨行）
        ]
        
        colors_second_row = [
            '', '', '', '',
            self.colors['header_analogy'], self.colors['header_analogy'], 
            self.colors['header_analogy'], self.colors['header_analogy'],
            self.colors['header_create'], self.colors['header_create'], 
            self.colors['header_create'], self.colors['header_create'],
            self.colors['header_create'], self.colors['header_create'], 
            self.colors['header_create'],
            self.colors['header_representation'], self.colors['header_representation'], 
            self.colors['header_representation'], self.colors['header_representation'],
            self.colors['header_representation'], self.colors['header_representation'],
            '', ''
        ]
        
        for i, (label, color) in enumerate(zip(subheader_labels, colors_second_row)):
            if label and color:  # 只绘制有内容的单元格
                self._draw_header_cell(ax, col_positions[i], subheader_y, col_widths[i], 
                                     header_height, label, color)

    def _draw_header_cell(self, ax, x, y, width, height, text, color):
        """绘制表头单元格"""
        # 绘制背景
        rect = Rectangle((x, y), width, height, 
                        facecolor=color, edgecolor=self.colors['border'], 
                        linewidth=0.5)
        ax.add_patch(rect)
        
        # 添加文字
        ax.text(x + width/2, y + height/2, text, 
               ha='center', va='center', fontsize=13, fontweight='bold', 
               color='white')

    def _draw_complete_table_data(self, ax):
        """绘制所有41篇论文的数据"""
        # 数据行设置 - 优化为紧凑布局
        row_height = 1.6  # 减小行高以容纳更多数据
        start_y = 92 - 5  # 表头下方
        col_widths = [2.5, 14, 3.5, 3, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 5, 8]  # Auto Level从3.5增加到4.7
        
        # 计算列位置
        col_positions = []
        current_x = 1
        for width in col_widths:
            col_positions.append(current_x)
            current_x += width
        
        for i, paper in enumerate(self.data):
            row_y = start_y - (i * row_height)
            
            # 基本信息列 - 从1开始递增计数
            self._draw_data_cell(ax, col_positions[0], row_y, col_widths[0], row_height, 
                               i + 1, self.colors['basic_info'])
            
            # 处理标题长度 - 不超过25则不省略
            title_display = paper['title'][:25] + '...' if len(paper['title']) > 25 else paper['title']
            self._draw_data_cell(ax, col_positions[1], row_y, col_widths[1], row_height, 
                               title_display, self.colors['basic_info'], align='left')
            
            # 处理venue缩写 - 超过10个字符则缩写
            venue = paper['venue']
            if len(venue) > 10:
                # 按空格分割，取每个单词首字母大写
                words = venue.split()
                venue_abbr = ''.join([word[0].upper() for word in words if word])
            else:
                venue_abbr = venue
            self._draw_data_cell(ax, col_positions[2], row_y, col_widths[2], row_height, 
                               venue_abbr, self.colors['venue'])
            self._draw_data_cell(ax, col_positions[3], row_y, col_widths[3], row_height, 
                               paper['year'], self.colors['year'])
            
            
            # 过程数据列
            col_idx = 4
            
            # Analogy Process
            for value in paper['analogy_process']:
                # 只要是'√'、'✔️'、'✔'都视为支持，空字符或其它都视为不支持
                if value.strip() in ['√', '✔️', '✔']:
                    color = self.colors['supported']
                    symbol = '✓'
                else:
                    color = self.colors['not_supported']
                    symbol = '×'
                self._draw_data_cell(ax, col_positions[col_idx], row_y, col_widths[col_idx], 
                                   row_height, symbol, color)
                col_idx += 1

            # Create Process
            for value in paper['create_process']:
                if value.strip() in ['√', '✔️', '✔']:
                    color = self.colors['supported']
                    symbol = '✓'
                else:
                    color = self.colors['not_supported']
                    symbol = '×'
                self._draw_data_cell(ax, col_positions[col_idx], row_y, col_widths[col_idx], 
                                   row_height, symbol, color)
                col_idx += 1

            # Representation
            for value in paper['representation']:
                if value.strip() in ['√', '✔️', '✔']:
                    color = self.colors['supported']
                    symbol = '✓'
                else:
                    color = self.colors['not_supported']
                    symbol = '×'
                self._draw_data_cell(ax, col_positions[col_idx], row_y, col_widths[col_idx], 
                                   row_height, symbol, color)
                col_idx += 1
            # Auto Level 和 Domain
            self._draw_data_cell(ax, col_positions[21], row_y, col_widths[21], row_height, 
                               paper['automation'][:5], self.colors['auto'])
            
            # 翻译domain为英文 - 完全显示，不缩写
            domain_en = self.translate_domain(paper['domain'])
            self._draw_data_cell(ax, col_positions[22], row_y, col_widths[22], row_height, 
                               domain_en, self.colors['domain'], align='left')

    def _draw_data_cell(self, ax, x, y, width, height, text, color, align='center'):
        """绘制数据单元格"""
        # 绘制背景
        rect = Rectangle((x, y), width, height, 
                        facecolor=color, edgecolor=self.colors['border'], 
                        linewidth=0.3)
        ax.add_patch(rect)
        
        # 添加文字
        text_color = self.colors['text_supported'] if color == self.colors['supported'] else (
                    self.colors['text_not_supported'] if color == self.colors['not_supported'] else 'black')
        fontweight = 'bold' if color == self.colors['supported'] else 'normal'
        
        ha = 'left' if align == 'left' else 'center'
        text_x = x + 0.3 if align == 'left' else x + width/2
        
        ax.text(text_x, y + height/2, str(text), 
               ha=ha, va='center', fontsize=10, fontweight=fontweight, 
               color=text_color)

    def _draw_bottom_legend(self, ax):
        """在表格下方绘制图例"""
        # 图例位置 - 在表格数据下方
        legend_start_y = 92 - 5 - (len(self.data) * 1.6) - 3
        
        # 图例背景
        legend_rect = Rectangle((2, legend_start_y - 13), 96, 16, 
                              facecolor=self.colors['legend_bg'], 
                              edgecolor=self.colors['border'], 
                              linewidth=1, alpha=0.9)
        ax.add_patch(legend_rect)
        
        # 图例标题
        ax.text(50, legend_start_y - 0.5, '📚 图例说明与缩写对照 (Legend & Abbreviations)', 
               ha='center', va='center', fontsize=10, fontweight='bold',
               color='#2c3e50')
        
        # 绘制分割线
        ax.plot([5, 95], [legend_start_y - 2, legend_start_y - 2], 
               color='#3498db', linewidth=2)
        
        # 图例内容 - 4列布局
        legend_items = [
            ("🔄 Analogy Process", [
                "Enc = Encoding/Representation",
                "Ret = Retrieval",
                "Map = Mapping", 
                "Eva = Evaluation"
            ]),
            ("🛠️ Create Process", [
                "Vis = Vision",
                "Ins = Inspiration",
                "Ide = Ideation",
                "Pro = Prototype",
                "Fab = Fabrication",
                "Eva = Evaluation",
                "Met = Meta-cognition"
            ]),
            ("📋 Representation", [
                "Txt = Text",
                "Vis = Visual", 
                "Str = Structure",
                "Fun = Function",
                "Wor = Workflow",
                "Unc = Unconventional"
            ]),
            ("🎨 Symbols", [
                "✓ = Supported",
                "× = Not Supported", 
                "Auto Level:",
                "augment/assist/automate"
            ])
        ]
        
        # 绘制4个图例卡片
        card_width = 22
        card_height = 9
        start_x = 4
        
        for i, (title, items) in enumerate(legend_items):
            card_x = start_x + i * 23
            card_y = legend_start_y - 12
            
            # 卡片背景
            card_rect = Rectangle((card_x, card_y), card_width, card_height, 
                                facecolor='white', edgecolor='#3498db', 
                                linewidth=1)
            ax.add_patch(card_rect)
            
            # 卡片标题
            ax.text(card_x + card_width/2, card_y + card_height - 1, title, 
                   ha='center', va='center', fontsize=7, fontweight='bold',
                   color='#2c3e50')
            
            # 卡片内容
            for j, item in enumerate(items):
                ax.text(card_x + 1, card_y + card_height - 2.5 - (j * 0.9), f"• {item}", 
                       ha='left', va='center', fontsize=5.5, color='#2c3e50')
        
        # 添加颜色示例
        # 支持状态颜色示例
        support_rect = Rectangle((85, legend_start_y - 8), 1.5, 0.8, 
                               facecolor=self.colors['supported'], 
                               edgecolor=self.colors['border'], linewidth=0.5)
        ax.add_patch(support_rect)
        ax.text(87, legend_start_y - 7.6, '✓ 支持', ha='left', va='center', fontsize=6)
        
        not_support_rect = Rectangle((85, legend_start_y - 9.2), 1.5, 0.8, 
                                   facecolor=self.colors['not_supported'], 
                                   edgecolor=self.colors['border'], linewidth=0.5)
        ax.add_patch(not_support_rect)
        ax.text(87, legend_start_y - 8.8, '× 不支持', ha='left', va='center', fontsize=6)
        
        # 添加生成信息
        ax.text(50, legend_start_y - 14, 
               f'Generated on {datetime.now().strftime("%Y-%m-%d %H:%M")} | '
               f'Total Papers: {len(self.data)} | Data Source: paper-process-4-vis.csv', 
               ha='center', va='center', fontsize=6, color='#666',
               style='italic')

    def create_publication_ready_image(self, save_path="analogy_design_publication_ready.png"):
        """创建发表级质量的图片"""
        return self.create_complete_table_image(
            save_path=save_path,
            image_width=20,
            image_height=28, 
            dpi=300
        )

    def create_presentation_image(self, save_path="analogy_design_presentation.png"):
        """创建演示用图片"""
        return self.create_complete_table_image(
            save_path=save_path,
            image_width=16,
            image_height=22,
            dpi=200
        )

    def print_data_summary(self):
        """打印数据摘要"""
        if not self.data:
            print("无数据可分析")
            return
        
        print(f"\n📊 数据摘要 (共{len(self.data)}篇论文)")
        print("=" * 50)
        
        # 会议统计
        venues = {}
        for paper in self.data:
            venue = paper['venue'] or 'Unknown'
            venues[venue] = venues.get(venue, 0) + 1
        
        print("🏛️ 会议分布:")
        for venue, count in sorted(venues.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(f"   {venue}: {count}篇")
        
        # 年份统计
        years = {}
        for paper in self.data:
            year = paper['year'] or 'Unknown'
            years[year] = years.get(year, 0) + 1
        
        print("\n📅 年份分布:")
        for year, count in sorted(years.items()):
            print(f"   {year}: {count}篇")
        
        # 自动化级别统计
        auto_levels = {}
        for paper in self.data:
            auto = paper['automation'] or 'Unknown'
            auto_levels[auto] = auto_levels.get(auto, 0) + 1
        
        print("\n🤖 自动化级别分布:")
        for level, count in auto_levels.items():
            print(f"   {level}: {count}篇")
        
        # 过程使用情况统计
        print("\n📈 特征使用统计:")
        analogy_usage = [0, 0, 0, 0]
        create_usage = [0, 0, 0, 0, 0, 0, 0]
        repr_usage = [0, 0, 0, 0, 0, 0]
        
        for paper in self.data:
            for i, val in enumerate(paper['analogy_process']):
                if val == '√':
                    analogy_usage[i] += 1
            for i, val in enumerate(paper['create_process']):
                if val == '√':
                    create_usage[i] += 1
            for i, val in enumerate(paper['representation']):
                if val == '√':
                    repr_usage[i] += 1
        
        analogy_labels = ['Enc', 'Ret', 'Map', 'Eva']
        create_labels = ['Vis', 'Ins', 'Ide', 'Pro', 'Fab', 'Eva', 'Met']
        repr_labels = ['Txt', 'Vis', 'Str', 'Fun', 'Wor', 'Unc']
        
        print("   类比过程:", dict(zip(analogy_labels, analogy_usage)))
        print("   创作过程:", dict(zip(create_labels, create_usage)))
        print("   表示方式:", dict(zip(repr_labels, repr_usage)))


def main():
    """主函数"""
    print("🎨 完整41篇论文表格图片生成器")
    print("=" * 50)
    
    # 使用你的CSV文件
    csv_file = "paper-process-4-vis.csv"
    
    # 检查文件是否存在
    if not Path(csv_file).exists():
        print(f"❌ 错误: 找不到文件 {csv_file}")
        print("请确保CSV文件在当前目录下")
        return
    
    # 创建图片生成器
    print("📂 正在加载CSV数据...")
    generator = Complete41PapersTableGenerator(csv_file)
    
    if not generator.data:
        print("❌ 没有加载到有效数据，请检查CSV文件格式")
        return
    
    # 打印数据摘要
    generator.print_data_summary()
    
    print(f"\n🎨 正在生成包含{len(generator.data)}篇论文的完整表格图片...")
    
    # 生成发表级质量图片
    print("\n📄 生成发表级质量图片 (300 DPI)...")
    try:
        generator.create_publication_ready_image("complete_41_papers_publication.png")
    except Exception as e:
        print(f"❌ 发表版生成失败: {e}")
    
    # 生成演示用图片
    print("\n📺 生成演示用图片 (200 DPI)...")
    try:
        generator.create_presentation_image("complete_41_papers_presentation.png")
    except Exception as e:
        print(f"❌ 演示版生成失败: {e}")
    
    print("\n✅ 图片生成完成!")
    print("📁 输出文件:")
    print("   📄 complete_41_papers_publication.png - 发表级质量 (300 DPI)")
    print("   📺 complete_41_papers_presentation.png - 演示级质量 (200 DPI)")
    print("\n💡 特点:")
    print("   • 包含全部41篇论文数据")
    print("   • 图例位于表格下方")
    print("   • 根据CSV数据自动填色")
    print("   • 紧凑布局优化可读性")
    print("   • 高分辨率适合发表和演示")


if __name__ == "__main__":
    main()