# # -*- coding: utf-8 -*-

# ##Interactive bokeh for cross location selection

# ## Updated with regression line on 29 Apr 18
# import numpy as np
# import pandas as pd
# from bokeh.io import curdoc,show
# from bokeh.layouts import row,column, widgetbox
# from bokeh.models import ColumnDataSource,LabelSet,Div,Paragraph,PointDrawTool,PolyDrawTool,PolyEditTool,PolySelectTool,CustomJS
# from bokeh.models.widgets import Slider, TextInput,Button,CheckboxGroup,CheckboxButtonGroup,RadioGroup,Select,DataTable, TableColumn
# from bokeh.plotting import figure
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import r2_score


# import scipy.spatial as spatial

# df = pd.read_csv('myapp/data/crosses_updated.csv')
# headers = ["cross_id", "x", "y","pass_end_x", "pass_end_y"]
# crosses = pd.DataFrame(df, columns=headers)


# dx=crosses.x
# dy=crosses.y

# rx=[]
# ry=[]

# source = ColumnDataSource({
#     'x': [80], 'y': [9], 'color': ['dodgerblue']
# })

# ix = source.data['x']
# iy = source.data['y']
# points = np.array(crosses[['x','y']])

# t1 = np.vstack((ix, iy)).T
# t2=np.vstack((crosses.x,crosses.y)).T

# point_tree = spatial.cKDTree(t2)

# ax=(point_tree.query_ball_point(t1, 3)).tolist()

# cx=crosses.pass_end_x[ax[0]]
# cy=crosses.pass_end_y[ax[0]]
# size=1

# source2 = ColumnDataSource({
#     'cx': [cx], 'cy': [cy]
# })

# source_reg = ColumnDataSource({
#     'rx': [], 'ry': []
# })

# source2 = ColumnDataSource(data=dict(cx=cx,cy=cy))
# source_reg = ColumnDataSource(data=dict(rx=rx,ry=ry))

# # Set up plot

# plot = figure(plot_height=500, plot_width=700,
#               tools="save",
#               x_range=[0,100], y_range=[0,100],toolbar_location="below")
# plot.image_url(url=["myapp/static/images/base.png"],x=0,y=0,w=100,h=100,anchor="bottom_left")


# plot.hex('cx','cy',source=source2,size=15,fill_color='#95D7FF',line_color='#584189',line_width=2,alpha=1)

# st=plot.scatter('x','y',source=source,size=15,fill_color='orangered',line_color='black',line_width=2)

# plot.xgrid.grid_line_color = None
# plot.ygrid.grid_line_color = None
# plot.axis.visible=False

# draw_tool = PointDrawTool(renderers=[st])
# draw_tool.add=False
# columns = [
#     #TableColumn(field="x", title="x"),
#    # TableColumn(field="y", title="y")
# ]

# data_table = DataTable(
#     source=source,
#     #columns=columns,
#     index_position=None,
#     width=800,
#     editable=False,
# )


# def linear_regression(cx,cy):
#     """Calculate the linear regression and r2 score"""
#     model = LinearRegression()
#     model.fit(cx[:,np.newaxis],cy)
#     #Get the x- and y-values for the best fit line
#     x_plot = np.linspace(50,100)
#     y_plot = model.predict(x_plot[:,np.newaxis])
#     #Calculate the r2 score
#     r2 = r2_score(cy,model.predict(cx[:,np.newaxis]))
#     #Position for the r2 text annotation
#     r2_x = [-cx + 0.1*cx]
#     r2_y = [cx - 0.1*cx]
#     text = ["R^2 = %02f" % r2]
#     return x_plot,y_plot, r2, r2_x, r2_y, text

# x_plot, y_plot, r2, r2_x, r2_y, text = linear_regression(cx,cy)
# text_source = ColumnDataSource(dict(x=[52], y=[3], text=text)) #R2 value
# line_source = ColumnDataSource(data=dict(x=x_plot, y=y_plot)) #Regression line

# reg_line=plot.line('x', 'y', source = line_source, color = 'black',line_width=0,line_alpha=0,line_cap="round")
# glyph = LabelSet(x="x", y="y", text="text", text_color="white",source=text_source)
# plot.add_layout(glyph)

# def on_change_data_source(attr, old, new):
#     ix = source.data['x']
#     iy = source.data['y']

#     t1 = np.vstack((ix, iy)).T
#     t2 = np.vstack((crosses.x, crosses.y)).T

#     point_tree = spatial.cKDTree(t2)

#     ax = (point_tree.query_ball_point(t1, 3)).tolist()
#     cx = crosses.pass_end_x[ax[0]]
#     cy = crosses.pass_end_y[ax[0]]
#     x_plot, y_plot, r2, r2_x, r2_y, text = linear_regression(cx,cy)


#     text_source.data = dict(x=[52], y=[3], text = text)

#     line_source.data = dict(x=x_plot, y=y_plot)
#     source2.data=dict(cx=cx,cy=cy)
#     # plot.scatter('cx','cy',source=source2)

