import random


#création de la classe "Player", qui enregistre un nom et un nombre de points
class Player():
    def __init__(self, nom, points):
        self.nom = nom
        self.points = points

    def addPoint(self):
        self.points += 1

    def checkWin(self):
        if self.points == 5: return True
        else: return False

#création de 2 instances de "Player" au noms de Alice et Bob
Alice = Player("Alice", 0)
Bob = Player("Bob", 0)

#premier joueur : Alice
player = Alice

#fonction du jeu
def play(player):
    #liste des resultats du dé
    tirage = []
    #tire 10 nombres aléatoires entre 1 et 6
    for i in range(10):
        tirage.append(random.randint(1,6))
    #affiche le joueur et son tirage
    print(player.nom, ": ",tirage)

    #si le tirage conte la valeur 6 plus de deux fois, ajoute un point au joueur
    if tirage.count(6) == 2:
        player.points += 1
        #affice les points
    print("Le nombre de points de", player.nom, "est de",player.points)
    if player.points == 5:
            print(player.nom,"à gagné")
            return None

    if player.nom == "Alice": play(Bob)
    else: play(Alice)

play(player)