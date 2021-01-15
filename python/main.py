import requests
from bs4 import BeautifulSoup
import datetime
import pandas as pd

orig_url = "https://www.lottery.net/powerball/numbers/{}"

pb_list = []

now = datetime.datetime.now()
for year in list(range(1992, now.year)):
    url = orig_url.format(year)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find("table").find("tbody").findAll('tr')
    for row in table:
        result = []
        date = row.findAll('a', href=True)
        result.append(date[0]['href'].split('/')[3])
        balls = row.findAll('li')

        for x in balls:
            result.append(x.text.strip())
        pb_list.append(result)
    
print(pb_list)
# df = pd.DataFrame(pb_list, columns=['date', 'num1', 'num2', 'num3', 'num4', 'num5', 'pwrbl', 'pwrply'])

# print(df.describe(include='all'))




