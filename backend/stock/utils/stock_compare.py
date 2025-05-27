# import yfinance as yf

# def get_stock_comparison_data(code, start_date, end_date):
#     try:
#         suffix = '.KS' if code.startswith('0') else '.KQ'
#         ticker = yf.Ticker(code + suffix)
#         df = ticker.history(start=start_date, end=end_date)

#         if df.empty:
#             return None

#         price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
#         avg_volume = int(df['Volume'].mean())
#         info = ticker.info

#         close_data = [
#             {'date': date.strftime('%Y-%m-%d'), 'close': round(price, 2)}
#             for date, price in df['Close'].items()
#         ]

#         return {
#             'code': code,
#             'name': info.get('shortName', 'Unknown'),
#             'price_change_rate': round(price_change, 2),
#             'avg_volume': avg_volume,
#             'dividend': {
#                 'amount': info.get('dividendRate', 0),
#                 'yield': round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else 0,
#                 'date': info.get('exDividendDate', '-')
#             },
#             'per': info.get('trailingPE', None),
#             'pbr': info.get('priceToBook', None),
#             'market_cap': info.get('marketCap', None),
#             'sector': info.get('sector', '-'),
#             'industry': info.get('industry', '-'),
#             'history': close_data
#         }
#     except Exception as e:
#         print(f"[ERROR] {code}: {e}")
#         return None
# backend/stock/utils/stock_compare.py
import yfinance as yf
from datetime import datetime


def get_stock_comparison_data(code: str, start_date: str, end_date: str):
    """
    단일 종목의 기간별 비교 지표와 가격 시계열(OHLC·Volume)을 반환합니다.

    Parameters
    ----------
    code : str
        6자리 숫자 종목코드 (예: '005930')
    start_date : str
        조회 시작일 (YYYY-MM-DD)
    end_date : str
        조회 종료일 (YYYY-MM-DD)

    Returns
    -------
    dict | None
        성공 시 지표·시계열을 담은 dict, 실패 시 None
    """
    try:
        # 국내 거래소 접미사 설정 (코스피 .KS / 코스닥 .KQ)
        suffix = ".KS" if code.startswith("0") else ".KQ"
        ticker = yf.Ticker(code + suffix)

        # OHLCV DataFrame
        df = ticker.history(start=start_date, end=end_date, auto_adjust=False)

        if df.empty:
            return None

        # ───────── 지표 계산 ─────────
        price_change = (
            (df["Close"].iloc[-1] - df["Close"].iloc[0]) / df["Close"].iloc[0]
        ) * 100
        avg_volume = int(df["Volume"].mean())

        # 티커 메타데이터
        info = ticker.info

        # ───────── 시계열 → 리스트(dict) ─────────
        # iterrows 사용하여 open/high/low/close/volume 모두 포함
        history = [
            {
                "date": date.strftime("%Y-%m-%d"),
                "open": round(row["Open"], 2),
                "high": round(row["High"], 2),
                "low": round(row["Low"], 2),
                "close": round(row["Close"], 2),
                "volume": int(row["Volume"]),
            }
            for date, row in df.iterrows()
        ]

        return {
            "code": code,
            "name": info.get("shortName", "Unknown"),
            "price_change_rate": round(price_change, 2),
            "avg_volume": avg_volume,
            # 배당 정보
            "dividend": {
                "amount": info.get("dividendRate", 0),
                "yield": round(info.get("dividendYield", 0) * 100, 2)
                if info.get("dividendYield")
                else 0,
                "date": info.get("exDividendDate", "-"),
            },
            # 밸류에이션
            "per": info.get("trailingPE"),      # None 허용
            "pbr": info.get("priceToBook"),
            "market_cap": info.get("marketCap"),
            "sector": info.get("sector", "-"),
            "industry": info.get("industry", "-"),
            # 가격·거래량 시계열
            "history": history,
        }

    except Exception as e:
        print(f"[ERROR] get_stock_comparison_data({code}): {e}")
        return None
