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
# dicts = {'terra1q5sa7eh5k5a2m6ma8jdtd9u6r9u55and2pqrru': 'husband tooth quick share crouch chronic biology visit basket smoke capital dignity dash sponsor festival banner loan ready move critic sponsor symbol broccoli timber', 'terra1len2wh0v7unmp543xhndhgrzcadj4fr64j6mkp': 'cement bacon office enlist august youth ski airport jar trust employ barely control style wealth average economy guard close walnut hurry laugh pupil unfold', 'terra17pupj6s57uapctk4pek2vhu8zdu4nxy6y8g7ew': 'venue penalty rail spray scene trumpet tip rural ready tip cushion note found motion gallery song civil retire sponsor relief rack anxiety rude cake' , 'terra1elk88ssjcdhkzx3sx8tnux6dk6nsdspmf3fuat': 'develop armor chair order anchor core essay visa upon extend secret goat blood indoor marble already kingdom blind slice devote unable over sun cost', 'terra1vsl60v2au6cpjn3dln9ewqz3zwjtg28gz4dv2x': 'enter vote confirm spare liberty engine hope bind voice curtain tumble tool weird august police basic solution ready episode canvas off paddle ignore bachelor', 'terra1k8p673zzmwp48us23frq8w7r3j4g9k3p96rlqc': 'trouble pumpkin sentence mean until axis involve tackle ostrich breeze excuse lounge music avocado garden squeeze soda comic aspect chair gauge rice explain task', 'terra1mrxyq38lnrsex6zzt2s2fgrmsf5d5a5rrrrmgl': 'scene good boss prefer scene cricket month early talent curious kiwi unknown eyebrow true someone fame coconut garage thunder rifle offer decorate effort give', 'terra1z4y99xjnul5clr7uxf7q8qynu2c7vfm9d7w0fn': 'response shock slight speed ski trim october service correct inflict creek path ice slender hundred list dish shove chair such print beauty trigger cycle', 'terra1tqftvcj5yas3w5le4n4eqaqwxqzryjxvya2hee': 'surge scheme canal trick modify sleep eyebrow original sibling claw moment mom list drift accuse toss snow twelve amount run toss cruise scrub winner', 'terra10rqqzc98nvd8jy85242ycgkdacfeeuzcxu7q0v': 'video grace seminar chronic gentle draft daughter warfare eye detail lift today fuel relief roast beef blanket tray insane mixed purpose obscure dentist trick', 'terra12r77hf5vxlgpvhwg6865hqc5swu0wa8rdnmnga': 'also panel wood voice merit deputy bulk know chair rival spot congress call drip bonus vault matter quiz crumble rough ghost dress drum fold', 'terra1ruth5q6gxkttqzjsjgta004y0k8xl37vp4lnwm': 'gas text pretty risk burger focus jewel hen shop favorite fragile submit forum truly swarm census coil survey swim better lens rib time tribe', 'terra162xqavwxxq4pgkg5nxxq378tm5cvgtncck2fjd': 'amused toss rare curious sustain budget calm jungle aspect tragic problem cluster equal photo effort chest submit olympic fiscal program arena have segment gym', 'terra1f09rq3lzgscteytt4aljm3jxfg53aa39886dmn': 'balcony beef beyond equal dress honey book cigar screen shrimp amused zebra acid pause atom cargo nasty initial item believe sadness napkin together half', 'terra1sug4e5nm44y6233hpxzuvt9fkkwke8z6x89dr6': 'monkey double about win photo during lab skill level open flavor business swim hire figure space mansion tourist sun artist visual give exchange dice', 'terra16rfvcz5sz82all3hpxj8ea46g89zlth6xkssup': 'document expand piano flee stool diary again run apart slam bunker stereo frame chunk degree ceiling truck sorry garbage wealth sheriff early control absent', 'terra1fxg5wy8dqc3qkdkt7algpcs79pa7yxn0s2vhvt': 'convince february hill illegal foil change suffer proof kangaroo broken guilt draw cat insane wish cycle noodle label rally sure flock visit shrug engine', 'terra1w8ay2kdpv6x2ceaw8ys4zgvy22rlyqjqp0pq29': 'garment attend tide exercise wage spider rack suit note fire junk small reject physical grant water juice sure voyage summer decline cannon kingdom pause', 'terra1gp3wrux6mz2fnncm5g2q86p9l22uyem64k32we': 'must where menu chalk spoil knife reveal spoon require have produce indoor night tower anger ten sample giggle trophy sight plunge repeat cream post', 'terra155er4pfrkrsek0g6k0mc0vpd5catshs0gkulwk': 'cause goat thing rather water cliff pond crew wrist glare october range outer you pizza child pipe injury need trip exotic vicious social neither', 'terra1squm9h978rc3lx9dudhh4gny6jt3zy92u0r88y': 'bulk pink media swallow visa fantasy that hurt culture town cruel duty enact abstract destroy snow elbow hybrid dwarf sponsor diet stable odor know', 'terra1gs4y7ls8s2rfrla2y79syyxnfxf3mpqlzzuawa': 'castle nest lucky educate stock wealth sketch young movie task history current mix destroy lyrics vendor panel tape rhythm oppose sight found liar bamboo', 'terra1cwt7jjsjpkefajg02vt43l65hxftxfclytdayu': 'post payment blanket mother table galaxy monkey spend spatial reopen almost effort bright winter degree echo treat say trip chair dune sheriff crumble onion', 'terra1ukx0cyxqy5h8ldjzyg0paj0mt9rzc3gnq2z8s6': 'broken lift above mirror tone girl goose annual choice service hedgehog write speak excite off welcome bid combine very concert garden absurd emotion bread'}
dicts = {'terra1q5sa7eh5k5a2m6ma8jdtd9u6r9u55and2pqrru': 'husband tooth quick share crouch chronic biology visit basket smoke capital dignity dash sponsor festival banner loan ready move critic sponsor symbol broccoli timber', 'terra1len2wh0v7unmp543xhndhgrzcadj4fr64j6mkp': 'cement bacon office enlist august youth ski airport jar trust employ barely control style wealth average economy guard close walnut hurry laugh pupil unfold', 'terra17pupj6s57uapctk4pek2vhu8zdu4nxy6y8g7ew': 'venue penalty rail spray scene trumpet tip rural ready tip cushion note found motion gallery song civil retire sponsor relief rack anxiety rude cake' , 'terra1elk88ssjcdhkzx3sx8tnux6dk6nsdspmf3fuat': 'develop armor chair order anchor core essay visa upon extend secret goat blood indoor marble already kingdom blind slice devote unable over sun cost', 'terra1vsl60v2au6cpjn3dln9ewqz3zwjtg28gz4dv2x': 'enter vote confirm spare liberty engine hope bind voice curtain tumble tool weird august police basic solution ready episode canvas off paddle ignore bachelor', 'terra1k8p673zzmwp48us23frq8w7r3j4g9k3p96rlqc': 'trouble pumpkin sentence mean until axis involve tackle ostrich breeze excuse lounge music avocado garden squeeze soda comic aspect chair gauge rice explain task', 'terra1mrxyq38lnrsex6zzt2s2fgrmsf5d5a5rrrrmgl': 'scene good boss prefer scene cricket month early talent curious kiwi unknown eyebrow true someone fame coconut garage thunder rifle offer decorate effort give', 'terra1z4y99xjnul5clr7uxf7q8qynu2c7vfm9d7w0fn': 'response shock slight speed ski trim october service correct inflict creek path ice slender hundred list dish shove chair such print beauty trigger cycle', 'terra1tqftvcj5yas3w5le4n4eqaqwxqzryjxvya2hee': 'surge scheme canal trick modify sleep eyebrow original sibling claw moment mom list drift accuse toss snow twelve amount run toss cruise scrub winner', 'terra10rqqzc98nvd8jy85242ycgkdacfeeuzcxu7q0v': 'video grace seminar chronic gentle draft daughter warfare eye detail lift today fuel relief roast beef blanket tray insane mixed purpose obscure dentist trick', 'terra12r77hf5vxlgpvhwg6865hqc5swu0wa8rdnmnga': 'also panel wood voice merit deputy bulk know chair rival spot congress call drip bonus vault matter quiz crumble rough ghost dress drum fold', 'terra1ruth5q6gxkttqzjsjgta004y0k8xl37vp4lnwm': 'gas text pretty risk burger focus jewel hen shop favorite fragile submit forum truly swarm census coil survey swim better lens rib time tribe', 'terra162xqavwxxq4pgkg5nxxq378tm5cvgtncck2fjd': 'amused toss rare curious sustain budget calm jungle aspect tragic problem cluster equal photo effort chest submit olympic fiscal program arena have segment gym', 'terra1f09rq3lzgscteytt4aljm3jxfg53aa39886dmn': 'balcony beef beyond equal dress honey book cigar screen shrimp amused zebra acid pause atom cargo nasty initial item believe sadness napkin together half', 'terra1sug4e5nm44y6233hpxzuvt9fkkwke8z6x89dr6': 'monkey double about win photo during lab skill level open flavor business swim hire figure space mansion tourist sun artist visual give exchange dice', 'terra16rfvcz5sz82all3hpxj8ea46g89zlth6xkssup': 'document expand piano flee stool diary again run apart slam bunker stereo frame chunk degree ceiling truck sorry garbage wealth sheriff early control absent', 'terra1fxg5wy8dqc3qkdkt7algpcs79pa7yxn0s2vhvt': 'convince february hill illegal foil change suffer proof kangaroo broken guilt draw cat insane wish cycle noodle label rally sure flock visit shrug engine', 'terra1w8ay2kdpv6x2ceaw8ys4zgvy22rlyqjqp0pq29': 'garment attend tide exercise wage spider rack suit note fire junk small reject physical grant water juice sure voyage summer decline cannon kingdom pause', 'terra1gp3wrux6mz2fnncm5g2q86p9l22uyem64k32we': 'must where menu chalk spoil knife reveal spoon require have produce indoor night tower anger ten sample giggle trophy sight plunge repeat cream post', 'terra155er4pfrkrsek0g6k0mc0vpd5catshs0gkulwk': 'cause goat thing rather water cliff pond crew wrist glare october range outer you pizza child pipe injury need trip exotic vicious social neither', 'terra1squm9h978rc3lx9dudhh4gny6jt3zy92u0r88y': 'bulk pink media swallow visa fantasy that hurt culture town cruel duty enact abstract destroy snow elbow hybrid dwarf sponsor diet stable odor know', 'terra1gs4y7ls8s2rfrla2y79syyxnfxf3mpqlzzuawa': 'castle nest lucky educate stock wealth sketch young movie task history current mix destroy lyrics vendor panel tape rhythm oppose sight found liar bamboo', 'terra1cwt7jjsjpkefajg02vt43l65hxftxfclytdayu': 'post payment blanket mother table galaxy monkey spend spatial reopen almost effort bright winter degree echo treat say trip chair dune sheriff crumble onion', 'terra1ukx0cyxqy5h8ldjzyg0paj0mt9rzc3gnq2z8s6': 'broken lift above mirror tone girl goose annual choice service hedgehog write speak excite off welcome bid combine very concert garden absurd emotion bread', 'terra1uqkhx9qy32e25p3f0ax7et7ssf0vysxdl673rh': 'surface glove shine shaft belt subject marine onion open deliver that cloth come invite tenant man canyon tourist public usage inform foil real gate', 'terra10p9v6yt246krt7d66d37yvc6c832vx75w4hjq6': 'demise mushroom bright quick deposit census present unfold mercy depth lecture tree boss snow elevator chief arena foster version acoustic milk oil basic weather', 'terra18sw3ncxxtwqfzx0ar6m72jw6v0df3ppg24p4rt': 'ketchup expect immune elder desk phone pigeon nasty olive exit poet genre canal mean wool blanket tornado giggle alter soap dune object erase mutual', 'terra1sfrj9k6mdzzfw2ad5t3xv647hhtgkjvshzz7rn': 'acid muscle tape dirt will senior drama quiz safe lonely brush egg crunch garden edge legend inner list enable fame lamp casual neglect grow', 'terra12cp66ungms69ytealc977u46wa08spd4p2naku': 'canal opera fetch trap enemy lesson gesture punch eager broken brave cycle renew must festival guitar vanish cushion luxury trash blue evolve slender uniform', 'terra1chj35hatjcf99f5e2htyjkt944y3m7h058vcvy': 'spring dizzy inject amused time coil order parade extend option open family swing sense scheme since top cover spike winner discover grief gown good', 'terra1afnc8zt6mhrd8plwyhf9m3qqc3jh6nys0fw4td': 'deal topic impulse soup glad into staff boring mention situate athlete cake honey deliver critic bomb add lyrics stereo pink shoot notice beach mutual', 'terra19ud7fn5cqlaraa6xuhhfxppr02xs3yl8ll09f4': 'lottery tone chief crane online domain region toy game horse beach hire planet spoil private track mushroom gold flee cube unknown spread admit history', 'terra19tt8g8lj54zly8ecspxelg22xs29rpck8ykdez': 'unlock carry grab fat dry alarm breeze rain blade praise ghost elephant barely pink draft bean twice laundry spoon save dance arm hand aspect', 'terra1e6ftntclwq9urec04v304atqvaxxnj4k7u4hqj': 'tribe taste odor upset obtain shoot dinosaur nest witness climb sausage country economy siren survey plate witness assume damage young salad pencil cheese tomato', 'terra1jue70w2q4dxppv9rd3586wmjc39029fhrywnkn': 'just spy genre fine vacuum claw young cattle angle market piece random together twice other report eight again aspect green ten tiny bind believe', 'terra18atnz5gder8kvqrdetqp64lqrgc6nwkxy6jcf6': 'reduce hero field team ten author tortoise month pledge road sense tag during much fire oven asthma inform lottery document hurdle small cherry daughter', 'terra1xsdsjffyl7sptucgp4rgk702y7uhc997hdwkjd': 'unfair half upon ecology auto cloud sketch merit song stool treat bomb voyage rich quiz focus penalty exhaust place diet chief laptop sell wall', 'terra140pcp2e0sj8ee6j79fn8ldv4n8sxg78gqmdd4r': 'afford erosion chimney frown arena blood profit deposit lonely erode burger liar lens hungry tornado ramp cable reduce mesh pizza twenty bag hunt law', 'terra1scl7r5rgpyq2fwu3fwvlkkgynevx5kfr46lzp7': 'ozone title payment business eagle dose crunch goddess organ tobacco fever vacuum trust use doctor trumpet health room letter crime club task barely angry', 'terra13vhccxl58drgc54d5s9q2hgfnsq7pztmmmhe6w': 'noodle cliff roast orphan lyrics dress yellow traffic cause inch subject dentist country normal rural volcano cloud category depend pink step draft analyst student', 'terra1x7hghft9tspz5se6pj7r8c3d5k7qewk4c7wk00': 'math laptop provide speed blue artefact letter oval luxury frown luxury tip orange table talk wagon knock script artist another pear visual hedgehog cloth', 'terra154cfqkmw5kzmj7jsgaz344aw7dvfkelsdtqh9x': 'approve access divert actor life feel spoon cheese clutch weapon then prosper small wave trim inquiry false faint success student chaos vibrant install candy', 'terra197t5dzlzjewa5dfujxl3wf7cjkx0007w0gymt6': 'daring wing thank when gesture urge borrow space hockey naive feature faint enjoy nut much enter number exile hybrid fruit clutch vacuum payment retire', 'terra1lyzs5guffa3d8wq4cfkxm5p6g7cxfd246tqm2t': 'atom keep motion use unique pipe mix joy dismiss hybrid opinion soda guilt layer razor security tribe divorce express page slot tooth black address'}
deposit_dict={'terra1q5sa7eh5k5a2m6ma8jdtd9u6r9u55and2pqrru': '0', 'terra1len2wh0v7unmp543xhndhgrzcadj4fr64j6mkp': '0', 'terra17pupj6s57uapctk4pek2vhu8zdu4nxy6y8g7ew': '10', 'terra1elk88ssjcdhkzx3sx8tnux6dk6nsdspmf3fuat': '15', 'terra1vsl60v2au6cpjn3dln9ewqz3zwjtg28gz4dv2x': '41.53', 'terra1k8p673zzmwp48us23frq8w7r3j4g9k3p96rlqc': '50', 'terra1mrxyq38lnrsex6zzt2s2fgrmsf5d5a5rrrrmgl': '100', 'terra1z4y99xjnul5clr7uxf7q8qynu2c7vfm9d7w0fn': '0', 'terra1tqftvcj5yas3w5le4n4eqaqwxqzryjxvya2hee': '0', 'terra10rqqzc98nvd8jy85242ycgkdacfeeuzcxu7q0v': '22', 'terra12r77hf5vxlgpvhwg6865hqc5swu0wa8rdnmnga': '50', 'terra1ruth5q6gxkttqzjsjgta004y0k8xl37vp4lnwm': '80', 'terra162xqavwxxq4pgkg5nxxq378tm5cvgtncck2fjd': '103.82', 'terra1f09rq3lzgscteytt4aljm3jxfg53aa39886dmn': '103.82', 'terra1sug4e5nm44y6233hpxzuvt9fkkwke8z6x89dr6': '500', 'terra16rfvcz5sz82all3hpxj8ea46g89zlth6xkssup': '1000', 'terra1fxg5wy8dqc3qkdkt7algpcs79pa7yxn0s2vhvt': '1200', 'terra1w8ay2kdpv6x2ceaw8ys4zgvy22rlyqjqp0pq29': '1250', 'terra1gp3wrux6mz2fnncm5g2q86p9l22uyem64k32we': '1300', 'terra155er4pfrkrsek0g6k0mc0vpd5catshs0gkulwk': '10000', 'terra1squm9h978rc3lx9dudhh4gny6jt3zy92u0r88y': '0', 'terra1gs4y7ls8s2rfrla2y79syyxnfxf3mpqlzzuawa': '0', 'terra1cwt7jjsjpkefajg02vt43l65hxftxfclytdayu': '8', 'terra1ukx0cyxqy5h8ldjzyg0paj0mt9rzc3gnq2z8s6': '100', 'terra1uqkhx9qy32e25p3f0ax7et7ssf0vysxdl673rh': '150', 'terra10p9v6yt246krt7d66d37yvc6c832vx75w4hjq6': '165', 'terra18sw3ncxxtwqfzx0ar6m72jw6v0df3ppg24p4rt': '174.42', 'terra1sfrj9k6mdzzfw2ad5t3xv647hhtgkjvshzz7rn': '200', 'terra12cp66ungms69ytealc977u46wa08spd4p2naku': '2000', 'terra1chj35hatjcf99f5e2htyjkt944y3m7h058vcvy': '0', 'terra1afnc8zt6mhrd8plwyhf9m3qqc3jh6nys0fw4td': '0', 'terra19ud7fn5cqlaraa6xuhhfxppr02xs3yl8ll09f4': '10.5', 'terra19tt8g8lj54zly8ecspxelg22xs29rpck8ykdez': '257.48', 'terra1e6ftntclwq9urec04v304atqvaxxnj4k7u4hqj': '1000', 'terra1jue70w2q4dxppv9rd3586wmjc39029fhrywnkn': '0', 'terra18atnz5gder8kvqrdetqp64lqrgc6nwkxy6jcf6': '0', 'terra1xsdsjffyl7sptucgp4rgk702y7uhc997hdwkjd': '100', 'terra140pcp2e0sj8ee6j79fn8ldv4n8sxg78gqmdd4r': '500', 'terra1scl7r5rgpyq2fwu3fwvlkkgynevx5kfr46lzp7': '840.56', 'terra13vhccxl58drgc54d5s9q2hgfnsq7pztmmmhe6w': '1000', 'terra1x7hghft9tspz5se6pj7r8c3d5k7qewk4c7wk00': '5000', 'terra154cfqkmw5kzmj7jsgaz344aw7dvfkelsdtqh9x': '0', 'terra197t5dzlzjewa5dfujxl3wf7cjkx0007w0gymt6': '1000', 'terra1lyzs5guffa3d8wq4cfkxm5p6g7cxfd246tqm2t': '2000'}
# deposit_dict={'terra1q5sa7eh5k5a2m6ma8jdtd9u6r9u55and2pqrru': '150'}

