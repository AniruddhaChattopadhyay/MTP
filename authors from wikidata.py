import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from pandas import DataFrame

endpoint_url = "https://query.wikidata.org/sparql"

query = """SELECT *

WHERE 
{
  ?s wdt:P1556 ?zbid.
  ?s wdt:P549 ?mgpid.
}"""
zbMath_id = []
MGP_id = []
wikilink = []


def get_results(endpoint_url, query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    # TODO adjust user agent; see https://w.wiki/CX6
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


results = get_results(endpoint_url, query)

for result in results["results"]["bindings"]:
    # print(result.get('s').get('value'),
    #       result.get('zbid').get('value'),
    #       result.get('mgpid').get('value'))
    MGP_id.append(result.get('mgpid').get('value'))
    zbMath_id.append(result.get('zbid').get('value'))
    wikilink.append(result.get('s').get('value'))

df = DataFrame(list(zip(zbMath_id, MGP_id, wikilink)),
               columns=['zbMath Id', 'MGP Id', 'wikidata link'])

# df.to_csv('wikidata authors.csv', encoding='utf-8', index=False)
