import pandas as pd
from pandas import DataFrame
#
# df1 = pd.read_csv("wiki+zbmath.csv")
# df2 = pd.read_csv("zbMath_rest.csv")
#
# mgpId1 = df1['MGP Id'].tolist()
# mgpId2 = df2['MGP Id'].tolist()
#
# zbMathId1 = df1['zbMath Id'].tolist()
# zbMathId2 = df2['zbMath Id'].tolist()
#
# mgpId1.extend(mgpId2)
# zbMathId1.extend(zbMathId2)
#
# print(len(zbMathId1))
# print(len(mgpId1))
#
#
#
# df_write = DataFrame(list(zip(zbMathId1, mgpId1)),
#                                  columns=['zbMath Id', 'MGP Id'])
# df_write.to_csv('author_zbmath_and_mgp_id.csv', encoding='utf-8', index=False)
#
df_all = pd.read_csv("mgp-nodes.tsv",sep="\t",header=0,engine='python')
df_zbmath = pd.read_csv("author_zbmath_and_mgp_id.csv")

zbmath = df_zbmath['MGP Id'].tolist()
li = df_all['Id'].tolist()
# li = [str(x) for x in li]
zbmath = [str(x) for x in zbmath]

# print(len(set(li).intersection(set(zbmath))))
print(df_all.shape)
print("hey")
# print(~df_all[df_all['Id'].isin(zbmath)])
print("ho")
df_all = df_all[~df_all['Id'].isin(zbmath)]
print(df_all.shape)
#
df_all.to_csv('remaining_authors_data_to_be_scrapped.csv', encoding='utf-8', index=False)