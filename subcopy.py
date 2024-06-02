from pyecharts.charts import Line,Grid
from pyecharts import options as opts
from pyecharts.globals import ThemeType

# 创建一个折线图对象
def rende(data:dict):  
    line = Line(init_opts=opts.InitOpts(theme=ThemeType.DARK))
    # 添加X轴和Y轴的数据  
    for i,j in data.items():
        version = list(map(lambda x:x[0],j))
        line.add_xaxis(version)
        continue
    for i,j in data.items():
        num = list(map(lambda x:x[1],j))
        line.add_yaxis(f"{i}",num,linestyle_opts=opts.LineStyleOpts(width=4),label_opts=opts.LabelOpts(is_show=False))

    line.set_global_opts(title_opts=opts.TitleOpts(title="版本触发次数",pos_left="center"),legend_opts=opts.LegendOpts(orient='vertical', pos_right='center',pos_top='75%'),
                        xaxis_opts=opts.AxisOpts(
                            splitline_opts=opts.SplitLineOpts(is_show=False)
                        ))
    g = Grid()
    g.add(line,grid_opts=opts.GridOpts(pos_bottom="30%"))
    # 渲染图表为HTML文件  
    g.render()
