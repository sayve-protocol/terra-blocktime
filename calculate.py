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

import base64
import os
import json
import time
import requests
import json
import csv

TIME_FUTURE=1656374400
TIME_NOW=int( time.time() )
AVERAGE_BLOCK_TIME=6
DURATION=float((TIME_FUTURE-TIME_NOW)/AVERAGE_BLOCK_TIME)

# Get time with https://www.epochconverter.com/
NETWORK = 'MAINNET'


if NETWORK == 'MAINNET':
    chain_id = 'columbus-5'
    public_node_url = 'https://lcd.terra.dev'
    tx_look_up = f'https://finder.terra.money/{chain_id}/tx/'


else:
    chain_id = 'bombay-12'
    public_node_url = 'https://bombay-lcd.terra.dev'
    tx_look_up = f'https://finder.terra.money/{chain_id}/tx/'


terra = LCDClient(chain_id=chain_id, url=public_node_url) 



# Print block height
print("Current Block Time")
print(terra.tendermint.block_info()['block']['header']['height']) 

# Print block at future time
print("Block time at snapshot")
print(float(terra.tendermint.block_info()['block']['header']['height']) +DURATION)