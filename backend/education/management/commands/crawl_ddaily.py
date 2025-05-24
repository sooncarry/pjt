import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = '디지털데일리 디버깅용 크롤러'

    def handle(self, *args, **kwargs):
        headers = {
            'User-Agent': 'Mozilla/5.0'
        }

        url = 'https://www.ddaily.co.kr/newsAjax?cat=22&page=1'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('li')

        self.stdout.write(self.style.WARNING(f'[DEBUG] 총 {len(articles)}개'))

        for i, article in enumerate(articles[:5]):  # 상위 5개만 확인
            try:
                a_tag = article.select_one('a')
                if not a_tag:
                    self.stdout.write(self.style.ERROR(f'[SKIP {i}] <a> 없음'))
                    continue

                title_tag = a_tag.select_one('strong')
                summary_tag = a_tag.select_one('p.lead')
                date_tag = a_tag.select_one('span.date')

                self.stdout.write(self.style.SUCCESS(f'[{i}]'))
                self.stdout.write(f'  ✅ 제목: {title_tag.text.strip() if title_tag else "❌ 없음"}')
                self.stdout.write(f'  ✅ 요약: {summary_tag.text.strip() if summary_tag else "❌ 없음"}')
                self.stdout.write(f'  ✅ 날짜: {date_tag.text.strip() if date_tag else "❌ 없음"}')

            except Exception as e:
                self.stderr.write(f'[ERROR {i}] {e}')
