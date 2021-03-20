from tkinter import *
import time
import pyaudio
import numpy as np
import wave
class Virtualizer:

    
    def __init__(self):
        self.kontinue = 1        
        self.nextSelected = 0
        self.backSelected = 0
        class NextButton(Button):
            def action1 (self):
                virtualiser.setPause()  
                virtualiser.buttonNextSelected()
        class BackButton(Button):
            def action2 (self):
                virtualiser.setPause()  
                virtualiser.buttonBackSelected()
        self.root = Tk()
        self.root.resizable(width=False, height=False)
        self.canvas = Canvas(self.root, width=520, height = 400,bg='black')
        self.canvas.pack()  
        self.items=[]
        for i in range(50) :
            self.items.append(self.canvas.create_rectangle(10+10*i, 375, 20+10*i, 375, fill="blue"))
        self.canvas.pack()
        next= NextButton(width = 10, text="Next", activebackground='red', bg="black", fg="red")
        next["command"]=next.action1
        next.place(x= 435, y=10)
        back= BackButton(width = 10, text="Back", activebackground='red',bg="black", fg="red")
        back["command"]=back.action2
        back.place(x= 10, y=10)
        self.label = Label(bg= "black", fg="red")
        self.label.place(x=130,y=10)
    
    def setContinue(self):
        self.kontinue=1
    
    def setPause(self):
        self.kontinue=0
    
    def buttonNextSelected(self):
        if self.nextSelected== 0 :
            self.nextSelected = 1
        else:
            self.nextSelected = 0
    
    def buttonBackSelected(self):
        if self.backSelected== 0 :
            self.backSelected = 1
        else:
            self.backSelected = 0
     
    def animation(self,filename,index):
        self.label["text"]="PLAYING FILE  :  "+filename[index]
        track = 0
        CHUNK =1024
        RATE = 44100
        wf = wave.open(filename[index])
        w= wave.open(filename[index])
        p=pyaudio.PyAudio()
        stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),  channels = wf.getnchannels(),rate=wf.getframerate(),output=True)
        peak=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        a= "a"
        while a!= "nan" and self.kontinue ==1:
            datas= wf.readframes(CHUNK)
            datab =  np.fromstring(datas,dtype=np.int16)
            peak1=   np.average(np.abs(datab))
            a= str((20*peak1/2**14))
            if(a!='nan' ):
                peak.pop(0)
                peak.append(peak1) 
                for i in range(50):
                    self.canvas.coords(self.items[i],10+i*10,375,20+i*10,375-10*int((20*peak[i]/2**14)))
                self.canvas.update()
                stream.write(datas)
            else : print("finish")
        stream.stop_stream()
        stream.close()
        p.terminate()
        if self.nextSelected ==1 :
            if index== len(filename)-1 : 
                self.setContinue()
                self.buttonNextSelected()
                self.animation(filename,0)
            else : 
                self.setContinue()
                self.buttonNextSelected()
                self.animation(filename,index+1)
        elif self.backSelected ==1:
            if index == 0 :
                self.setContinue()
                self.buttonBackSelected()
                self.animation(filename, len(filename)-1)    
            else :
                self.setContinue()
                self.buttonBackSelected()
                self.animation(filename, index-1)
        else:
            if index== len(filename)-1 : 
                self.animation(filename,0)
            else : 
                self.animation(filename,index+1)
                
fileslist=['D:\TT\Downloads\pooping.wav','D:\TT\Downloads\grownup.wav','D:\TT\Downloads\imlang.wav']
virtualiser = Virtualizer()
virtualiser.animation(fileslist,0)
virtualiser.root.mainloop() 

