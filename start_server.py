#!/usr/bin/env python3
"""
启动API服务器和前端页面
"""

import subprocess
import sys
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """检查依赖是否安装"""
    try:
        import flask
        import flask_cors
        import pandas
        import matplotlib
        import seaborn
        import numpy
        print("✅ 所有依赖已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖: {e}")
        print("请运行: pip install -r requirements.txt")
        return False

def main():
    print("🚀 启动完整41篇论文表格生成器")
    print("=" * 50)
    
    # 检查依赖
    if not check_dependencies():
        return
    
    # 检查必要文件
    required_files = [
        "paper-process-4-vis.csv",
        "complete_41_papers_generator.py", 
        "表格生成器.html",
        "domain_map.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ 缺少必要文件: {', '.join(missing_files)}")
        return
    
    print("✅ 所有必要文件已找到")
    
    # 启动API服务器
    print("\n🌐 启动API服务器...")
    try:
        from api_server import app
        print("📊 服务器地址: http://localhost:8081")
        print("🔗 API端点:")
        print("   GET /api/papers - 获取论文数据")
        print("   GET /api/statistics - 获取统计数据") 
        print("   POST /api/generate-image - 生成图片")
        print("\n💡 功能说明:")
        print("   • 前端页面会自动从API获取数据")
        print("   • 可以生成发表级和演示级图片")
        print("   • 支持数据统计和分析")
        print("\n⏳ 正在启动服务器...")
        
        # 延迟打开浏览器
        def open_browser():
            time.sleep(2)
            webbrowser.open('http://localhost:8081')
        
        import threading
        threading.Thread(target=open_browser).start()
        
        # 启动Flask应用
        app.run(debug=True, host='0.0.0.0', port=8081)
        
    except Exception as e:
        print(f"❌ 启动服务器失败: {e}")
        return

if __name__ == "__main__":
    main() 