import requests

username = "Shima-Bazzazan"
response = requests.get(f"https://api.github.com/users/{username}/followers?per_page=100")

if response.status_code == 200:
    followers = response.json()
    print(f"Followers of {username}:")
    
    for follower in followers:
        print(f"- {follower['login']}")
else:
    print(f"Failed to retrieve followers. Status code: {response.status_code}")
