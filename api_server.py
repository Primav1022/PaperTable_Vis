from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import pandas as pd
import json
from pathlib import Path
from domain_map import DOMAIN_ZH2EN

app = Flask(__name__)
CORS(app)  # 允许跨域请求

class DataAPI:
    def __init__(self):
        self.csv_file = "paper-process-4-vis.csv"
        self.data = []
        self.load_csv_data()
    
    def load_csv_data(self):
        """加载CSV数据"""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            for i, line in enumerate(lines[2:], start=3):
                row = [cell.strip() for cell in line.split(',')]
                if len(row) > 5 and row[0] and row[0].strip():
                    paper_data = {
                        'no': int(row[0].strip()),
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
            
            print(f"✅ API服务器加载了 {len(self.data)} 篇论文数据")
            
        except Exception as e:
            print(f"❌ API数据加载失败: {e}")
    
    def get_papers_data(self):
        """获取论文数据"""
        return self.data
    
    def get_statistics(self):
        """获取统计数据"""
        if not self.data:
            return {}
        
        venues = {}
        years = {}
        auto_levels = {}
        
        for paper in self.data:
            venues[paper['venue']] = venues.get(paper['venue'], 0) + 1
            years[paper['year']] = years.get(paper['year'], 0) + 1
            auto_levels[paper['automation']] = auto_levels.get(paper['automation'], 0) + 1
        
        return {
            'total_papers': len(self.data),
            'venues': venues,
            'years': years,
            'auto_levels': auto_levels
        }

# 初始化数据API
data_api = DataAPI()

@app.route('/api/papers', methods=['GET'])
def get_papers():
    """获取所有论文数据"""
    return jsonify(data_api.get_papers_data())

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取统计数据"""
    return jsonify(data_api.get_statistics())

@app.route('/api/generate-image', methods=['POST'])
def generate_image():
    """生成图片"""
    try:
        from complete_41_papers_generator import Complete41PapersTableGenerator
        
        # 获取参数
        data = request.get_json()
        image_type = data.get('type', 'publication')  # publication 或 presentation
        
        # 创建生成器
        generator = Complete41PapersTableGenerator("paper-process-4-vis.csv")
        
        # 生成图片
        if image_type == 'publication':
            filename = "complete_41_papers_publication.png"
            generator.create_publication_ready_image(filename)
        else:
            filename = "complete_41_papers_presentation.png"
            generator.create_presentation_image(filename)
        
        # 返回图片文件
        return send_file(filename, mimetype='image/png')
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/')
def index():
    """返回HTML页面"""
    return send_file('表格生成器.html')

if __name__ == '__main__':
    print("🚀 启动API服务器...")
    print("📊 访问 http://localhost:8081 查看表格")
    print("🔗 API端点:")
    print("   GET /api/papers - 获取论文数据")
    print("   GET /api/statistics - 获取统计数据")
    print("   POST /api/generate-image - 生成图片")
    app.run(debug=True, host='0.0.0.0', port=8081) 