from django.core.management.base import BaseCommand
import requests
from bs4 import BeautifulSoup

# 반드시 import!
from education.models import NewsItem

class Command(BaseCommand):
    help = '네이버 금융뉴스 최신기사 크롤링'

    def handle(self, *args, **kwargs):
        url = "https://news.naver.com/breakingnews/section/101/259?page=1"
        headers = {"User-Agent": "Mozilla/5.0"}

        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")

        articles = soup.select("div.section_article ul.sa_list > li.sa_item")
        self.stdout.write(f"총 {len(articles)}개 기사\n")

        save_count = 0
        NewsItem.objects.all().delete()  # **모든 기사 삭제 후 다시 저장**

        for idx, article in enumerate(articles, 1):
            title_tag = article.select_one("a.sa_text_title > strong.sa_text_strong")
            url_tag = article.select_one("a.sa_text_title")
            lede_tag = article.select_one("div.sa_text_lede")
            press_tag = article.select_one("div.sa_text_press")
            datetime_tag = article.select_one("div.sa_text_datetime")
            thumb_img = article.select_one("div.sa_thumb img")

            title = title_tag.text.strip() if title_tag else ""
            url = url_tag['href'] if url_tag else ""
            lede = lede_tag.text.strip() if lede_tag else ""
            press = press_tag.text.strip() if press_tag else ""
            date = datetime_tag.text.strip() if datetime_tag else ""
            # 썸네일 없으면 placeholder (120x80)
            thumbnail = thumb_img['src'] if thumb_img and thumb_img.has_attr('src') else "https://dummyimage.com/120x80/cccccc/ffffff&text=No+Image"

            # 콘솔 출력 (참고용)
            self.stdout.write(f"[{idx}] {title}")
            self.stdout.write(f"    URL: {url}")
            self.stdout.write(f"    요약: {lede}")
            self.stdout.write(f"    언론사: {press}")
            self.stdout.write(f"    작성일시: {date}")
            self.stdout.write(f"    썸네일: {thumbnail}\n")

            # 중복 방지: 전체 삭제 후 저장이므로 unique=True라도 아래만 필요
            NewsItem.objects.create(
                title=title,
                url=url,
                lede=lede,
                press=press,
                published_at=date,
                thumbnail=thumbnail,
            )
            save_count += 1

        self.stdout.write(self.style.SUCCESS(f"\n신규 저장된 기사 수: {save_count}개\n"))
