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

def itemscheck(list_src):

    items_url_json = request("items").json()

    list = []
    file = open(list_src, "r")
    list = file.read().splitlines()


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

def playerorderschecks(player_name):

    items_url_json = request("items").json()
    trade_list = []
    time.sleep(0.35)
    player_json = request("profile/" + player_name+ "/orders").json()
    for order in player_json['payload']['sell_orders']:
        trade_list.append(order['item']['en']["item_name"])
    P = -1
    for name in items_url_json['payload']['items']:
        for list_name in trade_list:

            if name["item_name"] == list_name:
                avg = 0
                sold_volume = 0
                price_min = 1000
                price_max = 0
                P +=1

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
                print("My price: " + str(player_json['payload']['sell_orders'][P]['platinum']))
                print("Sold: " + str(sold_volume))
                if sold_volume > 0:
                    print("Avg: " + str(avg/sold_volume))
                    print("Min: " + str(price_min))
                    print("Max: " + str(price_max))

def mode(input1):
    if input1 == "1":
        itemscheck("Parts.txt")
    elif input1 == "2":
        itemscheck("CephalonSimaris75.txt")
    elif input1 == "3":
        itemscheck("Mods.txt")
    else:
        playerorderschecks(input1)

#    print(json.dumps(player_json, indent=4, sort_keys=True))
# user input

print("Hello, select what u want.")
print("1 - Parts | 2 - Cephalon | 3 - Mods | Player name")
input1 = ""
if input1 == "":
    input1 = input()
    mode(input1)