# print(deposit_dict)

# Funding test wallets

# SEED = "lunar modify clutch like car business dizzy hero tunnel alley rough valve fork maid cannon midnight twenty crime similar steak connect awake slender unlock"
# mk = MnemonicKey(mnemonic=SEED)
# wallet = terra.wallet(mk)
# # print wallet address
# print(wallet.key.acc_address)
# seed(1)
# msg_ust=[]
# for key in deposit_dict:
#     # AMOUNT = randint(10, 500)
#     AMOUNT = float(deposit_dict[key])+10
#     msg_ust=MsgSend(
#         wallet.key.acc_address,
#         key,
#         str(int(AMOUNT*MILLION)) + "uusd" # send random amount 1 in UST,
#     )
#     tx = wallet.create_and_sign_tx(msgs=[msg_ust], memo="funding test wallets")
#     result = terra.tx.broadcast(tx)
#     print(result)
#     sleep(6)




#deposit part

seed(1)
deposit_contract_address='terra1cktfu50ahjwxwrryzlpuxpwwwajt69cj55ud55'
deposit_contract_new="terra1kc5vkpveadchmwsjza8s0hcwkh53pqkktkdumc"
# Depositing money
for key in deposit_dict:
    print(key,"-----")
    mk = MnemonicKey(mnemonic=dicts[key])
    wallet = terra.wallet(mk)
# print wallet address
    print(wallet.key.acc_address)
    balance = terra.bank.balance(key)
    min_amount_in_wallet = balance.get('uusd').amount/ MILLION
    print("amount of money in wallet")
    print(min_amount_in_wallet,deposit_dict[key])
    if deposit_dict[key] !="0":
        deposit_amount=int(float(deposit_dict[key])*MILLION)
        execute_msg={
            "deposit": {}
                    }
        msg=MsgExecuteContract(
            sender=key,
            contract=deposit_contract_new,
            execute_msg=execute_msg,
            coins=str(deposit_amount) + "uusd" # deposit amount
            )
        tx = wallet.create_and_sign_tx(msgs=[msg], memo="deposit")
        result = terra.tx.broadcast(tx)
        print(result)
        sleep(6)
