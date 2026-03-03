# 🤖 Daily AI News - AI 日报生成器

一个自动聚合 AI 行业最新资讯和热门开源项目的日报生成工具，每日自动抓取 **36氪 AI 频道**的最新新闻和 **GitHub** 热门 AI 项目，利用大模型智能筛选和总结，最终发送到飞书群聊。

## ✨ 项目特色

- **🌐 多源聚合**：同时获取 36 氪科技新闻和 GitHub 开源项目
- **🤖 AI 智能筛选**：使用深度学习模型（DeepSeek）进行内容筛选和总结
- **📱 飞书集成**：自动将日报发送到飞书群聊
- **🎯 高价值聚焦**：从众多信息中筛选出最有影响力的 Top 10 新闻
- **⚡ 全自动流程**：支持 GitHub Actions 定时运行
- **📊 结构化输出**：带 Emoji 和格式化的专业日报展示

## 🚀 快速开始

### 环境要求
- Python 3.8+
- 依赖库：`requests`, `beautifulsoup4`

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/wwJay1024/Daily_AI_News.git
cd Daily_AI_News

# 安装依赖
pip install -r requirements.txt
