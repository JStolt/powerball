import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
from dateutil.relativedelta import relativedelta
import re

orig_url = "https://www.lottery.net/powerball/numbers/{}"

def get_powerball_early_format(url):
    year_pbs = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
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
    return year_pbs

def get_powerball_later_format(url):
    year_pbs = []
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
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


def get_powerball_numbers(year):
    year_pbs = []
    page = requests.get(orig_url.format(year))
    soup = BeautifulSoup(page.content, 'html.parser')
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
        




def main():
    pb_list = []
    now = datetime.now() + relativedelta(years=1)
    for year in list(range(1992, now.year)):
        pb_list.extend(get_powerball_numbers(year))

    df = pd.DataFrame(pb_list, columns=['date', 'num1', 'num2', 'num3', 'num4', 'num5', 'pwrbl', 'pwrply'])
    # df = df[df['date'].str.startswith('2021')]
    # print(df)
    # print(df.describe())
    print(df["pwrbl"].value_counts())

if __name__ == '__main__':
    main()