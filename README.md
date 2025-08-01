# 📊 完整41篇论文表格生成器

一个集成了Python后端和HTML前端的论文分析工具，用于生成高质量的学术表格和可视化图表。

## 🚀 快速开始

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 启动服务器
```bash
python start_server.py
```

### 3. 访问应用
浏览器会自动打开 `http://localhost:5000`

## 📁 项目结构

```
AnalogyPaper/
├── api_server.py              # Flask API服务器
├── complete_41_papers_generator.py  # Python图片生成器
├── 表格生成器.html            # HTML前端页面
├── paper-process-4-vis.csv    # 论文数据文件
├── domain_map.py              # 领域映射文件
├── requirements.txt            # Python依赖
├── start_server.py            # 启动脚本
└── README.md                  # 项目说明
```

## 🔧 功能特性

### 后端功能 (Python)
- ✅ 从CSV文件读取论文数据
- ✅ 生成高质量PNG图片 (300 DPI)
- ✅ 支持发表级和演示级图片
- ✅ 数据统计和分析
- ✅ RESTful API接口

### 前端功能 (HTML)
- ✅ 交互式表格显示
- ✅ 实时数据统计
- ✅ 多种下载格式 (PNG, SVG, PDF)
- ✅ 响应式设计
- ✅ 美观的学术风格

### API接口
- `GET /api/papers` - 获取所有论文数据
- `GET /api/statistics` - 获取统计数据
- `POST /api/generate-image` - 生成图片

## 🎯 使用说明

### 1. 独立使用Python后端
```bash
python complete_41_papers_generator.py
```

### 2. 独立使用HTML前端
直接打开 `表格生成器.html` 文件

### 3. 集成使用 (推荐)
```bash
python start_server.py
```

## 📊 数据格式

CSV文件应包含以下列：
- 编号 (no)
- 标题 (title)
- 会议 (venue)
- 年份 (year)
- 作者 (author)
- 类比过程 (analogy_process) - 4列
- 创作过程 (create_process) - 7列
- 表示方式 (representation) - 6列
- 自动化级别 (automation)
- 应用领域 (application)
- 领域 (domain)

## 🎨 输出格式

### 图片格式
- **发表级**: 300 DPI, 20×28 英寸
- **演示级**: 200 DPI, 16×22 英寸

### 表格内容
- 基本信息 (编号、标题、会议、年份)
- 类比过程 (编码、检索、映射、评估)
- 创作过程 (愿景、灵感、构思、原型、制作、评估、元认知)
- 表示方式 (文本、视觉、结构、功能、工作流、非常规)
- 自动化级别和领域

## 🔗 联通方式

### 方案1: API接口联通 (当前实现)
- Python后端提供RESTful API
- HTML前端通过fetch调用API
- 支持实时数据更新

### 方案2: 文件共享
- Python生成CSV/JSON文件
- HTML读取本地文件
- 适合离线使用

### 方案3: WebSocket实时通信
- 支持实时数据同步
- 适合多人协作

## 🛠️ 技术栈

### 后端
- **Python 3.8+**
- **Flask** - Web框架
- **Pandas** - 数据处理
- **Matplotlib** - 图片生成
- **Seaborn** - 统计可视化

### 前端
- **HTML5** - 页面结构
- **CSS3** - 样式设计
- **JavaScript** - 交互逻辑
- **html2canvas** - 图片生成

## 📈 扩展功能

### 计划中的功能
- [ ] 数据筛选和搜索
- [ ] 更多图表类型
- [ ] 数据导出功能
- [ ] 用户权限管理
- [ ] 多语言支持

### 自定义开发
- 修改 `complete_41_papers_generator.py` 调整图片样式
- 修改 `表格生成器.html` 调整前端界面
- 修改 `api_server.py` 添加新的API接口

## 🐛 故障排除

### 常见问题

1. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **CSV文件读取错误**
   - 确保文件编码为UTF-8
   - 检查文件路径是否正确

3. **图片生成失败**
   - 确保matplotlib后端正确配置
   - 检查字体文件是否存在

4. **API连接失败**
   - 确保服务器正在运行
   - 检查端口5000是否被占用

## 📄 许可证

本项目仅供学术研究使用。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

---

**作者**: AnalogyPaper Team  
**版本**: 1.0.0  
**更新时间**: 2024年 