import feedparser
import json
import requests
from datetime import datetime

with open("links.json", "r", encoding="utf-8") as f:
    friends = json.load(f)

articles = []
for friend in friends:
    try:
        resp = requests.get(friend["rss"], timeout=8)
        feed = feedparser.parse(resp.text)
        for entry in feed.entries[:4]:
            pub = entry.get("published", datetime.now().isoformat())
            articles.append({
                "blog": friend["name"],
                "blogUrl": friend["url"],
                "avatar": friend["avatar"],
                "title": entry.get("title", "无标题"),
                "link": entry.get("link", ""),
                "date": pub
            })
    except Exception as err:
        print(f"抓取 {friend['name']} 失败: {err}")

articles.sort(key=lambda x: x["date"], reverse=True)
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)
