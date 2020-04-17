# # -*- coding: utf-8 -*-

from bokeh.plotting import figure, output_notebook, show, Column, Row
from bokeh.models import DataTable, TableColumn, PointDrawTool, ColumnDataSource, Button
from bokeh.models.widgets import Tabs, Panel
from bokeh.io import curdoc,show
import time
import uuid 
import pickledb
import numpy as np
import matplotlib.cm as cm

db = pickledb.load('./myapp/data/test.db', False)

    
i = {}
i["a"]=1
count = 4
curves = ["./myapp/data/1.txt","./myapp/data/2.txt","./myapp/data/3.txt","./myapp/data/4.txt","./myapp/data/5.txt","./myapp/data/6.txt","./myapp/data/7.txt","./myapp/data/8.txt","./myapp/data/9.txt"]
id = uuid.uuid1() 

#tools = ["xpan,pan,xwheel_zoom,wheel_zoom,box_zoom,reset,previewsave"]
p = figure(x_range=(0, 40), y_range=(0, 10), tools=[],
       title='Guess peaks!!! :-)')
source = ColumnDataSource({
    'x': [], 'y': [], 'color': []
})
renderer = p.scatter(x='x', y='y', source=source, color='color', size=20)
columns = [TableColumn(field="x", title="x"),
           TableColumn(field="y", title="y"),
           TableColumn(field='color', title='color')]
table = DataTable(source=source, columns=columns, editable=True, height=200)

draw_tool = PointDrawTool(renderers=[renderer], empty_value='black')
p.add_tools(draw_tool)
#p.toolbar.active_tap = draw_tool

p.y_range.start = -10
p.y_range.end = 220
p.x_range.start = -10
p.x_range.end = 180


sourcefk = ColumnDataSource(data=dict(x=[1,2,3], y=[1,2,3]))

data_raw = np.loadtxt(curves[i["a"]])

xdata = np.empty(0)
ydata = np.empty(0)
ydata1 = np.empty(0)

xdata = np.append(xdata,data_raw[:,0]*1e9)
ydata = np.append(ydata,data_raw[:,2]*1e12)
ydata1 = np.append(ydata1,data_raw[:,1]*1e12)

data=dict(x=xdata, y=ydata)
sourcefk.data=data

p.line('x', 'y', source=sourcefk)


p.xaxis.axis_label = "Extension [nm]"
p.xaxis.axis_label_text_font_size = "20pt"
p.xaxis.axis_label_text_font_style = 'bold'
p.yaxis.axis_label = "Force [pN]"
p.yaxis.axis_label_text_font_size = "20pt"
p.yaxis.axis_label_text_font_style = 'bold'





print "ssss",source.data['x']
print "ssss",source.data['y']

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
    print source.data['x']
    db.set(str(id)+str(old)+"y", source.data['y'])
    print source.data['y']
    db.dump()
    
    if db.get(str(id)+str(i["a"])+"x"):
        print "db there"
        print str(id)+str(i["a"])
        dat=dict(x=db.get(str(id)+str(i["a"])+"x"), y=db.get(str(id)+str(i["a"])+"y"), color= ['green']*len(db.get(str(id)+str(i["a"])+"x")))
        print dat
        source.data = dat
    else:
        print "no"
        so = ColumnDataSource({
            'x': [], 'y': [], 'color': []
        })
        source.data = so.data
        

    data_raw = np.loadtxt(curves[i["a"]])

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
    print source.data['x']
    db.set(str(id)+str(old)+"y", source.data['y'])
    print source.data['y']
    db.dump()
        
    if db.get(str(id)+str(i["a"])+"x"):
        print "db there"
        print str(id)+str(i["a"])
        dat=dict(x=db.get(str(id)+str(i["a"])+"x"), y=db.get(str(id)+str(i["a"])+"y"), color= ['green']*len(db.get(str(id)+str(i["a"])+"x")))
        print dat
        source.data = dat
    else:
        print "no"
        so = ColumnDataSource({
           'x': [], 'y': [], 'color': []
        })
        source.data = so.data
        


    data_raw = np.loadtxt(curves[i["a"]])

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


    #p.image(image=[H],x=-15, y=-15, dw=165, dh=165, palette=bokeh_palette)
    #from scipy.stats.kde import gaussian_kde

    #k = gaussian_kde(np.vstack([b, a]))
    #xi, yi = np.mgrid[-15:200:x.size**0.4*1j,-15:200:y.size**0.4*1j]
    #zi = k(np.vstack([xi.flatten(), yi.flatten()]))
    
    #dat=dict(image=[zi.reshape(xi.shape)])
    #print H
    #sourceimg.data=dat

    # print db.get(str(id)+"1"+"x")
    # print db.get(str(id)+"2"+"x")
    # print db.get(str(id)+"3"+"x")
    # print db.get(str(id)+"4"+"x")
    # print db.get(str(id)+"5"+"x")

    # print db.get(str(id)+"1"+"y")
    # print db.get(str(id)+"2"+"y")
    # print db.get(str(id)+"3"+"y")
    # print db.get(str(id)+"4"+"y")
    # print db.get(str(id)+"5"+"y")

    # print db.getall()
    #db.deldb()
    #db.dump()
    

