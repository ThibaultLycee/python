import tkinter as tk
import json


class Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("400x450")
        self.state = [
            [0 for i in range(8)] for i in range(8)
        ]

        self.makeCanvas()
        self.makeButton()

        self.mainloop()
    
    def mouseListener(self, event):
        if event.num == 1:
            self.tryRegister(event.x, event.y)

    def tryRegister(self, x, y):
        X, Y = int(x / 50), int(y / 50)
        if 0 <= X <= 8 and 0 <= Y <= 8:
            self.state[Y][X] = 1 if self.state[Y][X] == 0 else 0
            self.renderGrid()

    def makeCanvas(self):
        self.canvas = tk.Canvas(self, width=400, height=400)
        self.renderGrid()

    def makeButton(self):
        self.save_button = tk.Button(self, text="Save Letter", command=self.save)
        self.save_button.pack(side=tk.BOTTOM)

    def save(self):
        window = tk.Tk()    
        def save_letter(text):
            value = [hex(int("".join([str(b) for b in a]), 2)) for a in self.state]
            with open("out.txt", "at") as file:
                file.write(f"{text} : {value}\n")
                window.destroy()

        window.geometry("100x50")
        entry = tk.Entry(window)
        button = tk.Button(window, text="Save", command=lambda: save_letter(entry.get()))
        entry.pack()
        button.pack()
        window.mainloop()


    def renderGrid(self):
        for x in range(8):
            for y in range(8):
                self.canvas.create_rectangle(x * 50, y * 50, (x + 1) * 50, (y + 1) * 50, fill="grey" if self.state[y][x] == 0 else "black")
        self.canvas.pack()
        self.canvas.bind('<Button>', self.mouseListener)


w = Window()