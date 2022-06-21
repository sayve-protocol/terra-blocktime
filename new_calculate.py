import requests
import json
import csv

TOTAL_AMOUNT=250000000
MILLION=1000000
TIER=5
CONTACT="terra1tkgaag3gpj4suyt6qquudj3jq97xjvmya0zxs6"
fund_score={}
COIN_PRICE=0.004

#get total amount for each user
def loop_funders():
    try:
        r = requests.get("https://lcd.terra.dev/wasm/contracts/"+CONTACT+"/store?query_msg=%7B%22list%22:%7B%7D%7D")
        # print("https://bombay-lcd.terra.dev/wasm/contracts/"+CONTACT+"/store?query_msg=%7B%22list%22:%7B%7D%7D")
        r.raise_for_status()
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.HTTPError as err:
        print(f"Could not fetch get_terra_gas_prices from Terra's FCD. Error message: {err}")

#get guaranteen_allocations for each user
def guaranteen_allocations(terra_address):
    try:
        r = requests.get("https://i3o4z6vs8k.execute-api.ap-northeast-1.amazonaws.com/prod/api/v1/token-sale-wallet/"+terra_address)
        r.raise_for_status()
        if r.status_code == 200:
            if "guaranteedAllocation" not in str(r.json()):
                return "none"
            else:
                fund_score[terra_address] = r.json()["data"]["walletObj"]["mineral_grade"]
                # print(r.json()["data"]["walletObj"]["mineral_grade"],"score")
                return r.json()["data"]["walletObj"]["guaranteedAllocation"]
    except requests.exceptions.HTTPError as err:
        print(f"Could not fetch get_terra_gas_prices from Terra's FCD. Error message: {err}")

#get deposite timeline for each user
def deposite_history(terra_address):
    url="https://lcd.terra.dev/wasm/contracts/"+CONTACT+"/store?query_msg=%7B%22investor%22:%20%7B%22wallet%22:%20%22"+terra_address+"%22%7D%7D"
    # print(url)
    try:
        r = requests.get(url)
        r.raise_for_status()
        if r.status_code == 200:
                return r.json()
    except requests.exceptions.HTTPError as err:
        print(f"Could not fetch get_terra_gas_prices from Terra's FCD. Error message: {err}")



# stage 1: get info from each prefunders
CHANCE_GUY=[] # whose deposite number is higher than guranteened allocation

RIGHT_GUY=[] # whose deposite number is equal with guranteened allocation

BAD_GUY=[] # whose deposite number is less than guranteened allocation

LATE_GUY=[]

rest_ava={} # rest available sayve coins can be bought

total_deposite_address={}

g_al={} # guranteened coins for each funder

all_funders = loop_funders()
#check all the user deposite number

for single in all_funders["result"]["investors"]:
    #get their guranteened allocations
    print(single["wallet"])

    origin_at= guaranteen_allocations(single["wallet"])
    # print(single["wallet"],origin_at)
    #repalce symbol "," then can change it to int value
    

    new_ga = origin_at.replace(",","")
    deposit_value = int(single["total"])/MILLION
    # #create a hash to store guranteened allocations for each user
    g_al[single["wallet"]] = new_ga
    # #json info sometimes shows none, so we need do judgement
    total_deposite_address[single["wallet"]] = deposit_value
    if new_ga!="none":
    #     #creat a hash to store all the deposite value for each users
         
        #  print(single["wallet"],str(deposit_value)+"ust",str(float(new_ga)*0.01)+"ust")
    #     #if deposite value larger than guranteened allocation
         if deposit_value > float(new_ga)*COIN_PRICE:
    #         #let these users to buy sayve coins first based on guranteen allocation number
             TOTAL_AMOUNT = TOTAL_AMOUNT-float(new_ga)
    #         #store rest available ust for these users
             rest_ava[single["wallet"]] = deposit_value - float(new_ga)*COIN_PRICE # deposite ust minus guranteen value (ust)
             CHANCE_GUY.append(single["wallet"]) # do classification for these guy, means they still have chance to get more sayve coins
    #     # this means the deposite value equals guaranteen value
         elif deposit_value == float(new_ga)*COIN_PRICE:
             TOTAL_AMOUNT = TOTAL_AMOUNT-float(new_ga) 
             rest_ava[single["wallet"]] = 0 # no rest money for them to buy more
             RIGHT_GUY.append(single["wallet"])
    #         # print("good number")
         else:
             if deposit_value!=0:
                 TOTAL_AMOUNT = TOTAL_AMOUNT-deposit_value/COIN_PRICE
                 rest_ava[single["wallet"]] = 0
                 BAD_GUY.append(single["wallet"])
                 # print(single["wallet"],str(deposit_value)+"ust",str(float(new_ga)*0.01)+"ust ","fewer or not depsite")
    else:
        rest_ava[single["wallet"]]= deposit_value
        # CHANCE_GUY.append(single["wallet"])
        LATE_GUY.append(single["wallet"])
        
print("stage1:",TOTAL_AMOUNT)

#stage 2 pylon stakers to get rest coins sorted by their score
pylon_staker={}
buy_sequence=[]
alpha_tester=[]
for funder in CHANCE_GUY:
    if fund_score[funder] =="You are special":
        alpha_tester.append(funder)
    else:
        pylon_staker[funder]=float(fund_score[funder])
#doing sequence by score
#alpha_test first
for alpha in alpha_tester:
    buy_sequence.append(alpha)

score_result = sorted(pylon_staker.items(), key=lambda item: item[1], reverse=True)
new_seq_address=[]
for srt_td in score_result:
    buy_sequence.append(srt_td[0])
    # buy_sequence.append(srt_td[0]) = rest_ava[srt_td[0]]

