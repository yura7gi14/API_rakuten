import time

# 取得したレシピはDataFrameに格納する
df_recipe = pd.DataFrame(columns=['recipeId', 'recipeTitle', 'foodImageUrl', 'recipeMaterial', 'recipeCost', 'recipeIndication', 'categoryId', 'categoryName'])

for index, row in df_keyword.iterrows():
    time.sleep(3) # 連続でアクセスすると先方のサーバに負荷がかかるので少し待つのがマナー

    url = 'https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1050436635711957152&categoryId='+row['categoryId']
    res = requests.get(url)

    json_data = json.loads(res.text)
    recipes = json_data['result']

    for recipe in recipes:
        df_recipe = df_recipe.append({'recipeId':recipe['recipeId'],'recipeTitle':recipe['recipeTitle'],'foodImageUrl':recipe['foodImageUrl'],'recipeMaterial':recipe['recipeMaterial'],'recipeCost':recipe['recipeCost'],'recipeIndication':recipe['recipeIndication'],'categoryId':row['categoryId'],'categoryName':row['categoryName']}, ignore_index=True)