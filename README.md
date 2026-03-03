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
🤖 AI 日报 2026-03-03

🚀 AI 技术新闻
1. ⚔️刚刚，OpenClaw登顶GitHub软件星标历史第一，已超越Linux  
   链接：https://36kr.com/p/3706534311571843  
   概况：开源AI框架超越Linux，标志AI开发社区力量与趋势发生历史性转变。

2. 🤖九位具身大佬谈：去年量产遭遇了哪些难题，今年落地仍有哪些瓶颈？  
   链接：https://36kr.com/p/3706534449508864  
   概况：行业领袖深度剖析具身机器人量产与落地的核心挑战，指引产业关键方向。

3. 💰融资100亿，机器人狂热背后：明知是泡沫，没人敢不跟  
   链接：https://36kr.com/p/3706464469004421  
   概况：揭示机器人赛道融资狂热与泡沫化风险，反映资本市场的非理性繁荣。

4. 🧠全球算力格局震荡，“高阶TPU”崛起  
   链接：https://36kr.com/p/3706442509365633  
   概况：预示非GPU算力时代开启，可能重塑全球AI基础设施竞争格局。

5. ⚙️编程奇点逼近，程序员斩杀线就在眼前，软件版YouTube时刻在发生  
   链接：https://36kr.com/p/3706354539901061  
   概况：AI编程将极大降低开发门槛，预示“人人都是开发者”的软件生产革命。

💻 AI 开源项目
1. 🛡️safepilot - AI安全执行助手  
链接：https://github.com/3DCF-Labs/safepilot  
概况：AI助手安全执行实际任务，确保操作可靠性。  

2. 🤖DeepSeek-Claw - DeepSeek-Claw  
链接：https://github.com/TriangleMagistrate/DeepSeek-Claw  
概况：功能未描述，推测为DeepSeek相关AI工具或框架。  

3. 🎓ai-coding-for-beginners - AI编程入门  
链接：https://github.com/oujingzhou/ai-coding-for-beginners  
概况：面向初学者的AI编程教程，降低机器学习入门门槛。  

4. 🔍OpenAnt - 开源漏洞探测工具  
链接：https://github.com/knostic/OpenAnt  
概况：基于LLM的两阶段漏洞检测系统，精准识别真实安全威胁。  

5. 🛡️VibeGuard - 隐私防护编码工具  
链接：https://github.com/inkdust2021/VibeGuard  
概况：实时保护编码隐私，防止敏感信息泄露的开发辅助工具。
