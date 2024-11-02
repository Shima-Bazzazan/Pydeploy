import json
import requests

response_numbers = requests.get("http://numbersapi.com/42")
print("api numbers :",response_numbers.text)