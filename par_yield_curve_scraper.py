##scrapes treasury yield rates from treasury direct via HTML##

import pandas as pd
import requests
from bs4 import BeautifulSoup

base_url = 'https://home.treasury.gov/resource-center/data-chart-center/interest-rates/TextView?type=daily_treasury_yield_curve&field_tdr_date_value_month=202303'
page = requests.get(base_url)
my_data = {}
column_name = []
row_value = []
soup = BeautifulSoup(page.content, "html.parser")
#print(soup.prettify())
table = soup.select('table')
title = soup.title.string
for i in soup.select('th', id = 'table.views-table views-view-table cols-23'):
    column = i.get_text()
    column_name.append(column.strip())
for i in soup.select('td', id = 'table.views-table views-view-table cols-23'):
    row = i.get_text()
    if row.strip() != "N/A" :
        row_value.append(row.strip())
del column_name[1:10]

idx = [0,14,28,42,56,70]
for x in range(14):
    my_data[column_name[x]] = [row_value[i + x]for i in idx]

df = pd.DataFrame(my_data)
