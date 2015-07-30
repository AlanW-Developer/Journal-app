import tkinter as tk
import os
import tkinter.filedialog
import tkinter.messagebox

class Main(tk.Tk):

    def __init__(self, *args, **kwargs):
        '''This initialisation runs the whole program'''
        #textBoxList = []

        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Untitled')
        self.minsize(690,500)
        self.maxsize(690,500)
        self.geometry('690x500')
        self.canvas = tk.Canvas(self)
        #self.canvas = ResizingCanvas(self, width=850, height=400, highlightthickness=0)
        self.scroll = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.frame = tk.Frame(self.canvas) # frame does not get pack() as it needs to be embedded into canvas through canvas.
        self.scroll.pack(side='right', fill='y')
        #self.scroll.grid(row=0, column=1, sticky='ns')
        self.canvas.pack(fill='both', expand='yes')
        #self.canvas.grid(row=0, column=0, sticky='nesw')
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')              
        self.frame.bind('<Configure>', lambda event: self.OnFrameConfigure(self)) #Can also use self.frame.bind('<Configure>', self.OnFrameConfigure)
                                                                                  #Provided event=None is set

        self.menubar = Menubar(self)
        self.journal = TextBox(self.frame, name='Journal', n=0)
        self.good = TextBox(self.frame, name='Good', n=2)
        self.improvements = TextBox(self.frame, name='Improvements', n=4)
        
    def OnFrameConfigure(self, event):
        '''Used to allowed scrolled region in a canvas'''
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def getFileNameSave(self):
        return tkinter.filedialog.asksaveasfilename(initialfile = 'Untitled.txt',
               defaultextension='.txt', filetypes=[('All Files', '*.*'),('Text Documents', '*.txt')])

    def getFileNameOpen(self):
        return tkinter.filedialog.askopenfilename(defaultextension='.txt',
               filetypes = [('All Files', '*.*'),('Text Documents','*.txt')])

    # open function
    def open_file(self):
        global filename # required so that the save method and open_file method do not clash
        filename = Main.getFileNameOpen(self)
        if filename == '': # No file chosen
            filename = None
        else:
            self.journal.delete(1.0, 'end')
            self.good.delete(1.0, 'end')
            self.improvements.delete(1.0, 'end')
            fh = open(filename, 'r')
            textFromFile = fh.read().rstrip()
            import re # need to use regex to divide text into different parts
            splitText = re.split('Good|Improvements', textFromFile) # gets the 3 parts of the text as 3 strings and is entered into a list

            finalText = [] #list to hold strings of newText(text without newline characters) to be placed into textwidgets. 
            for text in splitText:                                
                newText = text.replace('\n', '') # Replaces all the newline characters of text so that no newlines appear in items and makes text
                finalText.append(newText) # Appends string into finalText list
            #
            # the following code inserts elements of finalText into each of the TextBox objects
            #
            self.journal.insert(1.0, finalText[0]) 
            self.good.insert(1.0, finalText[1])
            self.improvements.insert(1.0, finalText[-1])
            fh.close()

    def new_file(self):
        self.title('Untitled')
        global filename
        filename = None
        self.journal.delete(1.0, 'end')
        self.good.delete(1.0, 'end')
        self.improvements.delete(1.0, 'end')
        
    def save(self):
        global filename
        try:
            # opens file. Extracts text from the TextBox objects and writes it into the opened file
            with open(filename, 'w') as infile:
                journalText = self.journal.get(0.0, 'end')
                goodText = self.good.get(0.0, 'end')
                improvementText = self.improvements.get(0.0, 'end')
                infile.write(journalText + '\nGood\n' + goodText + '\nImprovements\n' + improvementText)
        except:
            self.save_as()
                        
    # Save as function
    def save_as(self):
        f = Main.getFileNameSave(self)
        with open(f, 'w') as infile:
            journalText = self.journal.get(0.0, 'end')
            goodText = self.good.get(0.0, 'end')
            improvementText = self.improvements.get(0.0, 'end')
            infile.write(journalText + '\nGood\n' + goodText + '\nImprovements\n' + improvementText)

    def exit_editor(self):
        if tkinter.messagebox.askokcancel('Quit', 'Do you really want to quit?'):
            root.destroy()
        
            
