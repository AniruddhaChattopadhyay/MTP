import pandas as pd
from pandas import DataFrame

df_wiki = pd.read_csv('wikidata authors.csv')
df_zbMath = pd.read_csv('zbmath.csv')
df = df_wiki.merge(df_zbMath,on=["MGP Id","zbMath Id"],how='outer')
df.to_csv('wiki+zbmath.csv', encoding='utf-8', index=False)

list_wiki = df_wiki['MGP Id'].tolist()
list_zbMath = df_zbMath['MGP Id'].tolist()
unique = set(list_zbMath).union(list_wiki)
print(len(unique))
# # for i in unique:
# #     print(unique)