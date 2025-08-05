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
from bibtex_citation_manager import PaperCitationManager
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

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
        
        # 初始化BibTeX风格的引用管理器
        self.citation_manager = PaperCitationManager(self.data)
        
        # 加载图标
        self.load_icons()
        
        # 优化的颜色方案 - 基于新配色方案
        self.colors = {
            'header_basic': '#203F9A',      # Bright Blue - 基础表头
            'header_analogy': '#4E7CB2',    # Pastel Blue - 类比过程表头
            'header_create': '#E84797',     # Bright Pink - 创作过程表头
            'header_representation': '#94C2DA', # Pastel Blue - 表示方式表头
            'header_auto': '#E8A87C',       # Warm Orange - Auto Level表头（偏暖色调）
            'header_domain': '#d1d871',      # Key Lime - Specific Domain表头（亮柠檬绿色）
            'supported': '#5FBBA6',
            'not_supported': '#F1EFF0',
            'basic_info': '#FCFCFC',        # 保持灰白色基础信息
            'venue': '#EFE8E0',             # Light Beige - 会议信息
            'year': '#EFE8E0',              # Light Beige - 年份信息
            'auto': '#EFE8E0',              # 灰白色 - 自动化级别
            'domain': '#FCFCFC',            # 灰白色 - 领域信息
            'border': '#203F9A',            # Bright Blue - 边框
            'legend_bg': '#FCFCFC',         # 灰白色 - 图例背景
            'text_supported': '#155724',
            'text_not_supported': '#721c24',
            # 不同过程的支持颜色 - 使用新配色方案
            'analogy_supported': '#4E7CB2',     # Pastel Blue - 类比过程支持
            'create_supported': '#E8AAD1',      # Bright Pink - 创作过程支持
            'representation_supported': '#94C2DA', # Pastel Blue - 表示方式支持
            # Domain分类背景颜色 - 使用左上角三个颜色
            'domain_creative': '#ECECE5',       # Powder Blue - Creative Industries
            'domain_manufacturing': '#D1D871',   # Key Lime - Intelligent Manufacturing
            'domain_education': '#BED4B1'        # Eggshell - Education and Service Industries
        }
        
        # 设置字体
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        plt.rcParams['font.size'] = 8
        
    def load_icons(self):
        """加载Auto Level对应的图标"""
        icon_path = Path("icon")
        self.icons = {}
        
        # 映射Auto Level到图标文件
        icon_mapping = {
            'automate': 'Bot.png',
            'augment': 'Handshake.png', 
            'assist': 'Wrench.png'
        }
        
        for level, icon_file in icon_mapping.items():
            icon_file_path = icon_path / icon_file
            if icon_file_path.exists():
                # 读取图标
                img = plt.imread(str(icon_file_path))
                self.icons[level] = img
            else:
                print(f"⚠️ 警告: 找不到图标文件 {icon_file_path}")
                self.icons[level] = None
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
                        'specific_domain': row[23].strip() if len(row) > 23 else '',
                        'domain_category': row[24].strip() if len(row) > 24 else ''  # 大分类
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
                                  image_width=16, image_height=22, dpi=300):
        """
        创建包含全部41篇论文的完整表格图片
        
        Args:
            save_path: 保存路径
            image_width: 图片宽度（英寸）
            image_height: 图片高度（英寸）
            dpi: 分辨率
        """
        # 创建紧凑图形以减少留白
        fig, ax = plt.subplots(figsize=(image_width, image_height), dpi=dpi)
        ax.set_xlim(0, 84)  # 扩大坐标范围以容纳所有列
        ax.set_ylim(0, 80)  # 缩小坐标范围
        ax.axis('off')
        
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
        # 表头位置设置 - 为41行数据优化（紧凑布局）
        header_y = 75
        header_height = 2.5
        col_widths = [2.5, 14, 3.5, 3, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 4.7, 9.5]  # Specific Domain从8增加到10.7 (增加1/3)
        
        # 计算列位置
        col_positions = []
        current_x = 1  # 缩小左边距（从2减少到1）
        for width in col_widths:
            col_positions.append(current_x)
            current_x += width
        
        # 绘制第一行表头
        self._draw_header_cell(ax, col_positions[0], header_y, col_widths[0], header_height, 
                              'Cite', self.colors['header_basic'])
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
        
                # Auto Level 和 Specific Domain
        self._draw_header_cell(ax, col_positions[21], header_y, col_widths[21], header_height, 
                               'Auto Level', self.colors['header_auto'])
        self._draw_header_cell(ax, col_positions[22], header_y, col_widths[22], header_height, 
                               'Specific Domain', self.colors['header_domain'])
        
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
               ha='center', va='center', fontsize=16, fontweight='bold', 
               color='white')

    def _wrap_text(self, text, max_width, fontsize=10, word_based=False):
        """文本自动换行功能"""
        import textwrap
        
        # 更准确的字符宽度估算
        # 对于8号字体，每个字符大约占0.15个单位宽度
        char_width = fontsize * 0.04
        
        # 计算每行能容纳的字符数
        chars_per_line = max(1, int(max_width / char_width))
        
        # 使用textwrap进行换行
        wrapped_lines = textwrap.wrap(text, width=chars_per_line)
        return wrapped_lines

    def _draw_complete_table_data(self, ax):
        """绘制所有41篇论文的数据"""
        # 数据行设置 - 优化为紧凑布局
        row_height = 1.6  # 减小行高以容纳更多数据
        start_y = 75 - 5  # 表头下方（紧凑布局）
        col_widths = [2.5, 14, 3.5, 3, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 2.5, 4.7, 9.5]  # 与表头保持一致
        
        # 计算列位置
        col_positions = []
        current_x = 1  # 缩小左边距（从2减少到1）
        for width in col_widths:
            col_positions.append(current_x)
            current_x += width
        
        # 按年份排序数据
        sorted_data = sorted(self.data, key=lambda x: int(x['year']) if x['year'].isdigit() else 9999)
        
        for i, paper in enumerate(sorted_data):
            row_y = start_y - (i * row_height)
            
            # 获取BibTeX风格的引用序号
            citation_number = self.citation_manager.get_paper_citation_number(paper['no'])
            citation_text = f"[{citation_number}]" if citation_number > 0 else str(i + 1)
            
            # 基本信息列 - 清空Cite列内容
            self._draw_data_cell(ax, col_positions[0], row_y, col_widths[0], row_height, 
                               '', self.colors['basic_info'])
            
            # 处理标题长度 - 不超过25则不省略
            title_display = paper['title'][:30] + '...' if len(paper['title']) > 25 else paper['title']
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
            
            # Analogy Process - 使用蓝色
            for value in paper['analogy_process']:
                # 只有空字符视为不支持，其他所有字符都视为支持
                if value.strip() == '':
                    color = self.colors['not_supported']
                    symbol = '×'
                else:
                    color = self.colors['analogy_supported']
                    symbol = '✓'
                self._draw_data_cell(ax, col_positions[col_idx], row_y, col_widths[col_idx], 
                                   row_height, symbol, color)
                col_idx += 1

            # Create Process - 使用粉色
            for value in paper['create_process']:
                if value.strip() == '':
                    color = self.colors['not_supported']
                    symbol = '×'
                else:
                    color = self.colors['create_supported']
                    symbol = '✓'
                self._draw_data_cell(ax, col_positions[col_idx], row_y, col_widths[col_idx], 
                                   row_height, symbol, color)
                col_idx += 1

            # Representation - 使用橙色
            for value in paper['representation']:
                if value.strip() == '':
                    color = self.colors['not_supported']
                    symbol = '×'
                else:
                    color = self.colors['representation_supported']
                    symbol = '✓'
                self._draw_data_cell(ax, col_positions[col_idx], row_y, col_widths[col_idx], 
                                   row_height, symbol, color)
                col_idx += 1
            # Auto Level 和 Domain - 使用图标
            automation_level = paper['automation'].strip().lower()
            if automation_level in self.icons and self.icons[automation_level] is not None:
                # 绘制图标
                self._draw_icon_cell(ax, col_positions[21], row_y, col_widths[21], row_height, 
                                   self.icons[automation_level])
            else:
                # 如果图标不存在，使用文字
                self._draw_data_cell(ax, col_positions[21], row_y, col_widths[21], row_height, 
                                   paper['automation'], self.colors['auto'])
            
            # 翻译specific domain为英文 - 使用小字体和自动换行，并根据大分类设置背景颜色
            specific_domain_en = self.translate_domain(paper['specific_domain'])
            
            # 根据大分类确定背景颜色 - 统一调整为80%透明度
            domain_category = paper.get('domain_category', '').strip()
            if 'Creative Industries' in domain_category:
                bg_color = self.colors['domain_creative']
            elif 'Intelligent Manufacturing' in domain_category:
                bg_color = self.colors['domain_manufacturing']
            elif 'Education and Service Industries' in domain_category:
                bg_color = self.colors['domain_education']
            else:
                bg_color = self.colors['domain']  # 默认颜色
            
            # 为Specific Domain列添加50%透明度
            bg_color_with_alpha = bg_color + '80'  # 添加50%透明度 (80 = 128/255 ≈ 50%)
            
            self._draw_data_cell(ax, col_positions[22], row_y, col_widths[22], row_height, 
                               specific_domain_en, bg_color_with_alpha, align='left', fontsize=11, wrap_text=True)

    def _draw_data_cell(self, ax, x, y, width, height, text, color, align='center', fontsize=12, wrap_text=False):
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
        
        if wrap_text and len(str(text)) > 10:  # 降低换行阈值
            # 换行处理
            wrapped_lines = self._wrap_text(str(text), width, fontsize)
            
            # 改进的行间距计算 - 向下自左向右换行
            if len(wrapped_lines) > 1:
                # 多行文本 - 从顶部开始向下排列
                line_spacing = height / (len(wrapped_lines) + 0.9)  # 增加间距
                for i, line in enumerate(wrapped_lines):
                    line_y = y + height - (i + 1) * line_spacing  # 从顶部开始向下
                    ax.text(text_x, line_y, line, 
                           ha=ha, va='center', fontsize=fontsize, fontweight=fontweight, 
                           color=text_color)
            else:
                # 单行文本
                ax.text(text_x, y + height/2, str(text), 
                       ha=ha, va='center', fontsize=fontsize, fontweight=fontweight, 
                       color=text_color)
        else:
            # 普通文本显示
            ax.text(text_x, y + height/2, str(text), 
                   ha=ha, va='center', fontsize=fontsize, fontweight=fontweight, 
                   color=text_color)

    def _draw_icon_cell(self, ax, x, y, width, height, icon_img):
        """绘制包含图标的单元格"""
        # 绘制背景
        rect = Rectangle((x, y), width, height, 
                        facecolor=self.colors['auto'], edgecolor=self.colors['border'], 
                        linewidth=0.3)
        ax.add_patch(rect)
        
        # 计算图标位置和大小 - 固定90x90像素
        icon_x = x + width/2
        icon_y = y + height/2
        
        # 计算缩放比例 - 目标像素大小（增加10%）
        target_size = 20  # 目标像素大小（从15增加到16.5，增加10%）
        # 获取图片的原始尺寸
        img_height, img_width = icon_img.shape[:2]
        # 计算缩放比例，取较小的缩放比例确保图片完整显示
        scale_factor = min(target_size / img_width, target_size / img_height)
        
        # 创建OffsetImage，使用计算出的缩放比例
        imagebox = OffsetImage(icon_img, zoom=scale_factor)
        ab = AnnotationBbox(imagebox, (icon_x, icon_y), 
                           frameon=False, box_alignment=(0.5, 0.5))
        ax.add_artist(ab)

    def _draw_bottom_legend(self, ax):
        """在表格下方绘制图例"""
        # 图例位置 - 在表格数据下方，紧凑布局
        legend_start_y = 75 - 5 - (len(self.data) * 1.5) - 1.7  # 紧凑布局
        
        # 新的图例内容 - 5列布局，单行格式，删除icon
        legend_items = [
            ("Analogy Process", [
                "Enc = Encoding/Representation",
                "Ret = Retrieval", 
                "Map = Mapping",
                "Eva = Evaluation"
            ], self.colors['analogy_supported']),
            ("Create Process", [
                "Vis = Vision",
                "Ins = Inspiration", 
                "Ide = Ideation",
                "Pro = Prototype",
                "Fab = Fabrication",
                "Eva = Evaluation",
                "Met = Meta"
            ], self.colors['create_supported']),
            ("Representation", [
                "Txt = Text",
                "Vis = Visual",
                "Str = Structure", 
                "Fun = Function",
                "Wor = Workflow",
                "Unc = Unconventional"
            ], self.colors['representation_supported']),
            ("Domain Categories", [
                "Creative Industries",
                "Intelligent Manufacturing", 
                "Education & Service"
            ], '#d1d871'),
            ("Symbols & Icons", [
                "✓ = Supported",
                "× = Not Supported",
                "Bot = Automate",
                "Handshake = Augment", 
                "Wrench = Assist"
            ], '#203F9A')
        ]
        
        # 绘制5个图例卡片
        card_width = 16  # 前四个卡片宽度增加1/3 (从12到16)
        card_height = 5  # 从10减少1/2到5
        start_x = 2  # 缩小左边距（从4减少到2）
        
        for i, (title, items, color) in enumerate(legend_items):
            if i == 1:  # Create Process卡片
                current_width = 16  # 增加1/3 (从12到16)
                spacing = 17  # 相应调整间距
            elif i == 2:  # Representation卡片
                current_width = 16  # 增加1/3 (从12到16)
                spacing = 17 # 相应调整间距
            elif i < 4:  # 其他前两个卡片
                current_width = 12  # 保持原有宽度
                spacing = 13  # 相应调整间距
            else:  # 最后一个卡片
                current_width = 19  # 增加1/6 (从16到19)
                spacing = 20  # 相应调整间距
            
            card_x = start_x + sum([13 if j < 4 and j != 1 and j != 2 else 17 for j in range(i)])  # 动态计算位置
            card_y = legend_start_y - 6.5  # 调整位置，适应新高度
            
            # 卡片标题（删除背景，文字颜色改为对应颜色）
            ax.text(card_x + current_width/2, card_y + card_height - 0.5, title, 
                   ha='center', va='center', fontsize=12, fontweight='bold',
                   color=color)
            
            # 卡片内容 - 根据卡片类型选择布局
            if i == 1 or i == 2:  # Create Process和Representation卡片 - 两列排布
                # 计算每列的项目数
                items_per_column = (len(items) + 1) // 2
                for j, item in enumerate(items):
                    if j < items_per_column:  # 左列
                        col_x = card_x + 1
                        row_y = card_y + card_height - 1.6 - (j * 0.8)  # 缩小1/5距离
                    else:  # 右列
                        col_x = card_x + current_width/2 + 0.5  # 进一步减少列间距（从0.7减少到0.5）
                        row_y = card_y + card_height - 1.6 - ((j - items_per_column) * 0.8)  # 缩小1/5距离
                    ax.text(col_x, row_y, f"• {item}", 
                           ha='left', va='center', fontsize=12, color='#2c3e50')
            elif i == 3:  # Domain Categories卡片 - 带颜色矩形
                for j, item in enumerate(items):
                    # 绘制颜色矩形
                    color_map = {
                        "Creative Industries": self.colors['domain_creative'],
                        "Intelligent Manufacturing": self.colors['domain_manufacturing'],
                        "Education & Service": self.colors['domain_education']
                    }
                    rect_color = color_map.get(item, '#d1d871')
                    rect = Rectangle((card_x + 1, card_y + card_height - 1.6 - (j * 0.8) - 0.3), 1.5, 0.6, 
                                   facecolor=rect_color, edgecolor=self.colors['border'], linewidth=0.5)
                    ax.add_patch(rect)
                    # 绘制文字
                    ax.text(card_x + 3, card_y + card_height - 1.6 - (j * 0.8), f"= {item}", 
                           ha='left', va='center', fontsize=12, color='#2c3e50')
            elif i == 4:  # Symbols & Icons卡片 - 两列排布，使用图标
                for j, item in enumerate(items):
                    if j < 2:  # 左列：前两行内容 (Supported相关)
                        col_x = card_x + 1
                        row_y = card_y + card_height - 1.6 - (j * 0.8)
                        ax.text(col_x, row_y, f"• {item}", 
                               ha='left', va='center', fontsize=12, color='#2c3e50')
                    else:  # 右列：后三行内容 (Automated相关) - 使用图标
                        col_x = card_x + current_width/2 + 0.75  # 减少1/4列间距
                        row_y = card_y + card_height - 1.6 - ((j - 2) * 0.8)
                        
                        # 根据内容选择图标
                        icon_mapping = {
                            "Bot = Automate": "automate",
                            "Handshake = Augment": "augment", 
                            "Wrench = Assist": "assist"
                        }
                        
                        if item in icon_mapping and icon_mapping[item] in self.icons:
                            # 绘制图标
                            icon_img = self.icons[icon_mapping[item]]
                            if icon_img is not None:
                                # 计算图标位置和大小
                                icon_size = 0.15  # 图标大小
                                icon_x = col_x
                                icon_y = row_y  # 与文字在同一水平线上
                                
                                # 创建OffsetImage
                                from matplotlib.offsetbox import OffsetImage, AnnotationBbox
                                im = OffsetImage(icon_img, zoom=icon_size)
                                ab = AnnotationBbox(im, (icon_x, icon_y), 
                                                   frameon=False, box_alignment=(0, 0.5))
                                ax.add_artist(ab)
                                
                                # 在图标右侧添加文字
                                ax.text(col_x + 1.5, row_y, f"= {item.split(' = ')[1]}", 
                                       ha='left', va='center', fontsize=12, color='#2c3e50')
                            else:
                                ax.text(col_x, row_y, f"• {item}", 
                                       ha='left', va='center', fontsize=12, color='#2c3e50')
                        else:
                            ax.text(col_x, row_y, f"• {item}", 
                                   ha='left', va='center', fontsize=12, color='#2c3e50')
            else:  # 其他卡片 - 单列排布
                for j, item in enumerate(items):
                    ax.text(card_x + 1, card_y + card_height - 1.6 - (j * 0.8), f"• {item}", 
                           ha='left', va='center', fontsize=12, color='#2c3e50')
        

        


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
        
        # 打印BibTeX风格的引用报告
        print(f"\n{self.citation_manager.generate_citation_report()}")


def main():
    """主函数"""
    print("🎨 完整41篇论文表格图片生成器")
    print("=" * 50)
    
    # 使用你的CSV文件
    csv_file = "paper-process-4-vis-2.csv"
    
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