import json
import collections
user=[]
def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]


with open("output.json", encoding="utf-8") as f:
    data = json.load(f)
    user = data[0]["update"]

list2 = list_split(user, 30)
out=[]
for item in list2:
    update={}
    update["update"] = item
    out.append(update)


with open('output_splice.json','w') as f:
    json.dump(out,f)
