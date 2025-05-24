# backend/education/management/commands/fetch_news.py

import os
import requests
from email.utils import parsedate_to_datetime
from datetime import datetime
from django.core.management.base import BaseCommand
from django.db import transaction
from dotenv import load_dotenv

from education.models import NewsItem


class Command(BaseCommand):
    help = "Fetch latest finance news for multiple keywords and keep top 100 items."

    def handle(self, *args, **options):
        # 1) Load environment variables from .env
        load_dotenv(dotenv_path=os.path.join(os.getcwd(), '.env'))
        client_id = os.getenv('NAVER_CLIENT_ID')
        client_secret = os.getenv('NAVER_CLIENT_SECRET')
        if not client_id or not client_secret:
            self.stderr.write(self.style.ERROR(
                'NAVER_CLIENT_ID or NAVER_CLIENT_SECRET is not set in .env'
            ))
            return

        headers = {
            'X-Naver-Client-Id':     client_id,
            'X-Naver-Client-Secret': client_secret,
        }
        api_url = 'https://openapi.naver.com/v1/search/news.json'

        # 2) Define finance-related keywords
        KEYWORDS = [
            '금융', '주식', '투자', '증권',
            '은행', '보험', '자산운용', '펀드'
        ]

        # 3) Fetch and dedupe by URL
        unique_items = {}
        for kw in KEYWORDS:
            params = {
                'query':   kw,
                'display': 100,  # max 100 per request
                'start':   1,
                'sort':    'date',
            }
            resp = requests.get(api_url, headers=headers, params=params)
            resp.raise_for_status()
            for it in resp.json().get('items', []):
                link = it.get('originallink')
                if not link or link in unique_items:
                    continue
                # Parse pubDate
                try:
                    pub_dt = parsedate_to_datetime(it.get('pubDate', ''))
                except Exception:
                    pub_dt = datetime.now()
                # Prepare record
                unique_items[link] = {
                    'title':        it.get('title', ''),
                    'summary':      it.get('description', ''),
                    'url':          link,
                    'published_at': pub_dt,
                    'source':       link.split('/')[2] if '//' in link else '',
                    'thumbnail':    '',
                    'category':     '금융',
                }

        # 4) Sort by published_at desc and limit to top 100
        sorted_items = sorted(
            unique_items.values(),
            key=lambda x: x['published_at'],
            reverse=True
        )[:100]
        new_urls = [item['url'] for item in sorted_items]

        # 5) Persist to DB within transaction
        with transaction.atomic():
            # Upsert each
            for data in sorted_items:
                NewsItem.objects.update_or_create(
                    url=data['url'],
                    defaults={
                        'title':        data['title'],
                        'summary':      data['summary'],
                        'published_at': data['published_at'],
                        'source':       data['source'],
                        'thumbnail':    data['thumbnail'],
                        'category':     data['category'],
                    }
                )
            # Delete any items not in the latest top 100 set
            NewsItem.objects.exclude(url__in=new_urls).delete()

        self.stdout.write(self.style.SUCCESS(
            f"[완료] 최신 금융 뉴스 {len(sorted_items)}건 저장 완료"
        ))
