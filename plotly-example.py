
import math
import plotly
import plotly.graph_objs as go

x = [i/10 for i in range(100)]
y = [math.sin(i) for i in x]

#check data
print(f'x={x}')
print(f'y={y}')

# build the figure and plot it!
# fig = go.Scatter(x=x, y=y)
# fig = go.Bar(x=x, y=y)
# plotly.offline.plot({'data': [fig]})

# pie chart example
x = ['apple pie', 'pumpkin pie', 'chhocolate pecan pie', 'chocalte bourbon pecan pie']
y = [10, 20, 15, 5]
fig = go.Pie(labels=x, values=y)
# plotly.offline.plot({'data': [fig]})
graph_div = plotly.offline.plot({'data': [fig]}, auto_open=False, output_type='div')