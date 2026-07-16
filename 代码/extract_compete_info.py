"""从竞品企业html.md中提取表格数据为DataFrame，删除产品图片列，导出CSV。"""
from bs4 import BeautifulSoup
import pandas as pd

tag='特金智能科技(上海)有限公司'
with open('竞品企业html.md', 'r', encoding='utf-8') as f:
    html = f.read()

soup = BeautifulSoup(html, 'html.parser')
table = soup.find('table', class_='ntable')
rows = table.find_all('tr')[1:]  # skip header row

data = []
for row in rows:
    cols = row.find_all('td')
    if len(cols) < 8:
        continue
    seq = cols[0].get_text(strip=True)
    # 跳过 cols[1] 产品图片列
    product_name = cols[2].get_text(strip=True)
    round_ = cols[3].get_text(strip=True)
    date_ = cols[4].get_text(strip=True)
    city = cols[5].get_text(strip=True)
    intro = cols[6].get_text(strip=True)
    company = cols[7].get_text(strip=True)
    data.append([seq, product_name, round_, date_, city, intro, company])

df = pd.DataFrame(data, columns=['序号', '产品名', '当前轮次', '成立日期', '所属城市', '产品介绍', '所属企业'])
df['tag'] = tag
output_path = r'../数据/竞品企业/竞品信息_提取.csv'
# 追加模式：若文件已存在则不写入表头，否则写入表头
header = not os.path.exists(output_path)
df.to_csv(output_path, mode='a', index=False, encoding='utf-8-sig', header=header)
print(f'已追加至: {output_path}')
print(f'共 {len(df)} 条记录, {len(df.columns)} 列')
print(df.columns.tolist())
