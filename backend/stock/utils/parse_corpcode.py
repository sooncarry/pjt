import xml.etree.ElementTree as ET
import pandas as pd

def parse_corpcode_xml(xml_path='utils/CORPCODE.xml', output_path='utils/corp_codes.csv'):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    corp_list = []
    for corp in root.findall('list'):
        name = corp.find('corp_name').text
        code = corp.find('corp_code').text
        stock_code_elem = corp.find('stock_code')
        stock_code = stock_code_elem.text if stock_code_elem is not None else ''

        corp_list.append({
            'corp_name': name,
            'corp_code': code,
            'stock_code': stock_code
        })

    df = pd.DataFrame(corp_list)
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Saved {len(df)} rows to {output_path}")

if __name__ == '__main__':
    parse_corpcode_xml()
