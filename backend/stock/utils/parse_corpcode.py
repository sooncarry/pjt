import xml.etree.ElementTree as ET
import pandas as pd
import os

def parse_corpcode_xml(xml_path: str, output_csv_path: str):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    data = []
    for corp in root.findall('list'):
        corp_name = corp.findtext('corp_name')
        corp_code = corp.findtext('corp_code')
        stock_code = corp.findtext('stock_code')

        if stock_code and stock_code.strip():
            data.append({
                'corp_name': corp_name,
                'corp_code': corp_code,
                'stock_code': stock_code,
            })

    df = pd.DataFrame(data)
    df.to_csv(output_csv_path, index=False, encoding='utf-8-sig')
    print(f'✅ CSV 저장 완료: {output_csv_path}')


if __name__ == '__main__':
    BASE = os.path.dirname(__file__)  # 현재 경로: backend/stock/utils/
    parse_corpcode_xml(
        xml_path=os.path.join(BASE, 'CORPCODE.xml'),
        output_csv_path=os.path.join(BASE, 'corp_codes.csv')
    )
