import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from synapse.utils.logger import get_logger

load_dotenv()
logger = get_logger(__name__)

class NewsScraper:
    def __init__(self):
        self.base_url = f"https://content.guardianapis.com/search?section=technology&tag=technology/artificialintelligenceai&api-key={os.getenv('GUARDIAN_API_KEY')}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
    def extract(self, date):
        main_data = []
        self.base_url = self.base_url + f"&from-date={date}&to-date={date}"
        response = requests.get(self.base_url)
        if response.status_code == 200:
            data = response.json()
            total_pages = data["response"]["pages"]
            for page in range(1, total_pages + 1):
                response = requests.get(self.base_url + f"&page={page}")
                data = response.json()
                for article in data["response"]["results"]:
                    title = article["webTitle"]
                    url = article["webUrl"]
                    section = article["sectionName"]
                    date = article["webPublicationDate"]

                    content_response = requests.get(url, headers = self.headers)
                    soup = BeautifulSoup(content_response.text, 'html.parser')
                    author = soup.select_one('address a[rel="author"]').get_text(strip=True)
                    tags = [t["title"] for t in soup.select('gu-island[props]')[0]
                            .get("props", "").split('"title":"')[1:]]
                    content = "\n".join(p.get_text(strip=True)
                    for p in soup.select('div.article-body-viewer-selector p'))
                    main_data.append({
                        "title": title,
                        "url": url,
                        "section": section,
                        "date": article["webPublicationDate"],
                        "author": author,
                        "tags": tags,
                        "content": content

                    })
            return main_data
        else:
            logger.error(f"Failed to extract news for {date}")
            return None


if __name__ == "__main__":
    news_scraper = NewsScraper()
    news = news_scraper.extract("2026-01-02")
    import pandas as pd
    pd.DataFrame(news).to_csv("news.csv", index=False)