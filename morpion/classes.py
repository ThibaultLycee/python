###################################
#   IMPORTS
###################################

import tkinter as tk
import tkinter.colorchooser as tkcc
import time
import random as rd
import copy
from data import signes, scores

###################################
#   CLASSES
###################################

class Window(tk.Tk):

    def __init__(self, width, height):
        tk.Tk.__init__(self)

        self.width = width
        self.height = height
        self.caseSize = 90
        self.output_text = tk.StringVar()

        self.isListening = False
        self.current_player = 'ordi'

        self.default_colors = {
            'bg': '#FFFFFF',
            'lines': '#000000',
            'cross': '#000000',
            'circles': '#FF0000',
            'button': '#678D8B'
        }

        self.default_settings = {
            'ai-correction': 0
        }

        self.colors = {}
        self.read_colors()

        self.settings = {}
        self.read_settings()

        self.grid = Grid()

        self.geometry(f'{width}x{height}')
        self.resizable(False, False)
        self.title('Morpion')
        self.configure(bg=self.colors['bg'])
        #Icone par Pixel Perfect, trouvé sur https://www.flaticon.com/fr/chercher?word=morpion, recolorisé par Thibault DURAND
        self.iconbitmap('icon.ico')

        self.makeCanvas()
        self.makeButton()
        self.makeLabel()
        self.makeMenu()

        self.after(1000, lambda: self.game(True))
        self.mainloop()

    def game(self, first=False):
        if not self.isListening:
            winner = self.grid.test_win(self.grid.grid)
            if winner != None:
                self.output(winner)
                return
            self.tour(first)
            self.load_grid(self.grid)
        self.after(100, self.game)
    
    def reset(self):
        del self.grid
        self.grid = Grid()
        self.refresh()
        self.current_player = 'ordi'
        self.isListening = False
        self.game(True)

    def refresh(self):
        self.canvas.delete('all')
        self.drawBoard()
        self.output_text.set('')

    def makeButton(self):
        self.button = tk.Button(
            self, text='RESET', bg=self.colors['button'], command=self.reset,
            width=12, font=('', 20, 'bold')
        )
        self.button.pack(side=tk.BOTTOM, pady=10)

    def makeCanvas(self):
        self.canvas = tk.Canvas(
            self, bg=self.colors['bg'], height=self.width, width=self.width,
            highlightbackground=self.colors['bg']
        )
        self.canvas.pack(side=tk.TOP)
        self.canvas.bind('<Button>', self.mouseListener)
        self.drawBoard()
    
    def mouseListener(self, event):
        if event.num == 1 and self.isListening:
            self.tryRegister(event.x, event.y)

    def tour(self, first=False):
        if self.current_player == 'joueur':
            self.listen()
        elif self.current_player == 'ordi':
            self.grid.get_ai_move(first)
            self.current_player = 'joueur'

    def listen(self):
        self.isListening = True

    def tryRegister(self, x, y):
        X = int((x - 20) / self.caseSize)
        Y = int((y - 20) / self.caseSize)
        if 0 <= X <= 2 and 0 <= Y <= 2:
            if self.grid[Y][X] == signes['vide']:
                self.grid.play(Y, X, signes['joueur'])
                self.isListening = False
                self.current_player = 'ordi'

    def makeLabel(self):
        self.label = tk.Label(
            self, bg=self.colors['bg'], height=20, width=self.width,
            textvariable=self.output_text, font=('', 12)
        )
        self.label.pack(side=tk.BOTTOM)

    def makeMenu(self):
        self.menuBar = tk.Menu(self)

        self.menuColors = tk.Menu(self.menuBar, tearoff=0)
        self.menuColors.add_command(label='Background', command=lambda: self.chooseColor('bg'))
        self.menuColors.add_command(label='Button', command=lambda: self.chooseColor('button'))
        self.menuColors.add_command(label='Crosses', command=lambda: self.chooseColor('cross'))
        self.menuColors.add_command(label='Circles', command=lambda: self.chooseColor('circles'))
        self.menuColors.add_command(label='Board Lines', command=lambda: self.chooseColor('lines'))
        self.menuColors.add_separator()
        self.menuColors.add_command(label='Reset Colors', command=self.reset_colors)

        self.menuBar.add_cascade(label='Colors', menu=self.menuColors)

        self.menuBar.add_command(label='Config', command=self.openSettings)

        self.config(menu=self.menuBar)

    def reset_colors(self):
        self.colors = copy.deepcopy(self.default_colors)
        self.reload_colors()
        self.write_colors()

    def chooseColor(self, mode):
        color = tkcc.askcolor()[1]
        self.colors[mode] = color if color != None else self.colors[mode]
        self.reload_colors()
        self.write_colors()

    def drawBoard(self):
        self.offsetX = 20
        self.offsetY = 20
        for x in range(3):
            for y in range(3):
                self.canvas.create_rectangle(
                    x * self.caseSize + self.offsetX, y * self.caseSize + self.offsetY,
                    (x + 1) * self.caseSize + self.offsetX, (y + 1) * self.caseSize + self.offsetY,
                    outline=self.colors['lines'], fill=None, width=3
                )
    
    def drawX(self, x, y):
        X = x * self.caseSize + self.offsetX + 10
        Y = (y + 1) * self.caseSize + self.offsetY - 10

        self.canvas.create_line(X, Y, X + 70, Y - 70, fill=self.colors['cross'], width=3)
        self.canvas.create_line(X + 70, Y, X, Y - 70, fill=self.colors['cross'], width=3)

    def drawO(self, x, y):
        X = x * self.caseSize + self.offsetX + 10
        Y = (y + 1) * self.caseSize + self.offsetY - 10

        self.canvas.create_oval(X, Y, X + 70, Y - 70, outline=self.colors['circles'], fill=None, width=3)
    
    def load_grid(self, grid):
        for row in range(3):
            for col in range(3):
                if grid[row][col] == signes['vide']:
                    continue
                if grid[row][col] == 'X':
                    self.drawX(col, row)
                if grid[row][col] == 'O':
                    self.drawO(col, row)
    
    def output(self, winner):
        if winner == 'tie':
            self.output_text.set('La partie est terminée, personne n\'a gagné !')
        else:
            self.output_text.set(f'La partie est terminée, et {winner} a gagné !')
    
    def read_colors(self):
        with open('colors.txt', 'r') as file:
            for line in file.read().split('\n'):
                line = line.split(' ')
                if len(line) == 2:
                    self.colors[line[0]] = line[1]

    def read_settings(self):
        with open('settings.txt', 'r') as file:
            for line in file.read().split('\n'):
                line = line.split(' ')
                if len(line) == 2:
                    self.settings[line[0]] = line[1]

    def reload_colors(self):
        self.configure(bg=self.colors['bg'])
        self.canvas.configure(bg=self.colors['bg'])
        self.canvas.configure(highlightbackground=self.colors['bg'])
        self.button.configure(bg=self.colors['button'])
        self.label.configure(bg=self.colors['bg'])

        self.canvas.delete('all')
        self.drawBoard()
        self.load_grid(self.grid.grid)

    def write_colors(self):
        with open('colors.txt', 'w') as file:
            for name, color in self.colors.items():
                file.write(f'{name} {color}\n')

    def openSettings(self):
        print('settings')

