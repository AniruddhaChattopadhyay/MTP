import time

import requests
from requests import RequestException
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

df = pd.read_csv('wiki+zbmath.csv')


def get_details(soup, class_name):
    divs = soup.findAll("div", {"class": class_name})
    # print(divs)
    outer_list = []
    for div in divs:
        table = div.find('table')
        # print(table)
        list_info = []
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            li = []
            for col in columns:
                # print(col.get_text().strip())
                td_class = col.attrs.get('class')
                if td_class is None:
                    continue
                if td_class[0] == 'number':
                    li.append(col.get_text().strip())
                    a = col.find('a')
                    li.append([a.attrs.get('href'), a.attrs.get('title')])
                if td_class[0] == 'text':
                    authored_text = col.get_text().strip()
                    if authored_text == 'single-authored':
                        li.append([None, None])
                    else:
                        a = col.find('a')
                        li.append([a.attrs.get('href'), a.attrs.get('title')])
            list_info.append(li)
        outer_list.append(list_info)
    if len(outer_list) == 0:
        return None, None, 0
    elif len(outer_list) == 1:
        if divs[0].find_next('h4').get_text() == 'Co-Authors':
            return outer_list[0], None, 0
        else:
            s = [int(s) for s in re.findall(r'-?\d+\.?\d*', divs[0].find_next('h4').get_text())]
            if len(s) > 0:
                return None, outer_list[0], s[0]
            return None, outer_list[0], 0
    s = [int(s) for s in re.findall(r'-?\d+\.?\d*', divs[1].find_next('h4').get_text())]
    if len(s) > 0:
        return outer_list[0], outer_list[1], s[0]  # 1rst table and then the 2nd table
    return outer_list[0], outer_list[1], 0


for index in range(24561, 24680):
    outer_flag = False
    print(df.iloc[index]['zbMath Id'])
    while 1:
        try:
            print('*' * 20 + str(index) + '*' * 20)
            with open('outputfile1_22000_24000_new.json', encoding='utf-8') as fout:
                big_list = json.load(fout)
            URL = "https://www.zbmath.org/authors/?q=ai%3A" + df.iloc[index]['zbMath Id']
            # URL = "https://www.zbmath.org/authors/?q=ai%3A" + "abrosimov.nikolai-vladimirovich"
            print(URL)
            page = requests.get(URL)
            if page.status_code == 429:
                outer_flag = True
                break
            soup = BeautifulSoup(page.content, "html.parser")
            list_co_authors, list_cited_by_co_authors, no_of_citation_co_authors = get_details(soup, 'facet1st')
            print('end of facet1rst')
            list_serials, list_cited_by_serials, no_of_citation_serials = get_details(soup, 'facet2nd')
            print('end of facet2nd')
            list_fields, list_cited_by_fields, no_of_citation_fields = get_details(soup, 'facet3rd')
            print('end of facet3rd')
            print('start creating the publications list')
            flag = False
            if soup.find(text='Documents Indexed:'):
                publications = soup.find(text='Documents Indexed:').findNext('td').a.get_text().split()[0]
                print(publications)
                i = 0
                publication_list = []
                while i * 200 <= int(publications.replace(',', '')):
                    print(f'publication number {i} for {index}')
                    if i == 0:
                        URL = "https://www.zbmath.org/?q=ai%3A" + df.iloc[index]['zbMath Id'] + '&c=200'
                    else:
                        URL = "https://www.zbmath.org/?q=ai%3A" + df.iloc[index]['zbMath Id'] + '&c=200' + '&p=' + str(
                            i)
                    # URL = "https://www.zbmath.org/?q=ai%3Aabrosimov.nikolai-vladimirovich&c=200"
                    page = requests.get(URL)
                    if page.status_code == 429:
                        flag = True
                        outer_flag = True
                        break
                    soup = BeautifulSoup(page.content, "html.parser")
                    div_list = soup.findAll('div', {'class': 'list'})
                    for div in div_list:
                        author_list = []
                        source_list = []
                        MSC_list = []
                        title_paper = []
                        if div.find('div', {"class": "author"}):
                            if div.find('div', {"class": "author"}).find('a'):
                                authors = div.find('div', {"class": "author"}).findAll('a')
                                for author in authors:
                                    # print(author.get_text(),author.attrs.get('href'))
                                    author_list.append([author.get_text(), author.attrs.get('href')])
                            else:
                                author_list.append(div.find('div', {"class": "author"}).get_text())
                        else:
                            author_list.append(None)
                        print('author')

                        if div.find('div', {"class": "title"}):
                            if div.find('div', {"class": "title"}).find('a'):
                                title = div.find('div', {"class": "title"}).findAll('a')
                                for t in title:
                                    title_paper.append(
                                        [t.find_next('a').get_text(), t.find_next('a').attrs.get('href')])
                            else:
                                title_paper.append(div.find('div', {"class": "title"}).get_text)
                        else:
                            title_paper.append(None)
                        print('title')

                        if div.find('div', {"class": "source"}):
                            if div.find('div', {"class": "source"}).find('a'):
                                sources = div.find('div', {"class": "source"}).findAll('a')
                                for source in sources:
                                    source_list.append(
                                        [source.attrs.get('title'), source.attrs.get('href'), source.get_text()])
                                publications_list = source_list[0:len(source_list) - 1]
                                publications_year = source_list[-1]
                            else:
                                source_list.append(div.find('div', {"class": "source"}).get_text())
                        else:
                            source_list.append(None)
                        print('source')

                        if div.find('div', {"class": "classification"}):
                            if div.find('div', {"class": "classification"}).find('a'):
                                classifications = div.find('div', {"class": "classification"}).findAll('a')
                                for classification in classifications:
                                    MSC_list.append(
                                        [classification.attrs.get('class'), classification.attrs.get('title'),
                                         classification.attrs.get('href'), classification.get_text()])
                            else:
                                MSC_list.append(div.find('div', {"class": "classification"}).get_text())
                        else:
                            MSC_list.append(None)

                        print('MSC')

                        publication_list.append(
                            {'authors': author_list, 'title': title_paper, 'sources': source_list, 'MSC': MSC_list})

                    i += 1
                if flag:
                    break
            else:
                publication_list = None
            dict_key = df.iloc[index]['zbMath Id'] + " " + str(df.iloc[index]['MGP Id'])
            total_list = [{'list_co_authors': list_co_authors,
                           'no_of_citation_co_authors': no_of_citation_co_authors,
                           'list_serials': list_serials,
                           'no_of_citation_serials': no_of_citation_serials,
                           'list_fields': list_fields,
                           'no_of_citation_fields': no_of_citation_fields,
                           'list_cited_by_co_authors': list_cited_by_co_authors,
                           'list_cited_serials': list_cited_by_serials,
                           'list_cited_by_fields': list_cited_by_fields,
                           'list_publications': publication_list}]
            big_list.append({dict_key: total_list})

            # except Exception as e:
            #     print('exception!!')
            #     print(e)
            #     pass
            with open('outputfile1_22000_24000_new.json', 'w', encoding='utf8') as fout:
                json.dump(big_list, fout)
            break
        except Exception as e:
            if isinstance(e, RequestException):
                print('Connection Error')
                time.sleep(120)

    if outer_flag:
        break
