import requests
import json
import time
import pandas as pd
from pprint import pprint


# 1. 楽天レシピのレシピカテゴリ一覧を取得する

res = requests.get('https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId=1050436635711957152')

json_data = json.loads(res.text)

parent_dict = {} # mediumカテゴリの親カテゴリの辞書

df = pd.DataFrame(columns=['category1','category2','category3','categoryId','categoryName'])

for category in json_data['result']['large']:
    df = pd.concat([df, pd.DataFrame({'category1':category['categoryId'],'category2':"",'category3':"",'categoryId':category['categoryId'],'categoryName':category['categoryName']}, index=[0])], ignore_index=True)

for category in json_data['result']['medium']:
    df = pd.concat([df, pd.DataFrame({'category1':category['parentCategoryId'],'category2':category['categoryId'],'category3':"",'categoryId':str(category['parentCategoryId'])+"-"+str(category['categoryId']),'categoryName':category['categoryName']}, index=[0])], ignore_index=True)
    parent_dict[str(category['categoryId'])] = category['parentCategoryId']

for category in json_data['result']['small']:
    df = pd.concat([df,pd.DataFrame({'category1':parent_dict[category['parentCategoryId']],'category2':category['parentCategoryId'],'category3':category['categoryId'],'categoryId':parent_dict[category['parentCategoryId']]+"-"+str(category['parentCategoryId'])+"-"+str(category['categoryId']),'categoryName':category['categoryName']}, index=[0])], ignore_index=True)

# キーワードを含む行を抽出
df_keyword = df.query('categoryName.str.contains("肉")', engine='python')

# 人気レシピを取得
res = requests.get('https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1050436635711957152')

df_recipe = pd.DataFrame(columns=['recipeId', 'recipeTitle', 'foodImageUrl',  'categoryId', 'categoryName'])

#for index, row in df_keyword.iterrows():
#    time.sleep(3) # 連続でアクセスすると先方のサーバに負荷がかかるので少し待つのがマナー
#
#    url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1050436635711957152&categoryId='+row['categoryId']
#    res = requests.get(url)
#
#    json_data = json.loads(res.text)
#    recipes = json_data['result']

json_data = json.loads(res.text)

pprint(json_data)