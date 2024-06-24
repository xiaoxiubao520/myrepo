from pyecharts.charts import Line,Grid
from pyecharts import options as opts
import pandas as pd
from pyecharts.globals import ThemeType

# 创建一个折线图对象
df = pd.read_excel("/Users/v_huangmin05/Downloads/工作簿2.xlsx",index_col=0)
line = Line()
line.add_xaxis(df.columns.tolist())
a = df.index
for j,i in enumerate(df.values.tolist()):
    print(i)
    line.add_yaxis(a[j],i, linestyle_opts=opts.LineStyleOpts(width=3),
                       label_opts=opts.LabelOpts(is_show=False))

line.set_global_opts(title_opts=opts.TitleOpts(title="RB2.0版本百公里触发次数", pos_left="center"),
                         legend_opts=opts.LegendOpts(orient='vertical', pos_right='center', pos_top='75%'),
                         xaxis_opts=opts.AxisOpts(
                             splitline_opts=opts.SplitLineOpts(is_show=False),
                             axislabel_opts=opts.LabelOpts(interval=0, rotate=-90)
                         ))
g = Grid()
g.add(line, grid_opts=opts.GridOpts(pos_bottom="40%"))
    # 渲染图表为HTML文件
g.render()