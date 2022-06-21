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
from random import seed
from random import randint
# seed phrase for test wallet 1
#SEED = "husband tooth quick share crouch chronic biology visit basket smoke capital dignity dash sponsor festival banner loan ready move critic sponsor symbol broccoli timber"
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
# Connect to netowrk
terra = LCDClient(chain_id=chain_id, url=public_node_url, gas_prices=terra_gas_prices['uusd']+"uusd",
        gas_adjustment=2) 
dicts = {'terra1q5sa7eh5k5a2m6ma8jdtd9u6r9u55and2pqrru': 'husband tooth quick share crouch chronic biology visit basket smoke capital dignity dash sponsor festival banner loan ready move critic sponsor symbol broccoli timber', 'terra1len2wh0v7unmp543xhndhgrzcadj4fr64j6mkp': 'cement bacon office enlist august youth ski airport jar trust employ barely control style wealth average economy guard close walnut hurry laugh pupil unfold', 'terra17pupj6s57uapctk4pek2vhu8zdu4nxy6y8g7ew': 'venue penalty rail spray scene trumpet tip rural ready tip cushion note found motion gallery song civil retire sponsor relief rack anxiety rude cake' , 'terra1elk88ssjcdhkzx3sx8tnux6dk6nsdspmf3fuat': 'develop armor chair order anchor core essay visa upon extend secret goat blood indoor marble already kingdom blind slice devote unable over sun cost', 'terra1vsl60v2au6cpjn3dln9ewqz3zwjtg28gz4dv2x': 'enter vote confirm spare liberty engine hope bind voice curtain tumble tool weird august police basic solution ready episode canvas off paddle ignore bachelor', 'terra1k8p673zzmwp48us23frq8w7r3j4g9k3p96rlqc': 'trouble pumpkin sentence mean until axis involve tackle ostrich breeze excuse lounge music avocado garden squeeze soda comic aspect chair gauge rice explain task', 'terra1mrxyq38lnrsex6zzt2s2fgrmsf5d5a5rrrrmgl': 'scene good boss prefer scene cricket month early talent curious kiwi unknown eyebrow true someone fame coconut garage thunder rifle offer decorate effort give', 'terra1z4y99xjnul5clr7uxf7q8qynu2c7vfm9d7w0fn': 'response shock slight speed ski trim october service correct inflict creek path ice slender hundred list dish shove chair such print beauty trigger cycle', 'terra1tqftvcj5yas3w5le4n4eqaqwxqzryjxvya2hee': 'surge scheme canal trick modify sleep eyebrow original sibling claw moment mom list drift accuse toss snow twelve amount run toss cruise scrub winner', 'terra10rqqzc98nvd8jy85242ycgkdacfeeuzcxu7q0v': 'video grace seminar chronic gentle draft daughter warfare eye detail lift today fuel relief roast beef blanket tray insane mixed purpose obscure dentist trick', 'terra12r77hf5vxlgpvhwg6865hqc5swu0wa8rdnmnga': 'also panel wood voice merit deputy bulk know chair rival spot congress call drip bonus vault matter quiz crumble rough ghost dress drum fold', 'terra1ruth5q6gxkttqzjsjgta004y0k8xl37vp4lnwm': 'gas text pretty risk burger focus jewel hen shop favorite fragile submit forum truly swarm census coil survey swim better lens rib time tribe', 'terra162xqavwxxq4pgkg5nxxq378tm5cvgtncck2fjd': 'amused toss rare curious sustain budget calm jungle aspect tragic problem cluster equal photo effort chest submit olympic fiscal program arena have segment gym', 'terra1f09rq3lzgscteytt4aljm3jxfg53aa39886dmn': 'balcony beef beyond equal dress honey book cigar screen shrimp amused zebra acid pause atom cargo nasty initial item believe sadness napkin together half', 'terra1sug4e5nm44y6233hpxzuvt9fkkwke8z6x89dr6': 'monkey double about win photo during lab skill level open flavor business swim hire figure space mansion tourist sun artist visual give exchange dice', 'terra16rfvcz5sz82all3hpxj8ea46g89zlth6xkssup': 'document expand piano flee stool diary again run apart slam bunker stereo frame chunk degree ceiling truck sorry garbage wealth sheriff early control absent', 'terra1fxg5wy8dqc3qkdkt7algpcs79pa7yxn0s2vhvt': 'convince february hill illegal foil change suffer proof kangaroo broken guilt draw cat insane wish cycle noodle label rally sure flock visit shrug engine', 'terra1w8ay2kdpv6x2ceaw8ys4zgvy22rlyqjqp0pq29': 'garment attend tide exercise wage spider rack suit note fire junk small reject physical grant water juice sure voyage summer decline cannon kingdom pause', 'terra1gp3wrux6mz2fnncm5g2q86p9l22uyem64k32we': 'must where menu chalk spoil knife reveal spoon require have produce indoor night tower anger ten sample giggle trophy sight plunge repeat cream post', 'terra155er4pfrkrsek0g6k0mc0vpd5catshs0gkulwk': 'cause goat thing rather water cliff pond crew wrist glare october range outer you pizza child pipe injury need trip exotic vicious social neither', 'terra1squm9h978rc3lx9dudhh4gny6jt3zy92u0r88y': 'bulk pink media swallow visa fantasy that hurt culture town cruel duty enact abstract destroy snow elbow hybrid dwarf sponsor diet stable odor know', 'terra1gs4y7ls8s2rfrla2y79syyxnfxf3mpqlzzuawa': 'castle nest lucky educate stock wealth sketch young movie task history current mix destroy lyrics vendor panel tape rhythm oppose sight found liar bamboo', 'terra1cwt7jjsjpkefajg02vt43l65hxftxfclytdayu': 'post payment blanket mother table galaxy monkey spend spatial reopen almost effort bright winter degree echo treat say trip chair dune sheriff crumble onion', 'terra1ukx0cyxqy5h8ldjzyg0paj0mt9rzc3gnq2z8s6': 'broken lift above mirror tone girl goose annual choice service hedgehog write speak excite off welcome bid combine very concert garden absurd emotion bread'}

