import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from education.models import NewsItem
from datetime import datetime

class Command(BaseCommand):
    help = '금융위원회 카드뉴스 크롤링'

    def handle(self, *args, **kwargs):
        url = "https://www.fsc.go.kr/edu/cardnews"
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        cards = soup.select('ul.edu_card_list li')

        for card in cards[:10]:
            try:
                anchor = card.select_one('a')
                title = anchor.select_one('.edu_title').text.strip()
                url_suffix = anchor['href']
                full_url = "https://www.fsc.go.kr" + url_suffix
                summary = anchor.select_one('.edu_txt').text.strip()
                thumbnail = card.select_one('img')['src']
                published_at = datetime.today().date()  # 카드뉴스는 날짜 없음

                if NewsItem.objects.filter(title=title, url=full_url).exists():
                    continue

                NewsItem.objects.create(
                    title=title,
                    summary=summary,
                    url=full_url,
                    thumbnail=thumbnail,
                    published_at=published_at,
                    source="금융위원회",
                    category="카드뉴스"
                )

                self.stdout.write(self.style.SUCCESS(f'Saved: {title}'))

            except Exception as e:
                self.stderr.write(f'Error: {e}')
