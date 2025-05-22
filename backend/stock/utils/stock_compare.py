import yfinance as yf

def get_stock_comparison_data(code, start_date, end_date):
    try:
        # 한국 종목은 .KS (코스피), .KQ (코스닥) 도메인 필요
        code_suffix = '.KS' if code.startswith('0') else '.KQ'
        ticker = yf.Ticker(code + code_suffix)
        df = ticker.history(start=start_date, end=end_date)

        if df.empty:
            return None

        price_change = ((df['Close'][-1] - df['Close'][0]) / df['Close'][0]) * 100
        avg_volume = int(df['Volume'].mean())

        info = ticker.info
        dividend_amount = info.get('dividendRate', 0)
        dividend_yield = round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else 0
        dividend_date = info.get('exDividendDate', '-')

        return {
            'code': code,
            'name': info.get('shortName', 'Unknown'),
            'price_change_rate': round(price_change, 2),
            'avg_volume': avg_volume,
            'dividend': {
                'amount': dividend_amount,
                'yield': dividend_yield,
                'date': dividend_date
            },
            'per': info.get('trailingPE', None),
            'pbr': info.get('priceToBook', None),
            'market_cap': info.get('marketCap', None),
            'sector': info.get('sector', '-'),
            'industry': info.get('industry', '-'),
        }

    except Exception as e:
        print(f"[ERROR] {code}: {e}")
        return None

def get_stock_comparison_data(code, start_date, end_date):
    try:
        suffix = '.KS' if code.startswith('0') else '.KQ'
        ticker = yf.Ticker(code + suffix)
        df = ticker.history(start=start_date, end=end_date)

        if df.empty:
            return None

        price_change = ((df['Close'][-1] - df['Close'][0]) / df['Close'][0]) * 100
        avg_volume = int(df['Volume'].mean())
        info = ticker.info

        # ✅ 종가 시계열 데이터 추가
        close_data = [{'date': date.strftime('%Y-%m-%d'), 'close': round(price, 2)}
                      for date, price in df['Close'].items()]

        return {
            'code': code,
            'name': info.get('shortName', 'Unknown'),
            'price_change_rate': round(price_change, 2),
            'avg_volume': avg_volume,
            'dividend': {
                'amount': info.get('dividendRate', 0),
                'yield': round(info.get('dividendYield', 0) * 100, 2) if info.get('dividendYield') else 0,
                'date': info.get('exDividendDate', '-')
            },
            'per': info.get('trailingPE', None),
            'pbr': info.get('priceToBook', None),
            'market_cap': info.get('marketCap', None),
            'sector': info.get('sector', '-'),
            'industry': info.get('industry', '-'),
            'history': close_data  # 👈 추가된 종가 시계열
        }
    except Exception as e:
        print(f"[ERROR] {code}: {e}")
        return None
