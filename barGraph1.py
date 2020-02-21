import matplotlib.pyplot as pltOne
import csvReaders
import matplotlib.ticker as ticker
import matplotlib.animation as animation
import ffmpeg
global figOne
global ax
global animator
finalArray = []
dates = []

figOne, ax = pltOne.subplots()
figOne.set_size_inches(19.2, 10.8, True)
pltOne.rcParams.update({'font.size': 22})
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
csvFilesName = ""
global players
players = csvReaders.openCSVFile (csvFilesName, False)
#Sets array data
def setFinalArray ():
    global finalArray
    global dates
    dates = players[-1].date [:]
    finalArray = csvReaders.createArray (dates)
#sets data in bar chart
def draw_barchart(frame):
    if (frame < len (dates)-1):
        ax.clear ()
        for i in range (1,-1,-1):
            ax.barh(y=finalArray [frame] [i].player.name,width=finalArray [frame] [i].player.data [finalArray [frame] [i].place+1],height=.8,color=finalArray [frame] [i].player.getim().get_color())
            ax.text(fontsize = 30,y=finalArray [frame] [i].player.name,x=finalArray [frame] [i].player.data [finalArray [frame] [i].place+1],s=finalArray [frame] [i].player.data [finalArray [frame] [i].place+1])
        pltOne.box(False)
    
#Saves chart animation to file  
def saveAnimation(name):
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=30, metadata=dict(artist='Me'), bitrate=4000)
    animator = animation.FuncAnimation(figOne, draw_barchart, frames=len (dates)*3, interval=1, blit=False)
    animator.save(name,writer=animation.FFMpegWriter(fps=30),dpi=100)
#Display bar chart animation
def showPlot ():
    animator = animation.FuncAnimation(figOne, draw_barchart, frames=len (dates)*3, interval=1, blit=False)
    pltOne.show ()
