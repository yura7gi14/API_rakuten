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
    df = df.concat([df,pd.DataFrame({'category1':category['categoryId'],'category2':"",'category3':"",'categoryId':category['categoryId'],'categoryName':category['categoryName']}, index=[0])], ignore_index=True)

for category in json_data['result']['medium']:
    df = df.concat([df,pd.DataFrame({'category1':category['parentCategoryId'],'category2':category['categoryId'],'category3':"",'categoryId':str(category['parentCategoryId'])+"-"+str(category['categoryId']),'categoryName':category['categoryName']}, index=[0])], ignore_index=True)
    parent_dict[str(category['categoryId'])] = category['parentCategoryId']

for category in json_data['result']['small']:
    df = df.concat([df,pd.DateFrame({'category1':parent_dict[category['parentCategoryId']],'category2':category['parentCategoryId'],'category3':category['categoryId'],'categoryId':parent_dict[category['parentCategoryId']]+"-"+str(category['parentCategoryId'])+"-"+str(category['categoryId']),'categoryName':category['categoryName']}, index=[0])], ignore_index=True)

# 2. キーワードからカテゴリを抽出する
df_keyword = df.query('categoryName.str.contains("魚")', engine='python')

# 3. 人気レシピを取得する
df_recipe = pd.DataFrame(columns=['recipeId', 'recipeTitle', 'foodImageUrl', 'recipeMaterial', 'recipeCost', 'recipeIndication', 'categoryId', 'categoryName'])

for index, row in df_keyword.iterrows():
    time.sleep(3) # 連続でアクセスすると先方のサーバに負荷がかかるので少し待つのがマナー

    url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1050436635711957152&categoryId='+row['categoryId']
    res = requests.get(url)

    json_data = json.loads(res.text)
    recipes = json_data['result']

    for recipe in recipes:
        df_recipe = df_recipe.concat([df,pd.DateFrame({'recipeId':recipe['recipeId'],'recipeTitle':recipe['recipeTitle'],'foodImageUrl':recipe['foodImageUrl'],'recipeMaterial':recipe['recipeMaterial'],'recipeCost':recipe['recipeCost'],'recipeIndication':recipe['recipeIndication'],'categoryId':row['categoryId'],'categoryName':row['categoryName']}, index=[0])], ignore_index=True)
        pprint(df_recipe)