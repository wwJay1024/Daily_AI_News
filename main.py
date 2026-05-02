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

# GitHub 分类搜索 topic 配置
GITHUB_CATEGORIES = {
    "agent": {
        "label": "Agent与工作流",
        "emoji": "🤖",
        "topics": ["ai-agent", "agent", "workflow", "orchestration", "multi-agent", "automation"],
    },
    "skill": {
        "label": "Skill",
        "emoji": "🔧",
        "topics": ["mcp", "function-calling", "tool-use", "plugin", "skill", "agent-skill"],
    },
    "app": {
        "label": "AI应用",
        "emoji": "🚀",
        "topics": ["chatbot", "text-to-image", "speech-recognition", "ai-app", "no-code", "low-code", "ai-assistant"],
    },
}

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
    """利用大模型从大量新闻中筛选 Top 5 并总结，返回结构化 JSON 列表"""
    if not articles:
        return []

    # 将文章列表转为文本交给 AI
    raw_content = "\n".join([f"标题: {a['title']}\n摘要: {a['description']}\n链接: {a['link']}\n---" for a in articles])
    
    prompt = f"""
    你是一个顶级的AI行业分析师。从以下AI相关新闻中筛选出5条最具突破性、冲击性、价值最大的新闻。
    
    输出要求：
    1. 只返回 JSON 数组，不要返回任何额外文字、markdown、注释。
    2. 数组每个元素必须是对象：{{"title":"", "link":"", "summary":""}}
    3. title 为"Emoji + 标题"，不要序号。
    4. link 使用原文链接。
    5. summary 根据新闻标题及摘要总结新闻价值，30字以内。
    6. 返回 5 条。
    
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


def _search_github_by_topics(topics, per_page=15):
    """按 topic 列表搜索 GitHub 仓库，返回带 star 增速的 item 列表"""
    topic_query = ",".join(topics)
    date_str = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
    url = f"https://api.github.com/search/repositories?q=topic:{topic_query}+created:>{date_str}&sort=stars&order=desc&per_page={per_page}"
    headers = {"Accept": "application/vnd.github.v3+json"}

    response = requests.get(url, headers=headers, timeout=15)
    if response.status_code != 200:
        print(f"GitHub API 请求失败 ({topic_query}): {response.status_code}")
        return []

    items = response.json().get('items', [])
    now = datetime.now()
    for item in items:
        created = datetime.strptime(item['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        days_alive = max((now - created).days, 1)
        item['_stars'] = item['stargazers_count']
        item['_velocity'] = round(item['_stars'] / days_alive, 1)
        item['_topics'] = ", ".join(item.get('topics', []))

    items.sort(key=lambda x: x['_velocity'], reverse=True)
    return items


def _classify_with_llm(candidates):
    """将所有候选项目一次性交给 LLM，统一筛选+分类，返回 {category_key: [items]} 字典"""
    if not candidates:
        return {}

    # 构造候选项目文本
    raw_info_list = []
    for i, item in enumerate(candidates):
        raw_info_list.append(
            f"[{i}] 项目原名: {item['name']}\n"
            f"原描述: {item.get('description', 'No description')}\n"
            f"链接: {item['html_url']}\n"
            f"Stars: {item['_stars']} | 增速: {item['_velocity']} stars/天\n"
            f"Topics: {item['_topics']}"
        )
    raw_content = "\n---\n".join(raw_info_list)

    # 构造分类说明
    cat_desc = "\n".join([
        f'- "{key}": {cat["label"]}（{", ".join(cat["topics"])}）'
        for key, cat in GITHUB_CATEGORIES.items()
    ])

    prompt = f"""
    你是一个资深的开源项目分析师。从以下 GitHub 开源项目中筛选、翻译并分类。

    分类标准：
    {cat_desc}

    输出要求：
    1. 只返回 JSON 对象，不要返回任何额外文字、markdown、注释。
    2. JSON 对象的 key 必须是分类标识：{", ".join(f'"{k}"' for k in GITHUB_CATEGORIES.keys())}
    3. 每个 key 对应一个 JSON 数组，每个元素是 {{"title":"", "link":"", "summary":""}}
    4. title 格式为"Emoji + 项目原名 - 中文项目名"，不要序号。
    5. link 使用项目链接。
    6. summary 根据原描述总结核心功能与价值，40字以内。
    7. 优先选择 star 增速快（新爆发）的项目。
    8. 每个分类最多选 5 条，没有合适的可以为空数组 []。
    9. 每个项目只能归入一个最匹配的分类，不要重复。

    待处理项目：
    {raw_content}
    """

    llm_headers = {"Authorization": f"Bearer {LLM_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "deepseek-ai/DeepSeek-V3.2",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    try:
        res = requests.post(f"{LLM_BASE_URL}/chat/completions", json=payload, headers=llm_headers, timeout=60)
        if res.status_code == 200:
            llm_output = res.json()['choices'][0]['message']['content'].strip()
            parsed = _extract_json_from_llm_output(llm_output)
            if isinstance(parsed, dict):
                return parsed
        print("LLM 分类返回异常，使用基础格式")
    except Exception as e:
        print(f"LLM 分类失败: {e}")

    # 降级：按搜索来源粗分
    fallback = {}
    for key, cat in GITHUB_CATEGORIES.items():
        cat_items = [c for c in candidates if any(t in cat["topics"] for t in c.get("topics", []))]
        if cat_items:
            fallback[key] = format_projects_basic(cat_items[:5])
    return fallback


def fetch_github_repos():
    """分 3 个分类搜索 → 合并去重 → LLM 统一分类，返回 {category_key: items}"""
    # 1. 分类搜索，收集所有候选
    all_candidates = {}  # repo_id -> item，自动去重
    for key, cat in GITHUB_CATEGORIES.items():
        print(f"搜索 GitHub [{cat['label']}]...")
        try:
            items = _search_github_by_topics(cat["topics"], per_page=15)
            for item in items:
                repo_id = item['id']
                if repo_id not in all_candidates:
                    all_candidates[repo_id] = item
            print(f"  [{cat['label']}] 获取 {len(items)} 个项目")
        except Exception as e:
            print(f"  [{cat['label']}] 搜索失败: {e}")

    if not all_candidates:
        return {}

    # 2. 按 star 增速排序，取前 25 个候选
    sorted_items = sorted(all_candidates.values(), key=lambda x: x['_velocity'], reverse=True)
    candidates = sorted_items[:20]
    print(f"去重后共 {len(all_candidates)} 个项目，取增速前 20 个交 LLM 统一分类...")

    # 3. LLM 统一分类
    return _classify_with_llm(candidates)


def format_projects_basic(items):
    """当LLM调用失败时，返回项目的基础结构化格式（含 star 增速）"""
    if not items:
        return []

    formatted_projects = []
    for item in items:
        desc = item.get('description', '暂无描述')
        if desc and len(desc) > 40:
            desc = desc[:40] + '...'
        velocity = item.get('_velocity', 0)
        stars = item.get('_stars', item.get('stargazers_count', 0))
        formatted_projects.append({
            "title": f"⭐ {item['name']}",
            "link": item['html_url'],
            "summary": f"[{stars}★ +{velocity}/天] {desc}"
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

    # 按分类抓取github开源项目
    github_results = fetch_github_repos()

    # 解析为飞书富文本结构
    final_content = []

    if tech_news:
        tech_blocks = build_feishu_post_blocks(
            tech_news,
            "🚀 AI 技术新闻"
        )
        final_content.extend(tech_blocks)

    # 按分类展示 GitHub 项目
    for key, cat in GITHUB_CATEGORIES.items():
        items = github_results.get(key)
        if items:
            blocks = build_feishu_post_blocks(
                items,
                f"{cat['emoji']} {cat['label']}"
            )
            final_content.extend(blocks)

    # 发送
    send_to_feishu(final_content)

if __name__ == "__main__":
    main()
