import requests

params = {
	"key": "8460848b-5516-4b2d-8229-f356bb8a06c7",
	"name": "Nothing76",
	"profiles": "Grappes"
}

data = requests.get(url="https://api.hypixel.net/player", params=params).json()

try:
	print(data['player'].keys())
except:
	print('Fail')