#db.deldb()
#db.dump()
layout = (Column(p, Row(button1, button)))


tools = ["xpan,pan,xwheel_zoom,wheel_zoom,box_zoom,reset,previewsave"]
q = figure(x_range=(0, 10), y_range=(0, 10), tools=tools,
       title='Analysis Peak')

q.y_range.start = -10
q.y_range.end = 220
q.x_range.start = -10
q.x_range.end = 180

q.xaxis.axis_label = "Extension [nm]"
q.xaxis.axis_label_text_font_size = "20pt"
q.xaxis.axis_label_text_font_style = 'bold'
q.yaxis.axis_label = "Force [pN]"
q.yaxis.axis_label_text_font_size = "20pt"
q.yaxis.axis_label_text_font_style = 'bold'

colormap =cm.get_cmap("jet")

different_colors=15
color_mapping=colormap(np.linspace(0,1,different_colors),1,True)
bokeh_palette=["#%02x%02x%02x" % (r, g, b) for r, g, b in color_mapping[:,0:3]]
sourceimg = ColumnDataSource(data=dict(image=[]))
q.image(image='image',source=sourceimg,x=-15, y=-15, dw=265, dh=265, palette=bokeh_palette)#dw=215, dh=215dw=165, dh=165

sourceanalysis = ColumnDataSource(data=dict(x=[1,2,3], y=[1,2,3]))

q.line('x', 'y',line_width=6, color="white", source=sourceanalysis)
def entries():
    xdatatot = np.empty(0)
    ydatatot = np.empty(0)
    for i in db.getall():
        if i[-1]=="x":
            #print db.get(i)
            xdatatot=np.append(xdatatot,np.array(db.get(i)))
        if i[-1]=="y":
            #print db.get(i)
            ydatatot=np.append(ydatatot,np.array(db.get(i)))
    print "bla"

    
    pw=310

    ph=370
    print ydatatot
    print len(ydatatot)
    print xdatatot
    print len(xdatatot)

    a=np.zeros(len(xdatatot))
    b=np.zeros(len(xdatatot))
    
    for idx,e in enumerate(xdatatot):
        a[idx]=e
    for idx,e in enumerate(ydatatot):
        b[idx]=e
    
    bslice = np.where( b > 1 )
    print "bsl",bslice
    b = b[bslice]
    print "bsl",bslice
    a = a[bslice]
    

    #H, xe, ye = np.histogram2d(x, y, bins=100)
    H, xe, ye = np.histogram2d(b,a,range=[[-15, 250], [-15, 250]],bins=40)
    Hmasked = np.ma.masked_where(H==0,H)
    dat=dict(image=[Hmasked])
    print H
    sourceimg.data=dat
    
    xdata=np.loadtxt("./myapp/data/parts.txt")
    ydata=np.loadtxt("./myapp/data/maxposs.txt")
    
    data=dict(x=xdata, y=ydata)
    sourceanalysis.data= data

button2 = Button(label="Analyse")
button2.on_click(entries)

def deletedb():
    db.deldb()
    db.dump()

button3 = Button(label="delete db")
button3.on_click(deletedb)

layout2 = (Column(q,button2,button3))




tab1 = Panel(child=layout, title="Guess")
tab2 = Panel(child=layout2, title="Analysis")

tabs = Tabs(tabs=[ tab1,tab2])#sizing_mode="stretch_both"

arguments = curdoc().session_context.request.arguments
keyvalid = False

for key in arguments.keys():
    print key
    variable = key
    keyvalid = True

if keyvalid:
    print variable
    if variable=="foo":
        print "analysis"

        curdoc().add_root(tabs)
        curdoc().title = "Guess the Peak!!!"

else:
    print "guessing"

    curdoc().add_root(layout)
    curdoc().title = "Guess the Peak!!!"