# Funding test wallets

SEED = "lunar modify clutch like car business dizzy hero tunnel alley rough valve fork maid cannon midnight twenty crime similar steak connect awake slender unlock"
mk = MnemonicKey(mnemonic=SEED)
wallet = terra.wallet(mk)
# print wallet address
print(wallet.key.acc_address)
seed(1)
msg_ust=[]
for key in dicts:
    AMOUNT = randint(1, 500)
    msg_ust=MsgSend(
        wallet.key.acc_address,
        key,
        str(int(AMOUNT*MILLION)) + "uusd" # send random amount 1 in UST,
    )
    tx = wallet.create_and_sign_tx(msgs=[msg_ust], memo="funding test wallets")
    result = terra.tx.broadcast(tx)
    print(result)
    sleep(6)

seed(1)
deposit_contract_address='terra1cktfu50ahjwxwrryzlpuxpwwwajt69cj55ud55'
# Depositing money
for key in dicts:
    mk = MnemonicKey(mnemonic=dicts[key])
    wallet = terra.wallet(mk)
# print wallet address
    print(wallet.key.acc_address)
    balance = terra.bank.balance(wallet.key.acc_address)
    min_amount_in_wallet = balance.get('uusd').amount/ MILLION
    print("amount of money in wallet")
    print(min_amount_in_wallet)
    scale = randint(4, 10)
    deposit_amount=int(balance.get('uusd').amount/scale) # deposit 4 to 10th of balance
    print(deposit_amount)
    execute_msg={
        "deposit": {}
                }
    msg=MsgExecuteContract(
        sender=wallet.key.acc_address,
        contract=deposit_contract_address,
        execute_msg=execute_msg,
        coins=str(deposit_amount) + "uusd" # deposit amount
        )
    tx = wallet.create_and_sign_tx(msgs=[msg], memo="deposit")
    result = terra.tx.broadcast(tx)
    print(result)

    sleep(6)
