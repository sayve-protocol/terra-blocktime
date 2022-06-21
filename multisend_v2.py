import http.client
import requests
import urllib3.exceptions
from terra_sdk.client.lcd import LCDClient
from terra_sdk.exceptions import LCDResponseError
from terra_sdk.key.mnemonic import MnemonicKey
from terra_sdk.core.auth import StdFee
from terra_sdk.core.bank import MsgSend
from terra_sdk.core.wasm import MsgExecuteContract
from terra_sdk.core.coins import Coins

from contact_addresses import contact_addresses_lookup
from time import sleep
import base64
import os
import json
import time

import csv

terra_address=[]
sayve_amount=[]
ust_amount=[]

with open('input.csv', encoding='utf-8') as f:
    reader = csv.reader(f)
    header = next(reader)
    for row in reader:
        t_address=row[0].rstrip()
        s_amount=row[1].rstrip()
        u_admount=row[2].rstrip()
        terra_address.append(t_address)
        sayve_amount.append(float(s_amount))
        ust_amount.append(float(u_admount))
        print(t_address,s_amount,u_admount)
# seed phrase for test wallet 1
SEED = "husband tooth quick share crouch chronic biology visit basket smoke capital dignity dash sponsor festival banner loan ready move critic sponsor symbol broccoli timber"
NETWORK = 'TESTNET'
MILLION = 1000000
TWOHUNDREDANDFIFTYTHOUSAND=250000
HUNDREDTHOUSAND=100000

def get_terra_gas_prices():
    try:
        r = requests.get("https://fcd.terra.dev/v1/txs/gas_prices")
        r.raise_for_status()
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.HTTPError as err:
        print(f"Could not fetch get_terra_gas_prices from Terra's FCD. Error message: {err}")


if NETWORK == 'MAINNET':
    chain_id = 'columbus-5'
    public_node_url = 'https://lcd.terra.dev'
    contact_addresses = contact_addresses_lookup(network='MAINNET')
    tx_look_up = f'https://finder.terra.money/{chain_id}/tx/'


else:
    chain_id = 'bombay-12'
    public_node_url = 'https://bombay-lcd.terra.dev'
    contact_addresses = contact_addresses_lookup(network='TESTNET')
    tx_look_up = f'https://finder.terra.money/{chain_id}/tx/'


# Get fee estimate
terra_gas_prices = get_terra_gas_prices()
print("gas estimates")
print(terra_gas_prices)
# Connect to netowrk
terra = LCDClient(chain_id=chain_id, url=public_node_url, gas_prices=terra_gas_prices['uusd']+"uusd",
        gas_adjustment=2) 



# Print block height
print(terra.tendermint.block_info()['block']['header']['height'])   
mk = MnemonicKey(mnemonic=SEED)
wallet = terra.wallet(mk)
# print wallet address
print(wallet.key.acc_address)

# Sending  1.03, 0.9 and 4.44 Sayve token
sayve_token='terra16t7x97wuckxm5h927jygjfrt3tcwrzh3u2rlqm'



header = ['terra_address', 'sayve_amount', 'ust_amount','txhash']

all=[]
msgall=[]
for x in range(0,len(terra_address)):
        data=[]
        execute_sayve = "execute_sayve_"+str(x)
        msg_sayve = "msg_sayve_"+str(x)
        msg_ust = "msg_ust_"+str(x)
        execute_sayve = {
            "transfer": {
                "amount": str(int(sayve_amount[x]*MILLION)),
                "recipient": terra_address[x],
            }
        }
        msg_sayve = MsgExecuteContract(
            sender=wallet.key.acc_address,
            contract=sayve_token,
            execute_msg=execute_sayve,
            coins=None
        )

        msg_ust = MsgSend(
            wallet.key.acc_address,
            terra_address[x],
            str(int(ust_amount[x]*MILLION)) + "uusd"  # send amount 1.5 in UST,
        )
        msgall.append(msg_sayve)
        msgall.append(msg_ust)
        tx = wallet.create_and_sign_tx(msgs=[msg_sayve,msg_ust], memo="testing sending sayve and ust at one time")
        result = terra.tx.broadcast(tx)
        data.append(terra_address[x])
        data.append(sayve_amount[x])
        data.append(ust_amount[x])
        data.append(result.txhash)
        all.append(data)
        sleep(6)



with open('output.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(header)
    writer.writerows(all)




