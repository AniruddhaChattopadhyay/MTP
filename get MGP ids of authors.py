import requests
from bs4 import BeautifulSoup
import pandas as pd
from pandas import DataFrame

# df = pd.read_csv('authorZbmath.csv')
df = pd.read_csv('remainingZbMath.csv')
for index in range(23999,24000):
    outer_flag = False
    # print(df.iloc[index]['zbMath Id'])
    print('*'*50)
    print(index)
    print(df.iloc[index]['zbMath Id'])
    df_write = pd.read_csv('/home/zeedx/Documents/MTP/zbMath_rest.csv')
    zbMath_id = df_write['zbMath Id'].tolist()
    MGP_id = df_write['MGP Id'].tolist()
    while 1:
        try:
            # URL = "https://zbmath.org" + df.iloc[index]['zb Math link']
            # URL = "https://www.zbmath.org/authors/?q=ai%3A" + df.iloc[index]['zbMath Id']
            URL = "https://www.zbmath.org/authors/?q=ai%3A" + 'hall.charles-allan'
            print(URL)
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, "html.parser")
            MGP_ID_a = soup.find('a', text='MGP')
            MGP_ID = MGP_ID_a.attrs.get('title')
            print(MGP_ID)
            zbMath_id.append(df.iloc[index]['zbMath Id'])
            MGP_id.append(MGP_ID)
            break

        except Exception as e:
            outer_flag = True
            break
            print('exception!!')
            print(e)
            pass
    if outer_flag:
        break
    # df_write = DataFrame(list(zip(zbMath_id, MGP_id)),
    #                      columns=['zbMath Id', 'MGP Id'])
    # df_write.to_csv('/home/zeedx/Documents/MTP/zbMath_rest.csv', encoding='utf-8', index=False)
