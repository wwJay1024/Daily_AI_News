#!/usr/bin/env python3
"""测试Selenium获取36氪数据"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

TARGET_URL = "https://36kr.com/information/AI/"

def test_selenium_fetch():
    """测试Selenium获取36氪"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    
    driver = None
    try:
        print("🚀 启动Selenium浏览器...")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print(f"📄 访问: {TARGET_URL}")
        driver.get(TARGET_URL)
        
        print("⏳ 等待页面加载...")
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "feed-item"))
            )
            print("✅ 页面加载成功")
        except Exception as e:
            print(f"⚠️ 等待超时: {e}")
        
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # 测试不同选择器
        selectors = [
            ('.feed-item', 'feed-item'),
            ('[data-feed-id]', 'data-feed-id'),
            ('.article-list-item', 'article-list-item'),
            ('article', 'article标签'),
            ('.information-item', 'information-item'),
        ]
        
        print("\n=== 测试选择器 ===")
        for selector, name in selectors:
            items = soup.select(selector)
            print(f"{name} ({selector}): {len(items)} 个")
        
        # 获取所有链接
        print("\n=== 前10个链接 ===")
        all_links = soup.find_all('a', limit=20)
        for i, link in enumerate(all_links[:10], 1):
            href = link.get('href', '无')
            text = link.get_text(strip=True)[:50]
            print(f"{i}. {text} -> {href}")
        
        # 尝试提取文章
        print("\n=== 尝试提取文章 ===")
        items = soup.select('.feed-item')
        print(f"找到 {len(items)} 个feed-item")
        
        for i, item in enumerate(items[:5], 1):
            title = item.select_one('h2') or item.select_one('a')
            print(f"\n{i}. {item.get('class')}")
            if title:
                print(f"   标题: {title.get_text(strip=True)[:50]}")
        
        # 保存HTML
        with open('/Users/wwj/Desktop/做点开发/每日AI新闻-发送飞书/Daily_AI_News/36kr_selenium.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print("\n✅ 完整HTML已保存到 36kr_selenium.html")
        
    except Exception as e:
        print(f"❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

if __name__ == "__main__":
    test_selenium_fetch()
