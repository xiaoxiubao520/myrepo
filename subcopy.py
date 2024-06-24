from pyecharts.charts import Line, Grid, Bar
from pyecharts import options as opts
import pandas as pd
from pyecharts.globals import ThemeType


def zxt(file_name):
    df = pd.read_excel(file_name, index_col=0)
    line = Line()
    line.add_xaxis(df.columns.tolist())
    a = df.index
    colors = ["#1f77b4",
              "#ff7f0e",
              "#FFA500",
              "#d62728",
              "#9467bd",
              "#8c564b",
              "#e377c2",
              "#7f7f7f",
              "#bcbd22",
              "#17becf",
              "#b2df8a",  # 浅绿色
              "#a65628",  # 深橙色
              '#800000']  # 粉红色]
    for j, i in enumerate(df.values.tolist()):
        line.add_yaxis(f"{a[j]}", i, linestyle_opts=opts.LineStyleOpts(width=4),
                       label_opts=opts.LabelOpts(is_show=False), itemstyle_opts=opts.ItemStyleOpts(color=colors[j]))

    line.set_global_opts(title_opts=opts.TitleOpts(title="RB2.0版本百公里触发次数", pos_left="center"),
                         legend_opts=opts.LegendOpts(orient='vertical', pos_right='center', pos_top='75%'),
                         xaxis_opts=opts.AxisOpts(
                             splitline_opts=opts.SplitLineOpts(is_show=False),
                             axislabel_opts=opts.LabelOpts(interval=0)
                         ))
    g = Grid()
    g.add(line, grid_opts=opts.GridOpts(pos_bottom="40%"))
    g.render()


def zzt(file_name):
    bar = Bar()
    df = pd.read_excel("/Users/v_huangmin05/Desktop/工作簿4.xlsx", index_col=0)
    bar.add_xaxis(df.columns.tolist())
    a = df.index
    for j, i in enumerate(df.values.tolist()):
        bar.add_yaxis(f"{a[j]}", i)
    bar.set_global_opts(title_opts=opts.TitleOpts(title="RB版本里程统计"), xaxis_opts=opts.AxisOpts(
        splitline_opts=opts.SplitLineOpts(is_show=False),
        axislabel_opts=opts.LabelOpts(interval=0)
    ))
    bar.render()


zxt("/Users/v_huangmin05/Downloads/工作簿1.xlsx")
