import requests
import json
from pprint import pprint

res = requests.get('https://app.rakuten.co.jp/services/api/Recipe/CategoryList/20170426?applicationId=1050436635711957152')

json_data = json.loads(res.text)
pprint(json_data)