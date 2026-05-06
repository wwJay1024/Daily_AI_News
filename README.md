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
- Python 3.10+
- 一个 LLM API Key
- 一个飞书机器人 Webhook

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/wwJay1024/Daily_AI_News.git
cd Daily_AI_News

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
export FEISHU_WEBHOOK="你的飞书webhook"
export LLM_API_KEY="你的LLM_API_KEY"

# 运行
python main.py
```

### GitHub Actions 自动定时运行
1️⃣ 在仓库添加 Secrets  
进入：  
Settings → Secrets and variables → Actions → New repository secret  
添加以下两个：  
Name	Value  
FEISHU_WEBHOOK —— 你的飞书机器人 webhook  
LLM_API_KEY —— 你的LLM API Key  
⚠️ 必须添加到 Secrets，不要添加到 Variables。  

2️⃣ 定时规则说明  
在 .github/workflows/schedule.yml 中：  
cron: '0 0 * * *'  
表示：  
UTC 00:00 = 北京时间 08:00  
UTC 01:00 = 北京时间 09:00  
如果要修改时间，可自行调整 cron。  

3️⃣ 手动测试  
进入仓库 → Actions →  
选择 workflow → 点击 Run workflow  
查看日志确认是否运行成功。  


### 日报示例
🤖 AI 日报 2026-05-05

🚀 AI 技术新闻
🤖 DeepSeek多模态技术范式公布，以视觉原语思考
提出全新多模态技术范式，让AI像人类一样用视觉原语思考。

🔍 DeepSeek给AI装了根赛博手指，于是它能看见了
突破性研究让AI不仅能”看见”，更能理解视觉信息，实现质的飞跃。

💼 CTO不香了？百亿公司高管们为何集体转身，去Anthropic当工程师
顶尖人才涌向AI一线研发，凸显大模型技术核心地位与权力转移。

💔 “今日头条鼻祖”BuzzFeed要破产了
AI冲击传统内容分发模式，标志着一个媒体时代的终结。

🛒 苹果悄悄砍掉丐版Mac mini，人人都要交「AI 税」的时代来了
硬件升级强制为AI买单，预示AI算力正成为基础消费成本。


🤖 Agent与工作流
🎨 open-design - 开源设计
本地优先的Claude Design开源替代品，集成19种技能与71个设计系统，支持生成网页、桌面、移动端原型及幻灯片。

🛠️ harmonist - 和谐协调器
便携式AI智能体编排框架，具有机械协议强制执行能力，包含186个智能体且无运行时依赖。

🚂 wanman - 一人列车
受日本一人列车启发的开源智能体矩阵运行时，协调自主多智能体工作流、任务执行和工件生成。

📈 trading-agents - 交易智能体
用于金融交易的多智能体系统，支持股票、加密货币的算法交易和情感分析。

🌐 world2agent - 世界到智能体
一个开放协议，用于标准化AI智能体感知现实世界的方式。


🔧 Skill
📖 oh-story-claudecode - 网文写作技能包
覆盖长篇与短篇网络小说全流程的写作技能包，包括扫榜、拆文、写作、去AI味和封面图生成。

🔧 opencode-power-pack - OpenCode增强包
将11个Claude Code技能移植到OpenCode，包括代码审查、安全审计、功能开发等，一键配置。

🔍 google-surf-mcp - 谷歌搜索MCP
无需API密钥的反机器人搜索MCP服务器，通过Playwright实现谷歌搜索。

📊 ian-handdrawn-ppt - 手绘PPT技能
中文手绘风格技术PPT整页图像生成技能，支持21:9封面和16:9正文配图，输出PNG格式。

💱 agent-trade-kit - 智能体交易套件
通过MCP协议将AI助手连接到OKX账户的MCP服务器和CLI工具，本地运行。


🚀 AI应用
📱 Aether - 以太
一款美观、本地化的通用AI智能体Android应用程序。

🖼️ Stable-Diffusion-AI-Free - 免费稳定扩散AI
免费的Stable Diffusion AI图像生成器，支持本地部署、实时视频、角色一致性、LoRA训练等多种功能。

📽️ open-slide - 开放幻灯片
一个专为智能体构建的幻灯片框架。

📱 baguette - 法棍
无头iOS模拟器管理器/农场，支持主机端输入注入，实现点击、滑动、多指手势和60fps流式传输。

🧩 shapez-2-simulated-3d-factory-optimizer - Shapez 2工厂优化器
Shapez 2多人游戏的终极工厂自动化与蓝图共享中心，包含3D工厂模拟和优化工具。
