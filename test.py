import json
import requests
CONTACT="terra1tkgaag3gpj4suyt6qquudj3jq97xjvmya0zxs6"
MILLION=1000000

def loop_funders():
    try:
        r = requests.get("https://lcd.terra.dev/wasm/contracts/"+CONTACT+"/store?query_msg=%7B%22list%22:%7B%7D%7D")
        # print("https://bombay-lcd.terra.dev/wasm/contracts/"+CONTACT+"/store?query_msg=%7B%22list%22:%7B%7D%7D")
        r.raise_for_status()
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.HTTPError as err:
        print(f"Could not fetch get_terra_gas_prices from Terra's FCD. Error message: {err}")



with open("output.json", encoding="utf-8") as f:
    data = json.load(f)

after={}
for block in data[0]["update"]:
    # print(block["user_addr"],block["allocation"]+block["refunded"])
    after[block["user_addr"]] = float(block["allocation"])/100+float(block["refunded"])/MILLION


all_funders = loop_funders()
for single in all_funders["result"]["investors"]:
    print(single["wallet"],int(single["total"])/MILLION,after[single["wallet"]])