import requests
import json
import time
from os import system, name
system('cls')

def request(target):
    root_url = "https://api.warframe.market/v1/"
    headers = {'language' : 'en','accept' : 'application/json', 'platform' : 'pc'}
    time.sleep(0.35)
    temp = requests.get(root_url+target,headers=headers)
    if temp:
        return temp
    else:
        print(root_url + target + ": Error 404!")
        exit()

def liststatistics(list):
    items_list = []
    items_list_json = request("items").json()['payload']['items']
    for name in items_list_json:
        for list_name in list:
            if name["item_name"] == list_name:
                price_avg = 0
                sold_volume = 0
                price_min = 10000
                price_max = 0

                items_statistics_json = request("items/" + name["url_name"] + "/statistics").json()
                for record in items_statistics_json['payload']['statistics_closed']['48hours']:
                    if ("mod_rank" not in record or record["mod_rank"] == 0) and record["volume"] > 0:
                        sold_volume += record["volume"]
                        if price_min > record["median"]:
                            price_min = record["median"]
                        if price_max < record["median"]:
                            price_max = record["median"]
                        if price_avg > 0:
                            price_avg = (price_avg+(record["volume"]*record["median"]))/((record["volume"]+1))
                        else:
                            price_avg = (price_avg+(record["volume"]*record["median"]))/((record["volume"]))

                items_list.append(item(list_name, name["url_name"], str(sold_volume), str(price_min), str(price_max), str(round(price_avg, 0))))

    return items_list

def itemorders(item_url,player_name):
    item_orders_json = request("items/" + item_url + "/orders").json()['payload']['orders']
    min_price = 10000
    for order in item_orders_json:
        if order["user"]["status"] == "ingame" and order["order_type"] == "sell" and order["user"]["ingame_name"] != player_name:
            if min_price > order["platinum"]:
                min_price = order["platinum"]
    return str(min_price)

class item:
  def __init__(self, name, url, sold, min, max, avg):
    self.name = name
    self.url = url
    self.sold = sold
    self.min = min
    self.max = max
    self.avg = avg

def itemscheck(list_src):
    items_list = []
    list = []
    file = open(list_src, "r")
    list = file.read().splitlines()


    for i in range(len(list)):
        list[i] = list[i].lower()
        list[i] = list[i].title()

    print(list)
    items_list = liststatistics(list)

    for item in items_list:
        print()
        print(item.name)
        print("Sold: "+item.sold)
        print("Min: "+item.min)
        print("Max: "+item.max)
        print("Avg: "+item.avg)



def playerorderschecks(player_name):
    P = -1
    list = []
    items_list = []
    player_json = request("profile/" + player_name + "/orders").json()

    for order in player_json['payload']['sell_orders']:
        list.append(order['item']['en']["item_name"])

    items_list = liststatistics(list)

    for item in items_list:
        print()
        print(item.name)
        print("My price: " + str(player_json['payload']['sell_orders'][P]['platinum']))
        print("Others min: " + itemorders(item.url,player_name))
        print("Sold: "+item.sold)
        print("Min: "+item.min)
        print("Max: "+item.max)
        print("Avg: "+item.avg)
        P += 1






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
#       user input

print("Hello, select what u want.")
print("1 - Parts | 2 - Cephalon | 3 - Mods | Player name")
input1 = ""
if input1 == "":
    input1 = input()
    mode(input1)
