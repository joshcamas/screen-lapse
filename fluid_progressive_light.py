"""
    Fluid Progressive is a special system that allows the implementation of fluid to be
    as readable as possible, by progressing through the code, adding parents and widgets in the order
    the code adds them.
    
    ie
    
    startvertical()
    addbutton("button1")
    addbutton("button2")
    addbutton("button3")
    stopvertical()
    
    This creates a vertical container with three buttons inside.
    
    I'll write some documentation if anyone needs it
    
"""


import tkinter as tk
from tkinter import ttk as ttk

import fluid.fluid_light as ui

class Progress(ui.Frame):
    """
    Wrapper for the progressive system. Anything you want to progress goes in here.
    """
    
    def __init__(self,parent):
        ui.Frame.__init__(self, parent)
        
        #This will not change. This tells the system the top level parent
        self.toplevel = BaseLevel(parent)
        
        #add this top level to the parent
        self.toplevel.grid(row=0,column=0)
        
        self.padding = {"x":5,"y":5}
        self.sticky = ""
        
        #This is the progressive level. This will change, depending if a level
        #has been started or stopped
        self.currlevel = self.toplevel
        self.currlevel.start(self)
    
    def _startcurrentlevel(self,newlevel):
        self.currlevel.add(self,newlevel)
        self.currlevel = newlevel
        self.currlevel.start(self)

    def _stopcurrentlevel(self):
        if(self.currlevel != self.toplevel):
            self.currlevel.stop(self)
            self.currlevel = self.currlevel.parentLevel

    def _add(self,widget):
        self.currlevel.add(self,widget)
        return(widget)
        
    def _gridwidget(self,widget,x,y):
        widget.grid(row=y,column=x,padx=self.padding["x"],pady=self.padding["y"],sticky=self.sticky)
    
    def setpadding(self,x=0,y=0):
        self.padding["x"] = x
        self.padding["y"] = y
    
    def setsticky(self,sticky):
        self.sticky = sticky
        
    #============[   Widgets   ]============#

    #Adds a ui.Button
    def addbutton(self,label):
        button = ui.Button(self.currlevel,label)
        self._add(button)
        return(button)
        
    #Adds a ui.Label
    def addlabel(self,label,bold=False):
        label = ui.Label(self.currlevel,label,bold)
        self._add(label)
        return(label)

    #Adds a ui.OutputBox
    def addoutput(self,label,value,vertical=False):
        horioutput = ui.OutputBox(self.currlevel,label,value,vertical)
        self._add(horioutput)
        return(horioutput)
    
    #Adds a ui.InputBox
    def addinputbox(self,label,default="",width=10):
        horioutput = ui.InputBox(self.currlevel,label,default,width)
        self._add(horioutput)
        return(horioutput)
    
    #Adds a ui.OutputBox
    def addcheckbox(self,label,value):
        checkbox = ui.CheckBox(self.currlevel,label,value)
        self._add(checkbox)
        return(checkbox)
    
    #Adds a ui.OutputBox
    def addscale(self,label,start,end):
        scale = ui.Scale(self.currlevel,label,start,end)
        self._add(scale)
        return(scale)

    def adddropdown(self,label,options=None):
        dd = ui.DropDown(self.currlevel,label,options)
        self._add(dd)
        return(dd)
        
    #Adds a custom ui widget element. 
    #Use this for ui Graphs and other things
    def addcustom(self,customclass,*args, **kwargs):
        if(isinstance(customclass,ui.Frame)):
            custom = customclass(self.currlevel,*args, **kwargs)
        else:
            custom = customclass(self.currlevel.frame,*args, **kwargs)
            
        self._add(custom)
        return(custom)
        
    #============[   Levels   ]============#
    
    #Start Horizontal List
    def starthorizontal(self):
        newlevel = HorizontalList(self.currlevel)
        self._startcurrentlevel(newlevel)
        return(newlevel)
    
    #Stop Horizontal List
    def stophorizontal(self):
        self._stopcurrentlevel()
        
    #Start Vertical List
    def startvertical(self):
        newlevel = VerticalList(self.currlevel)
        self._startcurrentlevel(newlevel)
        return(newlevel)
    
    #Stop Vertical List
    def stopvertical(self):
        self._stopcurrentlevel()
    
    #Start a Tab List (And create the first tab, optionally)
    def starttabs(self,tabname):
        newlevel = TabList(self.currlevel)
        self._startcurrentlevel(newlevel)
        if(tabname != None):
            newlevel.newtab(tabname,self)
    
    #Stop a Tab List
    def stoptabs(self):
        self._stopcurrentlevel()
	
    #Start a new Tab in a Tab List
    def newtab(self,tabname):
        self.currlevel.newtab(tabname,self)

class ProgressLevel(ui.Frame):
    """
    Base wrapper for levels. They can be "started" and "stopped",
    and anything added to the progressive application afterwards
    will be added to this level. (Including other levels)
    """

    def __init__(self,parent):
        ui.Frame.__init__(self,parent)
        self.parentLevel = parent
        
    def setParentLevel(self,level):
        self.parentLevel = level
        
    def start(self,progress):

        pass
    
    def add(self,progress,widget):
        pass
        
    def stop(self,progress):
        pass

class BaseLevel(ProgressLevel):
    """
    The level each `Progress` system starts at. By default, everything will
    be added in a horizontal manner
    """
    def start(self,progress):
        self.currentx = 0
    
    def add(self,progress,widget):
        progress._gridwidget(widget,self.currentx,0)
        self.currentx+=1

class HorizontalList(ProgressLevel):
    def start(self,progress):
        self.currentx = 0
    
    def add(self,progress,widget):
        progress._gridwidget(widget,self.currentx,0)
        self.currentx+=1
    
class VerticalList(ProgressLevel):
    def start(self,progress):
        self.currenty = 0
    
    def add(self,progress,widget):
        progress._gridwidget(widget,0,self.currenty)
        self.currenty+=1
    
class TabList(ProgressLevel):
    """
    The level each `Progress` system starts at. By default, everything will
    be added in a horizontal manner
    """
    def start(self,progress,text=None):
        self.tabs = ttk.Notebook(progress.currlevel.frame)
        self.tabs.grid(row=0,column=0,padx=5,pady=5,sticky=tk.NW)

    def newtab(self,text,progress):
        tab = Tab(self.parent)

        self.tabs.add(tab.frame, text=text)
        progress.currlevel = tab
        tab.start(progress)
        tab.setParentLevel(self.parentLevel)
        tab.tabOwner = self
        self.currentframe = tab
    
    def add(self,progress,widget):
        progress._gridwidget(widget,0,0)

        #progress._gridwidget(widget,self.currentx,0)
        #self.currentx+=1


class Tab(VerticalList):
    def newtab(self,text,progress):
        self.tabOwner.newtab(text,progress)
