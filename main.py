import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import os

# ================= 配置区 =================
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = "https://api.siliconflow.cn/v1" 
TARGET_URL = "https://36kr.com/information/AI/"

# ================= 辅助函数 =================

# ================= 数据获取模块 =================

def get_36kr_ai_news():
    """解析36氪AI频道页面"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(TARGET_URL, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = []
        # 36氪文章通常在 information-flow-item 中
        items = soup.select('.information-flow-item')
        
        for item in items:
            title_node = item.select_one('.article-item-title')
            desc_node = item.select_one('.article-item-description')
            link_node = item.select_one('.article-item-title')
            
            if title_node and link_node:
                title = title_node.get_text(strip=True)
                desc = desc_node.get_text(strip=True) if desc_node else ""
                href = link_node.get('href')
                link = f"https://36kr.com{href}" if href and href.startswith('/') else href
                
                articles.append({
                    "title": title,
                    "description": desc,
                    "link": link
                })
            print(f"抓取到文章: {title}")
        print(f"已获取 {len(articles)} 篇文章，正在利用大模型筛选...")
        return articles
    except Exception as e:
        print(f"抓取失败: {e}")
        return []

def filter_and_summarize_with_ai(articles):
    """利用大模型从大量新闻中筛选 Top 10 并总结"""
    if not articles:
        return "未能抓取到今日新闻。"

    # 将文章列表转为文本交给 AI
    raw_content = "\n".join([f"标题: {a['title']}\n摘要: {a['description']}\n链接: {a['link']}\n---" for a in articles])
    
    prompt = f"""
    你是一个顶级的AI行业分析师。从以下AI相关新闻中筛选出10条最具突破性、冲击性、价值最大的新闻。
    
    输出要求：
    1. 项目整理格式：[序号.][匹配的Emoji][标题] + [链接] + [概况]
    2. 概况要求：根据新闻标题及摘要总结新闻价值，字数在 30 字以内。
    3. 严格参考以下格式：
        1. ⚔️AI 助手的 "硬件实体"，还能怎么变？
           链接：https://www.huxiu.com/article/4838118.html?f=rss
           概况：探讨 AI 助手硬件形态的创新发展，分析 AI 与硬件结合的新趋势和可能性。
    
    待筛选内容：
    {raw_content}
    """

    headers = {"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-ai/DeepSeek-V3.2",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    try:
        res = requests.post(f"{LLM_BASE_URL}/chat/completions", json=payload, headers=headers)
        return res.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"AI 筛选失败: {e}"


def fetch_github_repos():
    """通过 GitHub API 获取今日热门 AI 开源项目"""
    # 搜索过去一周创建的，包含 ai topic 的项目，按 star 排序
    date_str = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
    url = f"https://api.github.com/search/repositories?q=topic:ai+created:>{date_str}&sort=stars&order=desc"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"GitHub API 请求失败: {response.status_code}")
            return []
        
        items = response.json().get('items', [])[:5] # 取前 5 个最热项目
        if not items:
            return []

        # 2. 准备批量处理的原始数据文本
        raw_info_list = []
        for item in items:
            raw_info_list.append(f"项目原名: {item['name']}\n原描述: {item.get('description', 'No description')}\n链接: {item['html_url']}")
        
        raw_content = "\n---\n".join(raw_info_list)

        # 3. 构造 Prompt 引导大模型按要求格式输出
        prompt = f"""
        你是一个资深的开源项目分析师。将以下 GitHub AI 项目翻译并整理格式。
        
        输出要求：
        1. 项目整理格式：[序号.][匹配的Emoji][项目原名] - [中文项目名] + [项目链接] + [项目概况]
        2. 概况要求：根据原描述总结其核心功能与价值，字数在 40 字以内。
        3. 项目之间空一行
        4. 严格参考以下格式：
           1. 🛠️infra-skills - AI 基础设施技能增强
              链接：https://github.com/xxx
              概况：使用 AI 技术检测植物病害，为西努沙登加拉农民提供智能解决方案，促进农作物健康和提高产量。
           
        待处理项目：
        {raw_content}
        """

        # 4. 调用大模型 (单次请求处理所有项目)
        llm_headers = {"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5
        }
        
        try:
            res = requests.post(f"{LLM_BASE_URL}/chat/completions", json=payload, headers=llm_headers, timeout=20)
            if res.status_code == 200:
                llm_output = res.json()['choices'][0]['message']['content'].strip()
                # 返回处理后的字符串列表（按行拆分或直接作为整段返回）
                return [llm_output]
            else:
                print(f"LLM API 返回错误代码: {res.status_code}, 使用原始项目信息")
                # LLM 失败时，返回原始格式的项目信息
                return format_projects_basic(items)
        except Exception as llm_error:
            print(f"LLM 处理失败 ({type(llm_error).__name__}): {llm_error}，使用原始项目信息")
            # LLM 处理失败（超时等），返回原始格式的项目信息
            return format_projects_basic(items)

    except Exception as e:
        print(f"GitHub 获取失败: {e}")
        return []


def format_projects_basic(items):
    """当LLM调用失败时，返回项目的基本格式"""
    if not items:
        return []
    
    formatted_projects = []
    for i, item in enumerate(items, 1):
        desc = item.get('description', '暂无描述')
        if desc and len(desc) > 40:
            desc = desc[:40] + '...'
        project_info = f"{i}. {item['name']}\n   链接：{item['html_url']}\n   概况：{desc}"
        formatted_projects.append(project_info)
    
    return ["\n\n".join(formatted_projects)]   

# ================= 发送与组装模块 =================

def send_to_feishu(content_text):
    """发送消息到飞书群"""
    payload = {
        "msg_type": "text",
        "content": {
            "text": content_text
        }
    }
    response = requests.post(FEISHU_WEBHOOK, json=payload)
    if response.status_code == 200 and response.json().get("code") == 0:
        print("✅ 飞书消息发送成功")
    else:
        print(f"❌ 发送失败: {response.text}")

def main():
    print("开始抓取今日 AI 资讯...")
    today_str = datetime.now().strftime("%Y-%m-%d")
    # 抓取36kr新闻
    articles = get_36kr_ai_news()
    tech_news = filter_and_summarize_with_ai(articles)
    # 抓取github开源项目
    github = fetch_github_repos()
    
    # 组装最终文本
    report_lines = [f"🤖 AI 日报 {today_str}"]
    
    if tech_news:
        report_lines.append("\n🚀 AI 技术新闻")
        report_lines.append(tech_news)
        
        
    if github:
        report_lines.append("\n💻 AI 开源项目")
        report_lines.extend(github)
        
    final_report = "\n".join(report_lines)
    
    print("\n生成日报如下：\n" + "="*40)
    print(final_report)
    print("="*40)
    
    send_to_feishu(final_report)

if __name__ == "__main__":
    main()
