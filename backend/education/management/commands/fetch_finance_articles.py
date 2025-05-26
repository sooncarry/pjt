from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.utils import IntegrityError
from datetime import timedelta
import requests
from bs4 import BeautifulSoup

from education.models import NewsItem

try:
    from dateutil import parser as date_parser
except ImportError:
    date_parser = None


def parse_korean_datetime(text: str):
    text = text.strip()
    now = timezone.now()
    if text.endswith("분전"):
        return now - timedelta(minutes=int(text[:-2]))
    if text.endswith("시간전"):
        return now - timedelta(hours=int(text[:-3]))
    if text.endswith("초전"):
        return now - timedelta(seconds=int(text[:-2]))
    if date_parser:
        try:
            dt = date_parser.parse(text)
            if timezone.is_naive(dt):
                return timezone.make_aware(dt, timezone.get_current_timezone())
            return dt
        except Exception:
            pass
    return None

class Command(BaseCommand):
    help = '네이버 금융뉴스 크롤링 (--page 옵션 지원, 중복 무시)'

    def add_arguments(self, parser):
        parser.add_argument('--page', type=int, help='크롤링할 페이지 번호(생략 시 전체)')

    def handle(self, *args, **options):
        base_url = "https://news.naver.com/breakingnews/section/101/259"
        headers = {"User-Agent": "Mozilla/5.0"}
        placeholder = "https://dummyimage.com/120x80/cccccc/ffffff&text=No+Image"

        total_saved = 0
        # 페이지 옵션이 주어졌으면 하나만, 아니면 1부터 끝까지 순회
        start_page = options.get('page') or 1
        end_page = start_page
        page = start_page

        while True:
            resp = requests.get(f"{base_url}?page={page}", headers=headers)
            soup = BeautifulSoup(resp.text, "html.parser")
            articles = soup.select("div.section_article ul.sa_list > li.sa_item")
            if not articles or page > end_page:
                break

            self.stdout.write(f"[페이지 {page}] 기사 수집: {len(articles)}건")

            for art in articles:
                title = (art.select_one("a.sa_text_title > strong.sa_text_strong") or "").get_text(strip=True)
                link = art.select_one("a.sa_text_title")["href"]
                lede = (art.select_one("div.sa_text_lede") or "").get_text(strip=True)
                press = (art.select_one("div.sa_text_press") or "").get_text(strip=True)
                raw_dt = (art.select_one("div.sa_text_datetime") or "").get_text(strip=True)

                thumb = art.select_one("div.sa_thumb img")
                if thumb:
                    if thumb.has_attr("data-src"):
                        thumbnail = thumb["data-src"]
                    elif thumb.has_attr("data-lazy-src"):
                        thumbnail = thumb["data-lazy-src"]
                    elif thumb.has_attr("src"):
                        thumbnail = thumb["src"]
                    else:
                        thumbnail = placeholder
                else:
                    thumbnail = placeholder

                published_dt = parse_korean_datetime(raw_dt)

                try:
                    obj, created = NewsItem.objects.update_or_create(
                        url=link,
                        defaults={
                            'title': title,
                            'lede': lede,
                            'press': press,
                            'published_at': published_dt,
                            'thumbnail': thumbnail,
                        }
                    )
                    if created:
                        total_saved += 1
                except IntegrityError:
                    continue

            self.stdout.write(self.style.SUCCESS(
                f"[페이지 {page}] 저장 완료 (신규 누적: {total_saved}건)"
            ))

            # 페이지 옵션이 없으면 다음 페이지 순회
            if options.get('page') is None:
                page += 1
            else:
                break

        self.stdout.write(self.style.SUCCESS(
            f"크롤링 완료! 최종 저장된 기사 수: {total_saved}건"
        ))
