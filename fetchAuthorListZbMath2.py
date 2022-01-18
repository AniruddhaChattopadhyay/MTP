import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame
import time
import string
import re

from requests import RequestException

while 1:
    exception_count = 0
    for i in range(0, 26):
        df = pd.read_csv('authorZbmath2.csv')
        try:
            print(str(i) + " Now starting" + string.ascii_lowercase[i])
            elem = string.ascii_lowercase[i]
            # URL = "https://zbmath.org/authors/?q=en%3AMGP+%26+ln%3A"+elem + '*'
            URL = "https://zbmath.org/authors/?q=en%3AMGP+%26+ln%3A" + elem + "%2A" + "&p=0&c=200"
            page = requests.get(URL)
            if page.status_code == 429:  # checking for too many requests exception
                print('breaking at : ' + string.ascii_lowercase[i])
                break
            soup = BeautifulSoup(page.content, "html.parser")
            header = soup.find("div", class_="head")
            text = header.find("h2").text
            if text == 'Your query produced no results':  # checking for invalid query
                continue
            text = text.replace(',','')
            number_of_authors = re.findall(r'\b\d+\b', text)[0]
            print("total authors")
            print(number_of_authors)
            # results = soup.find("div", class_="item")
            j = 0
            while j * 200 <= int(number_of_authors):
                print('Now starting page :' + str(j))
                URL = "https://zbmath.org/authors/?q=en%3AMGP+%26+ln%3A" + elem + "%2A" + "&p=" + str(j) + "&c=200"
                page = requests.get(URL)
                if page.status_code == 429:  # checking for too many requests exception
                    print('breaking at : ' + string.ascii_lowercase[i] + ' and page :' + str(j))
                    break
                soup = BeautifulSoup(page.content, "html.parser")
                name = df['author name'].tolist()
                zbMath_id = df['zbMath Id'].tolist()
                zbMath_link = df['zb Math link'].tolist()
                main_field_author = df['main fields'].tolist()
                for item_div in soup.findAll("div", class_="item"):
                    try:
                        # print(item_div.a.text)
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
                df = DataFrame(list(zip(name, zbMath_id, zbMath_link, main_field_author)),
                               columns=['author name', 'zbMath Id', 'zb Math link', 'main fields'])
                df.to_csv('authorZbmath2.csv', encoding='utf-8', index=False)
                exception_count = 0
                j = j + 1

        except Exception as e:
            if isinstance(e, RequestException):
                print('Connection Error')
                time.sleep(120)
            pass
