import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from dotenv import load_dotenv
load_dotenv()
import os
import json

# ================= 配置区 =================
FEISHU_WEBHOOK = os.getenv("FEISHU_WEBHOOK")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_BASE_URL = "https://api.siliconflow.cn/v1" 
TARGET_URL = "https://36kr.com/information/AI/"

# ================= 辅助函数 =================

# ================= 数据获取模块 =================

def _extract_json_from_llm_output(llm_output):
    """
    从 LLM 返回文本中提取 JSON（兼容 ```json 包裹）
    """
    if not llm_output:
        return []

    content = llm_output.strip()
    if content.startswith("```"):
        lines = content.splitlines()
        if len(lines) >= 3 and lines[0].startswith("```") and lines[-1].strip() == "```":
            content = "\n".join(lines[1:-1]).strip()
            if content.startswith("json"):
                content = content[4:].strip()

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        start_positions = [idx for idx, ch in enumerate(content) if ch in "[{"]
        for start in start_positions:
            try:
                parsed, _ = decoder.raw_decode(content[start:])
                return parsed
            except json.JSONDecodeError:
                continue
    return []


def build_feishu_post_blocks(items, section_title):
    """
    将结构化项目列表转换为飞书 post 富文本结构
    """
    if not isinstance(items, list):
        return []

    content_blocks = []

    # 添加分区标题
    content_blocks.append([
        {
            "tag": "text",
            "text": f"\n{section_title}\n"
        }
    ])

    for item in items:
        title = str(item.get("title", "")).strip().replace("**", "")
        link = str(item.get("link", "")).strip()
        summary = str(item.get("summary", "")).strip().replace("**", "")

        if not title or not link or not summary:
            continue

        # 标题作为超链接
        content_blocks.append([
            {
                "tag": "a",
                "text": title,
                "href": link
            }
        ])

        # 概况
        content_blocks.append([
            {
                "tag": "text",
                "text": f"{summary}"
            }
        ])

        # 空行分隔每条新闻/项目
        content_blocks.append([
            {
                "tag": "text",
                "text": "\n"
            }
        ])

    return content_blocks

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
    """利用大模型从大量新闻中筛选 Top 10 并总结，返回结构化 JSON 列表"""
    if not articles:
        return []

    # 将文章列表转为文本交给 AI
    raw_content = "\n".join([f"标题: {a['title']}\n摘要: {a['description']}\n链接: {a['link']}\n---" for a in articles])
    
    prompt = f"""
    你是一个顶级的AI行业分析师。从以下AI相关新闻中筛选出10条最具突破性、冲击性、价值最大的新闻。
    
    输出要求：
    1. 只返回 JSON 数组，不要返回任何额外文字、markdown、注释。
    2. 数组每个元素必须是对象：{{"title":"", "link":"", "summary":""}}
    3. title 为“Emoji + 标题”，不要序号。
    4. link 使用原文链接。
    5. summary 根据新闻标题及摘要总结新闻价值，30字以内。
    6. 返回 10 条。
    
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
        llm_output = res.json()['choices'][0]['message']['content']
        parsed = _extract_json_from_llm_output(llm_output)
        if isinstance(parsed, list):
            return parsed
        return []
    except Exception as e:
        print(f"AI 筛选失败: {e}")
        return []


def fetch_github_repos():
    """通过 GitHub API 获取今日热门 AI 开源项目，返回结构化 JSON 列表"""
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
        1. 只返回 JSON 数组，不要返回任何额外文字、markdown、注释。
        2. 数组每个元素必须是对象：{{"title":"", "link":"", "summary":""}}
        3. title 格式为“Emoji + 项目原名 - 中文项目名”，不要序号。
        4. link 使用项目链接。
        5. summary 根据原描述总结核心功能与价值，40字以内。
        6. 返回 5 条。
           
        待处理项目：
        {raw_content}
        """

        # 4. 调用大模型 (单次请求处理所有项目)
        llm_headers = {"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "deepseek-ai/DeepSeek-V3.2",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5
        }
        
        try:
            res = requests.post(f"{LLM_BASE_URL}/chat/completions", json=payload, headers=llm_headers, timeout=20)
            if res.status_code == 200:
                llm_output = res.json()['choices'][0]['message']['content'].strip()
                parsed = _extract_json_from_llm_output(llm_output)
                if isinstance(parsed, list):
                    return parsed
                print("LLM 返回非 JSON 数组，使用原始项目信息")
                return format_projects_basic(items)
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
    """当LLM调用失败时，返回项目的基础结构化格式"""
    if not items:
        return []
    
    formatted_projects = []
    for item in items:
        desc = item.get('description', '暂无描述')
        if desc and len(desc) > 40:
            desc = desc[:40] + '...'
        formatted_projects.append({
            "title": item['name'],
            "link": item['html_url'],
            "summary": desc
        })
    
    return formatted_projects

# ================= 发送与组装模块 =================

def send_to_feishu(post_content):
    """发送消息到飞书群"""
    payload = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": f"🤖 AI 日报 {datetime.now().strftime('%Y-%m-%d')}",
                    "content": post_content
                }
            }
        }
    }

    response = requests.post(FEISHU_WEBHOOK, json=payload)

    if response.status_code == 200 and response.json().get("code") == 0:
        print("✅ 飞书富文本发送成功")
    else:
        print(f"❌ 发送失败: {response.text}")

def main():
    print("开始抓取今日 AI 资讯...")
    today_str = datetime.now().strftime("%Y-%m-%d")

    # 抓取36kr新闻
    articles = get_36kr_ai_news()
    tech_news = filter_and_summarize_with_ai(articles)

    # 抓取github开源项目
    github_items = fetch_github_repos()

    # 解析为飞书富文本结构
    final_content = []

    if tech_news:
        tech_blocks = build_feishu_post_blocks(
            tech_news,
            "🚀 AI 技术新闻"
        )
        final_content.extend(tech_blocks)

    if github_items:
        github_blocks = build_feishu_post_blocks(
            github_items,
            "💻 AI 开源项目"
        )
        final_content.extend(github_blocks)

    # 4️⃣ 发送
    send_to_feishu(final_content)

if __name__ == "__main__":
    main()
