import pandas as pd
file = "/Users/v_huangmin05/Downloads/通用打点数据_1717577869446.xlsx"
data = pd.read_excel(file, header=1)
dt = {}
km = pd.read_excel(file,sheet_name="里程",header=1)
km2 = int(km[km["car_id"]==" 合计"]["自动驾驶里程"].tolist()[0].replace(",","")[:-4])
print(km2)
for i in set(data["事件类型"]):
    da = data[data["事件类型"] == i]
    sm = len(da)
    city = da[da["驾驶域"] == "城市"]

    city_yes = len(city[city["realtime_if_link"] == "issueFinder"])
    speed = da[da["驾驶域"] == "高速"]
    speed_yes = len(speed[speed["realtime_if_link"] == "issueFinder"])
    km3 = round(sm / km2 * 100,3)

    dt.update({
        i:[sm,km3,len(speed),speed_yes,len(city),city_yes]
    })
f = open("1.csv","w")

f.write("事件,总数,百公里触发次数,高速全部,高速有回传,城市全部,城市有回传\n")
for i in ["RadarAssignFusionMining",
"RadarTrackFusionMining",
"UnderlyingVelocityFusionMining",
"VRUVelocityFusionMining",
"RadarPositionFusionMining"]:
     if i in dt.keys():
        f.write("%s,%s\n"%(i,str(dt[i]).strip("[]")))
     else:
         f.write("0,0,0,0,0,0")
f.write(",自动驾驶里程,%d"%km2)
f.close()