# source.on_change('data', on_change_data_source)

# checkbox=CheckboxButtonGroup(labels=["Show Regression Plot"],button_type = "danger")

# checkbox.callback = CustomJS(args=dict(l0=reg_line,l1=glyph, checkbox=checkbox), code="""
# l0.visible = 0 in checkbox.active;
# l1.visible = 0 in checkbox.active;
# l0.glyph.line_width = 3;
# l0.glyph.line_alpha=1;
# l1.text_color="black";
# """)



# plot.add_tools(draw_tool)
# plot.toolbar.active_tap = draw_tool
# div = Div(text="""<b><h>WHERE DO TEAMS CROSS?</b></h></br></br>Interactive tool to get cross end locations based on user input. The tool uses <a href="https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.cKDTree.htmlL">cKDTree</a> 
# to calculate the nearest cross start locations and plots the corresponding end locations<br></br>
# <br>Created by <b><a href="https://twitter.com/Samirak93">Samira Kumar</a></b> using bokeh</br>""",
# width=550, height=110)

# div_help = Div(text="""<b><h>INSTRUCTIONS</b></h></br></br>Click on the below icon, in the bottom of the viz, to enable the option to drag the red circle.<br></br>
# <img src="https://bokeh.pydata.org/en/latest/_images/PointDraw.png" alt="Point Draw Tool">
# <br></br> 
# The crosses, which have started, from within 3 units of the red circle are collected and their corresponding end locations are plotted in blue 
# <br><b><a href="https://samirak93.github.io/analytics/projects/proj-1.html">Blog Post</a></br>""",
# width=400, height=100)




# layout=(column(checkbox,row(plot),data_table))
# curdoc().add_root(layout)
# curdoc().title = "Where do teams cross?"


from bokeh.plotting import figure, output_notebook, show, Column, Row
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource, Button
from bokeh.io import curdoc,show
import time
import uuid 
import pickledb

# db = pickledb.load('test.db', False)

# db.set('key', 'value')

# db.get('key')
# db.dump()
  
# id = uuid.uuid1() 
# p = figure(x_range=(0, 10), y_range=(0, 10), tools=[],
#        title='Point Draw Tool')
# p.background_fill_color = 'lightgrey'
# source = ColumnDataSource({
#     'x': [1, 5, 9], 'y': [1, 5, 9], 'color': ['red', 'green', 'yellow']
# })
# renderer = p.scatter(x='x', y='y', source=source, color='color', size=10)
# columns = [TableColumn(field="x", title="x"),
#            TableColumn(field="y", title="y"),
#            TableColumn(field='color', title='color')]
# table = DataTable(source=source, columns=columns, editable=True, height=200)

# draw_tool = PointDrawTool(renderers=[renderer], empty_value='black')
# p.add_tools(draw_tool)
# p.toolbar.active_tap = draw_tool

# def callback():
#     print "callback1"
#     print db.get('key')
#     print db.dump()
#     print id
#     print source.data
#     #time.sleep(10)
#     pass

# button = Button(label="Press Me")
# button.on_click(callback)


# def callback2():
#     print "callback2"
#     db.set('key', 'value')
#     print id
#     print source.data
#     #time.sleep(10)
#     pass

# button1 = Button(label="Press Me")
# button1.on_click(callback2)

# layout = (Column(p, Row(button, button1)))

# curdoc().add_root(layout)
# curdoc().title = "Guess the Peak!!!"
# print curdoc().session_context.request.arguments


# from bokeh.plotting import figure, output_notebook, show, Column, Row
# from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource, Button

# import time
# import uuid 
import numpy as np
#
#import pickledb

db = pickledb.load('myapp/data/test.db', False)

test = ["1","4","8"]

db.set('key', test)

print db.get('hjfhskjd')

  
i = {}
i["a"]=1
count = 4
curves = ["1.txt","2.txt","3.txt","4.txt","5.txt"]
id = uuid.uuid1() 

tools = ["xpan,pan,xwheel_zoom,wheel_zoom,box_zoom,reset,previewsave"]
p = figure(x_range=(0, 10), y_range=(0, 10), tools=tools,
       title='Point Draw Tool')

p.y_range.start = -10
p.y_range.end = 180
p.x_range.start = -10
p.x_range.end = 180

sourcefk = ColumnDataSource(data=dict(x=[1,2,3], y=[1,2,3]))

data_raw = np.loadtxt('myapp/data/'+curves[i["a"]])

xdata = np.empty(0)
ydata = np.empty(0)
ydata1 = np.empty(0)

xdata = np.append(xdata,data_raw[:,0]*1e9)
ydata = np.append(ydata,data_raw[:,2]*1e12)
ydata1 = np.append(ydata1,data_raw[:,1]*1e12)

data=dict(x=xdata, y=ydata)
sourcefk.data=data

p.line('x', 'y', source=sourcefk)


