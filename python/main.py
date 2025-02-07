import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import re



import argparse

parser = argparse.ArgumentParser(description='Lottery.')
parser.add_argument('--source', metavar='Source', choices=['powerball', 'megamillions'])

args = parser.parse_args()



PB_URL = "https://www.lottery.net/powerball/numbers/{}"
MM_URL = "https://www.molottery.com/gameHistory2.do?method=mmDisplay&order=desc"


def get_megamillions_numbers():
    year_pbs = []
    page = requests.get(MM_URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.findAll("tr")
    for row in table[1:]:
        items = ([i.text.strip() for i in row])
        result = []
        date = row.find("td").text.strip().split(' ', 1)[1]
        formatted_date = datetime.strftime(datetime.strptime(date, "%b %d, %Y"), "%Y-%m-%d")
        result.append(formatted_date)
        numbers = items[3]
        regular, meg_ball, multiplier = numbers.split(":")
        [result.append(i) for i in regular.replace("MB","").strip().split('-')]
        result.append(meg_ball.replace("MP","").strip())
        result.append(multiplier.strip())

        year_pbs.append(result)
    df = pd.DataFrame(year_pbs, columns=['date', 'num1', 'num2', 'num3', 'num4', 'num5', 'megaball', 'multiplier'])

    return df




def get_powerball_numbers(year):
    year_pbs = []

    page = requests.get(PB_URL.format(year))
    soup = BeautifulSoup(page.content, 'html.parser')
    # >2021 Split
    if year < 2021:
        table = soup.find("table").find("tbody").findAll('tr')
        for row in table:
            result = []
            date = row.find("td").text.strip().split(' ', 1)[1]
            formatted_date = datetime.strftime(datetime.strptime(date, "%B %d, %Y"), "%Y-%m-%d")
            result.append(formatted_date)
            balls = row.findAll('li')
            for x in balls:
                result.append(x.text.strip())
            year_pbs.append(result)

    else:
        table = soup.findAll("tr")
        for row in table[1:]:
            result = []
            date = row.find("td").text.strip().split(' ', 1)[1]
            formatted_date = datetime.strftime(datetime.strptime(date, "%B %d, %Y"), "%Y-%m-%d")
            result.append(formatted_date)
            balls = row.findAll('li')
            for x in balls[:7]:
                    result.append(x.text.strip())
            year_pbs.append(result)


    return year_pbs
        







def main(args):

    pb_list = []
    now = datetime.now()
    for year in list(range(1992, now.year)):
        pb_list.extend(get_powerball_numbers(year))

    df = pd.DataFrame(pb_list, columns=['date', 'num1', 'num2', 'num3', 'num4', 'num5', 'pwrbl', 'pwrply'])

    # print(df)

    for x in df.columns:
        print(df[x].value_counts())
    # get_powerball_numbers(2020)
    # if args["source"].lower() == "powerball":
    #     print("not ready yet")
        
    # else:
    #     df = get_megamillions_numbers()

        # df = df[df['date'].str.startswith('2021')]
        # print(df)
        # print(df.describe())
        # print(df['num1'].apply(pd.Series.value_counts))
        # print(df["num1"].value_counts().sort_index())

        # df = df[['num1', 'num2', 'num3', 'num4', 'num5', 'megaball']].melt(var_name='columns', value_name='index')
        # print(df)
        # print(pd.crosstab(index=df['index'], columns=df['columns']))

if __name__ == '__main__':
    main(vars(args))