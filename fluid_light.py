"""
    Fluid (Fluid and Lush User Interface Deity) is a small helper module to aid in prototyping
    and general user interface structure and design. The light version removes any plotting and graphing
"""

import sys
import math
import csv 

import tkinter as tk
from tkinter import ttk as ttk

def quicksetupapp(app,windowtitle=None):
    root = tk.Tk()

    app = app(root)
    app.frame.pack(side="top", fill="both", expand=True)
    app.build()
    app.root = root
    if(windowtitle != None):
        root.title(windowtitle)
    root.mainloop()
    

class Frame():
    """
    An small container that holds a frame. Can attach to a widget, a Frame, or nothing
    """
    
    def __init__(self, parent, *args, **kwargs):
        #Attach to Frame
        if(isinstance(parent,Frame)):
            self.frame = tk.Frame(parent.frame,*args, **kwargs)
        else:
            self.frame = tk.Frame(parent, *args, **kwargs)

        self.parent = parent

    def grid(self,**kwargs):
        self.frame.grid(kwargs)
    
    def setoutline(self,color,thickness=1):
        self.frame.config(highlightbackground=color,highlightcolor=color, highlightthickness=thickness)
    
    def setpadding(self,x,y):
        self.grid(padx=x,pady=y)
    
    def setinternalpadding(self,x,y):
        self.grid(ipadx=x,ipady=y)
        
        
class App(Frame):
    """
    Contains all content of an application window
    
    The master frame that contains all widgets and subframes in
    an application.
    """

    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.signals = []

    def build():
        pass
    
    def screenshot(self,widget,path):
        x=self.parent.winfo_rootx()+widget.winfo_x()
        y=self.parent.winfo_rooty()+widget.winfo_y()
        x1=x+widget.winfo_width()
        y1=y+widget.winfo_height()
        ImageGrab.grab().crop((x,y,x1,y1)).save(path)
        
        
    #Signals are a simple way to allow communication between applications
    def addsignal(id,function):
        signal = Signal(id,function)
        self.signals.append(signal)

    def sendsignal(id,*args, **kwargs):
        for i in range(len(self.signals)):
            if(id == self.signals[i].id):
                self.signals[i].function(*args, **kwargs)
                return True
        print("Could not send signal " + id)
        return False
		 
	

class Signal():
    def __init__(self,id,function):
        self.id = id
        self.function = function
		
class Widget(Frame):
    """
    A single component of the interface
    
    A singular component that can be attached to a `Frame`
    """
    def __init__(self,parent=None):
        Frame.__init__(self,parent)

    def grid(self,**kwargs):
        self.frame.grid(**kwargs)
    
    def hide(self):
        self.frame.grid_remove()
    
    def show(self):
        self.frame.grid()
         
class Button(Widget):
    """
    A button widget with text
    
    """
    def __init__(self,parent,text):
        """
        Initialize widget
        
        Parameters
        ----------
        parent: Frame
            Frame to attach to
        text: string, optional
            Text to display on button. (Default is 'Button')
        
        Returns
        -------
        Frame
            Created frame.
        
        """
        Widget.__init__(self,parent)
        self.button = tk.Button(master=self.frame, text=text)
        self.button.grid(row=0,column=0,padx=2)

    def setcommand(self,command):
        """
        Set function to run when button is pressed
        
        Parameters
        ----------
        command: function
            Function to run
        """
        self.button.configure(command=command)

    def disable(self):
        self.button.config(state='disabled')   
	
    def enable(self):
        self.button.config(state='normal')   
		 
class InputBox(Widget):
    """
    A widget with a label and a textbox
    """
    def __init__(self,parent,label,default="",width=10):
        """
        Initialize widget
        
        Parameters
        ----------
        parent: Frame
            Frame to attach to
        label: string
            Label of widget
        default: string, optional
            Default value of textbox. (Default is '')
        width: float, optional
            Width of textbox (Default is 10)
        Returns
        -------
        Frame
            Created frame.
        
        """
        Widget.__init__(self,parent)

        self.label = tk.Label(self.frame, text=label)
        self.entry = tk.Entry(self.frame,width=width)
        self.label.grid(row=0,column=0,padx=2)
        self.entry.grid(row=0,column=1,padx=1)

        self.entry.insert(0,default)
        
       # return(self.frame)

    def setvalue(self,value):
        """
        Set value of textbox
        
        Parameters
        ----------
        value: string
            value of textbox
        """
        self.entry.insert(0,value)

    def getvalue(self):
        """
        Get value of textbox
        
        Returns
        -------
        string
            value of textbox
        """
        return(self.entry.get())

    def disable(self):
        self.entry.config(state='disabled')   
	
    def enable(self):
        self.entry.config(state='normal')   
		 
