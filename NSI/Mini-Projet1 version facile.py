#on importe la bibliothèque random
import random

pointsAlice = 0
pointsBob = 0

def checkWin():
    """on test si un joueur à gagné"""
    if pointsAlice == 5:
        print("Alice a gagné")
        return True
    elif pointsBob == 5:
        print("Bob a gagne")
        return True
    else: return False

def addPoint(joueur, tirage):
    """on vérifie si il faut ajouter un point au joueur, si oui, on l'ajoute"""
    global pointsAlice, pointsBob
    # si le joueur à 2 fois 6, on lui ajoute un point
    if tirage.count(6) >= 2 and joueur == "Alice":
        pointsAlice = pointsAlice + 1
    elif tirage.count(6) >= 2 and joueur == "Bob":
        pointsBob = pointsBob + 1

def lancer():
    """on simule le tirage de 10 valeurs"""
    tirage = []
    for i in range(10):
        tirage.append(random.randint(1, 6))
    return tirage

def changeJoueur(joueur):
    """on change le joueur qui tire"""
    if joueur == "Alice":
        play("Bob")
    else:
        play("Alice")

def showTirage(joueur, tirage):
    """affiche le tirage du joueur"""
    print(joueur, ":", tirage)

def showPoints(joueur):
    """affiche les points du joueur"""
    global pointsBob, pointsAlice
    # on affiche les points
    if joueur == "Alice":
        print("Le nombre de points d'Alice est:", pointsAlice)
    if joueur == "Bob":
        print("Le nombre de points de Bob est:", pointsBob)

#on créé la fonction qui simule le jeu
def play(joueur):
    """fonction principale, fait le lien entre les différentes fonctions du code"""
    global pointsAlice, pointsBob
    #le tirage est simulé
    tirage = lancer()

    #on affiche le tirage
    showTirage(joueur, tirage)
    #on ajoute si nécesaire les points
    addPoint(joueur, tirage)
    #on affiche les points
    showPoints(joueur)

    #on test la victoire et arrête le programme si victoire il y a
    if checkWin():
        return None

    #on change le joueur
    changeJoueur(joueur)

#on commence le jeu
play("Alice")