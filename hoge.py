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
    df = df.append({'category1':category['categoryId'],'category2':"",'category3':"",'categoryId':category['categoryId'],'categoryName':category['categoryName']}, ignore_index=True)

for category in json_data['result']['medium']:
    df = df.append({'category1':category['parentCategoryId'],'category2':category['categoryId'],'category3':"",'categoryId':str(category['parentCategoryId'])+"-"+str(category['categoryId']),'categoryName':category['categoryName']}, ignore_index=True)
    parent_dict[str(category['categoryId'])] = category['parentCategoryId']

for category in json_data['result']['small']:
    df = df.append({'category1':parent_dict[category['parentCategoryId']],'category2':category['parentCategoryId'],'category3':category['categoryId'],'categoryId':parent_dict[category['parentCategoryId']]+"-"+str(category['parentCategoryId'])+"-"+str(category['categoryId']),'categoryName':category['categoryName']}, ignore_index=True)

# 2. キーワードからカテゴリを抽出する
df_keyword = df.query('categoryName.str.contains("魚")', engine='python')
pprint(df_keyword)