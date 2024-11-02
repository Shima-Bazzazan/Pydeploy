import json
import requests

response_fruit = requests.get("https://www.fruityvice.com/api/fruit/peach")
print("api fruit :", json.loads(response_fruit.text))