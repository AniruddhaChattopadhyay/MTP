import json
import pandas as pd

# with open('outputfile1_8000-10000.json') as fout:
#      li2 = json.load(fout)
#
# print(len(li2))
# print(li2[-1])

df = pd.read_csv("dblp_publication_data_for_mgp_researchers.csv")

df2 = pd.read_csv("/home/zeedx/Documents/MTP/extra copy/csv_scrapped/author_zbmath_and_mgp_id.csv")
print(df.columns)

# for col in df.columns:
#     print(df.iloc[1][col])
# print(df.iloc[1]["title"])
# print(df.iloc[1]["title"])

print(df.shape)

li1 = df['mgp_id'].to_list()

li2 = df2["MGP Id"].to_list()

s1 = set(li1)
s2 = set(li2)

s3 = s1.union(s2)

print(len(s1))
print(len(s2))
print(len(s3))