import matplotlib
matplotlib.use("TkAgg") 
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import csvReaders
import random
import copy
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.image as mpimg
import ffmpeg

csvFilesName = ""
global players
players = csvReaders.openCSVFile (csvFilesName, False)
global xMove
xMove = 1
global dates
dates = []
global frameGLB
frameGLB = 0
global finalArray
finalArray = []
fig = plt.figure()
ax2 = fig.add_subplot()
global dateInit
global dateInitLow
global finalY
finalY = 0


#add months to data
def addMonths ():
    global players
    players = csvReaders.addMonths ()
#add days to data
def addDays ():
    global players
    players = csvReaders.addDays ()
#gets rids of decimals in date
def cleanDates ():
    global dates
    i = 0
    for  i in range (len (dates)):
        dates[i] = dates[i].replace(".00", "")
        dates[i] = dates[i].replace(" ", "")
        i+=1
#returns full date
def findDates ():
    global dates
    dates = players[-1].date [:]
    
def searchDate (frame, player):
    i = 0
    for date in player.date:
        if date == dates [frame]:
            return i
        i+=1
    return -1
#sets color of line   
def setImage ():
    for player in players:
        player.setImage (ax2, [random.random (),random.random (),random.random ()] )
#formats date used
def setDateFormat (form):
    for player in players:
        player.setDateFormat (form)
#sets x and y values for points in line
def setPoints (frame,amount):
    if amount != -1:
        for i in range (0, len (finalArray [frame])):
            if (i > amount):
                break
            finalArray [frame] [i].player.getim ().set_data (finalArray [frame] [i].player.date [:finalArray [frame] [i].place+1],np.int_ (finalArray [frame] [i].player.data [:finalArray [frame] [i].place+1]))
            finalArray [frame] [i].player.getim ().set_xdata (finalArray [frame] [i].player.date [:finalArray [frame] [i].place+1])
#finds highest value of the data           
def findHighestValues (frame):
    high = 0
    for player in players:
        if len (dates) == len (player.date): 
            if (player.data [frame]) > int  (high):
                high = int (player.data [frame])
        else:
            num = searchDate (frame, player)
            if (num != -1):
                if (player.data [num]) > int  (high):
                    high = int (player.data [num])
    return high
#finds the lowest value of the data
def findLowestValue (frame, amount):
    if len (dates) == len (players [amount].date):
        return players [amount].data [frame]
    else:
        return players [amount].data [searchDate (frame, players [amount])]
    
    
#sets text position
def setAnnotatText (amount, frame):
    for i in range (0, len (finalArray [frame])):
        if (i > amount):
            break
        finalArray [frame][i].player.getAnnotate ().set_position ((finalArray [frame][i].player.getim ().get_xdata()[-1],finalArray [frame][i].player.getim ().get_ydata()[-1]))
        finalArray [frame][i].player.getAnnotate ().xy = (finalArray [frame][i].player.getim ().get_xdata()[-1],finalArray [frame][i].player.getim ().get_ydata()[-1])
#initializes text
def annotatText ():
    for player in players:
        player.setAnnotate (ax2,[0,0],[0,0])

#sets the title of figure
def setTitle (title, size):
    fig.suptitle(title, fontsize=size)

#sets initial date high and low
def dateInit (sizeLow ,size):
    global dateInitLow
    global dateInit
    dateInitLow = sizeLow
    dateInit = size

#formats axis to year
def yearFormat ():
    years = mdates.YearLocator()   # every year
    years_fmt = mdates.DateFormatter('%Y')
    ax2.xaxis.set_major_locator(years)
    ax2.xaxis.set_major_formatter(years_fmt)
#formates axis to month
def monthFormat ():
    months = mdates.MonthLocator()  # every month
    ax2.xaxis.set_minor_locator(months)
#sets axis labels and color and font size
def setAxis (xLabel, yLabel,fontSize, color, labelSize):
    ax2.set_xlabel (xLabel, fontsize=fontSize)
    ax2.set_ylabel (yLabel,  fontsize=fontSize)
    ax2.spines['bottom'].set_color(color)
    ax2.spines['top'].set_color(color) 
    ax2.spines['right'].set_color(color)
    ax2.spines['left'].set_color(color)
    ax2.tick_params(axis = 'both', which = 'major', labelsize = labelSize)
#sets array data
def setFinalArray ():
    global finalArray
    findDates ()
    finalArray = csvReaders.createArray (dates)

def lineInit (yLimLow, yLimHigh):
    global dates
    global finalArray
    #sets intial xaxis limits
    ax2.set_xlim(dateInitLow, dateInit)    
    setImage ()
    annotatText ()
    #sets intial yaxis liimites
    ax2.set_ylim(yLimLow, yLimHigh)
    fig.set_size_inches(19.2, 10.8, True)

#sets data for figure each frame 
def func(frame):
    num = 0
    global xMove
    global frameGLB
    frameGLB = frame
    global finalY
    if (frame < len (dates)):    
        if (finalArray [frame][0].player.data [finalArray [frame][0].place]*1.1 > ax2.get_ylim () [1]):
            ax2.set_ylim (top=finalArray [frame][0].player.data[finalArray [frame][0].place]*1.1)
            if (finalArray [frame][-1].player.data[finalArray [frame][-1].place]*.9>ax2.get_ylim ()[0]):
                ax2.set_ylim (bottom=ax2.get_ylim ()[0]+((ax2.get_ylim ()[1] - finalArray [frame][0].player.data[finalArray [frame][0].place])/80) )
        if (frame > ax2.get_xlim () [1]-1):
            lim = ax2.set_xlim (frame - dateInit ,frame+1)
        setPoints (frame, 2)
        setAnnotatText (2, frame)
        finalY = ax2.get_ylim () [0]
    elif (frame < len (dates)*2-dateInit):
        ax2.set_ylim (finalY * ((len (dates)-dateInit-xMove)/(len (dates)-dateInit)) ,finalArray [-1][0].player.data[finalArray [-1][0].place]*1.1)
        ax2.set_xlim (dates [(len (dates)-dateInit )-xMove],dates [-1])
        xMove += 1

#displays plot animation
def displayAnimation ():
    ani = animation.FuncAnimation(fig, func, frames=len (players [0].date)*3, interval=1, blit=False)
    figManager = plt.get_current_fig_manager()
    figManager.full_screen_toggle()
    win = plt.gcf().canvas.manager.window
    plt.show()
#saves pot animation to file
def saveAnimation (name):
    ani = animation.FuncAnimation(fig, func, frames=len (players [0].date)*3, interval=1, blit=False)
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=4000)
    ani.save(name,writer=animation.FFMpegWriter(fps=30),dpi=100)

