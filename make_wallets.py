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
NETWORK = 'TESTNET'
MILLION = 1000000
TWOHUNDREDANDFIFTYTHOUSAND=250000
HUNDREDTHOUSAND=100000


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



# Connect to netowrk
terra = LCDClient(chain_id=chain_id, url=public_node_url) 

# Make 10 Wallets
wallet_list=list(range(0, 10))
dicts = {}

for wallet in wallet_list:
    print(wallet)
# Print block height
#print(terra.tendermint.block_info()['block']['header']['height'])   
    # Create new wallet with no seed
    mk = MnemonicKey()
    wallet = terra.wallet(mk)
    print(wallet.key.acc_address)
    print(mk.mnemonic)
    dicts[wallet.key.acc_address] = mk.mnemonic
print(dicts)

