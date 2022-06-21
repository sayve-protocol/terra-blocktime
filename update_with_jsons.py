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
#SEED = "husband tooth quick share crouch chronic biology visit basket smoke capital dignity dash sponsor festival banner loan ready move critic sponsor symbol broccoli timber"
#SEED= 'hundred student mail february buyer found print keep pond all gym win unique latin pipe ski hurry ivory heart run inquiry among arrange thumb'
NETWORK = 'MAINNET'
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
    deposit_contract_address='terra1zxcdzls7pp0njc5ra6w9l62kdq40mujcestlgx'
    SEED= 'travel build sibling hamster juice orange point inmate raw sweet excuse patch slogan range chunk sight idea lumber thank zebra admit marble place sure'

else:
    chain_id = 'bombay-12'
    public_node_url = 'https://bombay-lcd.terra.dev'
    contact_addresses = contact_addresses_lookup(network='TESTNET')
    tx_look_up = f'https://finder.terra.money/{chain_id}/tx/'
    deposit_contract_address='terra1zjtnwt87tmuw4w5yagzmp2sz6jhnu93r73kp2k'
    SEED= 'hundred student mail february buyer found print keep pond all gym win unique latin pipe ski hurry ivory heart run inquiry among arrange thumb'


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
# print wallet address for admin updating the contract
print(wallet.key.acc_address)



# List of json of addresses to update, this is just an example that is why it repeats same numbers for allocation and returned ust
#, real case every line is unique, also make 30 addresses per json in eaach
import json
f= open('update_users.json')
list_of_jsons_to_update_allocation = json.load(f)


# loop through list of json, for each json, send to smart contract to update users allocation and refund amount
for json in list_of_jsons_to_update_allocation:
    print(json)
    msg=MsgExecuteContract(
        sender=wallet.key.acc_address,
        contract=deposit_contract_address,
        execute_msg=json
        )
    tx = wallet.create_and_sign_tx(msgs=[msg], memo="update contract")
    result = terra.tx.broadcast(tx)
    print(result)

    sleep(10)

