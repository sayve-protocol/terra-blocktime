from terra_sdk.client.lcd import LCDClient
from terra_sdk.exceptions import LCDResponseError
import time


# Get Unix time for snapshot with https://www.epochconverter.com/ or https://www.unixtimestamp.com/
TIME_FUTURE=1681398000

# Unix time
TIME_NOW=int( time.time() )
print("time now")
print(TIME_NOW)
# Get average block time https://terra-scanner.vercel.app/
AVERAGE_BLOCK_TIME=6.03
DURATION=float((TIME_FUTURE-TIME_NOW)/AVERAGE_BLOCK_TIME)


NETWORK = 'MAINNET'


if NETWORK == 'MAINNET':
    chain_id = 'phoenix-1'
    public_node_url = 'https://phoenix-lcd.terra.dev'
    tx_look_up = f'https://finder.terra.money/{chain_id}/tx/'


else:
    chain_id = 'pisco-1'
    public_node_url = 'https://pisco-lcd.terra.dev'
    tx_look_up = f'https://finder.terra.money/{chain_id}/tx/'


terra = LCDClient(chain_id=chain_id, url=public_node_url) 



# Print block height
print("Current Block Time")
print(terra.tendermint.block_info()['block']['header']['height']) 

# Print block at future time
print("Block time at snapshot")
print(float(terra.tendermint.block_info()['block']['header']['height']) +DURATION)
