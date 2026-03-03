import requests
from bs4 import BeautifulSoup

# 测试36氪页面结构
TARGET_URL = "https://36kr.com/information/AI/"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://36kr.com/",
    "Accept-Language": "zh-CN,zh;q=0.9"
}

try:
    print("正在访问36氪...")
    response = requests.get(TARGET_URL, headers=headers, timeout=15)
    print(f"状态码: {response.status_code}")
    print(f"响应长度: {len(response.text)}")
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 测试原有选择器
    print("\n=== 测试原有选择器 ===")
    items = soup.select('.information-flow-item')
    print(f"找到 .information-flow-item: {len(items)} 个")
    
    # 尝试其他可能的选择器
    print("\n=== 尝试其他可能的选择器 ===")
    
    # 查找所有可能包含文章的容器
    candidates = [
        ('.information-flow-item', '原始选择器'),
        ('.article-item', '简化选择器'),
        ('article', 'article标签'),
        ('[data-et-view]', 'data属性'),
        ('.feed-item', 'feed-item'),
        ('.information-item', 'information-item'),
    ]
    
    for selector, desc in candidates:
        elements = soup.select(selector)
        print(f"{desc} ({selector}): {len(elements)} 个")
        if elements and len(elements) > 0:
            print(f"  第一个元素: {str(elements[0])[:200]}...")
    
    # 打印所有可能包含标题和链接的元素
    print("\n=== 寻找所有链接 ===")
    all_links = soup.find_all('a', limit=20)
    for i, link in enumerate(all_links[:10]):
        print(f"{i+1}. href={link.get('href')}, text={link.get_text(strip=True)[:50]}")
    
    # 保存完整HTML用于分析
    with open('/Users/wwj/Desktop/做点开发/每日AI新闻-发送飞书/Daily_AI_News/36kr_response.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("\n✅ 完整响应已保存到 36kr_response.html")
    
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
