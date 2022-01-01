import copy

currentPlayer = 'X'

def test_win(grid):
    winner = None
    for row in grid:
        if row[0] == row[1] == row[2] != ' ': winner = row[0]
    
    for i in range(3):
        if grid[i][0] == grid[i][1] == grid[i][2] != ' ': winner = grid[i][0]
    
    if grid[0][0] == grid[1][1] == grid[2][2] != ' ': winner = grid[1][1]
    if grid[0][2] == grid[1][1] == grid[2][0] != ' ': winner = grid[1][1]

    if winner == None and is_grid_full(grid): return 'tie'
    else: return winner

def is_grid_full(grid):
    for row in grid:
        for val in row:
            if val == ' ': return False
    return True

def play(x, y, signe):
    global currentPlayer
    if grille[x][y] == ' ': grille[x][y] = signe
    currentPlayer = 'O' if currentPlayer == 'X' else 'X'

def get_ai_move():
    bestScore = -1000
    move = tuple()

    for x in range(3):
        for y in range(3):
            if grille[x][y] == ' ':
                grille[x][y] = signes['ordi']
                score = mini_max(grille, False)
                grille[x][y] = ' '
                if score > bestScore:
                    bestScore = score
                    move = (x, y)
    
    play(*move, signes['ordi'])

def mini_max(grid, maximize):
    winner = test_win(grid)

    if winner != None:
        return scores[winner]
    
    if maximize:
        bestScore = -100000
        for x in range(3):
            for y in range(3):
                if grid[x][y] == ' ':
                    grid[x][y] = signes['ordi']
                    score = mini_max(grid, False)
                    grid[x][y] = ' '
                    bestScore = max(score, bestScore)
        return bestScore
    else:
        bestScore = 100000
        for x in range(3):
            for y in range(3):
                if grid[x][y] == ' ':
                    grid[x][y] = signes['joueur']
                    score = mini_max(grid, True)
                    grid[x][y] = ' '
                    bestScore = min(score, bestScore)
        return bestScore

def ask_player():
    x = int(input('Entrez la ligne (0-2) : '))
    y = int(input('Entrez la colonne (0-2) : '))
    if grille[x][y] == ' ':
        play(x, y, signes['joueur'])
    else: ask_player()

def tour():
    if currentPlayer == 'O': ask_player()
    else: get_ai_move()

def output(winner):
    if winner == 'tie':
        print('La partie est terminée, personne n\'a gagné !')
    else:
        print(f'La partie est terminée, et {winner} a gagné !')

def show_grid():
    for row in grille:
        print(f' {row[0]} | {row[1]} | {row[2]} ')
        print('-----------')

def main():
    run = True
    while run:
        tour()
        show_grid()
        winner = test_win(grille)
        if winner != None:
            run = False
            output(winner)