#start to buy for stakers
success_terra_address={}
rest_terra_address={}
ust_return={}
for t_d in buy_sequence:
    if TOTAL_AMOUNT < rest_ava[t_d]/COIN_PRICE and TOTAL_AMOUNT!=0:
        print("last rest:",TOTAL_AMOUNT,t_d,total_deposite_address[t_d],rest_ava[t_d]/COIN_PRICE)
        return_ust = (rest_ava[t_d]/COIN_PRICE-TOTAL_AMOUNT)*COIN_PRICE
        rest_terra_address[t_d] = total_deposite_address[t_d]-return_ust 
        ust_return[t_d]=return_ust
        # print(total_deposite_address[t_d],return_ust,rest_terra_address[t_d])
        TOTAL_AMOUNT = 0
    elif TOTAL_AMOUNT > rest_ava[t_d]/COIN_PRICE:
        print("rest:",TOTAL_AMOUNT,t_d,total_deposite_address[t_d],rest_ava[t_d]/COIN_PRICE)
        TOTAL_AMOUNT = TOTAL_AMOUNT-(rest_ava[t_d]/COIN_PRICE)
        success_terra_address[t_d] = total_deposite_address[t_d]
        ust_return[t_d]=0
    elif TOTAL_AMOUNT==0:
        if t_d in LATE_GUY:
           rest_terra_address[t_d] = 0
        else:
           rest_terra_address[t_d] = g_al[t_d]
        ust_return[t_d] = rest_ava[t_d]

    # new_seq_address.append(srt_td[0])

print("stage2:",TOTAL_AMOUNT)

#last step for deposit guys
time_hash={}
for late in LATE_GUY:
    info_back = deposite_history(late)
    person_time=[]
    for time in info_back['result']['deposit_history']:
        person_time.append(time['date'])
    #get the oldest time for each user
    time_hash[late]=max(person_time)

value_sorted_result = sorted(time_hash.items(), key=lambda item: item[1], reverse=False)
#generate new sequence to buy
new_seq_address=[]
for srt_td in value_sorted_result:
    new_seq_address.append(srt_td[0])

#only deposit guys buy it
for t_d in new_seq_address:
    if TOTAL_AMOUNT < rest_ava[t_d]/COIN_PRICE and TOTAL_AMOUNT!=0:
        print("last rest:",TOTAL_AMOUNT,t_d,total_deposite_address[t_d],rest_ava[t_d]/COIN_PRICE)
        return_ust = (rest_ava[t_d]/COIN_PRICE-TOTAL_AMOUNT)*COIN_PRICE
        rest_terra_address[t_d] = total_deposite_address[t_d]-return_ust 
        ust_return[t_d]=return_ust
        # print(total_deposite_address[t_d],return_ust,rest_terra_address[t_d])
        TOTAL_AMOUNT = 0
    elif TOTAL_AMOUNT > rest_ava[t_d]/COIN_PRICE:
        print("rest:",TOTAL_AMOUNT,t_d,total_deposite_address[t_d],rest_ava[t_d]/COIN_PRICE)
        TOTAL_AMOUNT = TOTAL_AMOUNT-(rest_ava[t_d]/COIN_PRICE)
        success_terra_address[t_d] = total_deposite_address[t_d]
        ust_return[t_d]=0
    elif TOTAL_AMOUNT==0:
        rest_terra_address[t_d] = 0
        ust_return[t_d] = rest_ava[t_d]



#step 5: collecting data and save to csv file
all=[]
json_all=[]
for key in success_terra_address.keys():
    data=[]
    data.append(key)
    data.append(str(int(success_terra_address[key])*MILLION/COIN_PRICE))
    data.append(str(ust_return[key]*MILLION))
    all.append(data)
    hashdata={}
    hashdata["user_addr"] = key
    hashdata["allocation"] = str(int(success_terra_address[key]*MILLION/COIN_PRICE))
    hashdata["refunded"] = str(ust_return[key]*MILLION)
    json_all.append(hashdata)

for key in rest_terra_address.keys():
    # print(key,rest_terra_address[key],"8**8888")
    data=[]
    data.append(key)
    data.append(str(int(rest_terra_address[key])*MILLION))
    data.append(str(ust_return[key]*MILLION))
    all.append(data)
    hashdata={}
    hashdata["user_addr"] = key
    hashdata["allocation"] = str(int(rest_terra_address[key]*MILLION))
    hashdata["refunded"] = str(ust_return[key]*MILLION)
    json_all.append(hashdata)

for x in RIGHT_GUY:
   data=[]
   data.append(x)
   data.append(str(int(g_al[x])*MILLION/COIN_PRICE))
   data.append(0)
   all.append(data)
   hashdata={}
   hashdata["user_addr"] = x
   hashdata["allocation"] = str(int(g_al[x]*MILLION/COIN_PRICE))
   hashdata["refunded"] = "0"
   json_all.append(hashdata)

for y in BAD_GUY:
    hashdata={}
    data=[]
    data.append(y)
    data.append(str(int(total_deposite_address[y]*MILLION/COIN_PRICE)))
    data.append(0)
    all.append(data)
    hashdata["user_addr"] = y
    hashdata["allocation"] = str(int(total_deposite_address[y]*MILLION/COIN_PRICE))
    hashdata["refunded"] = "0"
    json_all.append(hashdata)




header = ['terra_address', 'sayve token given', 'ust to return']
with open('calculate.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(all)
    

#json format
output=[]
block={}
block["update"]=json_all
output.append(block)
with open('output.json','w') as f:
    json.dump(output,f)
