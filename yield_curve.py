##scrapes treasury yield rates from treasury direct via HTML and puts into a data-frame##

import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

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

for k,v in my_data.items():
    if k != 'Date':
        my_data[k] = [float(x) for x in v]

df = pd.DataFrame(my_data)

df.plot(x = 'Date', y = ['1 Mo', '2 Mo', '3 Mo', '6 Mo', '1 Yr', '2 Yr', '3 Yr', '5 Yr', '7 Yr', '10 Yr', '20 Yr', '30 Yr'])
plt.ylabel('Yield')
plt.show()

