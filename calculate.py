import requests
import json
import csv

TOTAL_AMOUNT=2400000
MILLION=1000000
TIER=5
CONTACT="terra1kc5vkpveadchmwsjza8s0hcwkh53pqkktkdumc"
fund_score={}


#get total amount for each user
def loop_funders():
    try:
        r = requests.get("https://bombay-lcd.terra.dev/wasm/contracts/"+CONTACT+"/store?query_msg=%7B%22list%22:%7B%7D%7D")
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
            if "guaranteedAllocation" not in r.json():
                return "none"
            else:
                print(terra_address)
                fund_score[terra_address] = r.json()["data"]["walletObj"]["mineral_grade"]
                # print(r.json()["data"]["walletObj"]["mineral_grade"],"score")
                return r.json()["data"]["walletObj"]["guaranteedAllocation"]
    except requests.exceptions.HTTPError as err:
        print(f"Could not fetch get_terra_gas_prices from Terra's FCD. Error message: {err}")

#get deposite timeline for each user
def deposite_history(terra_address):
    url="https://bombay-lcd.terra.dev/wasm/contracts/"+CONTACT+"/store?query_msg=%7B%22investor%22:%20%7B%22wallet%22:%20%22"+terra_address+"%22%7D%7D"
    print(url)
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
    origin_at= guaranteen_allocations(single["wallet"])
    # print(origin_at)
    #repalce symbol "," then can change it to int value
    new_ga = origin_at.replace(",","")
    deposit_value = int(single["total"])/MILLION
    #create a hash to store guranteened allocations for each user
    g_al[single["wallet"]] = new_ga
    #json info sometimes shows none, so we need do judgement
    if new_ga!="none":
        #creat a hash to store all the deposite value for each users
        total_deposite_address[single["wallet"]] = deposit_value
        # print(single["wallet"],str(deposit_value)+"ust",str(float(new_ga)*0.01)+"ust")
        #if deposite value larger than guranteened allocation
        if deposit_value > float(new_ga)*0.01:
            #let these users to buy sayve coins first based on guranteen allocation number
            TOTAL_AMOUNT = TOTAL_AMOUNT-float(new_ga)
            #store rest available ust for these users
            rest_ava[single["wallet"]] = deposit_value - float(new_ga)*0.01 # deposite ust minus guranteen value (ust)
            CHANCE_GUY.append(single["wallet"]) # do classification for these guy, means they still have chance to get more sayve coins
        # this means the deposite value equals guaranteen value
        elif deposit_value == float(new_ga)*0.01:
            TOTAL_AMOUNT = TOTAL_AMOUNT-float(new_ga) 
            rest_ava[single["wallet"]] = 0 # no rest money for them to buy more
            RIGHT_GUY.append(single["wallet"])
            # print("good number")
        else:
            if deposit_value!=0:
                TOTAL_AMOUNT = TOTAL_AMOUNT-deposit_value/0.01
                rest_ava[single["wallet"]] = 0
                BAD_GUY.append(single["wallet"])
                # print(single["wallet"],str(deposit_value)+"ust",str(float(new_ga)*0.01)+"ust ","fewer or not depsite")
    else:
        # print(single["wallet"],"-------------")
        rest_ava[single["wallet"]]= deposit_value
        CHANCE_GUY.append(single["wallet"])
        LATE_GUY.append(single["wallet"])
        

#stage 2: check rest amount and prefund users, also sort by timestamp
#after the first buy, total amount is decreased.
# print(TOTAL_AMOUNT)
time_hash={}
#loop chance guy to get their deposte timeline and do sort
for t_d in CHANCE_GUY:
    #get history
    info_back = deposite_history(t_d)
    person_time=[]
    for time in info_back['result']['deposit_history']:
        person_time.append(time['date'])
    #get the oldest time for each user
    time_hash[t_d]=min(person_time)

#sort time hash    
value_sorted_result = sorted(time_hash.items(), key=lambda item: item[1], reverse=False)

#generate new sequence to buy
new_seq_address=[]
for srt_td in value_sorted_result:
    new_seq_address.append(srt_td[0])

#step 3: start to buy
success_terra_address={}
rest_terra_address={}
ust_return={}
for t_d in new_seq_address:
    if TOTAL_AMOUNT < rest_ava[t_d]/0.01 and TOTAL_AMOUNT!=0:
        return_ust = (rest_ava[t_d]/0.01-TOTAL_AMOUNT)*0.01
        rest_terra_address[t_d] = total_deposite_address[t_d]-return_ust 
        ust_return[t_d]=return_ust
        # print(total_deposite_address[t_d],return_ust,rest_terra_address[t_d])
        TOTAL_AMOUNT = 0
    elif TOTAL_AMOUNT > rest_ava[t_d]/0.01:
        TOTAL_AMOUNT = TOTAL_AMOUNT-(rest_ava[t_d]/0.01)
        success_terra_address[t_d] = total_deposite_address[t_d]
        ust_return[t_d]=0
    elif TOTAL_AMOUNT==0:
        if t_d in LATE_GUY:
           rest_terra_address[t_d] = 0
        else:
           rest_terra_address[t_d] = g_al[t_d]
        ust_return[t_d] = rest_ava[t_d]


#step 4: collecting data and save to csv file
all=[]
json_all=[]
for key in success_terra_address.keys():
    data=[]
    data.append(key)
    data.append(float(success_terra_address[key])/0.01)
    data.append(ust_return[key])
    all.append(data)
    hashdata={}
    hashdata["user_addr"] = key
    hashdata["allocation"] = str(round(float(success_terra_address[key])/0.01,6))
    hashdata["refunded"] = str(round(ust_return[key]*MILLION,6))
    json_all.append(hashdata)

for key in rest_terra_address.keys():
    # print(key,rest_terra_address[key],"8**8888")
    data=[]
    data.append(key)
    data.append(float(rest_terra_address[key]))
    data.append(ust_return[key])
    all.append(data)
    hashdata={}
    hashdata["user_addr"] = key
    hashdata["allocation"] = str(round(float(rest_terra_address[key]),6))
    hashdata["refunded"] = str(round(ust_return[key]*MILLION,6))
    json_all.append(hashdata)

for x in RIGHT_GUY:
   data=[]
   data.append(x)
   data.append(float(g_al[x])/0.01)
   data.append(0)
   all.append(data)
   hashdata={}
   hashdata["user_addr"] = x
   hashdata["allocation"] = str(round(float(g_al[x])/0.01,6))
   hashdata["refunded"] = "0"
   json_all.append(hashdata)

for y in BAD_GUY:
    hashdata={}
    data=[]
    data.append(y)
    data.append(str(float(total_deposite_address[y])/0.01))
    data.append(0)
    all.append(data)
    hashdata["user_addr"] = y
    hashdata["allocation"] = str(round(float(total_deposite_address[y])/0.01,6))
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


