import argparse
import functools
import pandas as pd
from pyecharts.charts import Line, Grid
from pyecharts import options as opts
from pyecharts.globals import ThemeType


def summary_num(f, params):
    """
    计算每个事件类型的触发总数、百公里触发次数、高速场景下触发数量、高速场景下带有回传信息的触发数量、
    城市场景下触发数量、城市场景下带有回传信息的触发数量，并将结果写入文件。
    
    Args:
        f (TextIOWrapper): 文件对象，用于写入结果
    
    Returns:
        None
    """
    dt = {}
    data = params["data"]
    for i in set(data["事件类型"]):
        da = data[data["事件类型"] == i]
        sm = len(da)
        city = da[da["驾驶域"] == "城市"]

        city_yes = len(city[city["realtime_if_link"] == "issueFinder"])
        speed = da[da["驾驶域"] == "高速"]
        speed_yes = len(speed[speed["realtime_if_link"] == "issueFinder"])
        km3 = round(sm / params["km2"] * 100, 3)

        dt.update({
            i: [sm, km3, len(speed), speed_yes, len(city), city_yes]
        })

    f.write("事件,触发器,总数,百公里触发次数,高速全部,高速有回传,城市全部,城市有回传\n")
    for i in params["exc"]:
        exq = i[0]
        if exq in dt.keys():
            f.write("%s,%s,%s\n" % (exq, i[1], str(dt[exq]).strip("[]")))
        else:
            f.write(f"{i},0,0,0,0,0,0\n")
    f.write(",自动驾驶里程,%d\n\n" % params["km2"])


def mb_km(km):
    """
    计算自动驾驶里程的总和。
    
    Args:
        km (pd.DataFrame): 包含自动驾驶里程信息的DataFrame，其中需要包含"version"和"自动驾驶里程"两列。
    
    Returns:
        Tuple[float, float]: 一个元组，包含两个浮点数，分别表示master版本和rb版本的自动驾驶里程总和。
    
    """
    master_km = km[km["version"].str.find("8.3.4") >= 0]["自动驾驶里程"]
    master_sum = master_km.str[:-2].astype(float).sum()
    rb_km = km[(km["version"].str.find("8.4.40") >= 0) | (km["version"].str.find("8.4.37") >= 0)]["自动驾驶里程"]
    rb_sum = rb_km.str[:-2].astype(float).sum()
    print("master:", int(master_sum))
    print("rb:", int(rb_sum))
    return master_sum, rb_sum


def version_num(f, params):
    """
    生成版本数量统计信息，并写入到指定文件中。
    
    Args:
        f: 文件对象，用于写入数据。
        data: pandas DataFrame 类型，包含版本和事件类型等信息的数据集。
    
    Returns:
        vr: 字典类型，包含版本列表和每个事件类型对应的版本数量信息。
    
    """
    # f = open("2.csv", "w")
    vr = {}
    data = params["data"]
    versi = set(data["版本"])
    version_list = sorted(versi, key=lambda x: int(x.replace(".", "")))
    vr["ver_list"] = version_list
    for i in set(data["事件类型"]):
        ex = data[data["事件类型"] == i]
        a = ex["版本"].to_list()
        for ver in version_list:
            num = ex[ex["版本"] == ver]
            if ver in a:
                try:
                    vr[i].append([ver, len(num)])
                except Exception as e:
                    vr[i] = []
                    vr[i].append([ver, len(num)])
            else:
                try:
                    vr[i].append([ver, 0])
                except Exception as e:
                    vr[i] = []
                    vr[i].append([ver, 0])
    a = 0
    for i, j in vr.items():
        if i == "ver_list":
            continue
        version = list(map(lambda x: x[0], j))
        num_ver = list(map(lambda x: x[1], j))
        if a == 0:
            f.write(f"版本\事件,{','.join(version)}\n")
            a += 1
        f.write(f"{i},{','.join(map(str, num_ver))}\n")
    f.close()
    df = pd.read_csv(f)
    df.T.to_csv(f, header=False)
    return vr


def version_master(f, params):
    """
    计算master & rb 版本各事件类型的触发频率和总数，并写入文件。
    
    Args:
        kk (list): 包含各驾驶域的里程数。
        f (TextIO): 文件对象，用于写入结果。
    
    Returns:
        None
    """
    kk = params["kk"]
    for m, t in enumerate([params["master"], params["rb"]]):
        dt = {}
        f.write("事件,触发器,总数,百公里触发次数,高速全部,高速有回传,城市全部,城市有回传\n")
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

        for i in params["exc"]:
            exq = i[0]
            exc = i[1]
            if exq in dt.keys():
                f.write("%s,%s,%s\n" % (exq, exc, str(dt[exq]).strip("[]")))
            else:
                f.write(f"{exq},{exc},0,0,0,0,0,0\n")
        f.write(",自动驾驶里程,%d\n\n" % kk[m])


