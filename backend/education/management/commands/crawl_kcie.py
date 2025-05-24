import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from education.models import NewsItem
from datetime import datetime

class Command(BaseCommand):
    help = '전국투자자교육협의회 금융 콘텐츠 크롤링'

    def handle(self, *args, **kwargs):
        url = "https://www.kcie.or.kr/guide/series/2/53/"
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        articles = soup.select('ul.list-type1 > li')

        for article in articles[:10]:  # 상위 10개만 수집
            try:
                title = article.select_one('.tit').text.strip()
                url_suffix = article.select_one('a')['href']
                full_url = "https://www.kcie.or.kr" + url_suffix
                summary = article.select_one('.txt').text.strip()
                thumbnail = article.select_one('img')['src']
                published_at = datetime.today().date()  # 날짜 정보 없음

                if NewsItem.objects.filter(title=title, url=full_url).exists():
                    continue

                NewsItem.objects.create(
                    title=title,
                    summary=summary,
                    url=full_url,
                    thumbnail=thumbnail,
                    published_at=published_at,
                    source="전국투자자교육협의회",
                    category="금융교육"
                )

                self.stdout.write(self.style.SUCCESS(f'Saved: {title}'))

            except Exception as e:
                self.stderr.write(f'Error: {e}')
