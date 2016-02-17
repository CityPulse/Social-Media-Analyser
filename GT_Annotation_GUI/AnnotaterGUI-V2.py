'''
Created on 9 Jul 2015

@author: nf0010
'''
from tkinter import *
import numpy as np
import os.path
import pandas as pd

class Application(Frame):
    """ A GUI Application for Tweet Annotation """
    
    def __init__(self, master):
        """ Initialize the Frame """
        Frame.__init__(self, master)
        self.grid()
        self.Nextbutton_clicks=setIndicator()
        self.data= Data_Loader()
        self.create_widgets()
        
    def create_widgets(self):
        """ Create the label """
        self.instruction = Label(self, text="General instructions:\n 1. Click 'Next' to see the first (next) Tweet,\n 2. Assign appropriate tag(s),\n 3. Save your annotation,\n 4. Quit. ",justify=LEFT)
        self.instruction.grid(row=0, column=0, columnspan=2, sticky= W)
        
        """ The box showing the current tweet """
        self.text = Text(self, width=100, height=5,wrap=WORD, background='green')
        self.text.grid(row=1, column=0, columnspan=4, sticky= W)
        
        """ Create the buttons """
        self.nextTweet = Button(self, text='Next', bd=5,width=17, command=self.showNext)
        self.nextTweet.grid(row=2, column=2, columnspan=1, sticky= W)
        self.previousTweet = Button(self, text='Previous', bd=5,width=17, command=self.showPrevious)
        self.previousTweet.grid(row=2, column=1, columnspan=1, sticky= W)
        
        self.button0= Button(self, text='Food', bd=5,width=17,command=self.getLabel0)
        self.button0.grid(row=4, column=0, columnspan=1, sticky= W)
        self.button1= Button(self, text='Crime', bd=5,width=17, command=self.getLabel1)
        self.button1.grid(row=4, column=1, columnspan=1, sticky= W)
        self.button2= Button(self, text='Weather', bd=5,width=17, command=self.getLabel2)
        self.button2.grid(row=4, column=2, columnspan=1, sticky= W)
        self.button3= Button(self, text='Sport', bd=5,width=17, command=self.getLabel3)
        self.button3.grid(row=4, column=3, columnspan=1, sticky= W)
        self.button4= Button(self, text='Social event', bd=5,width=17, command=self.getLabel4)
        self.button4.grid(row=5, column=0, columnspan=1, sticky= W)
        self.button5= Button(self, text='Cultural event', bd=5,width=17, command=self.getLabel5)
        self.button5.grid(row=5, column=1, columnspan=1, sticky= W)
        self.button6= Button(self, text='Location', bd=5,width=17, command=self.getLabel6)
        self.button6.grid(row=6, column=1, columnspan=1, sticky= W)
        self.button7= Button(self, text='Health', bd=5,width=17, command=self.getLabel7)
        self.button7.grid(row=5, column=2, columnspan=1, sticky= W)
        self.button8= Button(self, text='Traffic', bd=5,width=17, command=self.getLabel8)
        self.button8.grid(row=5, column=3, columnspan=1, sticky= W)
        self.button9= Button(self, text='Other', bd=5,width=17, command=self.getLabel9)
        self.button9.grid(row=6, column=2, columnspan=1, sticky= W)
        
        self.button10= Button(self, text='Quit', bd=5,width=5, command=self.quit)
        self.button10.grid(row=7, column=4, columnspan=1, sticky= SE)
        self.button11= Button(self, text='Save', bd=5,width=5, command=self.saveAnnotation)
        self.button11.grid(row=7, column=5, columnspan=1, sticky= SE)
        
    def showNext(self):
        #print(len(self.tweets))
        #print(self.Nextbutton_clicks)
        self.text.delete(0.0,END)
        if self.data.shape[0] > self.Nextbutton_clicks:
            tweet=self.data.tweets[self.Nextbutton_clicks]
            self.text.insert(0.0,tweet)
            self.Nextbutton_clicks +=1
        else:
            self.text.insert(INSERT,'Thanks for your contribution. You have reached the End of file. Do not forget to save your effort before quitting.')
            self.text.tag_add("Thanks", "1.0", "1.150")
            self.text.tag_configure("Thanks", background="green", foreground="black")
    def showPrevious(self):
        self.text.delete(0.0,END)
        if self.Nextbutton_clicks > 0:
            self.Nextbutton_clicks -=1
            tweet=self.data.tweets[self.Nextbutton_clicks]
            self.text.insert(0.0,tweet)
        else:
            
            self.text.insert(INSERT,'Thanks for your contribution. Please click on Next to start the tweet-annotation task.')  
            self.text.tag_add("Thanks", "1.0", "1.100")
            self.text.tag_configure("Thanks", background="yellow", foreground="blue")
    def saveAnnotation(self):
        with open('Nextbutton_Indicator.txt', 'w') as f:
            f.write('%d' % self.Nextbutton_clicks)
        #np.save('GroundTruth-annotatedTweets',self.annotation)
        self.data.to_csv('GroundTruth-annotatedTweets.csv', header=True, index=False)
    def getLabel0(self):
        self.data.food[self.Nextbutton_clicks-1]=1
    def getLabel1(self):
        self.data.crime[self.Nextbutton_clicks-1]=1
    def getLabel2(self):
        self.data.weather[self.Nextbutton_clicks-1]=1
    def getLabel3(self):
        self.data.sport[self.Nextbutton_clicks-1]=1
    def getLabel4(self):
        self.data.social[self.Nextbutton_clicks-1]=1
    def getLabel5(self):
        self.data.cultural[self.Nextbutton_clicks-1]=1
    def getLabel6(self):
        self.data.location[self.Nextbutton_clicks-1]=1
    def getLabel7(self):
        self.data.health[self.Nextbutton_clicks-1]=1
    def getLabel8(self):
        self.data.traffic[self.Nextbutton_clicks-1]=1
    def getLabel9(self):
        self.data.other[self.Nextbutton_clicks-1]=1

# Create the window
root = Tk()

# Modify the GUI window properties
root.title("Tweet Manual Annotation GUI")
root.geometry('870x350')
#result_folder = './results/'

# Read the data file:
def Data_Loader():
	df=pd.read_csv('GroundTruth-annotatedTweets.csv')
    return df

def setIndicator():
    if not os.path.exists('Nextbutton_Indicator.txt'):
        IndicatorVal= 0
    else:
        with open('Nextbutton_Indicator.txt') as data:
            IndicatorVal=int(data.readline())
    return IndicatorVal 
        
app = Application(root)
root.mainloop()
