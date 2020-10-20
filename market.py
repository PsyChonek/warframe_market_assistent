import requests
import json
import time
from os import system, name
system('cls')


root_url = "https://api.warframe.market/v1/"
headers = {'language' : 'en','accept' : 'application/json', 'platform' : 'pc'}

def request(target):
    temp = requests.get(root_url+target,headers=headers)
    if temp:
        print()
    else:
        print(root_url + target + ": Error 404!")
        exit()
    return temp

items_url_json = request("items").json()

list = []
file = open("CephalonSimaris75.txt", "r")
list = file.read().split(", ")


for i in range(len(list)):
    list[i] = list[i].lower()
    list[i] = list[i].title()

print(list)

for name in items_url_json['payload']['items']:
    for list_name in list:
        if name["item_name"] == list_name:
            avg = 0
            sold_volume = 0
            price_min = 1000
            price_max = 0

            time.sleep(0.35)
            item_url_json = request("items/" +name["url_name"]+"/statistics").json()
            for record in item_url_json['payload']['statistics_closed']['48hours']:
                if "mod_rank" not in record or record["mod_rank"] == 0:
                    avg += record["median"]
                    sold_volume += record["volume"]
                    if price_min > record["median"]:
                        price_min = record["median"]
                        if price_max < record["median"]:
                            price_max = record["median"]

            print(list_name)
            print("Sold: " + str(sold_volume))
            if sold_volume > 0:
                print("Avg: " + str(avg/sold_volume))
                print("Min: " + str(price_min))
                print("Max: " + str(price_max))
