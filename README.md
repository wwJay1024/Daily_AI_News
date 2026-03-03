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
⚙️马斯克大赞阿里AI，9B参数硬刚120B，海外网友：这叫小模型？【带超链接跳转】  
小参数模型性能挑战大模型，预示模型效率与架构的重大突破。

🔄数据邪修大法好：仅用文本数据就能预训练多模态大模型  
突破多模态训练数据依赖，大幅降低模型训练成本与门槛。

🤖荣耀“转型”：发布Robot Phone和首款人形机器人丨MWC 2026  
消费电子巨头正式入局人形机器人，标志产业融合与竞争升级。

💡告别纯奖励试错，二次尝试+反思蒸馏，复杂任务提升81%  
强化学习新范式显著提升AI复杂任务处理效率，方法学突破。

🌐全球算力格局震荡，“高阶TPU”崛起  
非GPU算力架构挑战英伟达垄断，预示算力基础设施格局生变。


💻 AI 开源项目  
🛠️safepilot - 安全 AI 助手  
一个安全执行实际工作的 AI 助手，旨在可靠地完成任务。

🤖DeepSeek-Claw - DeepSeek-Claw 项目  
项目描述暂无，推测为与 DeepSeek 相关的 AI 工具或模型。

🔧lovable-openclaw - Lovable 开发环境一键配置工具  
macOS 命令行工具，一键安装、配置并验证完整的 Lovable 开发环境。

🧑‍🏫ai-coding-for-beginners - AI 编程入门指南  
面向初学者的 AI 编程学习资源，帮助新手入门 AI 辅助开发。

🛡️OpenAnt - 开源 LLM 漏洞发现工具  
基于大语言模型的开源漏洞发现产品，通过检测与攻击两阶段验证，精准识别安全缺陷
