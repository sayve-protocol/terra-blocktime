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

# Message arrays
msg_luna=[]
msg_ust=[]
msg_sayve=[]

# Print block height
print(terra.tendermint.block_info()['block']['header']['height'])   
mk = MnemonicKey(mnemonic=SEED)
wallet = terra.wallet(mk)
# print wallet address
print(wallet.key.acc_address)
# Send money to test wallet 2
RECIPIENT='terra1len2wh0v7unmp543xhndhgrzcadj4fr64j6mkp'
# Once you have your Wallet, you can simply create a StdTx using Wallet.create_and_sign_tx().
print("sending 1 luna")
tx = wallet.create_and_sign_tx(
    msgs=[MsgSend(
        wallet.key.acc_address,
        RECIPIENT,
        "1000000uluna" # send 1 luna
    )],
    memo="test transaction!"
)
# See result
result = terra.tx.broadcast(tx)
print(result)
RECIPIENTS=[
'terra1len2wh0v7unmp543xhndhgrzcadj4fr64j6mkp',
'terra1elk88ssjcdhkzx3sx8tnux6dk6nsdspmf3fuat']

print("sending luna, ust, and sayve to different people in one transaction")
time.sleep(6)
msg_luna.append(MsgSend(
        wallet.key.acc_address,
        RECIPIENTS[0],
        Coins(uluna=2000000), # send 2 luna
    ))

msg_luna.append(MsgSend(
        wallet.key.acc_address,
        RECIPIENTS[1],
        str(int(3*MILLION)) + "uluna" # send amount 1 in UST,
    ))


#the tx is here BlockTxBroadcastResult(height=7963609, txhash='69859D3B833C4B925ABBF6BB9C5EB6A383FF0250F76650127152F450201A1D94'then visit
#tx_look_up+txhas


# Send UST

AMOUNT_UST=[1,1.5] # use array

msg_ust.append(MsgSend(
        wallet.key.acc_address,
        RECIPIENTS[0],
        str(int(AMOUNT_UST[0]*MILLION)) + "uusd" # send amount 1 in UST,
    ))
msg_ust.append(MsgSend(
        wallet.key.acc_address,
        RECIPIENTS[1],
        str(int(AMOUNT_UST[1]*MILLION)) + "uusd" # send amount 1.5 in UST,
    ))


#tx = wallet.create_and_sign_tx(msgs=[msg,msg2], memo="testing sending 1ust and 1.5ust"
#    )


#result = terra.tx.broadcast(tx)
#print(result)

# Sending  1.03, 0.9 and 4.44 Sayve token
sayve_token='terra16t7x97wuckxm5h927jygjfrt3tcwrzh3u2rlqm'
AMOUNT_SAYVE=[1.03,0.9,4.444]
RECIPIENTS=[
'terra1len2wh0v7unmp543xhndhgrzcadj4fr64j6mkp',
'terra1elk88ssjcdhkzx3sx8tnux6dk6nsdspmf3fuat',
'terra17pupj6s57uapctk4pek2vhu8zdu4nxy6y8g7ew']
print("sending 1.03, 0.9 and 4.444 Sayve to 3 different addresses")
execute_msg1={
        "transfer": {
            "amount": str(int(AMOUNT_SAYVE[0]*MILLION)),
            "recipient": RECIPIENTS[0],
        }
    }
msg_sayve.append(MsgExecuteContract(
        sender=wallet.key.acc_address,
        contract=sayve_token,
        execute_msg=execute_msg1,
        coins=None
    ))

execute_msg2={
        "transfer": {
            "amount": str(int(AMOUNT_SAYVE[1]*MILLION)),
            "recipient": RECIPIENTS[1],
        }
    }
msg_sayve.append(MsgExecuteContract(
        sender=wallet.key.acc_address,
        contract=sayve_token,
        execute_msg=execute_msg2,
        coins=None
    ))

execute_msg3={
        "transfer": {
            "amount": str(int(AMOUNT_SAYVE[2]*MILLION)),
            "recipient": RECIPIENTS[2],
        }
    }
msg_sayve.append(MsgExecuteContract(
        sender=wallet.key.acc_address,
        contract=sayve_token,
        execute_msg=execute_msg3,
        coins=None
    ))



tx = wallet.create_and_sign_tx(msgs=[msg_luna[0],msg_luna[1],msg_ust[0],msg_ust[1],msg_sayve[0],msg_sayve[1],msg_sayve[2]], memo="testing ust and sayve"
    )


result = terra.tx.broadcast(tx)
print(result)