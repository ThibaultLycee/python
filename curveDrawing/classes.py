import tkinter as tk
from tkinter import filedialog as tfd

keyCodes = {
    'a': '\x01',
    'b': '\x02',
    'c': '\x03',
    'd': '\x04',
    'e': '\x05',
    'f': '\x06',
    'g': '\x07',
    'h': '\x08',
    'i': '\x09',
    'j': '\x0a',
    'k': '\x0b',
    'l': '\x0c',
    'm': '\x0d',
    'n': '\x0e',
    'o': '\x0f',
    'p': '\x10',
    'q': '\x11',
    'r': '\x12',
    's': '\x13',
    't': '\x14',
    'u': '\x15',
    'v': '\x16',
    'w': '\x17',
    'x': '\x18',
    'y': '\x19',
    'z': '\x1a'
}

def RegisterActionInStack(stack):
    def handler(func):
        def wrapper(*args, **kwargs):
            act = Action(func, args, func(*args), func.__name__)
            stack.add(act)
            return None
        return wrapper
    return handler


class Action:
    def __init__(self, fct, args, result, type_):
        self.fct = fct
        self.args = args
        self.result = result
        self.type = type_
    
    def redo(self):
        self.result = self.fct(*self.args)

    def undo(self, parent=[]):
        if self.type == "clearScene":
            for act in parent:
                act.redo()
        elif self.type == "createPoint":
            self.args[1].delete(self.result)
        else:
            self.args[1].delete(self.result)

    def __repr__(self):
        return f'[{self.fct.__name__}] : {self.args} \n'


class Point:
    def __init__(self, x, y, canvas, color="red", width="1"):
        self.x = x
        self.y = y
        self.canvas = canvas
        self.color = color
        self.width = width
    
    def render(self):
        return self.canvas.create_oval(self.x-.5*self.width, self.y-.5*self.width, self.x+.5*self.width, self.y+.5*self.width, outline=self.color, fill=self.color)


class Stack:
    def __init__(self):
        self.undoStack = []
        self.redoStack = []

    def canUndo(self): return len(self.undoStack) > 0
    def canRedo(self): return len(self.redoStack) > 0

    def add(self, act):
        self.undoStack.append(act)
        self.redoStack = []

    def undo(self):
        self.undoStack[-1].undo(self.undoStack[:-1])
        self.redoStack.append(self.undoStack[-1])
        self.undoStack.pop(-1)
    
    def redo(self):
        self.redoStack[-1].redo()
        self.undoStack.append(self.redoStack[-1])
        self.redoStack.pop(-1)
    
    def __repr__(self):
        return f'Undostack : {self.undoStack}\nRedostack : {self.redoStack}'


width, height = 1080, 720
settingFrameWidth = 270
stack = Stack()


class Window(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)

        #Personnal things
        self.currentColor = "green"
        self.lineWidth = 1

        #Create widgets
        self.createMenuBar()
        self.createDrawingCanvas()
        self.createSettingsFrame()
        self.createSettingsMenu()

        #Set the parameters for the window
        self.geometry(f"{width}x{height}")
        self.resizable(height=False, width=False)
        self.title("Drawing Curve")

        #Bind the keys
        self.bind("<Key>", self.keyPressed)
        self.canvas.bind("<Button>", self.mousePressedOnCanvas)
    

    def keyPressed(self, event):
        if event.state == 12: # Vérifier si une action "Ctrl + "
            if event.char == keyCodes['s']: self.save()
            elif event.char == keyCodes['o']: self.openFile()
            elif event.char == keyCodes['z']: self.undo()
            elif event.char == keyCodes['y']: self.redo()

    def mousePressedOnCanvas(self, event):
        self.lineWidth = self.lineWidthSlider.get()
        if event.num == 1: self.createPoint(self.canvas, event.x, event.y)

    @RegisterActionInStack(stack)
    def createImage(self, canvas, x, y, img):
        return canvas.create_image(x, y, image=img)

    @RegisterActionInStack(stack)
    def clearScene(self):
        self.canvas.delete("all")

    @RegisterActionInStack(stack)
    def createPoint(self, canvas, x, y):
        return Point(x, y, canvas, self.currentColor, self.lineWidth).render()

    def createSettingsFrame(self):
        self.settingsFrame = tk.Frame(self, height=height, width=settingFrameWidth, bg="gray")
        self.settingsFrame.pack(side="left")
        
        self.lineWidthFrame = tk.Frame(self.settingsFrame, height=40, width=settingFrameWidth, bg="gray")
        self.lineWidthFrame.place(x=3, y=3)

    def createSettingsMenu(self):
        self.lineWidthLabel = tk.Label(self.lineWidthFrame, text="Line width", fg='black', bg="gray")
        self.lineWidthSlider = tk.Scale(self.lineWidthFrame, from_=1, to_=10, orient=tk.HORIZONTAL, bg="gray")
        self.lineWidthLabel.pack(side="left")
        self.lineWidthSlider.pack(side="right")

    def createMenuBar(self):
        self.menuBar = tk.Menu(self, postcommand=self.update)
        
        self.menuFile = tk.Menu(self.menuBar, tearoff=0)
        self.menuFile.add_command(label="Open File", command=self.openFile, accelerator="Ctrl + O")
        self.menuFile.add_command(label="Save", command=self.save, accelerator="Ctrl + S")
        self.menuFile.add_separator()
        self.menuFile.add_command(label="Clear", command=self.clearScene)
        
        self.menuBar.add_cascade(label="File", menu=self.menuFile)

        self.menuEdit = tk.Menu(self.menuBar, tearoff=0)
        self.menuEdit.add_command(label="Undo", command=self.undo, accelerator="Ctrl + Z")
        self.menuEdit.add_command(label="Redo", command=self.redo, accelerator="Ctrl + Y")

        self.menuBar.add_cascade(label="Edit", menu=self.menuEdit)

        #Add the menu bar to the window
        self.config(menu=self.menuBar)

    def createDrawingCanvas(self):
        self.canvas = tk.Canvas(self, bg='white', height=height, width=width-settingFrameWidth, highlightbackground="black")
        self.canvas.pack(side="right")

    def undo(self):
        if stack.canUndo(): stack.undo()

    def redo(self):
        if stack.canRedo(): stack.redo()

    def openFile(self): 
        file = tfd.askopenfilename(title="Choose the file to open", filetypes=[("PNG Image", ".png"), ("Jpeg Image", ".jpg")])
        self.img = tk.PhotoImage(file=file)
        self.createImage(self.canvas, 0 + self.img.width() / 2 , 0 + self.img.height() / 2, self.img)
    
    def save(self):
        print("Saved !")

    def update(self):
        if stack.canUndo():
            self.menuEdit.entryconfig(0, state=tk.ACTIVE)
        else:
            self.menuEdit.entryconfig(0, state=tk.DISABLED)
        if stack.canRedo():
            self.menuEdit.entryconfig(1, state=tk.ACTIVE)
        else:
            self.menuEdit.entryconfig(1, state=tk.DISABLED)