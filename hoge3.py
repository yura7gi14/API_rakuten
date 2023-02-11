# 「煮魚」カテゴリの人気レシピを取得
res = requests.get('https://app.rakuten.co.jp/services/api/Recipe/CategoryRanking/20170426?applicationId=1050436635711957152&categoryId=32-339')

json_data = json.loads(res.text)
pprint(json_data)