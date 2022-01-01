from selenium import webdriver

import time

import bots as bot

#USEFULL VARIABLES
bots = []

nbr = int(input("Nombre de bots : "))
pin = int(input("Game PIN : "))
name = input("Bot name : ")

for i in range(nbr):
    bots.append(bot.KahootBot(f'{i}{name}', webdriver.Chrome()))

for bot_ in bots:
    bot_.connect(pin)