source = ColumnDataSource({
    'x': [0, 25, 50, 75, 100, 125], 'y': [0, 0, 0, 0, 0, 0], 'color': ['green', 'green', 'green', 'green', 'green', 'green']
})

renderer = p.scatter(x='x', y='y', source=source, color='color', size=20)
columns = [TableColumn(field="x", title="x"),
           TableColumn(field="y", title="y"),
           TableColumn(field='color', title='color')]
table = DataTable(source=source, columns=columns, editable=True, height=200)

draw_tool = PointDrawTool(renderers=[renderer], empty_value='black')
p.add_tools(draw_tool)
p.toolbar.active_tap = draw_tool

print "ssss",source.data['x']
print "ssss",source.data['y']

dat=dict(x=[0, 0, 0, 0, 0, 0], y=[0, 0, 0, 0, 0, 0], color= ['green', 'green', 'green', 'green', 'green', 'green'])
print dat
source.data = dat

def next():
    old = i["a"]
    print "old",old

    i["a"] = i["a"] + 1

    if i["a"]>count:
        i["a"]=0
    
    print "new",i["a"]

    #print str(id)+str(i["a"])
    #print source.data
    #if db.get(str(id)):
    #    print "db",db.get(str(id)+str(i["a"])).data
    #else:
    #    print "db",db.get(str(id)+str(i["a"]))
    
    print str(id)+str(old)
    db.set(str(id)+str(old)+"x", source.data['x'])
    db.set(str(id)+str(old)+"y", source.data['y'])
    db.dump()
    
    if db.get(str(id)+str(i["a"])+"x"):
        print "db there"
        print str(id)+str(i["a"])
        dat=dict(x=db.get(str(id)+str(i["a"])+"x"), y=db.get(str(id)+str(i["a"])+"y"), color= ['green', 'green', 'green', 'green', 'green', 'green'])
        print dat
        source.data = dat
    else:
        print "no"
        so = ColumnDataSource({
            'x': [0, 25, 50, 75, 100, 125], 'y': [0, 0, 0, 0, 0, 0], 'color': ['green', 'green', 'green', 'green', 'green', 'green']
        })
        source.data = so.data
        

    data_raw = np.loadtxt('myapp/data/'+curves[i["a"]])

    xdata = np.empty(0)
    ydata = np.empty(0)
    ydata1 = np.empty(0)

    xdata = np.append(xdata,data_raw[:,0]*1e9)
    ydata = np.append(ydata,data_raw[:,2]*1e12)
    ydata1 = np.append(ydata1,data_raw[:,1]*1e12)

    data=dict(x=xdata, y=ydata)
    sourcefk.data=data
    

button = Button(label="Next")
button.on_click(next)


def previous():
    old = i["a"]
    print "old",old
    
    i["a"] = i["a"] - 1

    if i["a"]<0:
        i["a"] = count

    print "new",i["a"]

    print str(id)+str(old)
    db.set(str(id)+str(old)+"x", source.data['x'])
    db.set(str(id)+str(old)+"y", source.data['y'])
    db.dump()
        
    if db.get(str(id)+str(i["a"])+"x"):
        print "db there"
        print str(id)+str(i["a"])
        dat=dict(x=db.get(str(id)+str(i["a"])+"x"), y=db.get(str(id)+str(i["a"])+"y"), color= ['green', 'green', 'green', 'green', 'green', 'green'])
        print dat
        source.data = dat
    else:
        print "no"
        so = ColumnDataSource({
            'x': [0, 25, 50, 75, 100, 125], 'y': [0, 0, 0, 0, 0, 0], 'color': ['green', 'green', 'green', 'green', 'green', 'green']
        })
        source.data = so.data
        


    data_raw = np.loadtxt('myapp/data/'+curves[i["a"]])

    xdata = np.empty(0)
    ydata = np.empty(0)
    ydata1 = np.empty(0)

    xdata = np.append(xdata,data_raw[:,0]*1e9)
    ydata = np.append(ydata,data_raw[:,2]*1e12)
    ydata1 = np.append(ydata1,data_raw[:,1]*1e12)

    data=dict(x=xdata, y=ydata)
    sourcefk.data=data

button1 = Button(label="Previous")
button1.on_click(previous)


def entries():
    print db.get(str(id)+"1"+"x")
    print db.get(str(id)+"2"+"x")
    print db.get(str(id)+"3"+"x")
    print db.get(str(id)+"4"+"x")
    print db.get(str(id)+"5"+"x")

    print db.get(str(id)+"1"+"y")
    print db.get(str(id)+"2"+"y")
    print db.get(str(id)+"3"+"y")
    print db.get(str(id)+"4"+"y")
    print db.get(str(id)+"5"+"y")
    
    print db.getall()
    print db.deldb()
    
button2 = Button(label="Previous")
button2.on_click(entries)



layout = (Column(p, Row(button, button1),button2))
curdoc().add_root(layout)
curdoc().title = "Guess the Peak!!!"
print curdoc().session_context.request.arguments