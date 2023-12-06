import pygame
import random
from pygame.locals import *

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Définition des couleurs
BLACK = (0, 0, 0)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Chargement des mots depuis le fichier 'mot.txt'
with open("mot.txt", "r") as file:
    mots = file.read().split()

# Choix aléatoire d'un mot dans la liste de mots
mot = random.choice(mots)
print(f"Le mot à deviner est : {mot}")

# Initialisation des variables
lettres_verifiees = set()
nb_essais = 11

# Définition des éléments du pendu
elements_pendu = [
    lambda: pygame.draw.rect(screen, BLACK, (100, 350, 300, 2)),#sol 
    lambda: pygame.draw.rect(screen, BLACK, (175, 50, 2, 300)),#verticale
    lambda: pygame.draw.rect(screen, BLACK, (175, 50, 200, 2)),#horizontale
    lambda: pygame.draw.line(screen, BLACK, (175, 100), (200, 50), 2), #diagonale
    lambda: pygame.draw.rect(screen, MAGENTA, (375, 50, 2, 50)),#corde
    lambda: pygame.draw.ellipse(screen, RED, (350, 100, 50, 50), 1),#tête
    lambda: pygame.draw.rect(screen, RED, (375, 150, 1, 100)),#corp
    lambda: pygame.draw.line(screen, RED, (375, 175), (340, 150), 1),#bras gauche
    lambda: pygame.draw.line(screen, RED, (375, 175), (410, 150), 1),#bras droit
    lambda: pygame.draw.line(screen, RED, (375, 250), (340, 275), 1),#jambe gauche
    lambda: pygame.draw.line(screen, RED, (375, 250), (410, 275), 1)#jambe droite
]

# Fonction pour dessiner le pendu
def dessiner_pendu(essais_restants):
    for i in range(11 - essais_restants):
        elements_pendu[i]()

# Charger une police pour le texte
font = pygame.font.Font(None, 36)

# Boucle principale du jeu
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Capture des événements de saisie
        if event.type == pygame.KEYDOWN:
            if event.key >= pygame.K_a and event.key <= pygame.K_z:
                lettre = chr(event.key)
                lettres_verifiees.add(lettre)
                if lettre not in mot:
                    nb_essais -= 1

    mot_a_afficher = ''.join([lettre if lettre in lettres_verifiees else '_' for lettre in mot])

    # Affichage du texte
    text = font.render(f"Tu as {nb_essais} essais. Devine une lettre : {mot_a_afficher}", True, BLACK)
    screen.blit(text, (100, 500))

    if nb_essais == 0: 
        text_end = font.render(f"Dommage... Le mot était '{mot}'. Voulez-vous rejouer ? (o/n)", True, RED)
        screen.blit(text_end, (20, 400))
        pygame.display.flip()
        wait_for_input = True
        while wait_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:  # Appuyer sur la touche 'o' pour recommencer
                        mot = random.choice(mots)
                        lettres_verifiees = set()
                        nb_essais = 11
                        wait_for_input = False
                    elif event.key == pygame.K_n:  # Appuyer sur la touche 'n' pour quitter
                        running = False
                        wait_for_input = False
    elif mot_a_afficher == mot:
        text_end = font.render(f"Bravo! Voulez-vous rejouer ? (o/n)", True, GREEN)
        screen.blit(text_end, (20, 400))
        pygame.display.flip()
        wait_for_input = True
        while wait_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_o:  # Appuyer sur la touche 'o' pour recommencer
                        mot = random.choice(mots)
                        lettres_verifiees = set()
                        nb_essais = 11
                        wait_for_input = False
                    elif event.key == pygame.K_n:  # Appuyer sur la touche 'n' pour quitter
                        running = False
                        wait_for_input = False

    dessiner_pendu(nb_essais)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()  # Ferme la fenêtre Pygame lorsque la boucle se termine
