dic = [
    {"name" : "abay" , "age" : 22},
    {"name" : "aida" , "age" : 18}
]
list = ["abay"]
for i in dic:
    if i["name"] in list  and i["age"] > 18 and i["age"] < 24:
        print ("pass")
    else:
        print ("denied")