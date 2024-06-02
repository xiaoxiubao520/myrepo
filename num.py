import pandas as pd
from pyecharts.charts import Line,Grid
from pyecharts import options as opts
from pyecharts.globals import ThemeType
def summary_num():
    dt = {}
    for i in set(data["事件类型"]):
        da = data[data["事件类型"] == i]
        sm = len(da)
        city = da[da["驾驶域"] == "城市"]

        city_yes = len(city[city["realtime_if_link"] == "issueFinder"])
        speed = da[da["驾驶域"] == "高速"]
        speed_yes = len(speed[speed["realtime_if_link"] == "issueFinder"])
        km3 = round(sm / km2 * 100, 3)

        dt.update({
            i: [sm, km3, len(speed), speed_yes, len(city), city_yes]
        })

    f.write("事件,总数,百公里触发次数,高速全部,高速有回传,城市全部,城市有回传\n")
    for i in ["CIPV_VEH_LOST",
              "CIPV_POS_EXCEPTION_VEH",
              "CIPV_POS_SHIFT_DIFF_VEH",
              "CIPV_THETA_DIFF_VEH",
              "LARGE_VEHICLE_POS_EXCEPTION",
              "LARGE_VEHICLE_POS_SHIFT_DIFF",
              "LARGE_VEHICLE_THETA_DIFF",
              "NarrowCIPV", "RadarAssignFusionMining",
              "RadarTrackFusionMining",
              "UnderlyingVelocityFusionMining",
              "VRUVelocityFusionMining",
              "RadarPositionFusionMining"]:
        if i in dt.keys():
            f.write("%s,%s\n" % (i, str(dt[i]).strip("[]")))
        else:
            f.write(f"{i},0,0,0,0,0,0\n")
    f.write(",自动驾驶里程,%d\n\n" % km2)


def mb_km():
    master_km = km[km["version"].str.find("8.3.4") >= 0]["自动驾驶里程"]
    master_sum = master_km.str[:-2].astype(float).sum()
    rb_km = km[(km["version"].str.find("8.4.40") >= 0) | (km["version"].str.find("8.4.37") >= 0)]["自动驾驶里程"]
    rb_sum = rb_km.str[:-2].astype(float).sum()
    print("master:", int(master_sum))
    print("rb:", int(rb_sum))
    return master_sum, rb_sum




def version_num():
    #f = open("2.csv", "w")
    vr = {}
    versi= set(data["版本"])     
    version_list = sorted(versi,key=lambda x:int(x.replace(".",""))) 
    vr["ver_list"] = version_list
    for i in set(data["事件类型"]):
            ex = data[data["事件类型"]==i]["版本"]
            a = ex.to_list()
            for ver in version_list:
                if ver in a:
                    try:
                        vr[i].append([ver,len(ex)])
                    except Exception as e:
                        vr[i] = []
                        vr[i].append([ver,len(ex)])
                else:
                    try:
                        vr[i].append([ver,0])
                    except Exception as e:
                        vr[i] = []
                        vr[i].append([ver,0])
            # for ip, count in j:
            #     if ip in ip_sums:
            #         ip_sums[ip] += count
            #     else:
            #         ip_sums[ip] = count
            # print(ip_sums)
    #         f.write("%s,%s\n"%(i,str(j).replace('[','').replace(']','').replace('\'','')))
    #     f.write("\n\n")
    # f.close()
    return vr

def version_master(kk):
    for m, t in enumerate([master, rb]):
        dt = {}
        f.write("事件,总数,百公里触发次数,高速全部,高速有回传,城市全部,城市有回传\n")
        for i in set(t["事件类型"]):
            da = t[t["事件类型"] == i]
            sm = len(da)
            city = da[da["驾驶域"] == "城市"]

            city_yes = len(city[city["realtime_if_link"] == "issueFinder"])
            speed = da[da["驾驶域"] == "高速"]
            speed_yes = len(speed[speed["realtime_if_link"] == "issueFinder"])
            km3 = round(sm / kk[m] * 100, 3)

            dt.update({
                i: [sm, km3, len(speed), speed_yes, len(city), city_yes]
            })

        for i in ["CIPV_VEH_LOST",
                  "CIPV_POS_EXCEPTION_VEH",
                  "CIPV_POS_SHIFT_DIFF_VEH",
                  "CIPV_THETA_DIFF_VEH",
                  "LARGE_VEHICLE_POS_EXCEPTION",
                  "LARGE_VEHICLE_POS_SHIFT_DIFF",
                  "LARGE_VEHICLE_THETA_DIFF",
                  "NarrowCIPV",
                  "RadarAssignFusionMining",
                  "RadarTrackFusionMining",
                  "UnderlyingVelocityFusionMining",
                  "VRUVelocityFusionMining",
                  "RadarPositionFusionMining"]:
            if i in dt.keys():
                f.write("%s,%s\n" % (i, str(dt[i]).strip("[]")))
            else:
                f.write(f"{i},0,0,0,0,0,0\n")
        f.write(",自动驾驶里程,%d\n\n" % kk[m])

def rende(data:dict):  
    line = Line(init_opts=opts.InitOpts(width="2500px",height="1700px"))
    # 添加X轴和Y轴的数据  
    line.add_xaxis(data["ver_list"])
    for i,j in data.items():
        num = list(map(lambda x:x[1],j))
        line.add_yaxis(f"{i}",num,linestyle_opts=opts.LineStyleOpts(width=3),label_opts=opts.LabelOpts(is_show=False))

    line.set_global_opts(title_opts=opts.TitleOpts(title="版本触发次数",pos_left="center"),legend_opts=opts.LegendOpts(orient='vertical', pos_right='center',pos_top='75%'),
                          xaxis_opts=opts.AxisOpts(
                            splitline_opts=opts.SplitLineOpts(is_show=False),
                            axislabel_opts=opts.LabelOpts(interval=0, rotate=-90)
                        ))
    g = Grid()
    g.add(line,grid_opts=opts.GridOpts(pos_bottom="40%"))
    # 渲染图表为HTML文件  
    g.render()


if __name__ == "__main__":
    file = "D:\GPT浏览器下载\通用打点列表--最多显示1万条.xlsx"
    data = pd.read_excel(file, header=1)

    # km = pd.read_excel(file, sheet_name="里程", header=1)

    # km2 = int(km[km["car_id"] == " 合计"]["自动驾驶里程"].tolist()[0].replace(",", "")[:-4])
    # f = open("1.csv", "w")
    master = data[data["版本"].str.find("8.3.4") >= 0]
    rb = data[(data["版本"].str.find("8.4.40") >= 0) | (data["版本"].str.find("8.4.37") >= 0)]
    # summary_num()
    # kk = mb_km()
    # version_master(kk)
    vr = version_num()
    rende(vr)
    # f.close()