class DropDown(Widget):
    """
    A widget with a label and a textbox
    """
    def __init__(self,parent,label,options=None):

        Widget.__init__(self,parent)
        
        self.value = tk.StringVar(self.frame)
        self.value.set(options[0])
        
        self.menu = tk.OptionMenu(self.frame, self.value,*options)
        self.menu.grid(row=0,column=0,padx=2)

        #self.entry.insert(0,default)
        
       # return(self.frame)

    def setoptions(self,options):

        self.value.set(options[0]) # default value
        
        self.menu = tk.OptionMenu(self.frame, self.value,*options)
        self.menu.grid(row=0,column=0,padx=0)

    def getvalue(self):
        return(self.value.get())
    
    def setvalue(self,value):
        self.value.set(value)
        
    def setcommand(self,command):
        self.value.trace('w', command)

class CheckBox(Widget):
    """
    A widget with a label and a checkbutton
    """
    def __init__(self,parent,label,default=0,width=10):
        """
        Initialize widget
        
        Parameters
        ----------
        parent: Frame
            Frame to attach to
        label: string
            Label of widget
        default: int, optional
            Default value of checkbox. (Default is 0)
        width: float, optional
            Width of checkbox (Default is 10)
        Returns
        -------
        Frame
            Created frame.
        
        """
        Widget.__init__(self,parent)

        self.value = tk.IntVar()
        self.value.set(default)
        #self.label = tk.Label(self.frame, text=label)
        self.check = tk.Checkbutton(self.frame, text=label, variable=self.value)
        
        #self.label.grid(row=0,column=0,padx=2)
        self.check.grid(row=0,column=1,padx=1)

       # return(self.frame)
    
    def setcommand(self,command):
        self.check.configure(command=command)
        
    def setvalue(self,value):
        """
        Set value of textbox
        
        Parameters
        ----------
        value: string
            value of textbox
        """
        self.value.set(value)

    def getvalue(self):
        """
        Get value of textbox
        
        Returns
        -------
        string
            value of textbox
        """
        return(self.value.get())

class Scale(Widget):
    """
    A widget with a tk Scale
    """
    def __init__(self,parent,label,start=0,end=100,default=0):
        """
        Initialize widget
        
        Parameters
        ----------
        parent: Frame
            Frame to attach to
        label: string
            Label of widget
        default: int, optional
            Default value of checkbox. (Default is 0)
        width: float, optional
            Width of checkbox (Default is 10)
        Returns
        -------
        Frame
            Created frame.
        
        """
        Widget.__init__(self,parent)

        #self.label = tk.Label(self.frame, text=label)
        self.scale = tk.Scale(self.frame, label=label,from_=start, to=end,orient=tk.HORIZONTAL)
        
        #self.label.grid(row=0,column=0,padx=2)
        self.scale.grid(row=0,column=1,padx=1)

       # return(self.frame)
    
    def setcommand(self,command):
        self.scale.configure(command=command)
        
    def setvalue(self,value):
        """
        Set value of textbox
        
        Parameters
        ----------
        value: float
            value of scale
        """
        self.scale.set(value)

    def getvalue(self):
        """
        Get value of scale
        
        Returns
        -------
        float
            value of scale
        """
        return(self.scale.get())

class Label(Widget):
    def __init__(self,parent,label,bold=False):
        Widget.__init__(self,parent)
        
        if(bold == False):
            f = "arial 9"
        else:
            f = "arial 9 bold"
            
        self.label = tk.Label(self.frame,text=label,font=f)
        self.label.grid(row=0,column=0,padx=2)
        
    def setText(self,label):
        self.label['text']=label
		
class OutputBox(Widget):
    """
    A widget with a label and another label. Used to display small bits of data
    """
    
    def __init__(self,master,label,value,vertical=False):
        """
        Initialize widget
        
        Parameters
        ----------
        parent: Frame
            Frame to attach to
        label: string
            Label of widget
        value: string
            Default value of displayed label
        vertical: bool, optional
            Whether to enable vertical mode or not (Default is false, disabled)
        Returns
        -------
        Frame
            Created frame.
        
        """
        Widget.__init__(self,master)
        
        self.label = tk.Label(self.frame, text=label,font = "arial 9 bold")
        self.value = tk.Label(self.frame, text=value)
        
        if(vertical == False):
            self.label.grid(row=0,column=0,padx=2)
            self.value.grid(row=0,column=1,padx=1)
        else:
            self.label.grid(row=0,column=0,padx=2)
            self.value.grid(row=1,column=0,padx=1)
        
    def setvalue(self,value,roundamount=None):
        """
        Sets value of display to a string
        
        Parameters
        ----------
        value: string
            value of display
        roundAmount: int, optional
            Number of digits to round to. (Default is None, will not round)
        """
        if(roundamount != None):
            value = str(round(value,roundamount))
        self.value.config(text=value)
