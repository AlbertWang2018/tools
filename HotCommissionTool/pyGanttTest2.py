import pandas as pd
import plotly.figure_factory as ff
import random
r = lambda: random.randint(0, 255)
colors = ['#%02x%02x%02x' % (r(), r(), r())]
for i in range(1, 150):
    colors.append('#%02x%02x%02x' % (r(),r(),r()))
df=pd.read_csv(r"D:\Download\00-CATL\KBESS\FireSystem\FIP log 20250304-1.csv")
fig = ff.create_gantt(df, colors=colors, show_colorbar=True, index_col='Task',group_tasks=True)
fig.show()