class Grid:

    def __init__(self):
        self.grid = [
            [signes['vide'], signes['vide'], signes['vide']],
            [signes['vide'], signes['vide'], signes['vide']],
            [signes['vide'], signes['vide'], signes['vide']]
        ]
        self.current_player = 'X'

    def test_win(self, grille):
        winner = None
        #test les lignes
        for row in grille:
            if row[0] == row[1] == row[2] != signes['vide']: winner = row[0]
        
        #test les colonnes
        for i in range(3):
            if grille[0][i] == grille[1][i] == grille[2][i] != signes['vide']: winner = grille[0][i]
        
        #test les diagonnales
        if grille[0][0] == grille[1][1] == grille[2][2] != signes['vide']: winner = grille[1][1]
        if grille[0][2] == grille[1][1] == grille[2][0] != signes['vide']: winner = grille[1][1]

        if winner == None and self.is_grid_full(grille): return 'tie'
        else: return winner
    
    def is_grid_full(self, grille):
        for row in grille:
            for val in row:
                if val == signes['vide']: return False
        return True
    
    def play(self, x, y, signe):
        if self.grid[x][y] == signes['vide']:
            self.grid[x][y] = signe
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def get_ai_move(self, first=False):
        bestScore = -1000
        moves = []

        if first:
            self.play(*rd.choice([(x, y) for x in range(3) for y in range(3)]), signes['ordi'])
            return 

        for x in range(3):
            for y in range(3):
                if self.grid[x][y] == signes['vide']:
                    self.grid[x][y] = signes['ordi']
                    score = self.mini_max(self.grid, False, 1)
                    self.grid[x][y] = signes['vide']
                    if score > bestScore:
                        bestScore = score
                        moves = [(x, y)]
                    elif abs(score - bestScore) < 2:
                        moves.append((x, y))

        move = rd.choice(moves)
        self.play(*move, signes['ordi'])

    def mini_max(self, grid, maximize, depth):
        winner = self.test_win(grid)

        if winner != None:
            return scores[winner] * (1 / depth)
        
        if maximize:
            bestScore = -100000
            for x in range(3):
                for y in range(3):
                    if grid[x][y] == signes['vide']:
                        grid[x][y] = signes['ordi']
                        score = self.mini_max(grid, False, depth + 1)
                        grid[x][y] = signes['vide']
                        bestScore = max(score, bestScore)
            return bestScore
        else:
            bestScore = 100000
            for x in range(3):
                for y in range(3):
                    if grid[x][y] == signes['vide']:
                        grid[x][y] = signes['joueur']
                        score = self.mini_max(grid, True, depth + 1)
                        grid[x][y] = signes['vide']
                        bestScore = min(score, bestScore)
            return bestScore
    
    def __getitem__(self, idx):
        return self.grid[idx]