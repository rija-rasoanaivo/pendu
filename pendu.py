import pygame
from pygame.draw import*

import pygame
from pygame.locals import *
import random

pygame.init()
screen = pygame.display.set_mode((800, 400), RESIZABLE)
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
background = GREY
screen.fill(background)


# Charger les mots du fichier dans une liste
mots = []
with open("mot.txt", "r") as file:
    for line in file:
        mots.extend(line.split())


# Choisir un mot aléatoire
mot = random.choice(mots)
print(f"Le mot à deviner est : {mot}")

lettres_verifiees = set()
nb_essais = 7
lettres_correctes = 0

print("Devine le mot.")

while nb_essais > 0:
    devinette = input(f"Tu as {nb_essais} essais. Devine une lettre : ")
    
    if devinette in lettres_verifiees:
        print("Tu as déjà deviné cette lettre. Essayez une autre lettre.")
        continue
    
    if devinette in mot:
        lettres_verifiees.add(devinette)
        lettres_correctes += mot.count(devinette)
        print(f"Bonne devinette ! La lettre '{devinette}' est dans le mot.")
    else:
        print(f"La lettre '{devinette}' n'est pas dans le mot.")
        nb_essais -= 1
    
    mot_a_afficher = ''
    for lettre in mot:
        if lettre in lettres_verifiees:
            mot_a_afficher += lettre
        else:
            mot_a_afficher += '_'
    
    print(f"Mot actuel : {mot_a_afficher}")
    
    if lettres_correctes == len(mot):
        print("Félicitations, vous avez deviné le mot!")
        break

if nb_essais == 0:
    print(f"Dommage, vous n'avez plus d'essais. Le mot était '{mot}'.")