def rende(data: dict, save_name):
    """
    根据传入的数据绘制版本触发次数的折线图，并将图表渲染为HTML文件。
    
    Args:
        data (dict): 包含版本号和对应触发次数的字典，其中"ver_list"键对应的值为版本号的列表，其余键对应的值为版本号对应触发次数的列表（每个列表中的元素为元组，第一个元素为版本号，第二个元素为触发次数）。
    
    Returns:
        None: 该函数无返回值，将绘制的图表渲染为HTML文件。
    
    """
    line = Line()
    # 添加X轴和Y轴的数据  
    line.add_xaxis(data["ver_list"])
    for i, j in data.items():
        if i == "ver_list":
            continue
        num = list(map(lambda x: x[1], j))
        line.add_yaxis(f"{i}", num, linestyle_opts=opts.LineStyleOpts(width=3),
                       label_opts=opts.LabelOpts(is_show=False))

    line.set_global_opts(title_opts=opts.TitleOpts(title="版本触发次数", pos_left="center"),
                         legend_opts=opts.LegendOpts(orient='vertical', pos_right='center', pos_top='75%'),
                         xaxis_opts=opts.AxisOpts(
                             splitline_opts=opts.SplitLineOpts(is_show=False),
                             axislabel_opts=opts.LabelOpts(interval=0, rotate=-90)
                         ))
    g = Grid()
    g.add(line, grid_opts=opts.GridOpts(pos_bottom="40%"))
    # 渲染图表为HTML文件  
    g.render(save_name)


def write_data(func):
    pass


def public_params(file):
    """
    获取公共参数，包括版本号、里程数和驾驶域。
    
    Returns:
        dict: 包含版本号、里程数和驾驶域的字典。
    """
    exc = [["CIPV_VEH_LOST", "车辆CIPV丢失触发器"],
           ["CIPV_POS_EXCEPTION_VEH", "车辆CIPV位置异常触发器"],
           ["CIPV_POS_SHIFT_DIFF_VEH", "车辆CIPV位置速度自洽性异常触发器"],
           ["CIPV_THETA_DIFF_VEH", "CIPV车辆朝向异常"],
           ["LARGE_VEHICLE_POS_EXCEPTION", "大车位置异常触发器"],
           ["LARGE_VEHICLE_POS_SHIFT_DIFF", "大车位置速度自洽性异常触发器"],
           ["LARGE_VEHICLE_THETA_DIFF", "大车朝向异常触发器"],
           ["NarrowCIPV", "narrow报出cipv"],
           ["RadarAssignFusionMining", "视觉ID跳变(短暂丢失)"],
           ["RadarTrackFusionMining", "视觉目标长时间丢失(CIPV"],
           ["UnderlyingVelocityFusionMining", "视觉速度灵敏性(CIPV)"],
           ["VRUVelocityFusionMining", "视觉速度朝向(行人)"],
           ["RadarPositionFusionMining", "视觉位置跳动(CIPV)"]]
    data = pd.read_excel(file, header=1)
    km = pd.read_excel(file, sheet_name="里程", header=1)
    km2 = int(km[km["car_id"] == " 合计"]["自动驾驶里程"].tolist()[0].replace(",", "")[:-4])
    master = data[data["版本"].str.find("8.3.4") >= 0]
    rb = data[(data["版本"].str.find("8.4.40") >= 0) | (data["版本"].str.find("8.4.37") >= 0)]
    kk = mb_km(km)
    return {"exc": exc, "data": data, "km": km, "km2": km2, "master": master, "rb": rb, "kk": kk}


def args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="input file")
    parser.add_argument("-o", "--output", help="save file")
    parser.add_argument("-v", "--vis", help="line map")
    return parser.parse_args()


if __name__ == "__main__":
    file = "/Users/v_huangmin05/Downloads/通用打点数据_1717490210000.xlsx"
    save_file = file.split("/")[-1]
    params = public_params(file)
    f = open(save_file.replace("xlsx", "csv"), "w")
    # summary_num(f, params)
    # version_master(f, params)
    vre = version_num(f, params)
    rende(vre, save_file.replace("xlsx", "html"))
