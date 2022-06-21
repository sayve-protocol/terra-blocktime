import json
result={}
with open("output_splice.json", encoding="utf-8") as f:
    data = json.load(f)
    # print(data)
    for block in data:
        # print(block["update"])
        for ur in block["update"]:
            # print(ur)
            result[ur["user_addr"]] = ur["allocation"]


with open("update_users.json", encoding="utf-8") as f:
    data = json.load(f)
    # print(data)
    for block in data:
        # print(block["update"])
        for ur in block["update"]:
            # result[ur["user_addr"]]= result[ur["user_addr"]].replace(".0",'')
            if result[ur["user_addr"]]!=ur["allocation"]:
                print(result[ur["user_addr"]],ur["allocation"])
            else:
                print("ok, it is")
            # result[ur["user_addr"]] = usr["allocation"]