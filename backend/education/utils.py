# backend/education/utils.py

import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from datetime import timedelta

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
                from django.utils.timezone import make_aware, get_current_timezone
                return make_aware(dt, get_current_timezone())
            return dt
        except Exception:
            pass

    return None


def crawl_news_page(page: int):
    """
    page 숫자에 해당하는 네이버 속보 뉴스 페이지만 크롤링해서
    dict 리스트를 반환합니다.
    """
    base_url = f"https://news.naver.com/breakingnews/section/101/259?page={page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    placeholder = "https://dummyimage.com/120x80/cccccc/ffffff&text=No+Image"

    resp = requests.get(base_url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    items = []

    for art in soup.select("div.section_article ul.sa_list > li.sa_item"):
        title_tag = art.select_one("a.sa_text_title > strong.sa_text_strong")
        url_tag   = art.select_one("a.sa_text_title")
        lede_tag  = art.select_one("div.sa_text_lede")
        press_tag = art.select_one("div.sa_text_press")
        dt_tag    = art.select_one("div.sa_text_datetime")
        thumb_img = art.select_one("div.sa_thumb img")

        title = title_tag.get_text(strip=True) if title_tag else ""
        url   = url_tag["href"] if url_tag else ""
        lede  = lede_tag.get_text(strip=True) if lede_tag else ""
        press = press_tag.get_text(strip=True) if press_tag else ""
        raw_dt= dt_tag.get_text(strip=True) if dt_tag else ""
        published = parse_korean_datetime(raw_dt) or raw_dt

        # 썸네일 추출
        if thumb_img:
            thumbnail = (
                thumb_img.get("data-src")
                or thumb_img.get("data-lazy-src")
                or thumb_img.get("src")
                or placeholder
            )
        else:
            thumbnail = placeholder

        items.append({
            "title":       title,
            "url":         url,
            "lede":        lede,
            "press":       press,
            "published_at": published,
            "thumbnail":   thumbnail,
        })

    return items
