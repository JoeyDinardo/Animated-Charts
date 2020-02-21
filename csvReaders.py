import csv
import numpy
import matplotlib.dates as mdates
from datetime import datetime
import datetime as datetimeTwo
import calendar
players = []
class Player:
    data = []
    date = []
    points = []
    def __init__ (self, n1, d1,d2, points):
        self.name = n1
        self.data = d1
        self.date = d2
        self.points = points 
    def addData (self,d1,d2):
        self.data.append (int (d1))
        print (d2)
        self.date.append (d2)
    def getName (self):
        return self.name
    def setImage (self,ax,color):
        self.im, = ax.plot ([],[],color=(color))
    def setAnnotate (self, ax,xy, xytext):
        self.annotation = ax.annotate (self.name,xy=(xy),xytext = (xytext),color =(self.im.get_color ()),fontsize=20)
    def setDateFormat (self, form):
        self.im.axes.xaxis.set_major_formatter(mdates.DateFormatter(form))
    def setBar (bar):
        self.bar = (bar)
    def getim (self):
        return self.im
    def getAnnotate (self):
        return self.annotation

class PlayerOne:
    def __init__ (self,num, player):
        self.place = num
        self.player = player
#Puts data in final array
def createArray (dates):
    finalArray = []
    for i in range (0, len ( dates )):
        finalArray.append ([])
    for t in range (0,len (players)):

        if (len (players[t].date) != len ( dates ) ):
            num = np.searchsorted (dates, players [t].date[0])
            for i in range (0 , len (players [t].data)):
                if (i >= len ( dates )):
                    break
                finalArray [num].append (PlayerOne (i, players[t] ))
                num+=1
        else:
            for j in range (0,len (players [t].data)):
                finalArray [j].append (PlayerOne ( j,players[t] ))

    for i in range (0,len (finalArray)):
        finalArray [i] = sorted(finalArray [i], key=lambda player: player.player.data[player.place], reverse = True)   
    return finalArray

def openCSVFile (csvFilesName,dateType):
    #opens csv file 
    with open (csvFilesName, newline = '') as csvfile:
        rows = csv.reader (csvfile)
        name = False
        for row in rows:
            for player in players:
                if (player.getName () == row [0]):
                    name = True
            if (name == False and row [0]!= "name"):
                players.append (Player (row[0], [], [],[]))
            if (row [0]!= "name"):
                #adds player values
                addValues (row,"%Y",dateType)
            name = False
    return players
#adds player values to array
def addValues (r1, form, dateType):
    for player in players:
        if (player.name == r1 [0]):
            r1[2] = r1[2].replace(".00", "")
            r1[2] = r1[2].replace(" ", "")
            player.data.append (int (float (r1 [1])+1))
            if dateType == True:
                player.date.append (datetime.strptime (r1[2],form))
            else:
                player.date.append (int (r1[2]))

            return
#adds months to data
def addMonths ():
    for player in players:
        dataTemp = []
        for i in range(0, len (player.data)):
            for j in range (1,13):
                if j == 1:
                    player.date [i] = datetimeTwo.date (player.date [i].year,j,1)
                    dataTemp.append (player.data [i])
                else:
                    if (len (player.data) > i+1):
                        dataTemp.append (player.data [i] + (player.data [i+1] - player.data [i])/12 * (j-1))
                    else:
                        dataTemp.append (player.data [i])
                    player.date.append (datetimeTwo.date (player.date [i].year,j,1))
        player.data = list(dataTemp)          
        player.date.sort ()
    return players
#adds days to data
def addDays ():
    for player in players:
        dataTemp = []
        for i in range(0, len (player.data)):
            for j in range (1, int (calendar.monthrange (player.date [i].year, player.date [i].month)[1])     + 1):
                if j == 1:
                    player.date [i] = datetimeTwo.date (player.date [i].year,player.date [i].month,j)
                    dataTemp.append (player.data [i])
                else:
                    if (len (player.data) > i+1):
                        dataTemp.append (player.data [i] + (player.data [i+1] - player.data [i])/int (calendar.monthrange (player.date [i].year, player.date [i].month)[1]) * j)
                    else:
                        dataTemp.append (player.data [i])
                    player.date.append (datetimeTwo.date (player.date [i].year,player.date [i].month,j))
        player.data = list(dataTemp)          
        player.date.sort ()
    return players
        
    
        
        
            
