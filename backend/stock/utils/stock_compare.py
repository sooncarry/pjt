import yfinance as yf

def get_stock_comparison_data(code, start_date, end_date):
    try:
        suffix = '.KS' if code.startswith('0') else '.KQ'
        ticker = yf.Ticker(code + suffix)
        df = ticker.history(start=start_date, end=end_date)

        if df.empty:
            return None

        price_change = ((df['Close'].iloc[-1] - df['Close'].iloc[0]) / df['Close'].iloc[0]) * 100
        avg_volume = int(df['Volume'].mean())
        info = ticker.info

        close_data = [
            {'date': date.strftime('%Y-%m-%d'), 'close': round(price, 2)}
            for date, price in df['Close'].items()
        ]

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
            'history': close_data
        }
    except Exception as e:
        print(f"[ERROR] {code}: {e}")
        return None