class Menubar:
    def __init__(self, parent):
        self.pt = parent # used for the fileMenu methods so that the method can access the parent object attribute, otherwise only the class attribute
                         # class attributed can be accessed
        self.menubar = tk.Menu(parent)
        self.fileMenu(self.menubar)
        self.editMenu(self.menubar)
        self.viewMenu(self.menubar)
        self.aboutMenu(self.menubar)
        self.helpMenu(self.menubar)
        self.dayMenu(self.menubar)
        
        parent.config(menu=self.menubar)
        

    def fileMenu(self, parent):
        #creating a file menu
        filemenu = tk.Menu(parent, tearoff=0)
        filemenu.add_command(label='New', accelerator='Ctrl+N', underline=0, command= lambda: Main.new_file(self.pt))
        filemenu.add_command(label='Open', accelerator='Ctrl+O', underline=0, command= lambda: Main.open_file(self.pt))
        filemenu.add_command(label='Save', accelerator='Ctrl+S', underline=0, command= lambda: Main.save(self.pt))
        filemenu.add_command(label='Save as', accelerator='Shift+Ctrl+S', underline=0, command=lambda: Main.save_as(self.pt))
        filemenu.add_separator()
        filemenu.add_command(label='Exit', accelerator='Alt+F4', command = lambda: Main.exit_editor(self.pt))
        parent.add_cascade(label='File', menu=filemenu)
    

    def editMenu(self, parent):
        # creating an edit menu
        editmenu = tk.Menu(parent, tearoff=0)
        parent.add_cascade(label='Edit', menu=editmenu)

    def viewMenu(self, parent):
        # creating a view menu
        viewmenu = tk.Menu(parent, tearoff=0)
        parent.add_cascade(label='View', menu=viewmenu)

    def aboutMenu(self, parent):
        # Creating an about menu
        aboutmenu = tk.Menu(parent, tearoff=0)
        parent.add_cascade(label='About', menu=aboutmenu)

    def helpMenu(self, parent):
        # Creating a Help Menu
        helpmenu = tk.Menu(parent, tearoff=0)
        parent.add_cascade(label='Help', menu=helpmenu)

    def dayMenu(self, parent):
        # Creating a Day Menu to easily access specific diary entries\
        daymenu = tk.Menu(parent, tearoff=0)
        parent.add_cascade(label='Date', menu=daymenu)

class TextBox(tk.Text):
           
    def __init__(self, parent, row=0, column=0, n=0, name='',*args, **kwargs):
        tk.Label(master=parent, text=name).grid(row=n, column=0)
        tk.Text.__init__(self, master=parent, *args, **kwargs)
        self.vsb = ScrollBar(parent=parent, textbox=self, row=n+1)
        self.configure(yscrollcommand=self.vsb.set)        
        self.grid(row=n+1, column=0)
      
class ScrollBar(tk.Scrollbar):

    def __init__(self, parent, textbox, row=None, column=1, *args, **kwargs): #row=None for now will obtain values when it is used by the TextBox class
        tk.Scrollbar.__init__(self, parent, *args, **kwargs)
        self.configure(command=textbox.yview) #binds the scrollbar to the y-axis of the textwidget
        self.grid(row=row, column=column, sticky='ns')

class ResizingCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        tk.Canvas.__init__(self, parent, **kwargs)
        self.bind('<Configure>', self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event):
        # Determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas
        self.config(width=self.width, height=self.height)
        self.scale('all', 0,0,wscale,hscale)
        


root = Main()
root.mainloop()
