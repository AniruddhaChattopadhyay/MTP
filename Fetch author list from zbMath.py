import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import time
i = 0
while 1:
    df = pd.read_csv('authorZbmath.csv')
    exception_count = 0
    try:
        print(i)
        URL = "https://zbmath.org/authors/?q=en%3AMGP&p=" + str(i)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        results = soup.find("div", class_="item")
        name = df['author name'].tolist()
        zbMath_id = df['zbMath Id'].tolist()
        zbMath_link = df['zb Math link'].tolist()
        main_field_author = df['main fields'].tolist()
        print('starting for')
        for item_div in soup.findAll("div", class_="item"):
            try:
                name.append(item_div.a.text)
                zbMath_id.append(item_div.a.attrs.get('title').split(' ')[1])
                zbMath_link.append(item_div.a.attrs.get('href'))
                main_field_author.append(item_div.table.findAll('tr')[2].findAll('td')[1].text)

            except Exception as e:
                exception_count = exception_count + 1
                print(e)
                if exception_count == 100:
                    print(e)
                    break
                pass
        print('outside for')
        df = DataFrame(list(zip(name, zbMath_id, zbMath_link, main_field_author)),
                       columns=['author name', 'zbMath Id', 'zb Math link', 'main fields'])
        # df.to_csv('authorZbmath.csv', encoding='utf-8', index=False)
        exception_count = 0
        i = i + 1

    except Exception as e:
        exception_count = exception_count + 1
        print(e)
        if exception_count == 100:
            print(e)
            break
        pass
