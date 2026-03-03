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

# 飞书 Webhook URL（必需）
FEISHU_WEBHOOK=https://open.feishu.cn/open-apis/bot/v2/hook/xxx

# LLM API Key（必需）
LLM_API_KEY=your_siliconflow_api_key

### 📝 输出示例
🤖 AI 日报 2026-03-03

🚀 AI 技术新闻
1. ⚔️AI 助手的 "硬件实体"，还能怎么变？
   链接：https://www.huxiu.com/article/4838118.html
   概况：探讨 AI 助手硬件形态的创新发展，分析 AI 与硬件结合的新趋势和可能性。

2. 🎯 GPT-5 训练启动，OpenAI 开支创新高
   链接：https://36kr.com/article/xxxx
   概况：OpenAI 启动 GPT-5 训练计划，年度开支突破历史新高...

💻 AI 开源项目
1. 🛠️ DeepSeek-V3 - 最强开源大模型
   链接：https://github.com/deepseek-ai/DeepSeek-V3
   概况：512K token 上下文，多语言支持，性能超越 GPT-4，完全开源可商用。
