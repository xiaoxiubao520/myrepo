# with open("1.txt") as f:
#     for i in f.read().splitlines():
#         par = i.strip().split("&")[2]
#         task = par[7:]
#         print(task)
#
#
from pyecharts.charts import Bar
from pyecharts import options as opts

# 创建一个柱状图对象
from pyecharts.charts import Bar
from pyecharts import options as opts
import pandas as pd

# 假设你已经有了 df 这个 DataFrame
a = Bar()
a.add_xaxis(["1", "2", "3", "4", "5"])
a.add_yaxis("商家A", [10, 20, 30, 40, 50])
a.render()